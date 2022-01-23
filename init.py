from flask import Flask, redirect, render_template, url_for, request, session, jsonify
import json
from characters import character

app = Flask(__name__)
app.secret_key = "hello"

character_names = ["Shanko", "Saelwyn", "Kaelar", "Owly", "Tree", "Gith", "Otadus"]
players = []


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['button'] == 'add_player':
            players.append(character("Test", 0, 0, False))
        elif request.form['button'] == 'submit':
            pass  # do something else
        else:
            pass  # unknown
        return render_template("dyn.html", content=players)
    elif request.method == 'GET':
        for char in character_names:
            players.append(character(char, 20, 20, True))

        return render_template("dyn.html", content=players)


if __name__ == "__main__":
    app.run(debug=True)
