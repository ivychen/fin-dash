import requests
import json
import datetime, calendar, math, statistics
from flask import Flask, render_template, request, redirect, url_for, Markup

app = Flask(__name__)

@app.route("/")
def main():
        API_KEY = "ca41b2d25861cebdfabb45477c97bcab"
        customer = "57e693dbdbd83557146123d8"
        account = "57e69755dbd83557146123dd"

        url = "http://api.reimaginebanking.com/accounts/{}/purchases?key={}".format(account, API_KEY)
        response = requests.get(url, headers={'content-type':'application/json'})
        x = response.json()
        x.sort(key=lambda item:item['purchase_date'], reverse=True)
        to_show = x[:50]
        date_data = {}
        for y in to_show:
                if y[u'purchase_date'] in date_data:
                        date_data[y[u'purchase_date']] += y[u'amount']
                else:
                        date_data[y[u'purchase_date']] = y[u'amount']
        sorted_amts = []
        for x in date_data:
                sorted_amts.append({'date': x, 'amount': date_data[x]})
        sorted_amts.sort(key=lambda item:item['date'], reverse=False)

        # weekly budgeting data

        x_budget = response.json()
        x_budget.sort(key=lambda item:item['purchase_date'])

        firstDate = datetime.date(*(int(s) for s in x_budget[0]['purchase_date'].split("-")))
        lastDate = datetime.date(*(int(s) for s in x_budget[len(x_budget) - 1]['purchase_date'].split("-")))

        timeSpan = (lastDate - firstDate).days

        weeklySpending = [0] * (math.floor(timeSpan/7) + 1)

        for purchase in x_budget:
            purchaseDate = datetime.date(*(int(s) for s in purchase['purchase_date'].split("-")))
            week = math.floor(((purchaseDate - firstDate).days)/7)
            weeklySpending[week] = weeklySpending[week] + purchase['amount']

        weeklySpendingAvg = statistics.mean(weeklySpending)

        currentWeekSpending = 0;
        i = 1
        currentDate = datetime.date(*(int(s) for s in x_budget[len(x_budget) - i]['purchase_date'].split("-")))
        weekday = datetime.timedelta(days = currentDate.weekday())
        beginWeek = currentDate - weekday

        while(currentDate > beginWeek):
            currentWeekSpending += x_budget[len(x_budget) - i]['amount']
            i += 1
            currentDate = datetime.date(*(int(s) for s in x_budget[len(x_budget) - i]['purchase_date'].split("-")))

        currentWeekSpending = float("{0:.2f}".format(currentWeekSpending))
        weeklySpendingAvg = float("{0:.2f}".format(weeklySpendingAvg))

        # MORE DAMN DATA
        # CUSTOMER INFO
        cust_url = "http://api.reimaginebanking.com/customers/{}?key={}".format(customer, API_KEY)
        cust_query = requests.get(cust_url, headers={'content-type':'application/json'})
        cust_info = cust_query.json()
        cust_firstname = cust_info['first_name']

        # ACCOUNT INFO
        acc_url = "http://api.reimaginebanking.com/accounts/{}?key={}".format(account, API_KEY)
        acc_query = requests.get(acc_url, headers={'content-type':'application/json'})
        acc_info = acc_query.json()

        acc_owner = cust_info['first_name'] + ' ' + cust_info['last_name']
        acc_type = acc_info['type']
        acc_balance = acc_info['balance']
        if acc_balance < 0:
        	acc_balance = '<span class="new badge red">' + '{:05.2f}'.format(acc_balance) + '</span>'
        else:
        	acc_balance = '<span class="new badge">' + '{:05.2f}'.format(acc_balance) + '</span>'
        acc_balance = Markup(acc_balance)
        acc_rewards = Markup('<span class="new badge blue">' + '{0:.2f}'.format(acc_info['rewards']) + '</span>')

        return render_template(
                'index.html',
                transactionData = json.dumps(sorted_amts),
                weeklyBudgetData = json.dumps([currentWeekSpending, weeklySpendingAvg-currentWeekSpending]),
                cust_firstname=cust_firstname,
                acc_owner=acc_owner,
                acc_type=acc_type,
                acc_balance=acc_balance,
                acc_rewards=acc_rewards
                ) 
@app.route("/showSignup")
def showSignup():
        return render_template('signup.html')

@app.route("/showSignin")
def showSignin():
        return render_template('signin.html')

if __name__ == "__main__":
        app.run(debug=True)
