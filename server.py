from flask import Flask, request, jsonify
import pyautogui
import threading
import time

app = Flask(__name__)
click_thread = None
stop_flag = False

def autoclick(x, y, interval, max_clicks):
    global stop_flag
    clicks = 0
    stop_flag = False
    while not stop_flag:
        pyautogui.click(x, y)
        clicks += 1
        print(f"Clicked at ({x},{y}) #{clicks}")
        if max_clicks > 0 and clicks >= max_clicks:
            break
        time.sleep(interval)

@app.route("/start", methods=["POST"])
def start_clicking():
    global click_thread
    data = request.json
    x = data.get("x", 0)
    y = data.get("y", 0)
    interval = data.get("interval", 1.0)
    max_clicks = data.get("maxClicks", 0)

    if click_thread and click_thread.is_alive():
        return jsonify({"status": "Already running"}), 400

    click_thread = threading.Thread(target=autoclick, args=(x, y, interval, max_clicks))
    click_thread.start()
    return jsonify({"status": "Started"})


@app.route("/stop", methods=["POST"])
def stop_clicking():
    global stop_flag
    stop_flag = True
    return jsonify({"status": "Stopped"})


if __name__ == "__main__":
    app.run(port=5000)
