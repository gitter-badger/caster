'''
Created on May 27, 2015

@author: dave
'''
from dragonfly import MappingRule, ActionBase

from caster.lib.dfplus.state.actions import ContextSeeker
from caster.lib.dfplus.state.short import L, S

class HintNode:
    def __init__(self, spec, base, children=[], extras=[], defaults={}):
        err = str(spec)+", "+str(base)+", "+str(children)
        assert isinstance(spec, basestring), "Node spec must be string: "+err
        assert isinstance(base, ActionBase), "Node base must be actionbase: "+err
        assert len(children)==0 or isinstance(children[0], HintNode), "Children must be nodes: "+err
        
        self.base = base
        self.children = children
        self.spec = spec
        self.extras = extras
        self.defaults = defaults
        self.active = False
        # 0 is the first set of children
        self.explode_depth = 1  # the level at which to turn all children into rules
    
    def all_possibilities(self):
        p = []
        for child in self.children:
            p += [x[0] for x in child.explode_children(0, True)]
        return p
    
    def explode_children(self, depth, max=False):
        results = [self.get_spec_and_base_and_node()]
        depth -= 1
        if depth>=0 or max:
            for child in self.children:
                e = child.explode_children(depth, max)
                for t in e:
                    results.append((results[0][0] + " " + t[0], results[0][1] + t[1], t[2]))
        return results
    
    def get_spec_and_base_and_node(self):
        return (self.spec, self.base, self)
            
    def fill_out_rule(self, mapping, extras, defaults, node_rule):
        specs = self.explode_children(self.explode_depth)
        if len(specs)>1:
            specs.append(self.get_spec_and_base_and_node())
        
        for spec, base, node in specs:
            action = base+NodeChange(node_rule, node)
            if node_rule.post!=None:
                action = action+node_rule.post
            mapping[spec] = action
        extras.extend(self.extras)
        defaults.update(self.defaults)

class NodeRule(MappingRule):
    master_node = None
    stat_msg = None
    
    def set_grammar(self, grammar):
        '''for when the grammar is not known in advance'''
        self.grammar = grammar
    
    def __init__(self, node, grammar, stat_msg=None, is_reset=False):
        # for self modification
        self.node = node
        first = False
        if self.master_node == None:
            self.master_node = self.node
            first = True
            self.post = ContextSeeker(forward=[L(S(["cancel"], self.reset_node, consume=False))], rspec=self.master_node.spec)
        if self.stat_msg == None:
            self.stat_msg = stat_msg        
        
        mapping = {}
        extras = []
        defaults = {}
        
        # each child node gets turned into a mapping key/value
        for child in self.node.children:
            child.fill_out_rule(mapping, extras, defaults, self)
        
        if len(mapping)==0:
            if self.stat_msg!=None and not first:
                self.stat_msg.text("Node Reset")# status window messaging
            self.reset_node()
            for child in self.node.children:
                child.fill_out_rule(mapping, extras, defaults, self)
        else:
            if self.stat_msg!=None and not first and not is_reset:# status window messaging
                self.stat_msg.hint("\n".join([x.get_spec_and_base_and_node()[0] for x in self.node.children]))
        
        
        MappingRule.__init__(self, "node_" + str(self.master_node.spec), mapping, extras, defaults)
        self.grammar = grammar
        
    
    def change_node(self, node, reset=False):
        self.grammar.unload()
        NodeRule.__init__(self, node, self.grammar, None, reset)
        self.grammar.load()
    
    def reset_node(self):
        self.change_node(self.master_node, True)
    
    def _process_recognition(self, node, extras):
        '''
        There are two kinds of nodes being referred to in here: Dragonfly _processor_recognition nodes, 
        and Caster hintnode.HintNode(s). "node" is the former, "self.node" is the latter.
        '''
        node=node[self.master_node.spec]
        node._action.execute(node._data)
        
    
class NodeAction(ActionBase):
    def __init__(self, node_rule):
        ActionBase.__init__(self)
        self.node_rule = node_rule
    def _execute(self, data):
        self.node_rule._process_recognition(data, None)

class NodeChange(ActionBase):
    def __init__(self, node_rule, node):
        ActionBase.__init__(self)
        self.node_rule = node_rule
        self.node = node
    def _execute(self, data):
        self.node_rule.change_node(self.node)

