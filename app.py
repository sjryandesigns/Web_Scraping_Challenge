# Import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create instance of Flask
app = Flask(__name__)

#Use Mongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    #Find one record of data from mongo database
    mars_data = mongo.db.marscollection.find_one()

    # Return template and data
    return render_template("index.html", mars = mars_data)

#Route that will trigger scrape function
@app.route("/scrape")
def scrape():
    
    #Run the scrape function
    mars_dict = scrape_mars.scrape_info()

    #Update the mongo database using update and upsert=True
    mongo.db.marscollection.update({}, mars_dict, upsert=True)

    #Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)