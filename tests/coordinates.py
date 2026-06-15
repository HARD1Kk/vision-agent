import pyautogui


def click_button():
    x, y = pyautogui.position()

    pyautogui.locateOnScreen("image2.png")
    print(pyautogui.locateOnScreen("image2.png"))
    pyautogui.click(760, 1061)
    print(pyautogui.click(x, y))
    pyautogui.hotkey("win", "s")
    # print(pyautogui.displayMousePosition())


click_button()
