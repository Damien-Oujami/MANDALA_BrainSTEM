# intake/tongue.py
import time
from router import run_router

print("👅 Tongue up. Watching mealboxes…")
interval = 5
while True:
    t0 = time.time()
    run_router()
    dur = time.time() - t0
    print(f"🫧 tick {time.strftime('%H:%M:%S')} ({dur:.3f}s)")
    time.sleep(interval)
