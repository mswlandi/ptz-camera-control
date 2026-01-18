Test for PTZ camera (SMTAV BA20UHD-X)

# setup

`pip install -r requirements.txt`

# running

```python
python main.py
```

# building executable

Create the venv and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # on Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

Build the executable with PyInstaller:

```bash
pyinstaller --clean --noconfirm PTZController.spec
```