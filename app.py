import sqlite3
from flask import Flask, abort
from flask import redirect, render_template, request, session
import config, music_collection, users, helper
import secrets

app = Flask(__name__)
app.secret_key = config.secret_key

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = music_collection.get_user(user_id)
    if not user:
        abort(404)
    releases = music_collection.get_user_releases(user_id)
    return render_template("user.html", user=user, releases=releases)

@app.route("/search")
def search():
    query = request.args.get("query")
    results = music_collection.search(query) if query else []
    return render_template("search.html", query=query, results=results)

@app.route("/")
def index():
    collections = music_collection.get_collections()
    return render_template("index.html", collections=collections)

@app.route("/collection/<int:collection_id>")
def show_collection(collection_id):
    collection = music_collection.get_collection(collection_id)
    like_count = music_collection.count_collection_likes(collection_id)
    tags = music_collection.get_collection_tags(collection_id)

    if not collection:
        abort(404)

    releases = music_collection.get_releases(collection_id)

    has_liked = False
    if "user_id" in session and music_collection.has_user_liked(session["user_id"], collection_id):
        has_liked = True 

    return render_template("collection.html", collection=collection, like_count=like_count, has_liked=has_liked, releases=releases, tags=tags)

@app.route("/like_collection", methods=["POST"])
@helper.require_login
def like_collection():
    check_csrf() 
    collection_id = request.form["collection_id"]
    user_id = session["user_id"]

    if music_collection.has_user_liked(user_id, collection_id):
        abort(403)
   
    try:
        music_collection.add_like(user_id, collection_id)
        return redirect("/")
    except sqlite3.IntegrityError:
        abort(403)
    
@app.route("/delete_like_collection", methods=["POST"])
@helper.require_login
def delete_like_collection():
    check_csrf() 
    collection_id = request.form["collection_id"]
    user_id = session["user_id"]

    if not music_collection.has_user_liked(user_id, collection_id):
        abort(403)
   
    try:
        music_collection.delete_like(user_id, collection_id)
        return redirect("/")
    except sqlite3.IntegrityError:
        abort(403)

@app.route("/edit_collection/<int:collection_id>", methods=["GET", "POST"])
@helper.require_login
def edit_collection(collection_id):    
    collection = music_collection.get_collection(collection_id)
    tags = music_collection.get_collection_tags(collection_id)
    if not collection:
        abort(404)
    elif collection["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit_collection.html", collection=collection, tags=tags)

    if request.method == "POST":
        check_csrf() 
        new_title = request.form["collection_title"]

        if not new_title:
            abort(403)
        
        if len(new_title) > 100:
            abort(403)
        
        music_collection.update_collection(collection["id"], new_title)
        return redirect("/collection/" + str(collection["id"]))

@app.route("/add_tags", methods=["POST"])
@helper.require_login
def add_collection_tags():
    check_csrf() 
    collection_id = request.form["collection_id"]
    
    if not music_collection.get_collection(collection_id):
        abort(404)

    tags = [tag.strip() for tag in request.form["tags"].split(',')]

    for tag_name in tags:
        tag_id = music_collection.get_tag_id(tag_name)
        if not tag_id:
            music_collection.add_tag(tag_name)
            tag_id = music_collection.get_tag_id(tag_name)
        try:    
            music_collection.add_collection_tag(tag_id, collection_id)
        except sqlite3.IntegrityError:
            abort(403)

    return redirect("/edit_collection/" + str(collection_id))

@app.route("/remove_tag/<int:tag_id>/<int:collection_id>", methods=["GET", "POST"])
@helper.require_login
def remove_tag(tag_id, collection_id):

    tag_name = music_collection.get_tag_name(tag_id)
    collection = music_collection.get_collection(collection_id)

    if not collection or not tag_name:
        abort(404)
    elif collection["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_tag.html", tag_id=tag_id, collection_id=collection_id, tag_name=tag_name)

    if request.method == "POST":
        check_csrf()
        if "continue" in request.form:
            music_collection.delete_collection_tag(tag_id, collection_id)
        return redirect("/collection/" + str(collection_id))

@app.route("/new_collection", methods=["POST"])
@helper.require_login
def new_collection():
    check_csrf()
    collection_title = request.form["collection_title"]
    artist = request.form["artist"]
    title = request.form["title"]
    user_id = session["user_id"]

    if not collection_title or not artist or not title:
        abort(403)

    if len(collection_title) > 100 or len(artist) > 100 or len(title) > 100:
        abort(403)

    collection_id = music_collection.add_collection(collection_title, artist, title, user_id)
    return redirect("/collection/" + str(collection_id))

@app.route("/new_release", methods=["POST"])
@helper.require_login
def new_release():
    check_csrf()
    artist = request.form["artist"]
    title = request.form["title"]
    user_id = session["user_id"]
    collection_id = request.form["collection_id"]

    collection = music_collection.get_collection(collection_id)
    if not collection:
        abort(404)
    elif collection["user_id"] != session["user_id"]:
        abort(403)

    if not artist or not title:
        abort(403)

    if len(artist) > 100 or len(title) > 100:
        abort(403)

    try:
        music_collection.add_release(artist, title, user_id, collection_id)
    except sqlite3.IntegrityError:
        abort(403)

    return redirect("/collection/" + str(collection_id))

@app.route("/edit/<int:release_id>", methods=["GET", "POST"])
@helper.require_login
def edit_release(release_id):
    release = music_collection.get_release(release_id)
    if not release:
        abort(404)
    elif release["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit.html", release=release)

    if request.method == "POST":
        check_csrf()
        artist = request.form["artist"]
        title = request.form["title"]

        if not artist or not title:
            abort(403)
        
        if len(artist) > 100 or len(title) > 100:
            abort(403)
        
        music_collection.update_release(release["id"], artist, title)
        return redirect("/collection/" + str(release["collection_id"]))

@app.route("/remove/<int:release_id>", methods=["GET", "POST"])
@helper.require_login
def remove_release(release_id):
    release = music_collection.get_release(release_id)
    if not release:
        abort(404)
    elif release["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove.html", release=release)

    if request.method == "POST":
        check_csrf()
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
            return redirect("/")
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
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["user_id"]
    return redirect("/")
