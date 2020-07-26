from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars_p

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/")
def index():
    mars_dictionary = mongo.db.mars_dict.find_one()
    return render_template("index_p.html", mars = mars_dictionary)

@app.route("/scrape")
def scrape():
    mars_dict = mongo.db.mars_dict
    mars_scrape= scrape_mars_p.scrape()
    mars_dict.replace_one({}, mars_scrape, upsert=True)
    # mars.update({}, mars_scrape, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)  
