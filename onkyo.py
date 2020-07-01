import serial
import logging
import time

class Onkyo:
    """
    Class for controlling RS232C-enabled Onkyo/Integra stereo receivers

    device is the serial port on your computer. Required
    """
    def __init__(self, device):
        self.device = str(device)

        # Try to connect to serial port.
        try:
            self.scon = serial.Serial(
                port=device,
                baudrate=9600,
                stopbits=serial.STOPBITS_ONE,
                parity=serial.PARITY_NONE,
                xonxoff=False
            )
        except Exception as e:
            # If there's some kind of exception, quit
            raise Exception(e)

        logging.debug('Connected to {}'.format(device))

    def sendRawCMD(self, command):
        """ Sends a raw command to the Onkyo receiver. """
        # Commands need to be sent as bytes
        command = bytes(''.join(['!1', command, '\r']), encoding='utf-8')
        try:
            self.scon.write(command)
            logging.debug('SEND: {}'.format(command))
        except Exception as e:
            raise Exception(e)

        # Wait 50ms for the receiver to process the command sent
        time.sleep(0.05)
        return 0


    def powerOn(self):
        """ Powers on the unit """
        return self.sendRawCMD('PWR01')
    
    def powerOff(self):
        """ Powers off the unit """
        return self.sendRawCMD('PWR00')

    def setVolume(self, level):
        """ Sets volume to the desired level from 0-80 """

        if 1 <= level <= 80:
            # Volume level must be in hexadecimal
            level = format(int(level), 'x')

            # Volume needs to always be 2 chars
            level = level.zfill(2)
        else:
            # volume is out of range
            return 1

        return self.sendRawCMD('MVL{}'.format(str(level)))

    def volUp(self):
        """ Increases the volume """
        return self.sendRawCMD('MVLUP')

    def volDown(self):
        """ Decreases the volume """
        return self.sendRawCMD('MVLDOWN')

    def setInput(self, recvinput):
        """ Sets the unit to the desired audio input """

        recvinput = recvinput.upper() # make uppercase, so you could do video0 or VIDEO0 etc.
        if recvinput == 'VIDEO1':
            inputcode = 0
        elif recvinput == 'VIDEO2':
            inputcode = 1
        elif recvinput == 'VIDEO3':
            inputcode = 2
        elif recvinput == 'VIDEO4':
            inputcode = 3
        elif recvinput == 'VIDEO5':
            inputcode = 4
        elif recvinput == 'VIDEO6':
            inputcode = 5
        elif recvinput == 'VIDEO7':
            inputcode = 6
        elif recvinput == 'DVD':
            inputcode = 10
        elif recvinput == 'TAPE1':
            inputcode = 20
        elif recvinput == 'TAPE2':
            inputcode = 21
        elif recvinput == 'PHONO':
            inputcode = 22
        elif recvinput == 'CD':
            inputcode = 23
        elif recvinput == 'FM':
            inputcode = 24
        elif recvinput == 'AM':
            inputcode = 25
        elif recvinput == 'TUNER':
            # This will cycle through all available radio inputs
            inputcode = 26
        elif recvinput == 'XM':
            inputcode = 31
        elif recvinput == 'SIRIUS':
            inputcode = 32
        else:
            logging.warning('Invalid input')
            return 1
        
        # Add a 0 before the input number if it is a single-digit number 
        inputcode = str(inputcode).zfill(2)
        
        return self.sendRawCMD('SLI{}'.format(inputcode))
        
    
    def tuneFreq(self, band, freq):
        """ Tunes the stereo to the desired frequency. 
        Specify as a float for a FM frequency (example: 93.3)
        Specify as an integer for an AM frequency (example: 1040)
        """

        # TODO: Implement Sirius and XM tuning

        # make band lowercase for the sake of simplicity
        band = band.lower()

        if band == 'am' and type(freq) == int:
            # AM
            freq = str(freq).zfill(5)
            self.setInput('AM')
        elif band == 'fm' and type(freq) == float:
            # FM
            freq = str(freq).replace('.', '') + '0'
            freq = freq.zfill(5)
            self.setInput('FM')
        else:
            return 1 # invalid band

        # tune to the input
        return self.sendRawCMD('TUN{}'.format(freq))

    def tunePreset(self, preset):
        """ Tunes to a specific preset. Range is 1-40
        """
        # preset must be between 1 and 40.
        if 1 <= preset <= 40:
            # preset is in hexadecimal form
            preset = format(preset, 'x')

            # preset must always be 2 chars long
            preset = preset.zfill(2)

            return self.sendRawCMD('PRS{}'.format(preset))
        else:
            # Invalid preset
            return 1

    def sendTrigger(self, trigger, power):
        """ Turn on/off a 12V trigger. This may be limited to Integra units only
        trigger: 12v trigger plug A, B, or C
        power: True is ON, False is OFF
        """

        trigger = str(trigger).upper()
        if trigger not in ('A', 'B', 'C'):
            return 'wrong 12v trigger'

        if power == True: trigcode = '01'
        else: trigcode == '00'

        return self.sendRawCMD('TG{}{}'.format(trigger,trigcode))

    def setDimmer(self, level):
        """ Dims the display. Valid options: bright, dim, dark, off """

        level = level.lower() # make lowercase for sake of simplicity

        if level == 'bright': dimcode = 0
        elif level == 'dim': dimcode = 1
        elif level == 'dark': dimcode = 2
        elif level == 'off': dimcode = 3

        # Add a 0 before the dimmer level
        levelcode = str(dimcode).zfill(2)

        return self.sendRawCMD('DIM{}'.format(levelcode))


    def close(self):
        """ Closes the serial connection """

        # You can only close the connection if there is an active session
        if self.scon.is_open == True:
            self.scon.close()
            logging.debug("Connection closed")
            return 0
        return 1
