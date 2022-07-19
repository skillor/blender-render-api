# Telegraf Build Api

### Docs

API-Documentation can be found here: https://skillor.github.io/blender-render-api/

## Installation

All settings can be overwritten with environment variables with the same name.

### Setup in Unix

> Install Blender

> Install requirements

```bash
pip3 install -r requirements.txt
```

> Install API requirements

```bash
pip3 install -r requirements_api.txt
```

> Copy "settings_example.py" to "settings.py"

```bash
cp settings_example.py settings.py
```

> Edit your settings.py

> Start the server

```bash
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --log-level warning
```
