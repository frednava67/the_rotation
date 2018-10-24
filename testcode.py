import datetime
import urllib, urllib.request, ssl

# mystr = "10/23/2018"
# result = datetime.datetime.strptime(mystr, "%m/%d/%Y")
# print(result)
# print(result.date() == datetime.datetime.today().date())
# print(result)

imageURL = "https://1drv.ms/u/s!AiqQzee7nmH7mqBZSwSt0X-7LrUPew"
ssl._create_default_https_context = ssl._create_unverified_context
r = urllib.request.urlopen(imageURL)
if (r.headers.get_content_maintype() != 'image'):
    print("IMAGE!")






#https://1drv.ms/u/s!AiqQzee7nmH7mqBZSwSt0X-7LrUPew
