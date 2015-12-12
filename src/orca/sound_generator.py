'''
Utilities for generating sound.
'''

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__license__   = "LGPL"

import pyatspi
import orca.debug as debug
import orca.settings_manager as settings_manager
import orca.generator as generator
_settingsManager = settings_manager.getManager()

class SoundGenerator():

    def __init__(self):
        pass

    # Progressbar
    def getFreqForPercentage(self, percentage):
        if percentage < 7: # whe have to adjust this, otherwhise the first beeps are too deep
            return( int((98 + percentage * 5.4)))
        return( int(percentage * 22))

    def getVolumeFactorForPercentage(self, percentage):
        return(1 - (percentage / 120)) # then higher then more quiter (we wont damage the ears).

    def getDurationForPercentage(self, percentage):
            if percentage >= 99: #long beeps for the last two percent (to notify the end)
                return(1)
            return (0.075)

    def isProgressBarBeepEnabled(self):
        return (_settingsManager.getSetting('beepProgressBarUpdates'))

    def getSoundIconToneSequence(self, obj, role):
        if not role:
            return False, []
        soundIcons = _settingsManager.getSetting('soundIcons')
#        soundIcons = {\
#          pyatspi.ROLE_CHECK_BOX:[{'duration':0.1, 'frequence':360, 'volumeFactor':1, 'wave':2}] ,\
#          pyatspi.ROLE_PUSH_BUTTON:[{'duration':0.1, 'frequence':880, 'volumeFactor':1, 'wave':3}], \
#          pyatspi.ROLE_RADIO_BUTTON:[{'duration':0.1, 'frequence':420, 'volumeFactor':1, 'wave':1}] ,\
#          pyatspi.ROLE_COMBO_BOX:[{'duration':0.1, 'frequence':418, 'volumeFactor':1, 'wave':0},
#{'duration':0.1, 'frequence':460, 'volumeFactor':1, 'wave':0},
#{'duration':0.1, 'frequence':500, 'volumeFactor':1, 'wave':0}] ,\
#          #pyatspi.ROLE_ENTRY:[{'duration':0.1, 'frequence':420, 'volumeFactor':1, 'wave':5}] ,\
#          pyatspi.ROLE_TEXT:[{'duration':0.1, 'frequence':420, 'volumeFactor':1, 'wave':5}] ,\
#          }

        try:
            state = obj.getState()
            if (role in [pyatspi.ROLE_RADIO_BUTTON,pyatspi.ROLE_CHECK_BOX]) and state.contains(pyatspi.STATE_CHECKED):
                return True, soundIcons[str(int(role)) + '-' + str(int(pyatspi.STATE_CHECKED))]
            return True, soundIcons[str(int(role))]
        except:
            return False, []
