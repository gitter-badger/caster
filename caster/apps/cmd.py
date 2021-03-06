#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for git

"""


#---------------------------------------------------------------------------

from dragonfly import (Grammar, AppContext, MappingRule,
                       Key, Text)
from caster.lib.dfplus.state.short import R

class CommandRule(MappingRule):

    mapping = {
        "C drive":          R(Text(r"cd C:/")+Key("enter"), rdescript="CMD: Go To C:"),
        "CD up":            R(Text( "cd .." )+Key("enter"), rdescript="CMD: Up Directory"),
        "CD":               R(Text( "cd " ), rdescript="CMD: Navigate Directory"),
        "list":             R(Text( "dir" )+Key("enter"), rdescript="CMD: List Files"),
        "make directory":   R(Text( "mkdir " ), rdescript="CMD: Make directory"),
        
        
        
        "exit":             R(Text( "exit" )+Key("enter"), rdescript="CMD: Exit"),
        }
    extras = [
              
             ]
    defaults ={}


#---------------------------------------------------------------------------

context = AppContext(executable="cmd")
grammar = Grammar("cmd", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None