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
except ImportError:
    print("Required packages must be installed! Try:")
    print("pip install tkinter")
    print("pip install requests")
    print("pip install time")
    print("pip install re")
    print("pip install playsound3")
    print("Other modules: threading, webbrowser, os, sys, re, pystray, pillow")
    print("If \"pip\" does not work then please reinstall python.")
    raise("a")

# Build a tkinter window
app = tkinter.Tk()
app.overrideredirect(1)
app.title("Config")

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
    def countdown():
        for i in range(10, 0, -1):
            if cancel_flag[0]:
                return
            try:
                label.config(text=f"{thing} (+{more}) is in stock\nOpening GAG in {i} seconds...")
            except Exception as e:
                print(e)
                break
            time.sleep(1)
            if open_flag:
                # Open Roblox place
                webbrowser.open("roblox://experiences/start?placeId=126884695634066")
                root.destroy() 
                break
        if not cancel_flag[0]:
            webbrowser.open("roblox://experiences/start?placeId=126884695634066")
            root.destroy()

    p = playsound("alert.mp3", block=False)

    def cancel():
        cancel_flag[0] = True
        p.stop()
        root.destroy()
        

    def open():
        open_flag = True
        webbrowser.open("roblox://experiences/start?placeId=126884695634066")
        p.stop()
        root.destroy()

    root = tkinter.Tk()
    root.title("Rare Seed Alert")
    root.geometry("400x200")
    root.resizable(False, False)

    # Optional: add an image using Pillow
    # image = Image.open("seed.png")
    # photo = ImageTk.PhotoImage(image)
    # img_label = tk.Label(root, image=photo)
    # img_label.pack()

    label = tkinter.Label(root, text="A rare seed/gear you selected is in stock", font=("Arial", 14), pady=20)
    label.pack()

    cancel_btn = tkinter.Button(root, text="Cancel", command=cancel, font=("Arial", 12))
    cancel_btn.pack(pady=10)
    open_btn = tkinter.Button(root, text="Open GAG", command=open, font=("Arial", 12))
    open_btn.pack(pady=10)

    cancel_flag = [False]
    open_flag = False

    threading.Thread(target=countdown, daemon=True).start()

    root.mainloop()

def show_tray_icon():

    def on_exit(icon, item):
        icon.stop()
        exit()

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


    checking = []
    for name, var in seedcheckbuttons.items():
        if var.get():
            print(f"{name} is selected")
            checking.append(name)
    for name, var in gearcheckbuttons.items():
        if var.get():
            print(f"{name} is selected")
            checking.append(name)
    print(checking)
    minimize_to_tray()
    while True:
        timestamp = int(time.time())

        url = f"https://growagardenstock.com/api/stock?type=gear-seeds&ts={timestamp}"
        response = requests.get(url)
        data = response.json()

        # Extract and print gear and seed stock
        
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

        seed_match = [item for item in checking if item in seeds]
        gear_match = [item for item in checking if item in gears]

        if seed_match or gear_match:
            combined = seed_match + gear_match
            threading.Thread(target=rare_seed_alert, args=(combined[0], len(combined)-1), daemon=True).start()
        
        

        print("Sleeping for 300 more seconds")

        time.sleep(300)
    
    print("How did you get here?!")

btn_Start = tkinter.Button(app, text="Start!", command=actual_MainLoop)
btn_Start.pack()

print("Thank you for using the \033[41mGaG Alerts System\033[0m!")
print("Report bugs: DM \033[34m@vifgaming\033[0m!")
print("\033[32mRemember: Ctrl+C (in this window) to stop alerts, if the tray icon isn't there.\033[0m")

app.protocol("WM_DELETE_WINDOW", minimize_to_tray)
app.mainloop()
