import pyautogui
import time
import threading
import os
import sys
from flask import Flask, request, jsonify

app = Flask(__name__)
click_thread = None
stop_flag = threading.Event()

# --- helper to get app directory (works for .py and PyInstaller exe) ---
def get_app_dir():
    if getattr(sys, 'frozen', False):  # running in PyInstaller bundle
        return os.path.dirname(sys.executable)
    else:  # running as script
        return os.path.dirname(os.path.abspath(__file__))


@app.route("/start", methods=["POST"])
def start_clicking():
    global click_thread, stop_flag
    data = request.json
    interval = data.get("interval", 1.0)
    max_clicks = data.get("maxClicks", 0)
    image_path = data.get("image")  # optional image

    if image_path:
        app_dir = get_app_dir()
        image_path = os.path.join(app_dir, image_path)
        print(f"Resolved image path: {image_path}")
        if not os.path.exists(image_path):
            return jsonify({"error": f"Image not found at {image_path}"}), 400

    print(f"data is {data}")

    def autoclick():
        stop_flag.clear()
        clicks = 0

        while not stop_flag.is_set():
            if image_path:
                try:
                    button = pyautogui.locateOnScreen(image_path, confidence=0.8)
                except Exception as e:
                    print(f"Image search failed: {e}")
                    break

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

    click_thread = threading.Thread(target=autoclick, daemon=True)
    click_thread.start()
    return jsonify({"status": "Started"})


@app.route("/stop", methods=["POST"])
def stop_clicking():
    global stop_flag
    stop_flag.set()
    return jsonify({"status": "Stopped"})


if __name__ == "__main__":
    from waitress import serve
    print("Clicky app started!")
    print("Listening at http://127.0.0.1:5000")
    print("Send POST requests to /start and /stop")
    serve(app, host="127.0.0.1", port=5000)
