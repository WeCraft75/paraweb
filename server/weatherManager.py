# -*- coding: UTF-8 -*-
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config


class manager:
    def __init__(self, lat, lon):
        # setup language and OWM
        configDict = get_default_config()
        configDict["language"] = "sl"
        owm = OWM('fccbb7f106f4603371910d9b192f519e', config=configDict)
        # get weather
        manager = owm.weather_manager()
        owmData = manager.one_call(
            lat, lon, exclude='minutely,hourly', units='metric')
        self.location = (lat, lon)
        self.temperature = owmData.current.temperature().get('temp')  # °C
        self.humidity = owmData.current.humidity  # %
        self.pressure = owmData.current.pressure  # mbar
        self.uvi = owmData.current.uvi
        observation = manager.weather_at_coords(lat=lat, lon=lon)
        self.weather = observation.weather.status
        self.detailedWeather = observation.weather.detailed_status

    def getTemperature(self):
        return self.temperature

    def getHumidity(self):
        return self.humidity

    def getPressure(self):
        return self.pressure

    def getUvi(self):
        return self.uvi

    def getWeather(self):
        return self.weather

    def getDetailedWeather(self):
        return self.detailedWeather
