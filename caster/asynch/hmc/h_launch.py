from subprocess import Popen
import sys, os


try: # Style C -- may be imported into Caster, or externally
    BASE_PATH = os.path.realpath(__file__).split("\\caster")[0].replace("\\", "/")
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
finally:
    from caster.asynch.hmc.hmc_ask_directory import Homunculus_Directory
    from caster.asynch.hmc.hmc_recording import Homunculus_Recording
    from caster.asynch.hmc.hmc_vocabulary import Homunculus_Vocabulary
    from caster.asynch.hmc.hmc_confirm import Homunculus_Confirm
    from caster.asynch.hmc.homunculus import Homunculus
    from caster.lib import settings

'''
To add a new homunculus (pop-up ui window) type:
    (1) create the module
    (2) and its type and title constants to settings.py
    (3) add it to  _get_title(), and "if __name__ == '__main__':" in this module
    (4) call launch() from this module with its type and any data it needs (data as a single string with no spaces)
'''

def launch(hmc_type, callback, data=None):
    from dragonfly import (WaitWindow, FocusWindow, Key)
    instructions=_get_instructions(hmc_type)
    if data!=None:
        instructions.append(data)
    Popen(instructions)
    
    hmc_title=_get_title(hmc_type)
    WaitWindow(title=hmc_title, timeout=5).execute()
    FocusWindow(title=hmc_title).execute()
    Key("tab").execute()
    
    from caster.asynch.hmc import squeue
    squeue.add_query(callback)

def _get_instructions(hmc_type):
    if hmc_type==settings.WXTYPE_SETTINGS:
        return ["pythonw", settings.SETTINGS["paths"]["SETTINGS_WINDOW_PATH"]]
    else:
        return ["pythonw", settings.SETTINGS["paths"]["HOMUNCULUS_PATH"], hmc_type]

def _get_title(hmc_type):
    default=settings.HOMUNCULUS_VERSION
    if hmc_type==settings.QTYPE_DEFAULT or hmc_type==settings.QTYPE_INSTRUCTIONS:
        return default
    elif hmc_type==settings.QTYPE_SET or hmc_type==settings.QTYPE_REM:
        return default+settings.HMC_TITLE_VOCABULARY
    elif hmc_type==settings.QTYPE_RECORDING:
        return default+settings.HMC_TITLE_RECORDING
    elif hmc_type==settings.QTYPE_DIRECTORY:
        return default+settings.HMC_TITLE_DIRECTORY
    elif hmc_type==settings.QTYPE_CONFIRM:
        return default+settings.HMC_TITLE_CONFIRM
    elif hmc_type==settings.WXTYPE_SETTINGS:
        return settings.SETTINGS_WINDOW_TITLE+settings.SOFTWARE_VERSION_NUMBER
    return default

if __name__ == '__main__':
    found_word=None
    if len(sys.argv)>2:
        found_word=sys.argv[2]
    if sys.argv[1]==settings.QTYPE_DEFAULT:
        app = Homunculus(sys.argv[1])
    elif sys.argv[1]==settings.QTYPE_SET:
        app = Homunculus_Vocabulary([settings.QTYPE_SET, found_word])
    elif sys.argv[1]==settings.QTYPE_REM:
        app = Homunculus_Vocabulary([settings.QTYPE_REM, found_word])
    elif sys.argv[1]==settings.QTYPE_RECORDING:
        app = Homunculus_Recording([settings.QTYPE_RECORDING, found_word])
    elif sys.argv[1]==settings.QTYPE_INSTRUCTIONS:
        app = Homunculus(sys.argv[1], sys.argv[2])
    elif sys.argv[1]==settings.QTYPE_DIRECTORY:
        app = Homunculus_Directory(sys.argv[1])
    elif sys.argv[1]==settings.QTYPE_CONFIRM:
        app = Homunculus_Confirm([sys.argv[1], sys.argv[2]])
