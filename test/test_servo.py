#!/usr/bin/env python3
from gpiozero import Servo
from time import sleep

# 🔧 Change pin if needed
SERVO_PIN = 13

# ✅ Better calibration (important for real servo)
servo = Servo(SERVO_PIN, min_pulse_width=0.0005, max_pulse_width=0.0025)

def set_angle(angle):
    """
    Convert 0–180° → -1 to +1 (gpiozero range)
    """
    if angle < 0 or angle > 180:
        print("❌ Angle must be between 0 and 180")
        return
    
    value = (angle - 90) / 90
    servo.value = value
    print(f"✅ Moved to {angle}°")

print("\n===== Servo Test =====")
print("1 → Manual angle input")
print("2 → Auto sweep test")
print("q → Quit\n")

try:
    while True:
        choice = input("Select mode (1/2/q): ").strip()

        if choice == "q":
            print("👋 Exiting...")
            break

        elif choice == "1":
            while True:
                angle_input = input("Enter angle (0–180) or 'b' to go back: ").strip()
                
                if angle_input.lower() == 'b':
                    break
                
                try:
                    angle = int(angle_input)
                    set_angle(angle)
                    sleep(1)
                except:
                    print("❌ Invalid input")

        elif choice == "2":
            print("🔄 Running auto sweep test...")
            
            for angle in [0, 45, 90, 135, 180]:
                set_angle(angle)
                sleep(1)

            print("🔄 Reverse sweep...")
            for angle in [180, 135, 90, 45, 0]:
                set_angle(angle)
                sleep(1)

            print("✅ Sweep complete\n")

        else:
            print("❌ Invalid option")

except KeyboardInterrupt:
    print("\n👋 Stopped by user")

finally:
    servo.detach()
