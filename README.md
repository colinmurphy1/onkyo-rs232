# Onkyo-RS232

A python library (and later, utility) for controlling an Onkyo or Integra stereo receiver using the Onkyo [RS232 protocol][1].

For a general overview of usage, see `test.py`. 


## Command list

### `sendRawCMD`

Sends a raw command to the receiver. Omit the `!1` from the command.

Example:

    # turns on the receiver
    onkyo.sendRawCMD('PWR01')

### `powerOn`

Turns on the receiver.

### `powerOff`

Turns off the receiver.

### `setVolume`

Sets volume to the desired level.

**Not fully implemented yet! You may accidentally set the volume to a level that is too high.**

### `volUp`

Increases the volume by 1.

### `volDown`

Decreases the volume by 1.

### `setInput`

Changes the input on the receiver to the desired input.

Implemented options:

* VIDEO0 (VCR/DVR)
* VIDEO1 (CBL/SAT)
* VIDEO2 (GAME/TV)
* VIDEO3 (AUX1)
* VIDEO4 (AUX2)
* VIDEO5
* VIDEO6
* VIDEO7
* DVD
* TAPE1
* TAPE2
* PHONO
* CD
* FM
* AM
* TUNER
* XM
* SIRIUS

Each receiver model has different inputs that are supported. If the input does not exist, it will not change inputs and will remain on the current input. 

### `setFreq`

Tunes to the specified frequency.

* If frequency is specified as a float, or `xxx.x`, it will tune to a FM frequency.
* If frequency is specified as an integer, or `xxxx`, it will tune to an AM frequency. 

To tune to 93.3 MHz, do `setFreq(93.3)`. Meanwhile, to tune to 540 KHz, do `setFreq(540)`.

### `sendTrigger`

Turns on or off the 12V triggers on Integra receivers.

To turn 12V trigger A to ON: `sendTrigger('A', True)`

### `setDimmer`

Dims the display on the receiver.

Options:

* `bright`
* `dim`
* `dark`
* `off`

To dim the screen, `setDimmer('dim')`

### `close`

Closes the serial connection to the receiver.

[1]: http://www.schematicsforfree.com/archive/file/Video/DVD%20&%20Other%20Disc%20Players/Onkyo%20-%20Dtr-6%202-Rs-232Codes.pdf