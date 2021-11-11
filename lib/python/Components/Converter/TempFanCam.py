# TempFanCam (c) BlackFish 2020
from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.Converter.Poll import Poll
from Components.Sensors import sensors
from Tools.Directories import fileExists
import os

class TempFanCam(Poll, Converter, object):
    TEMPINFO = 1
    FANINFO = 2
    CAMNAME = 5

    def __init__(self, type):
        Poll.__init__(self)
        Converter.__init__(self, type)
        self.type = type
        self.poll_interval = 30000
        self.poll_enabled = True
        if type == 'TempInfo':
            self.type = self.TEMPINFO
        elif type == 'FanInfo':
            self.type = self.FANINFO
        elif type == 'CamName':
            self.type = self.CAMNAME   

    @cached
    def getText(self):
        textvalue = ''
        if self.type == self.TEMPINFO:
            textvalue = self.tempfile()
        elif self.type == self.FANINFO:
            textvalue = self.fanfile()
        elif self.type == self.CAMNAME:
            textvalue = self.getCamName()    
        return textvalue

    text = property(getText)

    def tempfile(self):
        temp = ''
        try:
            f = open('/proc/hisi/msp/pm_cpu', 'rb')
            temp = open ("/proc/hisi/msp/pm_cpu", "r").readlines()[2].strip('Tsensor: temperature = ')[:-9]
            f.close()
            mark = str('\xc2\xb0')
            tempinfo = 'CPU ' + str(temp) + mark + 'C'
            return tempinfo
        except:
            pass

    def fanfile(self):
        fan = ''
        try:
            f = open('/proc/stb/fp/fan_speed', 'rb')
            fan = f.readline().strip()
            f.close()
            faninfo = 'FAN: ' + str(fan)
            return faninfo
        except:
            pass
            
    def getCamName(self):
        if os.path.exists('/etc/init.d/softcam'):
            try:
                for line in open('/etc/init.d/softcam'):
                    line = line.lower()
                    if 'wicardd' in line:
                        return 'WiCard'
                    if 'incubus' in line:
                        return 'Incubus'
                    if 'gbox' in line:
                        return 'Gbox'
                    if 'mbox' in line:
                        return 'Mbox'
                    if 'cccam' in line:
                        return 'CCcam'
                    if 'oscam-emu' in line:
                        return 'oscam-emu'
                    if 'oscam' in line:
                        return 'OSCam'
                    if 'camd3' in line:
                        if 'mgcamd' not in line:
                            return 'Camd3'
                    else:
                        if 'mgcamd' in line:
                            return 'Mgcamd'
                        if 'gcam' in line:
                            if 'mgcamd' not in line:
                                return 'GCam'
                        else:
                            if 'ncam' in line:
                                return 'NCam'
                            if 'common' in line:
                                return 'CI'
                            if 'interface' in line:
                                return 'CI'

            except:
                pass

        return ''
        

    def changed(self, what):
        if what[0] == self.CHANGED_POLL:
            Converter.changed(self, what)
