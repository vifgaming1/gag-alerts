try:
    import tkinter
    import requests
    import time
    import re
    from playsound3 import playsound
    from PIL import Image
    import threading
    import webbrowser
    import pystray 
    import os
except ImportError:
    print("Required packages must be installed! Try:")
    print("pip install tkinter")
    print("pip install requests")
    print("pip install time")
    print("pip install re")
    print("pip install playsound3")
    print("Other modules: threading, webbrowser, os, sys, re, pystray, pillow, os")
    print("If \"pip\" does not work then please reinstall python.")
    raise("a")

# Build a tkinter window
app = tkinter.Tk()
app.title("Made with <3 by vifgaming")

app.update_idletasks()  # Ensure geometry info is updated
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
window_width = 400
window_height = 800
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
app.geometry(f"{window_width}x{window_height}+{x}+{y}")

txt_Title_Tray = tkinter.Label(app, text="Look in the System Tray to stop alerts btw")
txt_Title_Tray.pack()

txt_Title_Seeds = tkinter.Label(app, text="Notify me for seeds:")
txt_Title_Seeds.pack()

# Seeds
seed_names = [
    "Bamboo", "Coconut", "Cactus", "Dragon Fruit", "Mango", "Grape",
    "Mushroom", "Pepper", "Cacao", "Beanstalk", "Ember Lily", "Sugar Apple"
]
seedcheckbuttons = {}
for name in seed_names:
    var = tkinter.BooleanVar()
    cb = tkinter.Checkbutton(app, text=name, variable=var)
    cb.pack()
    seedcheckbuttons[name] = var

txt_Title_Gears = tkinter.Label(app, text="Notify me for gears:")
txt_Title_Gears.pack()

# Gears
gear_names = [
    "Basic Sprinkler", "Advanced Sprinkler", "Night Staff", "Star Caller",
    "Chocolate Sprinkler", "Godly Sprinkler", "Lightning Rod", "Nectar Staff",
    "Pollen Radar", "Favorite Tool", "Friendship Pot", "Harvest Tool",
    "Honey Sprinkler", "Master Sprinkler"
]
gearcheckbuttons = {}
for name in gear_names:
    var = tkinter.BooleanVar()
    cb = tkinter.Checkbutton(app, text=name, variable=var)
    cb.pack()
    gearcheckbuttons[name] = var

txt_Title_Warning = tkinter.Label(app, text="It's recommended to start on about 1 minute after stock.")
txt_Title_Warning.pack()

def rare_seed_alert(thing, more):
    root = tkinter.Toplevel()
    root.title("Rare Seed Alert")
    root.geometry("400x200")
    root.resizable(False, False)

    label = tkinter.Label(
        root, 
        text=f"A rare seed/gear you selected is in stock\n{thing} (+{more})", 
        font=("Arial", 14), 
        pady=20
    )
    label.pack()

    def open_action():
        if sound.is_alive():
            sound.stop()
        webbrowser.open("roblox://experiences/start?placeId=126884695634066")
        root.destroy()

    def cancel_action():
        if sound.is_alive():
            sound.stop()
        root.destroy()

    cancel_btn = tkinter.Button(root, text="Cancel", command=cancel_action, font=("Arial", 12))
    cancel_btn.pack(pady=10)

    open_btn = tkinter.Button(root, text="Open GAG", command=open_action, font=("Arial", 12))
    open_btn.pack(pady=10)

    # Countdown label update in the main thread 
    def countdown(i=10):
        if i == 0:
            open_action()
        else:
            label.config(text=f"{thing} (+{more}) is in stock\nOpening GAG in {i} seconds...")
            root.after(1000, countdown, i - 1)

    countdown()

    sound = playsound("alert.mp3", block=False)
    sound.play(block=False)

def rsa_threader(a, b):
    print(f"Triggering alert for {a} (+{b})")
    app.after(0, lambda: rare_seed_alert(a, b))

def show_tray_icon():

    def on_exit(icon, item):
        icon.stop()
        os.system(f"taskkill /pid {str(os.getppid())}")
        

    image = Image.open("icon.png")  # Use a small 16x16 PNG or ICO icon
    menu = pystray.Menu(
        pystray.MenuItem("Exit", on_exit)
    )
    tray_icon = pystray.Icon("Grow a Garden Alert", image, "GAG Notifier", menu)
    tray_icon.run()

def minimize_to_tray():
    app.withdraw()
    threading.Thread(target=show_tray_icon, daemon=True).start()

def actual_MainLoop():
    def worker():
        checking = []
        for name, var in seedcheckbuttons.items():
            if var.get():
                checking.append(name)
        for name, var in gearcheckbuttons.items():
            if var.get():
                checking.append(name)

        minimize_to_tray()
        
        while True:
            timestamp = int(time.time())
            url = f"https://growagardenstock.com/api/stock?type=gear-seeds&ts={timestamp}"
            response = ""
            try:
                response = requests.get(url)
            except ConnectionError:
                response = '''{"updatedAt":1750425104889,"gear":["Cleaning Spray **x3**","Recall Wrench **x1**","Trowel **x2**","Basic Sprinkler **x1**","Favorite Tool **x3**","Watering Can **x2**","Harvest Tool **x2**"],"seeds":["Carrot **x5**","Blueberry **x3**","Tomato **x3**","Strawberry **x5**"]}'''
            data = response.json()

            def parse_items(item_list):
                result = {}
                for item in item_list:
                    match = re.match(r"(.+?)\s\*\*x(\d+)\*\*", item)
                    if match:
                        name = match.group(1).strip()
                        count = int(match.group(2))
                        result[name] = count
                return result

            seeds = parse_items(data.get("seeds", []))
            gears = parse_items(data.get("gear", []))

            print("Checking for:", checking)
            print("Parsed seeds:", list(seeds.keys()))
            print("Parsed gears:", list(gears.keys()))

            seed_match = [item for item in checking if item in seeds]
            gear_match = [item for item in checking if item in gears]
            combined = seed_match + gear_match

            print(combined)

            if combined:
                rsa_threader(combined[0], len(combined)-1)

            time.sleep(300)

    threading.Thread(target=worker, daemon=True).start()

btn_Start = tkinter.Button(app, text="Start!", command=actual_MainLoop)
btn_Start.pack()

print("Thank you for using the \033[41mGaG Alerts System\033[0m!")
print("Report bugs: DM \033[34m@vifgaming\033[0m!")
print("\033[32mRemember: Ctrl+C (in this window) to stop alerts, if the tray icon isn't there.\033[0m")

app.protocol("WM_DELETE_WINDOW", minimize_to_tray)
app.mainloop()
