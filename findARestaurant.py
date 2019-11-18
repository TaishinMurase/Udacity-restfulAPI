from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs

import sys

args = sys.argv

foursquare_client_id = "2BAWNPEEJM5UELMLYUQJNCTWGWRUKBTY5XHU2SS3POAOMTEP"
foursquare_client_secret = "50VUICQ2MYEAXP1MMKHC0KFWLUBIHNOSD5GTSPTQV4Y0OWIY"

def findARestaurant(mealType,location):
	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
	latitude, longitude = getGeocodeLocation(location)
	
	#2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
	#HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
	url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20130815&ll=%s,%s&query=%s' % (foursquare_client_id, foursquare_client_secret,latitude,longitude,mealType))
	h = httplib2.Http()
	result = json.loads(h.request(url,'GET')[1])

	#3. Grab the first restaurant
	firstInfo = result['response']['venues'][0]
	venue_id = firstInfo['id']
	restaurant_name = firstInfo['name']
	restaurant_address = firstInfo['location']['formattedAddress']
	address = ''
	for i in restaurant_address:
		address = i + ' '
	restaurant_address = address

	#4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
	url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&v=20150603&client_secret=%s' % ((venue_id,foursquare_client_id,foursquare_client_secret)))
	result = json.loads(h.request(url, 'GET')[1])

	#5. Grab the first image
	if result['response']['photos']['items']:
		firstpic = result['response']['photos']['items'][0]
		prefix = firstpic['prefix']
		suffix = firstpic['suffix']
		imageURL = prefix + "300x300" + suffix
	else:
		#6.  if no image available, insert default image url
		imageURL = "http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct"

	#7. Return a dictionary containing the restaurant name, address, and image url
	restaurantInfo = {'name':restaurant_name, 'address': restaurant_address, 'image':imageURL}
	print("Restaurant Name: %s" % restaurantInfo['name'])
	print("Restaurant Address: %s" % restaurantInfo['address'])
	print("Image: %s \n" % restaurantInfo['image'])
	print(restaurantInfo)
	return restaurantInfo

def main():
    findARestaurant(args[1], args[2])
	# findARestaurant("Pizza", "Tokyo, Japan")
	# findARestaurant("Tacos", "Jakarta, Indonesia")

if __name__ == '__main__':
    main()
