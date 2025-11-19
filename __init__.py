import os
from flask import Flask, render_template, abort, send_from_directory
from dotenv import load_dotenv
import json

load_dotenv()       # go into the .env file and populate the environment variable

app = Flask(__name__)

# lazy load projects from the database
def get_projects():
    json_path = os.path.join(os.path.dirname(__file__), "projects.json")
    with open(json_path) as f:
        return json.load(f)

def get_slug_to_project(projects):
    return {p["slug"]: p for p in projects}

@app.route("/")
def home():
    projects = get_projects()
    return render_template("home.html",projects=projects)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/resume")
def resume():
    return send_from_directory('static', 'Resume.pdf')

@app.route("/project/<string:slug>")
def project(slug):
    projects = get_projects()
    slug_to_project = get_slug_to_project(projects)

    if slug not in slug_to_project:
        abort(404)
    return render_template(
        f"project_{slug}.html",
        project=slug_to_project[slug]
    )

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

