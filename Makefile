

setup:
	python -m pip install flask
	python -m pip install --upgrade pip setuptools wheel
	python -m pip install --upgrade pillow pyscreeze pygetwindow pymsgbox mouseinfo
	python -m pip install --upgrade pyautogui opencv-python

start:
	python server.py
