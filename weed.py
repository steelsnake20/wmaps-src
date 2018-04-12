import requests
import json
import operator
import WeedItem
import sys

def getCityUrl(city):
	url = "https://api-g.weedmaps.com/wm/v2/listings?filter%5Bplural_types%5D%5B%5D=deliveries&filter%5Bregion_slug%5Bdeliveries%5D%5D="
	url += city
	url += "&page_size=100&size=100"
	return url

# default city if no command line argument is given is SF
mainURL = getCityUrl("san-francisco")

if(len(sys.argv) > 1):
	mainURL = getCityUrl(sys.argv[1])
	if(sys.argv[1] == "peninsula"):
		mainURL = getCityUrl("the-penisula")

print("1. eighth")
print("2. quarter")
print("3. half_ounce")
print("4. ounce")
desiredAmount = input("How much weed? (1-4): ")
while(desiredAmount != "1" and desiredAmount != "2" and desiredAmount != "3" and desiredAmount != "4"):
	print("1. eighth")
	print("2. quarter")
	print("3. half_ounce")
	print("4. ounce")
	desiredAmount = input("How much? (1-4): ")
print("Loading results... This may take 20 - 30 seconds.")
amount = ""
if desiredAmount == "1":
	amount = "eighth"
elif desiredAmount == "2":
	amount = "quarter"
elif desiredAmount == "3":
	amount = "half_ounce"
elif desiredAmount == "4":
	amount = "ounce"

allDispensaries = requests.get(mainURL).json()
weedItemObjectList = []



for dispensary in allDispensaries["data"]["listings"]:
	dispensaryName = dispensary["name"]
	city = dispensary["city"]
	name = "https://api-g.weedmaps.com/wm/web/v1/listings/"
	name += dispensary["web_url"].rsplit('/', 1)[-1]
	name += "/menu?type=delivery"
	dispensaryURL = requests.get(name).json()
	openStatus = dispensaryURL["listing"]["todays_hours"]["open_status"]
	closingTime = dispensaryURL["listing"]["todays_hours"]["closing_time"]
	licenseType = dispensaryURL["listing"]["license_type"]
	for menuItems in dispensaryURL["categories"]:
		for x in menuItems["items"]:
			categoryName = x["category_name"]
			strainName = x["name"]
			if categoryName == "Indica" or categoryName == "Sativa" or categoryName == "Hybrid":
			# if categoryName == "Concentrate" or categoryName == "Wax":
				price = x["prices"][amount]
				url = "https://weedmaps.com" + x["url"]
				#  'and "Cartridge" not in strainName' (for wax search)
				#  'and licenseType != medical' (for reactional-only results)
				if price > 3.0 and openStatus != "CLOSED" and licenseType != "medical":
					weedItemObjectList.append(WeedItem.WeedItem(dispensaryName,strainName,price,url,city,closingTime))

sortedWeedItems = sorted(weedItemObjectList, key=operator.attrgetter('price'), reverse=True)

for item in sortedWeedItems:
	print(amount,"Price: $" + str(item.getPrice()))
	print("Strain:",item.getStrainName())
	print("Dispensary:",item.getStoreName())
	print("City: ",item.getCity())
	print("Closing time: " + item.getClosingTime())
	print("URL: " + item.getWebURL())
	print()

