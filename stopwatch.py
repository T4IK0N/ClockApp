import time
import keyboard

sec = 0
min = 0
running = True

while True:
    if keyboard.is_pressed('space'):
        running = not running
        time.sleep(0.5)
        if running:
            print("Zegar wznowiony.")
        else:
            print("Zegar zatrzymany.")

    if running:
        if sec < 59:
            sec += 1
            print(sec)
            time.sleep(1)
        else:
            sec = 0
            min += 1
            print(f"Min: {min}")
            time.sleep(1)
