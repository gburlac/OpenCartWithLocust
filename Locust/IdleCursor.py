import pyautogui
import time
import random
import signal
import sys

running = True

def signal_handler(sig, frame):
    global running
    print("\nCtrl+C detectat. Închidere...")
    running = False

signal.signal(signal.SIGINT, signal_handler)

# ======= CONFIGURARE =======
delay_sec = 60           # Pauza între mișcări (secunde)
duration_min = 180        # Durata totală a rulării (minute)
# ============================

print(f"Program pornit: va muta cursorul la fiecare {delay_sec} secunde.")
print(f"Se va opri automat după {duration_min} minute sau cu Ctrl+C.\n")

start_time = time.time()
end_time = start_time + duration_min * 60  # convertim în secunde

try:
    while running and time.time() < end_time:
        # Calculează timpul rămas
        remaining = int(end_time - time.time())
        minutes_left = remaining // 60
        seconds_left = remaining % 60

        print(f"Timp rămas: {minutes_left:02d}:{seconds_left:02d} minute")

        # Așteaptă cu verificare pe parcurs
        for _ in range(delay_sec):
            if not running or time.time() >= end_time:
                break
            time.sleep(1)

        if not running or time.time() >= end_time:
            break

        width, height = pyautogui.size()
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        pyautogui.moveTo(x, y)
        print(f"Mutat cursorul la: ({x}, {y})\n")

except Exception as e:
    print(f"Eroare: {e}")

print("Program încheiat.")
