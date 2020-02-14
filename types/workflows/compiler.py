from string import Template
from lark import Lark
import itertools
import re

class BehaviorTemplate(Template):
    delimiter = "$"
    idpattern = r'[a-z][=\->._a-z0-9\[\]\{\}]*'

class AccessPatternCompiler():
   grammar = '''
                    ?path: "this" point "[" access "]" -> readprop
                    | "this" point "{" access "}"   -> readattr

                    ?point: pnod point
                    | prel point
                    | pcap point
                    |                   -> empty

                    ?pnod: ".node"      -> node
                    | "=>" ID           -> dfa
                    | "<=" ID           -> dba
                    | ".src"            -> src

                    ?pcap: "<-" ID      -> ba
                    | ".dst"            -> dst

                    ?prel: ".rel"       -> rel
                    | "->" ID           -> fa

                    ?access: ID | ID "(" ID ")"

                    SYMBOL: LETTER | DIGIT | "_"
                    ID: SYMBOL+                 

                    %import common.LETTER
                    %import common.DIGIT
   '''
   start = 'path'

   def _compilepoint(self, point, ptr):
        if point.data == "empty": # Eboli
            return [ptr]
        # elif point.data == "point":
        #     return self.compile(point.children[0], ptr)
        elif point.children[0].data == "node":
            # check ptr is requirement or capability else error
            # move ptr to the node declaring the current requirement/capability
            # return LIST = eval(self, point.children[0], nuovo ptr)
            return self._compilepoint(point.children[1], ptr.node)
        elif point.children[0].data == "dfa":
            # TODO: ptr is a node AND ID is a requirement of ptr
            # move ptr to ALL :P the nodes pointed by the relationship starting from ID
            #for p ptr.outbound_relationships
            retlist = []
            for r in [r for r in ptr.outbound_relationships if r.name == str(point.children[0].children[0])]:
                retlist += self._compilepoint(point.children[1],r.target_node)
            return retlist
            # return LIST = UNION of ALL eval(self, point.children[1], nuovo ptr)
        elif point.children[0].data == "dba":
            # ptr is a node AND ID is a capability of ptr
            # move ptr to ALL :P the nodes pointed by the relationship arriving in ID
            # return LIST = UNION of ALL eval(self, point.children[1], nuovo ptr)
            retlist = []
            for r in [r for r in ptr.inbound_relationships if r.target_capability.name == str(point.children[0].children[0])]:
                retlist += self._compilepoint(point.children[1],r.source_node)
            return retlist
        elif point.children[0].data == "fa":
            # ptr is a node AND ID is a requirement of ptr
            # move the ptr to ALL the relationship starting from ID
            retlist = []
            for r in [r for r in ptr.outbound_relationships if r.name == str(point.children[0].children[0])]:
                retlist += self._compilepoint(point.children[1],r)
            return retlist
            # return LIST UNION eval(self, point.children[1], nuovo ptr)
        elif point.children[0].data == "ba":
            # ptr is a node AND ID is a capability of ptr
            # move the ptr to the requirement ID
            retlist = []
            for r in [r for r in ptr.inbound_relationships if r.target_capability.name == str(point.children[0].children[0])]:
                retlist += self._compilepoint(point.children[1],r)
            return retlist
            # return LIST eval(self, point.children[1], nuovo ptr)
        elif point.children[0].data == "src":
            # ptr is a relationship
            # move ptr to the source requirement of the relationship
            # return/Tem LIST eval (self, point.children[0], nuovo ptr)
            return self._compilepoint(point.children[1],ptr.source_node)
        elif point.children[0].data == "dst":
            # ptr is a relationship
            # move ptr to the destination capability of the relationship
            # return LIST eval (self, point.children[0], nuovo ptr)
            return self._compilepoint(point.children[1],ptr.target_capability)
        elif point.children[0].data == "rel":
            # ptr is a capability or a requirement
            # move ptr to ALL the relationships starting/arriving from/to ptr
            # TBD
            print("TODO implement rel")
            # return LIST UNION eval (self, point.children[0], nuovo ptr)

   def _compile(self, tree, ptr):
        retlist = []
        for p in self._compilepoint(tree.children[0], ptr):
            if tree.data == "readprop":
                retlist.append(p.properties[str(tree.children[1])])
            else:
                retlist.append(p.attributes[str(tree.children[1])])

        return retlist

   def compile(self, pattern, ptr):
       parser = Lark(self.grammar, start=self.start)

       tstring = BehaviorTemplate(pattern)

       result = [x[1] if x[1] != '' else x[2] for x in re.findall(tstring.pattern, tstring.template) if x[0] == '']
       # result = [ max(x) for x in re.findall(tstring.pattern, tstring.template) ] # re.findall(tstring.pattern, tstring.template)

       listofvalues = []
       for r in result:
           parse_tree = parser.parse(r)
           listofvalues.append(self._compile(parse_tree, ptr))

       listoftuples = []
       for v in itertools.product(*listofvalues):
           listoftuples.append(v)

       # "enriquez sanitization"(TM)

       i = 0
       for r in result:
           pattern = pattern.replace(result[i], "thisSUB" + str(i), 1)
           result[i] = "thisSUB" + str(i)
           i += 1

       tstring = BehaviorTemplate(pattern)

       rules = []
       for x in listoftuples:
           sub = dict(zip(tuple(result), x))
           rules.append(tstring.safe_substitute(sub))

       return rules