#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for MSVC

"""


#---------------------------------------------------------------------------

from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, IntegerRef,
                       Key, Text, Repeat, Pause)
from caster.lib.dfplus.state.short import R

class CommandRule(MappingRule):

    mapping = {
        
           
            "cursor prior":                             R(Key("c-minus"), rdescript="MSVC: Cursor Prior"), 
            "cursor next":                              R(Key("cs-minus"), rdescript="MSVC: Cursor Next"), 
            "toggle fullscreen":                        R(Key("sa-enter"), rdescript="MSVC: Toggle Fullscreen"), 
            "resolve":                                  R(Key("c-dot"), rdescript="MSVC: Resolve"), 
            "jump to source":                           R(Key("f12"), rdescript="MSVC: Jump To Source"), 
            "snippet":                                  R(Key("tab"), rdescript="MSVC: Snippet"), 
            "search for this everywhere":               R(Key("cs-f"), rdescript="MSVC: Search Everywhere"), 
             
            "step over [<n>]":                          R(Key("f10/50") * Repeat(extra="n"), rdescript="MSVC: Step Over"),
            "step into":                                R(Key("f11"), rdescript="MSVC: Step Into"),
            "step out [of]":                            R(Key("s-f11"), rdescript="MSVC: Step Out"),
            "resume":                                   R(Key("f8"), rdescript="MSVC: Resume"),
            "build [last]":                             R(Key("ca-f7"), rdescript="MSVC: Build"),
            "debug [last]":                             R(Key("f5"), rdescript="MSVC: Debug"),
            "comment out":                              R(Key("c-k/50, c-c"), rdescript="MSVC: Comment Out"),
            "on comment out":                           R(Key("c-k/50, c-u"), rdescript="MSVC: Uncomment Out"),
            
            "set bookmark":                             R(Key("c-k, c-k"), rdescript="MSVC: Set Bookmark"), 
            "next bookmark":                            R(Key("c-k, c-n"), rdescript="MSVC: Next Bookmark"), 
            "breakpoint":                               R(Key("f9"), rdescript="MSVC: Breakpoint"),
            
            "format code":                              R(Key("cs-f"), rdescript="MSVC: Format Code"),
            "(do imports | import all)":                R(Key("cs-o"), rdescript="MSVC: Do Imports"),
            "comment line":                             R(Key("c-slash"), rdescript="MSVC: Comment Line"),
        }
    extras = [
              Dictation("text"),
              IntegerRef("n", 1, 1000),
              
             ]
    defaults = {"n": 1}

#---------------------------------------------------------------------------

context = AppContext(executable="WDExpress")
grammar = Grammar("WDExpress", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
