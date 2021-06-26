def generirajLink(lat, long):
    coord_API_endpoint = "http://api.openweathermap.org/data/2.5/weather?"
    lat_long = "lat=" + str(lat) + "&lon=" + str(long)
    join_key = "&appid=" + "fccbb7f106f4603371910d9b192f519e"  # drugi je kljuc
    units = "&units=metric"
    current_coord_weather_url = coord_API_endpoint + lat_long + join_key + units
    return current_coord_weather_url


print(generirajLink(46.33941534887242, 14.331205906510517))
# works
