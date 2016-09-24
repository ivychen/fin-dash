from flask import Flask, render_template, request, redirect, url_for
import requests
import json
import datetime

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
	merch_info = getMerchantInfo()

	date_data = {}
	for y in to_show:
		if y[u'purchase_date'] in date_data:
			add_to = date_data[y[u'purchase_date']]
			add_to["total"] += y[u'amount']
		else:
			date_data[y[u'purchase_date']] = {"total" : y[u'amount'], "food": 0, "groceries": 0, "entertainment": 0, "gas": 0, "coffee": 0, "music": 0, "shopping": 0}

		merch = str(y[u'merchant_id'])
		cat = merch_info[merch]["categories"]

		for c in cat:
			if c == 'enterta':
				c = "entertainment"
			add_to = date_data[y[u'purchase_date']]
			add_to[c] += y[u'amount']

	d = datetime.datetime.strptime(to_show[49][u'purchase_date'], "%Y-%m-%d")
	delta = datetime.timedelta(days=1)
	while d <= datetime.datetime.strptime(to_show[0][u'purchase_date'], "%Y-%m-%d"):
	    str_date = d.strftime("%Y-%m-%d")
	    if str_date not in date_data:
	    	date_data[str_date] = {"total" : 0, "food": 0, "groceries": 0, "entertainment": 0, "gas": 0, "coffee": 0, "music": 0, "shopping": 0}
	    d += delta

	sorted_amts = []
	for x in date_data:
		sorted_amts.append({'date': x, 'amounts': date_data[x]})
	print sorted_amts
	sorted_amts.sort(key=lambda item:item['date'], reverse=False)

	return render_template('index.html', data = json.dumps(sorted_amts))

@app.route("/showSignup")
def showSignup():
	return render_template('signup.html')

@app.route("/showSignin")
def showSignin():
        return render_template('signin.html')

def getMerchantInfo():
	merchants = ['57e69aaedbd83557146123df', '57e6a242dbd83557146123f9', '57e6a242dbd83557146123fa', '57e6a242dbd83557146123fb', '57e6a243dbd83557146123fc', '57e6a243dbd83557146123fd', '57e6a243dbd83557146123fe', '57e6a243dbd83557146123ff', '57e6a243dbd8355714612400', '57e6a243dbd8355714612401', '57e6a243dbd8355714612402', '57e6a243dbd8355714612403', '57e6a243dbd8355714612404']
	API_KEY = "ca41b2d25861cebdfabb45477c97bcab"
	merchant_info = {}
	for merchant in merchants:
		url = "http://api.reimaginebanking.com/merchants/{}?key={}".format(merchant, API_KEY)
		response = requests.get(url, headers={'content-type':'application/json'})
		merchant_dict = response.json()
		merchant_id = str(merchant_dict[u'_id'])
		merchant_categories = [str(x) for x in merchant_dict[u'category']]
		name = str(merchant_dict[u'name'])

		merchant_info[merchant_id] = {"name": name, "categories": merchant_categories}

	return merchant_info

if __name__ == "__main__":
	app.run(debug=True)
