import pyautogui, keyboard, time, os, sys, threading

CONFIDENCE = 0.8
bot_running = False
program_running = True
looping = True  # Set to False for one-time execution
quitSwitch = True # Set to True to quit on 1st run

# --- Logging ---
def log(msg):
    print(f"[LOG] {msg}")

# --- Image path resolver ---
def resource_path(relative_path):
    try: base_path = sys._MEIPASS
    except: base_path = os.path.abspath(".")
    return os.path.join(base_path, "img", relative_path)

# --- PyAutoGUI Helpers ---
def is_bot_active():
    return bot_running and program_running and not keyboard.is_pressed('f7')

def click_image(image_path, timeout=5, delay=1, confidence=CONFIDENCE):
    start = time.time()
    while time.time() - start < timeout and is_bot_active():
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
            pyautogui.moveTo(location)
            pyautogui.click()
            time.sleep(delay)
            return True
        except: time.sleep(0.1)
    log(f"Couldn't find {image_path}")
    return False

def hover_image(image_path, timeout=5, confidence=CONFIDENCE):
    start = time.time()
    while time.time() - start < timeout and is_bot_active():
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
            pyautogui.moveTo(location)
            return True
        except: time.sleep(0.1)
    log(f"[WARN] Couldn't find {image_path}")
    return False

def safe_locate_center(image_path, confidence=CONFIDENCE, grayscale=False):
    try:
        location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence, grayscale=grayscale)
        return location  # returns (x, y) or None if not found
    except Exception as e:
        #print(f"[ERROR] Can't locate {image_path}: {e}")
        return None

def wait_for_image(image_path, timeout=300, confidence=CONFIDENCE):
    start = time.time()
    while time.time() - start < timeout and is_bot_active():
        if safe_locate_center(image_path, confidence):
            return True
        time.sleep(0.1)
    log(f"[WARN] Timeout waiting for {image_path}")
    return False

def checkGamertag():
    if hover_image(resource_path("gamertag.png"), confidence=0.97):
        log("Gamertag found, proceeding with the match.")
        return True
    else:
        log("Gamertag not found, relogging.")
        return False

# --- Automation Tasks (add more as needed) ---
count = 1  # Counter for automation runs
def automation():
    global quitSwitch, count
    
    # --- Automation Steps ---
    # def loadMatchmaking():
    #     click_image(resource_path("findMatch.png"))

    #     if not click_image(resource_path("partyGames.png")):
    #         click_image(resource_path("findMatch.png"))
    #         pyautogui.click()
    #         click_image(resource_path("partyGames.png"))

    #     click_image(resource_path("gunFight.png"))
    #     log("Started matchmaking.")
    
    def loadMatchmaking():
        click_image(resource_path("findMatch.png"))
        click_image(resource_path("partyGames.png"))
        click_image(resource_path("gunFight.png"))
        log("Started matchmaking.")

    def relogToMatchmaking():
        click_image(resource_path("back.png"))
        click_image(resource_path("leaveWithParty.png"))
        loadMatchmaking()

    def goIntoMatch():

        if wait_for_image(resource_path("GUNFIGHTmatch.png")):
            log("Match loaded...")
            if quitSwitch:
                log("Quitting match...")
                keyboard.press_and_release('esc')
                time.sleep(1)
                click_image(resource_path("leaveMatch.png"))
                click_image(resource_path("yes.png"))
                pyautogui.click()
            else:
                log("Waiting for the other team to quit match...")
                while not wait_for_image(resource_path("lobby.png")) and is_bot_active():
                    click_image(resource_path("skip.png"))
                    click_image(resource_path("back.png"))
                    time.sleep(2)
                if safe_locate_center(resource_path("lobby.png")):
                    log("Match won, back to matchmaking...")
                else:
                    log("Something went wrong, still can't find lobby.png")
 #Try again...

    # --- Actual Automation ---
    log(f"Running Automation {count}...")

    loadMatchmaking()

    while is_bot_active():
        
        if wait_for_image(resource_path("fullLobby.png"), confidence=0.5): # Must have for the bot to not fail silently.
            log("Full lobby found, checking gamertag...")
            
            if checkGamertag():
                goIntoMatch()
                break
            else:
                relogToMatchmaking()
    
    if quitSwitch:
        log(f"Waiting for the other team to load (60seconds)...")
        time.sleep(55)  # Wait for the other team to load
        pyautogui.click() # For "FIND A MATCH" button to be clickable
    quitSwitch = not quitSwitch  # Toggle quitSwitch for next run
    log(f"Automation {count} Done.")
    count += 1
    time.sleep(1)  # Delay before next run if looping is enabled

# --- Keyboard Listener ---
def key_listener():
    global bot_running, program_running
    while program_running:
        if keyboard.is_pressed('f8') and not bot_running:
            bot_running = True
            log("F8 pressed: Starting Automation")
            time.sleep(0.5)
        elif keyboard.is_pressed('f7') and bot_running:
            bot_running = False
            log("f7 pressed: Bot stopped")
            time.sleep(0.5)
        elif keyboard.is_pressed('esc'):
            log("ESC pressed: Exiting")
            bot_running = False
            program_running = False
            break
        time.sleep(0.05)

# --- Main Execution Loop ---
def main_loop():
    global bot_running
    while program_running:
        if bot_running:
            automation()
            if not looping:
                bot_running = False
        time.sleep(0.1)

if __name__ == "__main__":
    log("COD Automation Bot Started")
    log("Press F8 to start, f7 to stop, ESC to quit.")

    threading.Thread(target=key_listener, daemon=True).start()
    main_loop()

    log("Bot exited.")
