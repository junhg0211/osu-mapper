from time import time
from math import inf

from pygame import midi
import keyboard

midi.init()

KPS_DURATION = 1
last_kps = 0
kps_max_record = 0

input_device = midi.Input(midi.get_default_input_id())

map_ = {
    36: 's', 37: 'escape', 38: 'd', 39: 'f1', 40: 'f2', 41: 'space', 42: 'f'
}

records = list()


def get_kps():
    global records, kps_max_record

    now = time()
    records.append(now)

    offset = 0
    for i, timestamp in enumerate(records):
        if timestamp < now - KPS_DURATION:
            records.pop(i - offset)
            offset += 1
    
    try:
        kps = (len(records) - 1) / (records[-1] - records[0])
        kps_max_record = max(kps_max_record, kps)
    except ZeroDivisionError:
        return inf
    else:
        return kps


while True:
    if data := input_device.read(1024):
        for datum in data:
            input_data, _ = datum
            if input_data[2] > 0:
                if input_data[1] in map_:
                    keyboard.press(map_[input_data[1]])
                    print(f'Press {map_[input_data[1]]}\t\t{(last_kps := get_kps()):3.03f} KPS')
                if input_data[1] == 37:
                    kps_max_record = 0
            else:
                if input_data[1] in map_:
                    keyboard.release(map_[input_data[1]])
                    print(f'Release {map_[input_data[1]]}\t{last_kps:3.03f} KPS\t\t{kps_max_record:f}')

