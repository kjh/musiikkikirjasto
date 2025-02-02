import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
import config, music_collection, users

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    collections = music_collection.get_collections()
    return render_template("index.html", collections=collections)

@app.route("/collection/<int:collection_id>")
def show_collection(collection_id):
    collection = music_collection.get_collection(collection_id)
    releases = music_collection.get_releases(collection_id)
    return render_template("collection.html", collection=collection, releases=releases)

@app.route("/new_collection", methods=["POST"])
def new_collection():
    collection_title = request.form["title"]
    artist = request.form["content"]
    title = request.form["content"]
    user_id = session["user_id"]

    collection_id = music_collection.add_collection(collection_title, artist, title, user_id)
    return redirect("/collection/" + str(collection_id))

@app.route("/new_release", methods=["POST"])
def new_release():
    artist = request.form["artist"]
    title = request.form["title"]
    user_id = session["user_id"]
    collection_id = request.form["collection_id"]

    music_collection.add_release(artist, title, user_id, collection_id)
    return redirect("/collection/" + str(collection_id))

@app.route("/edit/<int:release_id>", methods=["GET", "POST"])
def edit_release(release_id):
    release = music_collection.get_release(release_id)

    if request.method == "GET":
        return render_template("edit.html", release=release)

    if request.method == "POST":
        artist = request.form["artist"]
        title = request.form["title"]
        music_collection.update_release(release["id"], artist, title)
        return redirect("/collection/" + str(release["collection_id"]))

@app.route("/remove/<int:release_id>", methods=["GET", "POST"])
def remove_release(release_id):
    release = music_collection.get_release(release_id)

    if request.method == "GET":
        return render_template("remove.html", release=release)

    if request.method == "POST":
        if "continue" in request.form:
            music_collection.remove_release(release["id"])
        return redirect("/collection/" + str(release["collection_id"]))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            return "VIRHE: salasanat eivät ole samat"

        try:
            users.create_user(username, password1)
            return "Tunnus luotu"
        except sqlite3.IntegrityError:
            return "VIRHE: tunnus on jo varattu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["user_id"]
    return redirect("/")
