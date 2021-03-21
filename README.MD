# linux-deep-hotkeys

This script allows you to use Space-key as a modifier key like Shift or Ctrl and as a usual Space-key at the same time.

This script adds the following bindings:
```
   Space + j = Left
   Space + l = Right
   Space + i = Up
   Space + k = Down
   Space + u = Backspace
   Space + o = Delete
   Space + h = Home
   Space + ; = End
   Space + n = PageUp
   Space + m = PageDown

   Ctrl+Alt+Win+q = quit script
   Ctrl+Alt+Win+z = pause/unpase bindings
```   
But you can modify it as you like.


<br/>

## Step 1 : install evdev

Evdev is a library for working with input devices.

More details here: https://en.wikipedia.org/wiki/Evdev

To install it for Ubuntu:

```
sudo apt-get install python-dev python3-pip gcc
```

```
sudo pip install evdev 
```

For more details and other distros please see:

https://python-evdev.readthedocs.io/en/latest/install.html

<br/>

## Step 2 : get script

```
wget https://raw.githubusercontent.com/LexRiver/linux-deep-hotkeys/main/linux-deep-hotkeys.py
```

<br/>

## Step 3 : run script

To modify keyboard codes user must be in group `input`, so run the script as root.

```
sudo python3 linux-deep-hotkeys.py
```

Select your keyboard when asked.

Check if binding is working.


<br/>

## To modify key bindings

Edit the script `linux-deep-hotkeys.py` line number around 50 `keycodes_to_bind`

<br/>

## To set keyboard device name as argument

Run the script like so:

```
sudo python3 linux-deep-hotkeys.py --device /dev/input/event3
```

Again, to find your keyboard name, run the script without arguments.

<br/>

## Licence

MIT

<br/>


## Keywords to find this script

linux keyboard remapping shortcuts hotkeys binding evdev libevdev xmodmap xlib libinput xorg


