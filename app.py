from flask import Flask
import python_weather
from takeOff import vzletisce


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

print(hello_world)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=390)
client = python_weather.Client(format=python_weather.METRIC)

gozd = vzletisce("Gozd", "J", 3.5, 5, "Soncno", 46.33941534887242, 14.331205906510517)
