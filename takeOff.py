from pyowm.owm import OWM

class takeOff:

    def __init__(self, name, lat, lon):
        owm = OWM('fccbb7f106f4603371910d9b192f519e')
        mgr = owm.weather_manager()
        one_call = mgr.one_call(lat, lon, exclude='minutely,hourly', units='metric')
        self.name = name
        self.location = (lat, lon)
        self.wind = one_call.current.wind().get('speed') # m/s
        self.windGust = one_call.current.wind().get('gust') # m/s
        self.windDeg = one_call.current.wind().get('deg') # (deg)
        self.temperature = one_call.current.temperature().get('temp') # C
        self.humidity = one_call.current.humidity # %
        self.pressure = one_call.current.pressure.get('press') # mbar
        self.uvi = one_call.current.uvi # uvi
        self.weather = one_call.current.weather_code

    def getName(self):
        return self.name

    def getWind(self):
        return self.wind

    def getWindGust(self):
        return self.windGust

    def getWindDirection(self):
        return None

