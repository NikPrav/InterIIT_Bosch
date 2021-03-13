# Server
Server that implements augmentations, serves trained model and allows adding new data.

Currently takes in a JSON string of the format { "image":, "transform":"type fo transform" }
and returns the transformed image as base64ImageData.

## Setup
Note: this code is set in DEBUG mode,remember to set the debug flag in the `config.py` to false

For installing requirments, do
`poetry install`

For running the app, do 
```sh
poetry shell # everytime
python run.py
```
