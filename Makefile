.PHONY: setup start build build-no-console clean

setup:
	python -m pip install --upgrade pip setuptools wheel
	python -m pip install -r requirements.txt

start:
	python ./api/clicky.py

build:
	python -m PyInstaller --onefile --icon=./icon/clicky.ico ./api/clicky.py
	cp ./api/stop_button.png ./dist

build-no-console:
	python -m PyInstaller --onefile --noconsole --icon=./icon/clicky.ico ./api/clicky.py

clean:
	rm -rf build dist __pycache__ *.spec
