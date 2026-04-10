#!/usr/bin/env python3
from gpiozero import Servo
from time import sleep

# 🔧 Use GPIO 12
SERVO_PIN = 12

# ✅ Calibrated servo setup
servo = Servo(SERVO_PIN, min_pulse_width=0.0005, max_pulse_width=0.0025)

# 🎯 Define 5 positions (0 → 180 divided into 5)
ANGLES = [0, 45, 90, 135, 180]

def set_angle(angle):
    """Convert 0–180° to -1 to +1"""
    value = (angle - 90) / 90
    servo.value = value
    print(f"✅ Moved to {angle}°")

print("\n===== Servo Position Test (5 Angles) =====")

try:
    # 🔵 Initial position → CENTER
    print("🔵 Setting initial position to CENTER (90°)")
    set_angle(90)
    sleep(2)

    while True:
        print("\nAvailable positions:")
        for i, ang in enumerate(ANGLES):
            print(f"{i+1} → {ang}°")

        print("q → Quit")

        choice = input("Select position (1-5): ").strip().lower()

        if choice == "q":
            print("👋 Exiting...")
            break

        if choice in ["1", "2", "3", "4", "5"]:
            angle = ANGLES[int(choice) - 1]
            set_angle(angle)
            sleep(1)
        else:
            print("❌ Invalid input")

except KeyboardInterrupt:
    print("\n👋 Stopped by user")

finally:
    servo.detach()
