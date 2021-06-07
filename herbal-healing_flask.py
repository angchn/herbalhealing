import sqlite3
from flask import Flask, g, render_template, request, redirect

app = Flask(__name__)
DATABASE = "plants.db"

def get_db():
    #connects database "plants.db" to Python file.
    db = getattr (g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    #error check for previous function "get_db()".
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

@app.route ("/")
def home():
    #home page, where user is presented with links to other pages.
    return render_template("home.html")

@app.route ("/repository")
def repository():
    #repository page, where all data are displayed in a table.
    cursor = get_db().cursor()
    #sql statement, displaying data from foreign key onto primary key.
    sql = "SELECT herb.name, rarity.level, type.classification, herb.place_of_origin, herb.description FROM herb JOIN rarity ON herb.rarity = rarity.id JOIN type ON herb.type = type.id"
    if request.args.get ('name')  == 'a-z': #sort by name (a-z).
        sql += " ORDER BY herb.name"
    elif request.args.get ('name') == 'z-a': #sort by name (z-a).
        sql += " ORDER BY herb.name DESC"
    elif request.args.get ('rarity') == 'common': #sort by rarity (common).
        sql += " WHERE rarity.level='common'"
    elif request.args.get ('rarity') == 'rare':#sort by rarity (rare).
        sql += " WHERE rarity.level='rare'"
    elif request.args.get ('rarity') == 'unique': #sort by rarity (unique).
        sql += " WHERE rarity.level='unique'"
    elif request.args.get ('type') == 'flower': #sort by type (flower).
        sql += " WHERE type.classification='flower'" 
    elif request.args.get ('type') == 'fruit':  #sort by type (fruit).
        sql += " WHERE type.classification='fruit'"
    elif request.args.get ('type') == 'leaf': #sort by type (leaf).
        sql += " WHERE type.classification='leaf'"
    elif request.args.get ('type') == 'root': #sort by type (root).
        sql += " WHERE type.classification='root'"
    elif request.args.get ('type') == 'seed': #sort by type (seed).
        sql += " WHERE type.classification='seed'"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("repository.html", results=results)

@app.route ("/search", methods=["POST", "GET"])
def search():
    #search bar, allows user to search for a specific herb and redirects them to the specific page for that herb.
    if request.method == "POST":
        print (request.form.get("filter"))
        cursor = get_db().cursor()
        sql = "SELECT * FROM herb WHERE name LIKE ?"
        cursor.execute (sql, (request.form.get("filter"),))
        results = cursor.fetchone()
        if results == None:
            return redirect ("/error")
        else: 
            print (f"results={results}")
            return redirect (f"/herb/{results[0]}")

@app.route ("/herb/<int:id>")
def herb(id):
    #page that displays all the information about the specific herb the user has searched for.
    cursor = get_db().cursor()
    sql = "SELECT herb.id, herb.name, rarity.level, type.classification, herb.place_of_origin, herb.description FROM herb JOIN rarity ON herb.rarity = rarity.id JOIN type ON herb.type = type.id WHERE herb.id = ?"
    cursor.execute(sql, (id,))
    result = cursor.fetchone()
    return render_template("herb.html", result=result)

@app.route ("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route ("/about")
def about():
    #about page, provides user with more information about the website.
    return render_template("about.html")

@app.route ("/contact")
def contact():
    return render_template("contact.html")

@app.route ("/error")
def error():
    #error page, for when user input returns no results.
    return render_template("error.html")

if __name__ == "__main__":
    app.run(debug=True)