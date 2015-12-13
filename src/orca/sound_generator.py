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

    def getSoundIconToneSequence(self, obj, soundIconName = ''):
        '''
        obj = accessible object, could be None if soundIconName is set
        soundIconName = could be a fix name for an soundIcon (for non widget soundIcons
        return1 True = soundIcon found; False = no soundIcon found
        return2 the soundsequence to play with sound.playToneSequence(returnvalue) 
        or [] ( if no soundIcon is found)
        '''
        soundIcons = _settingsManager.getSetting('soundIcons')

        try:
            if (soundIconName != ''): # for a named soundIcon
                return True, soundIcons[soundIconName]

            role = obj.getRole() # soundIcon for a Role
            if (role in [pyatspi.ROLE_RADIO_BUTTON, pyatspi.ROLE_CHECK_BOX]) and\
              obj.getState().contains(pyatspi.STATE_CHECKED):
                return True, soundIcons[str(int(role)) + '-' + str(int(pyatspi.STATE_CHECKED))]
            return True, soundIcons[str(int(role))]
        except:
            return False, []
