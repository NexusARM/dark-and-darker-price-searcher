import pyautogui
from time import sleep
from ImageProcessor import ImageProcessor

def click_on_site(name, stat):
    if len(text) != 0:
        pyautogui.click(-950, -60)
        pyautogui.write(name)
        pyautogui.press('down')
        pyautogui.press('enter')
        pyautogui.click(-950, 200)
        sleep(0.1)
        if len(stat) == 1:
            pyautogui.click(-950, 215)
        elif len(stat) == 2:
            pyautogui.click(-950, 240)
        elif len(stat) == 3:
            pyautogui.click(-950, 265)
        elif len(stat) == 4:
            pyautogui.click(-950, 280)
        for x in range(0, len(stat)):
            pyautogui.click(-780, 30 + 25 * x)
            sleep(0.1)
            pyautogui.write(stat[x])
            pyautogui.press('enter')
        pyautogui.click(-130, -60)
    pyautogui.moveTo(initial_mouse_position)
    
if __name__ == "__main__":   
    imageProcessor = ImageProcessor(1440,2560)
    initial_mouse_position = pyautogui.position()

    cropped_image, match_val = imageProcessor.find_and_crop_image()
    if cropped_image:
        text = imageProcessor.extract_text_from_image(cropped_image)
        name, stat = imageProcessor.extract_name_and_stat(text)
        if name and stat:
            print("Extracted name:", name)
            print("Extracted stat:", stat)
            click_on_site(name, stat)
        else:
            print("Name or stat is empty, skipping click operation.")
    else:
        print("Template not found in the screenshot.")