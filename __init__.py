import os
from flask import Flask, render_template, abort, send_from_directory
from pymongo import MongoClient         # create a client side session that we can use to connect mongoDB
from dotenv import load_dotenv

load_dotenv()       # go into the .env file and populate the environment variable


app = Flask(__name__)
client = MongoClient(os.getenv("MONGODB_URI")) #create a connection to the cluster
app.db = client.portfolio   # create a connection to the database

projects = [e for e in app.db.projects.find({})]
slug_to_project = {project["slug"]: project for project in projects}

@app.route("/")
def home():
    return render_template("home.html",projects=projects)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/resume")
def resume():
    return send_from_directory('static', 'Resume_Chi-Wei Hu.pdf')

@app.route("/project/<string:slug>")
def project(slug):
    if slug not in slug_to_project:
        abort(404)
    return render_template(
        f"project_{slug}.html",
        project=slug_to_project[slug]
    )

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404