import time
import threading

# One LS which keeps track if an effect should be exiting
# and if the last effect was a "set"
class LightState():
    def __init__(self):
        self.endEffect = False
        self.lastWasSet = False
    
    # Call each loop. Returns the executing effect thread if
    # there is one. There might not be if previous effect was 
    # a "set"
    def get_prev_thread(self):
        threads = threading.enumerate()
        if len(threads) > 1:
            return threads[-1]
        else:
            return None

    # Call before executing each effect. Sets the endEffect flag
    # to end the effect, then waits for the executing effect to finish
    # it is the effect's job to reset the flag
    # returns when the flag is reset
    def exit_wait(self, thread):
        if self.lastWasSet:
            # do not need to wait for a set
            return
        self.endEffect = True
        # wait until the thread terminates
        thread.join()
        if self.endEffect:
            print("ERROR: prev effect did not close correctly")
        return

# Create a new LT every time you have a valid effect
# Just pass input text in and thread will re-parse and execute
class LightThread(threading.Thread):
    def __init__(self, master, text):
        threading.Thread.__init__(self)
        self.text = text
        self.master = master
    def run(self):
        print("New thread running: {}".format(self.text))
        effect_map(self.master, self.text)

# Call each loop. Gets input from user. Calls effect_map
# with jc == True to test if input is a valid color or 
# effect. Returns string if valid. Returns False if invalid.
# Also handles exits because I say so
def get_input(master):
    in_string = input("Setting: ")
    if in_string == "exit":
        exit()
    if effect_map(master, in_string, True) == True:
        return in_string
    else:
        return False

# jc==False (default): Takes thread to set or effect function
# as destination. If no corresponding effect, prints error 
# not intended to return
# jc==True (justCheck): Helper function returns true if input
# is valid false otherwise
def effect_map(master, text, jc=False):
    # form "set <r> <g> <b>" such as:
    #      "set 123 255 0" or
    # form "set <color-name>"
    if text[0:3].lower() == "set":
        textList = text[3:].split()
        r,g,b = get_rgb(textList)
        if r == None:
            return False # same whether jc or not
        else:
            if jc:
                return True
            set_color(master, r, g, b)
    elif text.lower() == "rainbow":
        if jc:
            return True
        # print("set effect: {}".format(text))
        set_effect(master, text)
    elif text.lower() == "breathe":
        if jc:
            return True
        # print("set effect: {}".format(text))
        set_effect(master, text)
    elif text.lower() == "christmas":
        if jc:
            return True
        # print("set effect: {}".format(text))
        set_effect(master, text)
    else:
        return False

# Helper function takes a list of strings (such as from str.split())
# and returns r,g,b as values 0-255. If input is invalid returns
# None,None,None
def get_rgb(textList):
    if len(textList) == 1:
        if textList[0].lower() == "white":
            return 255,255,255
        if textList[0].lower() == "black":
            return 0,0,0
        if textList[0].lower() == "red":
            return 255,0,0
        if textList[0].lower() == "green":
            return 0,255,0
        if textList[0].lower() == "teal":
            return 0,128,128
        if textList[0].lower() == "b-teal":
            return 0,255,255
        if textList[0].lower() == "blue":
            return 0,0,255
        if textList[0].lower() == "mag":
            return 128,0,128
        if textList[0].lower() == "b-mag":
            return 255,0,255
    if len(textList) == 3:
        try:
            rgb = list(map(int, textList))
            if rgb[0]<0 or rgb[0]>255 or rgb[1]<0 or rgb[1]>255 or rgb[2]<0 or rgb[2]>255:
                print("Color values out of bounds (0-255)")
                return None,None,None
            else:
                return rgb[0],rgb[1],rgb[2]
        except:
            print("Color values not recognized")
            return None,None,None

# Set the lights to specified values. Does not check that 
# values are in range.
def set_color(master, r, g, b):
    master.lastWasSet = True
    print("Set to: rgb({},{},{})".format(r, g, b))

# TEMP pretend how an effect works
#   eventually there will be one for each effect
# loops forever
# when LightState.endEffect is True exit and  
def set_effect(master, effect):
    print("Effect: {}".format(effect))
    while 1:
        # print("Effect: {}".format(effect))
        time.sleep(4)
        if master.endEffect:
            print("Terminate Effect: {}".format(effect))
            master.endEffect = False
            exit()
