from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def main():
	return render_template('index.html')

@app.route("/showSignup")
def showSignup():
	return render_template('signup.html')

if __name__ == "__main__":
	app.run(debug=True)
