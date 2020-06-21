#Required for keyboard and mouse listeners
from pynput import keyboard, mouse
#Gui
from guizero import App, Picture, Text, Box, Window, PushButton
#Required to check if the client is in-game, urllib is to remove the warning for unchecked certificates
import requests
import urllib3
#Pausing
from time import sleep, perf_counter
#Required to run multiple threads so that they don't overlap in execution time
import threading
#The get request from the client returns a json object so this is needed to parse it
import json
#Required to check the current foreground window
from ctypes import wintypes, windll, create_unicode_buffer
from typing import Optional
#Process indexer
import psutil
#Disable urllib warning for unchecked certificates
urllib3.disable_warnings()
#Real time variables
i = 0
tot_q = 0
tot_w = 0
tot_e = 0
tot_r = 0
tot_lc = 0
tot_rc = 0
apm = 0
tot_a = 0
perf1 = 0
perf2 = 0
champ = ""
#For saving the previous results
last_q = 0
last_w = 0
last_e = 0
last_r = 0
last_lc = 0
last_rc = 0
last_apm = 0
last_time = 0
last_champ = ""
last_key = ""
#Flags that pause the execution of the listeners, the in-game check and the victory check if you're not in game
run = False
check = False
count_time = False
get_last = True
check_game = True
#Declaring UI app
app = App(layout="grid",width=300,height=260,title="LoL apm tracker",bg="green")
app.tk.resizable(True,True)
#Giant fucking UI block
#Main window
b1 = Box(app,width=200,height=180,border=False,layout="auto",grid=[0,0])
b2 = Box(app,width=115,height=130,border=False,layout="auto",grid=[1,0])
curr_champ = Text(b1, text="Playing: Not in game",align="top",size=16,color="white")
b3 = Box(b1,width=180,height=80,border=False,layout="grid",align="top")
b4 = Box(b1,width=180,height=60,border=False,layout="grid",align="bottom")
b5 = Box(b2,border=False,layout="grid",align="top",width=115,height=95)
count_lc = Text(b5,text=tot_lc, grid=[0,1], size=16, color="white")
count_rc = Text(b5, text=tot_rc, grid=[1,1],size=16,color="white")
p1 = Picture(b3, image="assets/key_Q.png", grid=[0,0])
p2 = Picture(b3, image="assets/key_W.png", grid=[1,0])
p3 = Picture(b3, image="assets/key_E.png", grid=[2,0])
p4 = Picture(b3, image="assets/key_R.png", grid=[3,0])
p5 = Picture(b5,image="assets/mouse_left.png",grid=[0,0])
p6 = Picture(b5,image="assets/mouse_right.png",grid=[1,0])
p7 = Picture(b3, image="assets/key_Q_pressed.png", grid=[0,0],visible=True)
p8 = Picture(b3, image="assets/key_W_pressed.png", grid=[1,0],visible=True)
p9 = Picture(b3, image="assets/key_E_pressed.png", grid=[2,0],visible=True)
p10 = Picture(b3, image="assets/key_R_pressed.png", grid=[3,0],visible=True)
p11 = Picture(b5, image="assets/mouse_right_pressed.png", grid=[1,0],visible=True)
p12 = Picture(b5, image="assets/mouse_left_pressed.png", grid=[0,0],visible=True)
#Switched to using TKinter layers instead of hiding and showing the items because that was causing weird issue with the grid alignment
p7.tk.lower()
p8.tk.lower()
p9.tk.lower()
p10.tk.lower()
p11.tk.lower()
p12.tk.lower()
count_q = Text(b3,text=tot_q, grid=[0,1],size=18,color="white")
count_r = Text(b3,text=tot_r, grid=[3,1],size=18,color="white")
count_e = Text(b3,text=tot_e, grid=[2,1],size=18,color="white")
count_w = Text(b3,text=tot_w, grid=[1,1],size=18,color="white")
time = Text(b4,text="T: 0s",grid=[1,2],size=16,color="white")
curr_apm = Text(b4,text="Apm: 0",grid=[2,2],size=16,color="white")
#Last report window
last_report = Window(app,layout="grid",width=300,height=260,title="Last game report",bg="green",visible=False)
b6 = Box(last_report,width=200,height=180,border=False,layout="auto",grid=[0,0])
b7 = Box(last_report,width=115,height=130,border=False,layout="auto",grid=[1,0])
prev_champ = Text(b6, text="Playing: Not in game",align="top",size=16,color="white")
b8 = Box(b6,width=180,height=80,border=False,layout="grid",align="top")
b9 = Box(b6,width=180,height=60,border=False,layout="grid",align="bottom")
b10 = Box(b7,border=False,layout="grid",align="top",width=115,height=95)
prev_lc = Text(b10,text=tot_lc, grid=[0,1], size=16, color="white")
prev_rc = Text(b10, text=tot_rc, grid=[1,1],size=16,color="white")
p13 = Picture(b8, image="assets/key_Q.png", grid=[0,0])
p14 = Picture(b8, image="assets/key_W.png", grid=[1,0])
p15 = Picture(b8, image="assets/key_E.png", grid=[2,0])
p16 = Picture(b8, image="assets/key_R.png", grid=[3,0])
p17 = Picture(b10,image="assets/mouse_left.png",grid=[0,0])
p18 = Picture(b10,image="assets/mouse_right.png",grid=[1,0])
prev_q = Text(b8,text=tot_q, grid=[0,1],size=18,color="white")
prev_r = Text(b8,text=tot_r, grid=[3,1],size=18,color="white")
prev_e = Text(b8,text=tot_e, grid=[2,1],size=18,color="white")
prev_w = Text(b8,text=tot_w, grid=[1,1],size=18,color="white")
prev_time = Text(b9,text="T: 0s",grid=[1,2],size=16,color="white")
prev_apm = Text(b9,text="Apm: 0",grid=[2,2],size=16,color="white")
#Functions for the buttons
def open_last_report():
    last_report.show()
