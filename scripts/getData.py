import requests, datetime, calendar, math, statistics

API_KEY = "ca41b2d25861cebdfabb45477c97bcab"
customer = "57e693dbdbd83557146123d8"
account = "57e69755dbd83557146123dd"
url = "http://api.reimaginebanking.com/accounts/{}/purchases?key={}".format(account, API_KEY)
response = requests.get(url, headers={'content-type':'application/json'})
x = response.json()
x.sort(key=lambda item:item['purchase_date'])
print(x)

firstDate = datetime.date(*(int(s) for s in x[0]['purchase_date'].split("-")))
lastDate = datetime.date(*(int(s) for s in x[len(x) - 1]['purchase_date'].split("-")))

timeSpan = (lastDate - firstDate).days

weeklySpending = [0] * (math.floor(timeSpan/7) + 1)

for purchase in x:
    purchaseDate = datetime.date(*(int(s) for s in purchase['purchase_date'].split("-")))
    week = math.floor(((purchaseDate - firstDate).days)/7)
    weeklySpending[week] = weeklySpending[week] + purchase['amount']

weeklySpendingAvg = statistics.mean(weeklySpending)

currentWeekSpending = 0;
i = 1
currentDate = datetime.date(*(int(s) for s in x[len(x) - i]['purchase_date'].split("-")))
weekday = datetime.timedelta(days = currentDate.weekday())
beginWeek = currentDate - weekday

while(currentDate > beginWeek):
    currentWeekSpending += x[len(x) - i]['amount']
    i += 1
    currentDate = datetime.date(*(int(s) for s in x[len(x) - i]['purchase_date'].split("-")))

weeklySpendingRatio = currentWeekSpending/weeklySpendingAvg

    


