let intervalId = null;

function simulateClick(x, y) {
    const el = document.elementFromPoint(x, y);
    if (!el) return false;

    const opts = { bubbles: true, cancelable: true, clientX: x, clientY: y, view: window };

    ["mousemove", "mousedown", "mouseup", "click"].forEach(type => {
        el.dispatchEvent(new MouseEvent(type, opts));
    });
    return true;
}

function startClicking({ x = 0, y = 0, interval = 1000, maxClicks = 0 }) {
    stopClicking();
    let clicks = 0;

    intervalId = setInterval(() => {
        const ok = simulateClick(x, y);
        if (ok) {
            console.log("Clicked!");
            clicks++;
            if (maxClicks > 0 && clicks >= maxClicks) {
                stopClicking();
            }
        }
    }, interval);
}

function stopClicking() {
    if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
    }
}

window.addEventListener("message", (event) => {
    console.log("Message received:", event.data);

    const msg = event.data;
    if (!msg || typeof msg !== "object") return;

    if (msg.type === "START_CLICKING") {
        startClicking(msg.settings || {});
    } else if (msg.type === "STOP_CLICKING") {
        stopClicking();
    }
});
