#!/usr/bin/python3
#
# This script allows you to use Space-key as a modifier key like Shift or Ctrl and also as a usual Space-key at the same time.
# It should work in any linux distributive.
# 
# Install dependencies first:
#   For Ubuntu:
#       sudo apt-get install python-dev python3-pip gcc
#       sudo pip install evdev 
#
#   For other distros:
#       https://python-evdev.readthedocs.io/en/latest/install.html
#
# This script adds the following bindings:
#   Space+j = Left
#   Space+l = Right
#   Space+i = Up
#   Space+k = Down
#   Space+u = Backspace
#   Space+o = Delete
#   Space+h = Home
#   Space+; = End
#   Space+n = PageUp
#   Space+m = PageDown
#
#   Ctrl+Alt+Win+q = quit script
#   Ctrl+Alt+Win+z = pause/unpase bindings
#
# You can change the bindings as you like, see the keycodes_to_bind section
#
# To run the script execute it with sudo:
#   sudo python3 linux-deep-hotkeys.py
#
# Then when you know your device name, you can run the script in background:
#   sudo python3 linux-deep-hotkeys.py --device /dev/input/event7 &
#


import evdev
import time
import asyncio
import sys
import logging
import argparse





# list of ecodes is available by intellisense autocomplete or by link: https://gitlab.freedesktop.org/libevdev/libevdev/-/blob/master/include/linux/linux/input-event-codes.h#L64
keycodes_to_bind = {
    evdev.ecodes.KEY_J : evdev.ecodes.KEY_LEFT,
    evdev.ecodes.KEY_L : evdev.ecodes.KEY_RIGHT,
    evdev.ecodes.KEY_I : evdev.ecodes.KEY_UP,    
    evdev.ecodes.KEY_K : evdev.ecodes.KEY_DOWN,    
    evdev.ecodes.KEY_U : evdev.ecodes.KEY_BACKSPACE,    
    evdev.ecodes.KEY_O : evdev.ecodes.KEY_DELETE,    
    evdev.ecodes.KEY_H : evdev.ecodes.KEY_HOME,    
    evdev.ecodes.KEY_SEMICOLON : evdev.ecodes.KEY_END,    
    evdev.ecodes.KEY_N : evdev.ecodes.KEY_PAGEUP,
    evdev.ecodes.KEY_M : evdev.ecodes.KEY_PAGEDOWN
}



# switch between log level
#logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)




def get_device_name_from_cli():
    # print(sys.argv)

    # Initiate the parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--device", help="set keyboard device path", metavar="/dev/input/event<N>")

    # Read arguments from the command line
    args = parser.parse_args()

    if args.device:
        return args.device



def get_device_from_user_input():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    # for device in devices:
    #     #print('')
    #     print(device.path, device.name, device.phys)
    #     #print(device.capabilities(True))


    if len(devices) == 0:
        # If you do not see any devices, ensure that your user is in the correct group (typically input) to have read/write access.    
        # https://python-evdev.readthedocs.io/en/latest/usage.html#listing-accessible-event-devices
        sys.exit('ERROR: no devices found, please restart as root, or add user to `input` group')

    print('list of devices:')
    for i, device in enumerate(devices):
        print(str(i).rjust(3, ' '), ':', device.path, '-', device.name, '-', device.phys)    

    keyboard_index = int(input('Select your keyboard (number): '))

    if keyboard_index < 0 or keyboard_index >= len(devices):
        sys.exit('ERROR: Wrong keyboard number')

    return devices[keyboard_index].path



                                                                   
