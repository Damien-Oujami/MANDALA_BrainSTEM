# intake/tongue.py
import time
from router import run_router

print("👅 Tongue initialized. Watching mealboxes...")

while True:
    run_router()
    time.sleep(15)  # adjust interval