def close_last_report():
    last_report.hide()
#Button creation
button1 = PushButton(app, text="Last game", command=open_last_report, grid=[0,3],padx=5,pady=5)
button1.tk.config(borderwidth=2,relief="groove")
button2 = PushButton(last_report, text="Close", command=close_last_report,grid=[0,3])
button2.tk.config(borderwidth=2,relief="groove")
#End of the UI block
#Functions that increment the values for the key press, needed because python doesn't have switch statements
#The keys are shown and hidden by raising and lowering their layer 
def inc_q(flag):
    global tot_q
    if flag:
        tot_q += 1
        p7.tk.lift()
    else:
        p7.tk.lower()
def inc_w(flag):
    global tot_w
    if flag:
        tot_w += 1
        p8.tk.lift()
    else:
        p8.tk.lower()
def inc_e(flag):
    global tot_e
    if flag:
        tot_e += 1
        p9.tk.lift()
    else:
        p9.tk.lower()
def inc_r(flag):
    global tot_r
    if flag:
        tot_r += 1
        p10.tk.lift()
    else:
        p10.tk.lower()
def inc_rc(flag):
    global tot_rc
    if flag:
        tot_rc += 1
        p11.tk.lift()
    else:
        p11.tk.lower()
def inc_lc(flag):
    global tot_lc
    if flag:
        tot_lc += 1
        p12.tk.lift()
    else:
        p12.tk.lower()
def nothing(flag):
    pass
#Timer function that runs at the start of the match
t=0
def timer():
    global t
    while True:
        if count_time:
            t += 1
        sleep(1)
#Reset values after the game ends
def reset():
    global tot_e, tot_q, tot_r ,tot_rc, tot_w, apm, t, get_last, perf1, perf2, run, count_time, check, champ, tot_lc
    tot_e = 0
    tot_q = 0
    tot_r = 0
    tot_rc = 0
    tot_lc = 0
    tot_w = 0
    apm = 0
    t = 0
    get_last = True
    perf1 = 0
    perf2 = 0
    run = False
    count_time = False
    check = False
    champ = ""
#Copy values to another variable so you can compare between games
def copy():
    global last_e, last_q, last_r, last_rc, last_w, last_apm, last_time, last_champ, last_lc
    last_e = tot_e
    last_q = tot_q
    last_r = tot_r
    last_lc = tot_lc
    last_rc = tot_rc
    last_w = tot_w
    last_apm = apm
    last_time = t
    last_champ = champ
#Update function to change the numbers in the gui
def update():
    global tot_e,tot_q,tot_r,tot_rc,tot_w, apm, tot_a,tot_lc
    count_e.value = tot_e
    count_q.value = tot_q
    count_r.value = tot_r
    count_rc.value = tot_rc
    count_lc.value = tot_lc
    count_w.value = tot_w
    time.value = "T: "+str(t)+"s"
    tot_a = tot_e+tot_q+tot_r+tot_rc+tot_w+tot_lc
    if t!=0:
        apm = int((tot_a/(t/60)*(10**2))/(10**2))
    curr_apm.value = "Apm: "+str(apm)
    if champ == "":
        curr_champ.value = "Playing: Not in game"
    else:
        curr_champ.value = "Playing: "+champ
