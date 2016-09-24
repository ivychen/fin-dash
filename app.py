from flask import Flask, render_template, request, redirect, url_for
import requests
import json

app = Flask(__name__)

@app.route("/")
def main():
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
	return render_template('index.html', data = json.dumps(sorted_amts))

@app.route("/showSignup")
def showSignup():
	return render_template('signup.html')

@app.route("/showSignin")
def showSignin():
        return render_template('signin.html')


if __name__ == "__main__":
	app.run(debug=True)
