import math

import pyautogui


def run_precision_test():
    print("\n" + "=" * 40)
    print(" PyAutoGUI Mouse Precision Tester")
    print("=" * 40)

    # Step 1: Record Start
    print("\n1. Place your mouse exactly where you want to start.")
    input("   Press [ENTER] to record the START position...")
    start_x, start_y = pyautogui.position()
    print(f"   -> Start Position Recorded: (X: {start_x}, Y: {start_y})")

    # Step 2: Record End
    print("\n2. Move your mouse in a straight line (horizontally or vertically).")
    input("   Press [ENTER] to record the END position...")
    end_x, end_y = pyautogui.position()
    print(f"   -> End Position Recorded: (X: {end_x}, Y: {end_y})\n")

    # Step 3: Calculations
    dx = end_x - start_x
    dy = end_y - start_y
    distance = math.sqrt(dx**2 + dy**2)

    # Determine which way the user was trying to go to calculate error
    if abs(dx) > abs(dy):
        direction = "Horizontal (Left/Right)"
        intended_movement = abs(dx)
        deviation = abs(dy)
    else:
        direction = "Vertical (Up/Down)"
        intended_movement = abs(dy)
        deviation = abs(dx)

    # Calculate accuracy percentage
    if intended_movement != 0:
        accuracy = max(0, 100 - (deviation / intended_movement * 100))
    else:
        accuracy = 0.0

    # Step 4: Display Results
    print("=" * 15 + " RESULTS " + "=" * 16)
    print(f"Total Distance:       {distance:.2f} pixels")
    print(f"X-Axis Movement (ΔX): {abs(dx)} pixels")
    print(f"Y-Axis Movement (ΔY): {abs(dy)} pixels")
    print("-" * 40)
    print(f"Dominant Axis:        {direction}")
    print(f"Axis Deviation:       {deviation} pixels off-target")
    print(f"Straight-Line Score:  {accuracy:.2f}%")
    print("=" * 40 + "\n")


if __name__ == "__main__":
    # PyAutoGUI Failsafe: Moving your mouse to any of the 4 corners
    # of your primary screen will abort the script if it ever gets stuck.
    pyautogui.FAILSAFE = True

    while True:
        run_precision_test()
        retry = input("Would you like to test again? (y/n): ").strip().lower()
        if retry != "y":
            print("Exiting tester...")
            break
