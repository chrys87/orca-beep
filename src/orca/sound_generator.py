'''
Utilities for generating sound.
'''

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__license__   = "LGPL"

import orca.settings_manager as settings_manager
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
