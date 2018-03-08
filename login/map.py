from geopy.geocoders import Nominatim
geolocator = Nominatim()
location = geolocator.geocode("Canton,MA")
print(location.address)
print((location.latitude, location.longitude))
print(location.raw)