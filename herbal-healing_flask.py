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
    if request.args.get ('name' == 'a-z'):
        sql += " ORDER BY herb.name"
    elif request.args.get ('name' == 'z-a'):
        sql += " ORDER BY herb.name DESC"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("repository.html", results=results)

@app.route ("/about")
def about():
    #about page, provides user with more information about the website.
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)