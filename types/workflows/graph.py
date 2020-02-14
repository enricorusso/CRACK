from aria import workflow

@workflow
def creategraph(ctx, graph):
    print '''
digraph {
 node [shape=record]
 rankdir=LR;

    '''

    rel = []
    for n in ctx.nodes:
        if "aria" in n.type.name:
            t = n.type.name[21:]
            s = "style=dashed"
        else:
            t = n.type.name[10:]
            s = ""

        if t not in [ "invariant" ]:

            name = n.node_template_name.replace("-", "_")

            print ''' {} [
            label=<<font point-size="12"><b>{}</b></font> | 
            <font point-size="11">{}</font> | 
            <font point-size="3"> </font>> shape=Mrecord {} ]        
            '''.format(name, n.node_template_name, t, s)


            for r in n.outbound_relationships:
                if ((r.name != "host") or (r.name == "host" and
                                           (n.type.name[0:16] == "sdl.nodes.System" or n.type.name[
                                                                                       0:18] == "sdl.nodes.Firewall"))):
                    if r.name not in [ "keypair" ]:
                       rel.append("{} -> {}".format(name, r.target_node.node_template_name.replace("-", "_")))

    for r in rel:
        print r

    print '''
    }
'''


'''


label=<<font point-size="12"><b>gigi</b></font> | 
<font point-size="11">pippo</font> | 
<font point-size="3"> </font>> shape=Mrecord ]

if (n.type.name == "aria.openstack.nodes.Server") or (n.type.name[0:4] == "sdl."):
    print n.node_template_name + " [label=<"
    print "<table border=\"0\" cellborder=\"1\" cellspacing=\"0\">"
    print ("<tr><td bgcolor=\"lightblue\"><FONT POINT-SIZE=\"12\"><b>%s</b></FONT></td></tr>" % (n.node_template_name))
    print ("<tr><td><FONT POINT-SIZE=\"8\">%s</FONT></td></tr>" % (n.type.name))
    if n.type.name != "aria.openstack.nodes.Server":
        for r in n.outbound_relationships:
            if ((r.name != "host") or (r.name == "host" and
                                       (n.type.name[0:16] == "sdl.nodes.System" or n.type.name[0:18] == "sdl.nodes.Firewall"))):
                print("<tr><td port=\"%s\"><FONT POINT-SIZE=\"12\">%s</FONT></td></tr>" % (r.name, r.name))
        print "</table>>];"
        print
        # n.type.name[0:4] aria
        for r in n.outbound_relationships:
            if ((r.name != "host") or (r.name == "host" and
                                       (n.type.name[0:16] == "sdl.nodes.System" or n.type.name[0:18] == "sdl.nodes.Firewall"))):
                print("%s:%s -> %s" % (n.node_template_name, r.name, r.target_node.node_template_name))
        print
    else:
        print "</table>>];"
        print
'''
