#!/usr/bin/env python3

import time
from hardware_module import (
    read_ir,
    capture_image,
    move_bin,
    get_distance,
    open_lid,
    close_lid,
    cleanup
)
from faas_client import send_to_faas

THRESHOLD = 5  # cm

print("\n===== Smart Bin System Started =====\n")

try:
    while True:

        # 1️⃣ Wait for object detection
        print("👀 Waiting for object...")
        while not read_ir():
            time.sleep(0.2)

        print("📦 Object detected!")

        # 2️⃣ Capture image
        image = capture_image()

        # 3️⃣ Send to FAAS → get bin
        bin_number = send_to_faas(image)

        # 4️⃣ Move bin servo
        move_bin(bin_number)

        # 5️⃣ Check ultrasonic
        print("📏 Checking distance...")

        while True:
            distance = get_distance()
            print(f"Distance: {distance:.2f} cm")

            # 6️⃣ Condition check
            if distance <= THRESHOLD:
                open_lid()
                break
            else:
                print("⏳ Waiting... (10s)")
                time.sleep(10)

        # 7️⃣ Wait 5 sec
        time.sleep(5)

        # 8️⃣ Close lid
        close_lid()

        # 9️⃣ Wait 5 sec
        time.sleep(5)

        print("\n🔁 Cycle complete\n")

except KeyboardInterrupt:
    print("\n🛑 Stopping system...")

finally:
    cleanup()
