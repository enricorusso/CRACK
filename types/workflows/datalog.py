from __future__ import print_function
from aria import workflow
from compiler import AccessPatternCompiler
from cStringIO import StringIO
from aria.orchestrator.workflows.api import task
from aria.orchestrator.workflows.exceptions import TaskException
import re
import json
import os
import tempfile
import sys

@workflow
def verify(ctx, graph, output_directory):
    def addID(rule, label):
        goal = False
        if "print(" in rule:
            index = rule.find('(', 1)
            goal = True
        else:
            index = rule.find('(', 0)
        id = 0
        while (index > 0):
            index += 1
            if id == 0:
                if not goal:
                    rule = rule[:index] + str(label) + "," + rule[index:]
            else:
                if rule[index - 2:index - 1] != " ":
                    rule = rule[:index] + "ID" + str(id) + "," + rule[index:]
            index = rule.find('(', index)

            id += 1

        return rule


    datalog = {}
    goals = []
    goalID = 1
    for node in ctx.nodes:
        if 'behavior' in node.properties.keys():
            if not node.properties['behavior'] is None:
                for key in node.properties['behavior']:
                    behavior = node.properties['behavior'][key]

                    node_rules = AccessPatternCompiler().compile(behavior, node)

                    for rule in node_rules:
                        # goal
                        if "print(" in rule:
                            if "description" in node.properties.keys():
                                description = AccessPatternCompiler().compile(node.properties['description'], node)
                            else:
                                description = ['']
                            goals.append((goalID, rule, description[0]))
                            goalID+=1
                        else:
                            if not hasattr(node.host, 'name'):
                                key1 = node.name
                            else:
                                key1 = node.host.name

                            if not key1 in datalog:
                                datalog[key1] = [ { 'node': node.name, 'key': key, 'rule': rule, 'type': node.type.name,
                                                    'relationship': '', 'requirement': '' } ]
                            else:
                                datalog[key1].append( { 'node': node.name, 'key': key, 'rule': rule, 'type': node.type.name,
                                                        'relationship': '', 'requirement': '' } )

        for rel in node.outbound_relationships:
            if 'behavior' in rel.properties.keys():
                if not rel.properties['behavior'] is None:
                    for key in rel.properties['behavior']._value.keys(): # boh..
                        behavior = rel.properties['behavior']._value[key]

                        node_rules = AccessPatternCompiler().compile(behavior, rel)

                        for rule in node_rules:
                            if not hasattr(node.host, 'name'):
                                key1 = node.name
                            else:
                                key1 = node.host.name

                            if not key1 in datalog:
                                datalog[key1] = [ { 'node': node.name, 'key': key, 'rule': rule, 'type': node.type.name,
                                                    'relationship': rel.type.name, 'requirement': rel.name } ]
                            else:
                                datalog[key1].append( { 'node': node.name, 'key': key, 'rule': rule, 'type': node.type.name,
                                                        'relationship': rel.type.name, 'requirement': rel.name } )

    output_directory = os.path.expanduser(output_directory)

    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)

    terms = set()
    label=1
    rules = []
    m = {}

    for n in datalog:
        rules.append("## " + n + " ##")
        for r in datalog[n]:
            rules.append("#  " + r['node'] + " (" + r['type'] + ")," + r['key'])

            #if not r in m.values():
            rid = [x for x in m if (r['node'] == m[x]['node'] and r['key'] == m[x]['key'] and r['relationship'] == m[x]['relationship'])]

            if rid == []:
                m[label] = {k:r[k] for k in r if k != 'rule'}
                rule = addID(r['rule'], label)
                label+=1
            else:
                rule = addID(r['rule'], rid[0])

            rules.append(rule)

            # find terms
            for s in re.split('[,()&]', rule): # rule.split(','):
                s = s.replace('+', '').replace('=', '').replace('<', '').replace(' ', '')
                if s and ("'" not in s) and (not s.isdigit()):
                    terms.add(s) # print("-" + s + "-")
        rules.append("\n")

    f = open(output_directory + "/datalog.py", "w")
    d = open(output_directory + "/datalog.json", "w")
    print(json.dumps({'id': m, 'goal': goals}), file = d)

    print('''
import logging
from pyDatalog import pyDatalog
from pyDatalog import pyEngine
pyEngine.Logging = True
logging.basicConfig(level=logging.INFO)
    
    ''', file = f)

    print("pyDatalog.create_terms('", end="", file = f)
    print(*terms, sep=",", end="')\n", file = f)
    print(file = f)
    print(*rules, sep="\n", file = f)

    f.close()
    d.close()

    for goal in goals:
        print ("- Test goal " + str(goal[0]) + ": " + goal[2] + " [" + goal[1] + "]")
        datalogfile = open(output_directory + "/datalog.py", 'r')
        content = datalogfile.read()

        content+=addID(goal[1], goal[0])

        old_stdout = sys.stdout
        old_stderr = sys.stderr
        log = sys.stderr = StringIO()
        res = sys.stdout = StringIO()
        # TODO: security hole!
        exec(content) in locals()
        print(log.getvalue())
        while not log.getvalue():
            print("acc")
        sys.stdout = old_stdout
        sys.stderr = old_stderr

        if res.getvalue()[:2] == "[]":
            print("  Result: FALSE")
        else:
            # TODO delete all old traces
            logfname = output_directory + "/goal" + str(goal[0]) + ".trace"
            logfile = open(logfname, 'w')
            print("  Result: \033[92mTRUE\033[0m")
            print("  Save trace in: " + logfname)
            logfile.write(log.getvalue())
            logfile.close()
            '''
            for l in log.getvalue().splitlines():
                if "New fact" in l:
                    #print(l[l.find("New fact") + 11:])
                    logfile.write(l[l.find("New fact") + 11:] + "\n")
            '''

        datalogfile.close()