#Updates the last game window with new stats every second
def update_last():
    global last_e, last_q, last_r, last_rc, last_w, last_time, last_apm, last_champ, last_lc
    prev_e.value = last_e
    prev_q.value = last_q
    prev_r.value = last_r
    prev_rc.value = last_rc
    prev_lc.value = last_lc
    prev_w.value = last_w
    prev_time.value = "T: "+str(last_time)
    prev_apm.value = "Apm: "+str(last_apm)
    prev_champ.value = "Played: "+last_champ
#Dictionary that is used to save the last game stats as a json file for easy reading and writing
def make_dict():
    global last_game_dict
    last_game_dict = {
        "q_pressed":last_q,
        "w_pressed":last_w,
        "e_pressed":last_e,
        "r_pressed":last_r,
        "lc_pressed":last_lc,
        "rc_pressed":last_rc,
        "time":last_time,
        "apm":last_apm,
        "champ":last_champ
    }
#Copies the last game's stats to the json file
def copy_to_file():
    with open("last_game.json","w") as file:
        json.dump(last_game_dict, file, indent=4)
#Attempts to load the last game's stats from the json file
def load_from_file():
    global last_q, last_e, last_r, last_rc, last_w, last_time, last_apm, last_champ, last_lc
    try:
        with open("last_game.json","r") as file:
            last_game_dict = json.load(file)
        last_q=last_game_dict["q_pressed"]
        last_e=last_game_dict["e_pressed"]
        last_r=last_game_dict["r_pressed"]
        last_lc=last_game_dict["lc_pressed"]
        last_rc=last_game_dict["rc_pressed"]
        last_w=last_game_dict["w_pressed"]
        last_time=last_game_dict["time"]
        last_apm=last_game_dict["apm"]
        last_champ=last_game_dict["champ"]
    #In case of failure i just skip the rest of the values, honestly just too lazy to try except every value
    except (FileNotFoundError,json.decoder.JSONDecodeError,KeyError):
        pass
#Dictionary that is used in place of a switch statement
switcher = {
    "q": inc_q,
    "w": inc_w,
    "e": inc_e,
    "r": inc_r,
    "def": nothing
}
#Gets foreground window title so that the program only counts key strokes and clicks in the game
def getForegroundWindowTitle() -> Optional[str]:
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buf, length + 1)
    if buf.value:
        return buf.value
    else:
        return None
#What should run on key presses
def on_press_kb(key):
    if True:
        global perf1, perf2, get_last,last_key
        #Everything before the second try statement is a half-assed attempt at ignoring held keys as multiple presses, seems to work pretty well
        #TODO attempt to fix held keys counting as 2 presses although I don't think that's possible(?)
        if get_last == True:
            perf1 = perf_counter()
            get_last = not get_last
        else:
            perf2 = perf1
            perf1 = perf_counter()
        try:
            if last_key != "":
                if not((perf1-perf2) < 0.08 and key.char == last_key):
                    if getForegroundWindowTitle() == "League of Legends (TM) Client":
                        #"Switch-case" statement, it takes the key as input and converts it to the appropriate function, otherwise it defaults to a pass function
                        func = switcher.get(key.char,lambda x: "def")
                        func(True)
        except(AttributeError):
            pass
        try:
            last_key = key.char
        except(AttributeError):
            last_key = "other" 
#What should run when releasing keys
def on_release_kb(key):
    if run and (getForegroundWindowTitle() == "League of Legends (TM) Client"):
        try:
            #"Switch-case" statement, it takes the key as input and converts it to the appropriate function, otherwise it defaults to a pass function
            func = switcher.get(key.char,lambda x: "def")
            func(False)
        except(AttributeError):
            pass
#What should run when clicking
def on_click(x, y, button, pressed):
    if run and (getForegroundWindowTitle() == "League of Legends (TM) Client"):
        #print("Clicked")
        if button == mouse.Button.right and pressed == True:
            inc_rc(True)
        elif button == mouse.Button.right and pressed == False:
            inc_rc(False)
        if button == mouse.Button.left and pressed == True:
            inc_lc(True)
        elif button == mouse.Button.left and pressed == False:
            inc_lc(False)
