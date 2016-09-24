import requests
import json
from flask import Flask, render_template, request, redirect, url_for, Markup

app = Flask(__name__)

@app.route("/")
def main():
	# CAPITAL ONE API
	API_KEY = "api key goes here"
	customer = "customer id goes here"
	account = "acc id goes here"

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

	return render_template('index.html', data = json.dumps(sorted_amts), cust_firstname=cust_firstname, acc_owner=acc_owner, acc_type=acc_type, acc_balance=acc_balance, acc_rewards=acc_rewards)

@app.route("/showSignup")
def showSignup():
	return render_template('signup.html')

@app.route("/showSignin")
def showSignin():
        return render_template('signin.html')

if __name__ == "__main__":
	app.run(debug=True)
