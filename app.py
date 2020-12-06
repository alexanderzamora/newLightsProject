import lightState as LS
import threading
import time

#todo:
#main thread
#control lights
#control over ssh

master = LS.LightState()

init = LS.LightThread(master, "set black")
init.run()

while 1:
    prevThread = master.get_prev_thread()
    in_string = LS.get_input(master)
    if in_string == False:
        print("Error: no command")
        continue
    if in_string == "exit":
        master.exit_wait(master, prevThread)
        exit()
    master.exit_wait(prevThread)
    child = LS.LightThread(master, in_string)
    child.start()