async def action(device, fake_device):
    global keycodes_to_bind

    try:
        is_on_pause = False # no remapping if script is on pause

        is_leftctrl_down = False
        is_rightctrl_down = False
        is_ctrl_down = False

        is_leftalt_down = False
        is_rightalt_down = False
        is_alt_down = False

        is_leftshift_down = False
        is_rightshift_down = False
        is_shift_down = False

        is_leftwin_down = False
        is_rightwin_down = False
        is_win_down = False

        is_space_down = False

        list_of_keydowns_while_space_down = []
        
        # const from evdev
        key_is_hold = 2 # key is holding
        key_is_down = 1 # key is pressed
        key_is_up = 0   # key is released
        
        
        # for catching space hotkey
        hotkey_with_space_pressed = False
        
        device.grab() # https://python-evdev.readthedocs.io/en/latest/tutorial.html#getting-exclusive-access-to-a-device
        async for event in device.async_read_loop(): # https://python-evdev.readthedocs.io/en/latest/tutorial.html#reading-events-using-asyncio

        
            # event.type == evdev.ecodes.EV_...
            # https://www.kernel.org/doc/Documentation/input/event-codes.txt
        
            skip_send = False # for not to send current key
    
        
            if event.type != evdev.ecodes.EV_KEY:
                if event.type == evdev.ecodes.EV_MSC:
                    logging.debug('')
                
                logging.debug('event.type=%s, event=%s, sending as is', event.type, evdev.categorize(event))
                fake_device.write_event(event)
        
            else:
                logging.debug('event.type=EV_KEY event.code=%s event.value=%s %s %s', event.code, event.value, 'isDown' if event.value==key_is_down else '', 'isUp' if event.value==key_is_up else '')

        
                if event.code == evdev.ecodes.KEY_LEFTCTRL:
                    is_leftctrl_down = event.value

                elif event.code == evdev.ecodes.KEY_RIGHTCTRL:
                    is_rightctrl_down = event.value                   
                
                elif event.code == evdev.ecodes.KEY_LEFTALT:
                    is_leftalt_down = event.value

                elif event.code == evdev.ecodes.KEY_RIGHTALT:
                    is_rightalt_down = event.value                    
        
                elif event.code == evdev.ecodes.KEY_LEFTSHIFT:
                    is_leftshift_down = event.value

                elif event.code == evdev.ecodes.KEY_RIGHTSHIFT:
                    is_rightshift_down = event.value

                elif event.code == evdev.ecodes.KEY_LEFTMETA:
                    is_leftwin_down = event.value

                elif event.code == evdev.ecodes.KEY_RIGHTMETA:
                    is_rightwin_down = event.value
        
                elif event.code == evdev.ecodes.KEY_SPACE:
                    is_space_down = event.value
                    if event.value == key_is_down or event.value == key_is_hold:
                        list_of_keydowns_while_space_down = []
                        skip_send = True
                        hotkey_with_space_pressed = False
        
                    if event.value == key_is_up:
                        if hotkey_with_space_pressed:
                            skip_send = True
                        else:
                            # send `space` key if no hotkey with `space` was pressed
                            # send `space` down before sending current event (`space` up)
                            logging.debug('---> send space event-down before sending event-up')
                            fake_device.write_event(evdev.InputEvent(event.sec, event.usec, event.type, evdev.ecodes.KEY_SPACE, 1))
        
            # print('leftctrl=', is_leftctrl_down, 'leftalt=', is_leftalt_down, 'leftshift=', is_leftshift_down, 'leftmeta=', is_leftmeta_down, 'space=', is_space_down)           

                is_ctrl_down = is_leftctrl_down or is_rightctrl_down
                is_alt_down = is_leftalt_down or is_rightalt_down
                is_shift_down = is_leftshift_down or is_rightshift_down
                is_win_down = is_leftwin_down or is_rightwin_down


                if event.value == key_is_down:
                    #handle special hotkeys on key-down only!

                    if event.code == evdev.ecodes.KEY_Q and is_win_down and is_ctrl_down and is_alt_down:
                        print('win+ctrl+alt+q, quit!')
                        device.ungrab()
                        sys.exit()
                        break

                    if event.code == evdev.ecodes.KEY_Z and is_win_down and is_ctrl_down and is_alt_down:
                        if is_on_pause:
                            print('win+ctrl+alt+z, unpause script')
                            is_on_pause = False
                        else:
                            print('win+ctrl+alt+z, pause script')
                            is_on_pause = True




                # main logic begins

                if event.value == key_is_down or event.value == key_is_hold:
                    if not is_on_pause and is_space_down and event.code in keycodes_to_bind:
                        # that is our key, modify it

                        # save keys to modify on key-up
                        list_of_keydowns_while_space_down.append(event.code)

                        # modify key code
                        event.code = keycodes_to_bind[event.code]

                        # save flag that hotkey was pressed for not to send space-key
                        hotkey_with_space_pressed = True


                elif event.value == key_is_up: 
                    # we must modify key-up event even when space-key was just released and not pressed anymore

                    if event.code in list_of_keydowns_while_space_down:
                        # that is our key, modify it

                        # remove that key from list
                        list_of_keydowns_while_space_down.remove(event.code)

                        # modify key code
                        event.code = keycodes_to_bind[event.code]
    
                if not skip_send:
                    logging.debug('---> sending event: %s', evdev.categorize(event))
                    fake_device.write_event(event)

    except Exception as e:
        logging.error(e)
        device.ungrab()
        print('device ungrabbed')




def main():
    device_path = get_device_name_from_cli() or get_device_from_user_input()

    time.sleep(1) # waiting for key-up events after pressing previous Enter

    try:
        device = evdev.InputDevice(device_path)
    except:
        sys.exit('ERROR: Wrong device name: '+device_path+', try run without arguments')

    print('Device selected:', device)
    print('')
    print('Start listening for events...')

    fake_device = evdev.UInput() 

    loop = asyncio.get_event_loop()
    loop.run_until_complete(action(device, fake_device))       


main()


