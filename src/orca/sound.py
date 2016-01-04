'''
Generating sound.
'''

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__license__   = "LGPL"

import os
import os.path
from gi.repository import GObject
import orca.settings_manager as settings_manager
import uuid

try:
    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gst', '1.0')
    from gi.repository import Gst
    import time, _thread
    _gstreamerAvailable = True
except:
    _gstreamerAvailable = False

_settingsManager = settings_manager.getManager()

class Sound():

    def __init__(self):
        Gst.init_check()
        self.lock = _thread.allocate_lock()

    def createTone(self, duration, frequence, volumeFactor = 1, wave = 0):
        '''
        duration = Integer (sec), it defines how long does a tone appear
        frequence = Integer (0-20000), defines the hight of the tone
        volumeFactor = Float (0.00-1.00), contain a difference to the sound volume
        (default 1 = no difference)
        wave = int (0 - 12) here are the types
        0 - a sine wave
        1 - a square wave
        2 - a saw wave
        3 - a tringle wave
        4 - silence
        5 - white uniform noise
        6 - pink noise
        7 - sine wave using a table
        8 - periodic ticks
        9 - white (zero mean) Gaussian noise; volume sets the standard deviation of the noise in units of the range of values of the sample type, e.g. volume=0.1 produces noise with a standard deviation of 0.1*32767=3277 with 16-bit integer samples, or 0.1*1.0=0.1 with floating-point samples.
        10 - red (brownian) noise
        11 - spectraly inverted pink noise
        12 - spectraly inverted red (brownian) noise
        returns a tone. a tone is a dict.
        '''
        if (frequence < 0): #check parameters
            frequence = 0
        if (frequence > 20000):
            frequence = 20000
        if volumeFactor < 0.00:
            volumeFactor = 0.00
        if volumeFactor > 1.00:
            volumeFactor = 1.00
        if (wave < 0) or (wave > 12):
            wave = 0
        return {'duration':duration, 'frequence':frequence, 'volumeFactor':volumeFactor, 'wave':wave}

    def playTone(self, tones):
        '''
        Plays a list of tones. is a blocking call
        tones is a list of "tones" created with createTone
        '''
        if not _gstreamerAvailable:
            return
        if not _settingsManager.getSetting('enableSound'):
            return
        self.lock.acquire(True)
        pipeline = Gst.Pipeline.new(str(uuid.uuid4()))
        source = Gst.ElementFactory.make('audiotestsrc')
        sink = Gst.ElementFactory.make('autoaudiosink')
        pipeline.add(source)
        pipeline.add(sink)
        source.link(sink)
        for tone in tones:
            source.set_property("volume", \
              _settingsManager.getSetting('soundVolume') * tone['volumeFactor'])
            source.set_property("freq", tone['frequence'])
            source.set_property("wave", tone['wave'])

            pipeline.set_state(Gst.State.PLAYING)
            time.sleep(tone['duration'])
            pipeline.set_state(Gst.State.NULL)
        self.lock.release()

    def playSoundFile(self, location):
        '''
        Plays a Audiofile
        '''
        if not _gstreamerAvailable:
            return
        if not _settingsManager.getSetting('enableSound'):
            return
        location = location.replace('~', os.path.expanduser('~'))
        if not self.isValidFile(location):
            return
        self.lock.acquire(True)
        pipeline = Gst.Pipeline.new()
        self.lock.release()
        source = Gst.ElementFactory.make('playbin')
        pipeline.add(source)
        source.set_property("uri", 'file://' + location)
        bus = pipeline.get_bus()
        pipeline.set_state(Gst.State.PLAYING)
        self.lock.acquire(True)
        message = None
        try:
            while(not message or 
              (message.type != Gst.MessageType.EOS) and  
              (message.type != Gst.MessageType.ERROR)):
                message = bus.pop()
        except Exception as e: 
            pass
        pipeline.set_state(Gst.State.NULL)
        self.lock.release()

    def playSimpleTone(self, duration, frequence, volumeFactor = 1, wave = 0):
        '''
        Plays as singel tone
        tone is created with createTone
        '''
        if not _gstreamerAvailable:
            return
        if not _settingsManager.getSetting('enableSound'):
            return
        tone = self.createTone( duration, frequence, volumeFactor, wave)
        tones = []
        tones.append(tone)
        self.playToneSequence(tones)

    def isValidFile(self, location):
        return (location != None) and\
          (location != '') and\
          os.path.exists(location) and\
          os.path.isfile(location) and\
          os.access(location, os.R_OK)

    def playSound(self, location ):
        '''
        plays a list of tones
        tones is a list of "tones" created with createTone
        '''
        if not _gstreamerAvailable:
            return
        location = location.replace('~', os.path.expanduser('~'))
        if not self.isValidFile(location):
            return 
        _thread.start_new_thread( self.playSoundFile, (location,  ) )

    def playToneSequence(self, tones):
        '''
        plays a list of tones
        tones is a list of "tones" created with createTone
        '''
        if not _gstreamerAvailable:
            return
        _thread.start_new_thread( self.playTone, (tones,  ) )
