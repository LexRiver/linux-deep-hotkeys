import evdev

x = []

x.append(123)

print(x)

x.append(234)

print(x)

x.remove(234)

print(x)

try:
    x.remove(222)

except:
    # print('not in list')
    pass
    

print(x)


print('Event types:') 
print(evdev.ecodes.EV_ABS, 'EV_ABS') # 3
print(evdev.ecodes.EV_CNT, 'EV_CNT') # 32
print(evdev.ecodes.EV_FF, 'EV_FF') # 21
print(evdev.ecodes.EV_FF_STATUS, 'EV_FF_STATUS') # 23
print(evdev.ecodes.EV_KEY, 'EV_KEY') # 1 -------------------------
print(evdev.ecodes.EV_LED, 'EV_LED') # 17
print(evdev.ecodes.EV_MAX, 'EV_MAX') # 31
print(evdev.ecodes.EV_MSC, 'EV_MSC') # 4 -------------------------
print(evdev.ecodes.EV_PWR, 'EV_PWR') # 22
print(evdev.ecodes.EV_REL, 'EV_REL') # 2
print(evdev.ecodes.EV_REP, 'EV_REP') # 20
print(evdev.ecodes.EV_SND, 'EV_SND') # 18
print(evdev.ecodes.EV_SW, 'EV_SW') # 5
print(evdev.ecodes.EV_SYN, 'EV_SYN') # 0 -------------------------
print(evdev.ecodes.EV_UINPUT, 'EV_UINPUT') # 257
print(evdev.ecodes.EV_VERSION, 'EV_VERSION') # 65537


keycodes_to_bind = {
    evdev.ecodes.KEY_J : evdev.ecodes.KEY_LEFT,
    evdev.ecodes.KEY_L : evdev.ecodes.KEY_RIGHT,
    evdev.ecodes.KEY_I : evdev.ecodes.KEY_UP,    
    evdev.ecodes.KEY_K : evdev.ecodes.KEY_DOWN,    
    evdev.ecodes.KEY_U : evdev.ecodes.KEY_BACKSPACE,    
    evdev.ecodes.KEY_O : evdev.ecodes.KEY_DELETE,    
    evdev.ecodes.KEY_H : evdev.ecodes.KEY_HOME,    
    evdev.ecodes.KEY_SEMICOLON : evdev.ecodes.KEY_END,    
    evdev.ecodes.KEY_M : evdev.ecodes.KEY_PAGEDOWN,    
}

print(keycodes_to_bind)

print(evdev.ecodes.KEY_X in keycodes_to_bind)

my_list = [1,2,3]

print(20 in my_list, 'in list')

my_list.remove(3)

print(my_list)

x = 1
y = 0

if x:
    print('x!')

if y:
    print('y!')    

print('done')

