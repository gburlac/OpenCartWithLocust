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
delay_sec = 123            # pauză între mișcări (secunde)
duration_min = 123         # cât timp rulează (minute) – poate fi modificat
# ============================

print(f"Program pornit. Se va opri automat după {duration_min} minute sau cu Ctrl+C.")

start_time = time.time()
end_time = start_time + duration_min * 60  # convertim în secunde

try:
    while running and time.time() < end_time:
        # Dormim în pași de 1 sec. pentru a prinde Ctrl+C
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
        print(f"Mutat cursorul la: ({x}, {y})")

except Exception as e:
    print(f"Eroare: {e}")

print("Program încheiat.")