#Check if the given process is running
#This is currently unused because of high run time but i might implement it later as another thread that sets a flag value instead of checking it every time in the check_if_won function
def checkIfProcessRunning(processName):
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False
#Checks if the current game has finished, only runs while you're in a game
def check_if_won():
    global run, count_time, check, check_game
    #This url asks your client for you current game's event data
    url = "https://127.0.0.1:2999/liveclientdata/eventdata"
    while True:
        if check:
            try:
                #This attempts to retrieve the current game's event list
                events = requests.get(url,verify=False)
                events_list = json.loads(events.text)["Events"]
                #This gets the last event in the list
                if len(events_list)>0:
                    last_event = events_list[len(events_list)-1]
                try:
                    #The GameEnd event signals that you have just finished a game
                    if last_event["EventName"] == "GameEnd":
                        print("Game over")
                        copy()
                        reset()
                        make_dict()
                        copy_to_file()
                        last_report.show()
                        #This is to make sure it stops incresing any stats after the game has ended because technically you're still in-game on the victory/defeat screen
                        check_game = False
                        #This sleep prevents the script from running twice which would override the last stats with zeros
                        sleep(20)
                        #Resume normal operation
                        check_game = True
                except(TypeError,UnboundLocalError):
                    pass
            except(requests.exceptions.ConnectionError):
                run = False
                count_time = False
        #This sleep instruction may or may not improve performance but lowers the consistency, although with .5 I haven't encountered any issues
        sleep(0.5)

def check_in_game():
    global run, check, count_time, t
    while True:
        while check_game:
            #This url requests the current game stats, and if it returns anything it means you're in a game
            url = "https://127.0.0.1:2999/liveclientdata/gamestats"
            try:
                live_match = requests.get(url, verify=False)
                #Code 200 is a successful request to the client
                if live_match.status_code == 200:
                    count_time = True
                    check = True
                    run = True
                else:
                    count_time = False
                    check = False
                    run = False
            except(requests.exceptions.ConnectionError):
                count_time = False
                check = False
                run = False
        sleep(1)
#Checks the current champion the user is playing to display at the top of the window
def check_champ():
    global champ
    while True:
        if run:
            #These 2 urls are to get the current list of players and the name of the player
            url = "https://127.0.0.1:2999/liveclientdata/playerlist"
            url2 = "https://127.0.0.1:2999/liveclientdata/activeplayername"
            try:
                #The only way I could get the player's current champion is by checking the player's name in the player list and copying the value of the champion they're playing
                player_name_get = requests.get(url2, verify=False)
                player_list_get = requests.get(url, verify=False)
                player_name = player_name_get.text
                player_list = json.loads(player_list_get.text)
                player_name = player_name.translate(str.maketrans('', '', '"'))
                #What was described in the previous comment happens here
                for item in player_list:
                    if player_name in item["summonerName"]:
                        champ = item["championName"]
                        break
            except(requests.exceptions.ConnectionError):
                pass
        sleep(1)
#These are required because after packaging the code with pyinstaller they prevent some stutters in the mouse listener
def on_move(x,y):
    pass
def on_scroll(x,y,z,w):
    pass
#Listeners used to check for mouse and keyboard input
def mouse_listen():
    with keyboard.Listener(on_press=on_press_kb,on_release=on_release_kb) as listener_kb:
        listener_kb.join()
def kb_listen():
    with mouse.Listener(on_click=on_click,on_move=on_move,on_scroll=on_scroll) as listener_m2:
        listener_m2.join()
#This if statement may or may not be required but I'm keeping it for safety
if __name__ == "__main__":
    #Starts the required threads
    process1 = threading.Thread(target=check_in_game,daemon=True)
    process1.start()
    process2 = threading.Thread(target=mouse_listen,daemon=True)
    process2.start()
    process3 = threading.Thread(target=kb_listen,daemon=True)
    process3.start()
    process4 = threading.Thread(target=check_if_won,daemon=True)
    process4.start()
    process5 = threading.Thread(target=timer,daemon=True)
    process5.start()
    process6 = threading.Thread(target=check_champ,daemon=True)
    process6.start()
    #These 2 functions tell the 2 UI windows to update respectively every 50ms and every second
    time.repeat(50,update)
    prev_time.repeat(1000,update_last)
    #Load last game data from the json file
    load_from_file()
    #Display the main UI window
    app.display()