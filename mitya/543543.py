from googlemaps import GoogleMaps

gmaps = GoogleMaps(API_KEY)
lat, lng = gmaps.address_to_latlng(address)