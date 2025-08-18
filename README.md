# OPGI(v.0.0.1)
OPGI or open-GL python gui interface is a library which uses open-GL to render gui interface.
OPGI enable you to create gui interface quickly and easily and write now in v.0.0.1 have these abilities

- Create a window
- 3 widget which are label, button and entry

### Usage
- clone the OPGI repository

```
git clone https://github.com/mohamadashrafi-py/CMS-form-creator.git
```

- create a venv and install requirements

```
python -m venv .venv
pip install -r requirements.txt
```

use this simple code to have a simple demo

```
from Opgi import App, Label, Button, TextInput

def button_clicked():
    print(f"Button clicked! Text input value: {text_input.text}")

app = App(400, 300, "Window")

label = Label("Enter your name:", 50, 50)
text_input = app.add_widget(TextInput(50, 80, 200, 30))
button = app.add_widget(Button("Submit", 150, 120))
button.set_on_click(button_clicked)

app.add_widget(label)
app.run()
```

### Docs
read the docs to use the library in `docs` directory

### What you are going to see for the next version in v.0.0.2

- more widgets
- better structure of library
