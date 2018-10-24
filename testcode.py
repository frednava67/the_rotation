import datetime

mystr = "10/23/2018"
result = datetime.datetime.strptime(mystr, "%m/%d/%Y")
print(result)
print(result.date() == datetime.datetime.today().date())
