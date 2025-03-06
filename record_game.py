import time
from pathlib import Path

import keyboard
import pyautogui
from PIL import Image

FILE = Path(__file__)
images_save_directory = FILE.parent / "games"
print(images_save_directory)
primary_images_buffer = []
secondary_images_buffer = []
MAX_SIZE = 50


def save_image(image: Image.Image, file_path) -> None:
    global primary_images_buffer
    global secondary_images_buffer
    if len(primary_images_buffer) <= MAX_SIZE:
        primary_images_buffer.append((image, file_path))
        return
    for im, f in secondary_images_buffer:
        im.save(f, format="JPEG", quality=85)
    secondary_images_buffer = primary_images_buffer
    primary_images_buffer = [(image, file_path)]


def is_game_over():
    try:
        global primary_images_buffer
        global secondary_images_buffer
        pyautogui.locateOnScreen("play_again.png", grayscale=True, region=(1015, 781, 600, 100))
        primary_images_buffer = []
        secondary_images_buffer = []
        return True
    except Exception:
        return False


def get_pos(filename: str):
    num = filename.split(r"/")[1]
    num = num.split(r"_")[1]
    num = num.split(".")[0]
    return int(num)

def is_going_left() -> bool:
    return keyboard.is_pressed("a") or keyboard.is_pressed("left arrow")

def is_going_right() -> bool:
    return keyboard.is_pressed("d") or keyboard.is_pressed("right arrow")

def main() -> None:
    images_save_directory.mkdir(parents=True, exist_ok=True)
    action_0 = images_save_directory / "0"
    action_0.mkdir(exist_ok=True)
    action_1 = images_save_directory / "1"
    action_1.mkdir(exist_ok=True)
    action_2 = images_save_directory / "2"
    action_2.mkdir(exist_ok=True)
    actions = [0, 0, 0]
    actions_dir = [action for action in images_save_directory.glob("*")]
    for action in actions_dir:
        if action.name == "0":
            actions[0] = len(list(action.glob("*")))
        if action.name == "1":
            actions[1] = len(list(action.glob("*")))
        if action.name == "2":
            actions[2] = len(list(action.glob("*")))
    print(actions)

    time.sleep(1)
    previous = time.perf_counter()

    while not keyboard.is_pressed("q"):
        im = pyautogui.screenshot()
        if not is_game_over():
            if is_going_left():
                im = im.convert("L")
                im = im.resize((85, 85))
                file_path = images_save_directory / "1" / f"{actions[1]}.jpg"
                actions[1] += 1
                save_image(im, file_path)
            elif is_going_right():
                im = im.convert("L")
                im = im.resize((85, 85))
                file_path = images_save_directory / "2" / f"{actions[2]}.jpg"
                actions[2] += 1
                save_image(im, file_path)
            else:
                if time.perf_counter() - previous > 0.7:
                    previous = time.perf_counter()
                    im = im.convert("L")
                    im = im.resize((85, 85))
                    file_path = images_save_directory / "0" / f"{actions[0]}.jpg"
                    actions[0] += 1
                    save_image(im, file_path)
        else:
            pyautogui.keyDown("enter")
            time.sleep(0.1)
            pyautogui.keyUp("enter")
            previous = time.perf_counter()


if __name__ == '__main__':
    main()
