from aria import workflow
import os
import yaml
import json
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

import tempfile
import json
import yaml

from fabric.api import run, execute, local, hide, env, put, sudo

from localruntimes import runtimes

from literals import *
from compiler import AccessPatternCompiler
import re

def runlocalLinux(filename, params):
    with hide('everything'):
        local("chmod a+x {}".format(filename))
        return local("{} {}".format(filename, params), capture=True)

def runLinux(filename, params, proxy_ip, proxy_port):
    with hide('everything'):
        put(filename, filename)
        run("chmod a+x {}".format(filename))
        if proxy_ip and proxy_port:
          return sudo("export http_proxy=\"http://{}:{}\"; export https_proxy=\"http://{}:{}\"; {} {}".format(proxy_ip,proxy_port,proxy_ip,proxy_port,filename, params))
        else:
          return sudo("{} {}".format(filename, params))

def showLinuxLog(filename):
    with hide('everything'):
        return sudo("test -f {} && cat {}".format(filename, filename))


@workflow
def test(ctx, graph, output_directory, username, key_path, runtime_path, proxy_ip, proxy_port):

    tempdb = tempfile._get_default_tempdir() + "/" + next(tempfile._get_candidate_names()) + ".db"
    engine = create_engine('sqlite:///' + tempdb) # "/tmp/sdl")

    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)
    session.commit()

    # set username and key for ssh
    env.user = username
    env.key_filename = os.path.expanduser(key_path)
    env.sudo_user = 'root'

    runtimepath = os.path.expanduser(runtime_path)

    # proxy_ip="192.168.168.1"
    # proxy_port="80"

    output_directory = os.path.expanduser(output_directory)

    with open(output_directory + "/datalog.json") as fruledict:
        ruledict = json.load(fruledict)
    fruledict.close()

    host_address = ""
    with open(output_directory + "/goal1.trace") as ftrace:
        flog = open(output_directory + "/goal1-test.log", "w+")
        for line in ftrace:
            if "fact" in line:
                fact = (line[line.find("New fact") + 11:-1])

                if fact[0] != "_":
                    ruleid = fact[fact.find("(") + 1:fact.find(",")].replace("'", "")
                    # create a class from literal name
                    literalClass = globals()[fact[:fact.find("(")]]
                    params = literalClass.fromDatalog(fact, ctx, session)

                    ptr = [ n for n in ctx.nodes if n.name == ruledict['id'][ruleid]['node'] ][0]
                    if not ptr.host:
                        ptr = [ n for n in ctx.nodes if n.name == literalClass.getNode(fact) ][0]

                    host_address = ptr.host_address
                    node_name = ptr.host.name

                    runtime = ""
                    key = ruledict['id'][ruleid]['key']
                    if ruledict['id'][ruleid]['relationship']:
                        # move the ptr to the correct relationship
                        ptr = [x for x in ptr.outbound_relationships if x.type.name == ruledict['id'][ruleid]['relationship']][0]
                        #rule = ptr.properties['behavior']._value[str(key)]

                        if "runtime" in ptr.properties.keys() and ptr.properties['runtime']._value != None:
                            if key in ptr.properties['runtime']._value.keys():
                                runtime = ptr.properties['runtime']._value[str(key)]
                    else:
                        #rule = ptr.properties['behavior'][key]
                        if ptr.type.name != ruledict['id'][ruleid]['type']:
                            ptr = [n for n in ctx.nodes if n.type.name == ruledict['id'][ruleid]['type']][0]

                        if "runtime" in ptr.properties.keys() and ptr.properties['runtime'] != None:
                            if key in ptr.properties['runtime'].keys():
                                runtime = ptr.properties['runtime'][str(key)]

                    ### LOCAL RUNTIME ###
                    '''
                    runtime = ""
                    r = ruledict['id'][ruleid]

                    if r["type"] in runtimes:
                        if r["key"] in runtimes[r["type"]]:
                            runtime = runtimes[r["type"]][r["key"]]
                    '''

                    if runtime:
                        inputparams = ""
                        for p in literalClass.parameters: # params:
                            inputparams += " '{}'".format(json.dumps(params[p]))

                        if "extra" in params:
                            for p in literalClass.extra_parameters:
                                inputparams += " '{}'".format(json.dumps(params['extra'][p]))

                        #!invariant
                        if runtime.strip()[0:8] == "!include":
                            with open("{}/{}".format(runtimepath,runtime.strip()[9:])) as stream:
                                test = yaml.safe_load(stream)
                            stream.close()
                        else:
                            test = yaml.safe_load(runtime)

                        success = False

                        print("Verify: {} ({}) {}".format(fact, ptr.type.name, inputparams))
                        flog.write("Verify: {} ({}) {}\n".format(fact, ptr.type.name, inputparams))

                        ## Linux ##

                        try:
                            description = literalClass.__name__

                            tmpfile = "/tmp/SDL_{}_{}.script".format(description, next(tempfile._get_candidate_names()))
                            with open(tmpfile, "w") as f:
                                f.write(test['script'])
                            f.close

                            exe = "remote"
                            if "execute" in test:
                                exe = test['execute']

                            if "description" in test:
                                description = test['description']

                            out = ""
                            if exe == "local":
                                print("Execute local {} with parameters {}".format(tmpfile, inputparams))
                                out = execute(runlocalLinux, tmpfile, inputparams)

                            if exe == "remote":
                                if not host_address:
                                    #host_address =
                                    #print("cerco in" + node_name)
                                    host_address = a.get(node_name)
                                if host_address:
                                    #print("Execute on {} {} with parameters {}".format(host_address, tmpfile, inputparams))
                                    env.hosts = [ host_address ]
                                    out = execute(runLinux, tmpfile, inputparams, proxy_ip, proxy_port)
                                else:
                                    print("Unable to find remote address!")

                            success = True
                        except Exception as e:
                            print("Execution of test '{}' on {} with parameters {}: script FAIL with {}".format(description, node_name, inputparams, e))
                            pass

                        if success:
                            # verify test
                            success = literalClass.verifyResult(out)

                        if success:
                            print("\033[1mExecution of test '{}' on {} with parameters {}\033[0m: \033[92mOK\033[0m".format(description, node_name, inputparams))
                            flog.write("Execution of test '{}' on {} with parameters {}: OK\n".format(description, node_name, inputparams))
                            literalClass.saveResult(out, session)
                            session.commit()
                        else:
                            print("\033[1mExecution of test '{}' on {} with parameters {}\033[0m: \033[91mFAIL\033[0m".format(description, node_name, inputparams))
                            out = " \n".join(execute(showLinuxLog,tmpfile+".log")[host_address].split("\r\n"))
                            print("Log ({}):\n{}".format(tmpfile+".log", out))
                            flog.write("-> Execution of test '{}' on {} with parameters {}: FAILED\n".format(description, node_name, inputparams))
                            flog.write("Log:\n{}\n".format(out))
                    else:
                        print("\033[93mUnverified: {} ({})\033[0m".format(fact, ptr.type.name))

        flog.close()