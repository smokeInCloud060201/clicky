import pyautogui
import time
import threading
from flask import Flask, request, jsonify

app = Flask(__name__)
click_thread = None
stop_flag = False

@app.route("/start", methods=["POST"])
def start_clicking():
    global click_thread, stop_flag
    data = request.json
    interval = data.get("interval", 1.0)
    max_clicks = data.get("maxClicks", 0)
    image_path = data.get("image")  # optional image

    def autoclick():
        global stop_flag
        stop_flag = False
        clicks = 0

        while not stop_flag:
            if image_path:
                # locate the button on screen
                button = pyautogui.locateOnScreen(image_path, confidence=0.8)
                if button:
                    x, y = pyautogui.center(button)
                    print(f"Found button at ({x},{y})")
                else:
                    print("Button not found, retrying...")
                    time.sleep(interval)
                    continue
            else:
                # fallback to manual coords
                x = data.get("x", 0)
                y = data.get("y", 0)

            pyautogui.click(x, y)
            clicks += 1
            print(f"Clicked at ({x},{y}) #{clicks}")

            if max_clicks > 0 and clicks >= max_clicks:
                break

            time.sleep(interval)

    if click_thread and click_thread.is_alive():
        return jsonify({"status": "Already running"}), 400

    click_thread = threading.Thread(target=autoclick)
    click_thread.start()
    return jsonify({"status": "Started"})

@app.route("/stop", methods=["POST"])
def stop_clicking():
    global stop_flag
    stop_flag = True
    return jsonify({"status": "Stopped"})

if __name__ == "__main__":
    app.run(port=5000)
