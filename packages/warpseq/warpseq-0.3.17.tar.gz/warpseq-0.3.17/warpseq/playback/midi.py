
MIDI_NOTE_OFF = 0x80
# 1000cccc 0nnnnnnn 0vvvvvvv (channel, note, velocity)
MIDI_NOTE_ON = 0x90
# 1001cccc 0nnnnnnn 0vvvvvvv (channel, note, velocity)
MIDI_POLYPHONIC_PRESSURE = AFTERTOUCH = 0xA0
# 1010cccc 0nnnnnnn 0vvvvvvv (channel, note, velocity)
MIDI_CONTROLLER_CHANGE = 0xB0 # see Channel Mode Messages!!!
# 1011cccc 0ccccccc 0vvvvvvv (channel, controller, value)
MIDI_PROGRAM_CHANGE = 0xC0
# 1100cccc 0ppppppp (channel, program)
MIDI_CHANNEL_PRESSURE = 0xD0
# 1101cccc 0ppppppp (channel, pressure)
MIDI_PITCH_BEND = 0xE0
# 1110cccc 0vvvvvvv 0wwwwwww (channel, value-lo, value-hi)
MIDI_NOTE_OFF = 0x80
# 1000cccc 0nnnnnnn 0vvvvvvv (channel, note, velocity)
MIDI_NOTE_ON = 0x90

import rtmidi as rtmidi
import functools

def get_midi_out():
    return rtmidi.MidiOut()

@functools.lru_cache()
def get_ports():
    out = get_midi_out()
    return out.get_ports()

def get_devices():
    return get_ports()

def open_port(device_name):
    out = get_midi_out()
    ports = get_ports()

    midi_port = None
    index = 0
    for p in ports:
        if p == device_name:
            midi_port = index
            break
        index = index + 1

    if midi_port is None:
        raise MIDIConfigError("MIDI device named (%s) not found, available choices: %s" % (device_name, ports))

    return out.open_port(midi_port)


def midi_note_on(out, channel, note_number, velocity):
    if not note_number:
        return
    out.send_message([MIDI_NOTE_ON | channel - 1, note_number, velocity])

def midi_note_off(out, channel, note_number, velocity):
    if not note_number:
        return
    out.send_message([MIDI_NOTE_OFF | channel - 1, note_number, velocity])

def _channel_message(out, command, channel, *data):
    command = (command & 0xf0) | (channel - 1 & 0xf)
    msg = [command] + [value & 0x7f for value in data]
    out.send_message(msg)

def midi_cc(out, channel, controller, value):
    _channel_message(out, MIDI_CONTROLLER_CHANGE, channel, controller, value)


