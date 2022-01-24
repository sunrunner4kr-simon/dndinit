from operator import attrgetter

from flask import Flask, render_template, request, redirect, url_for
from characters import Character
from flask_sockets import Sockets

app = Flask(__name__)
app.secret_key = "hello"

character_names = ["Shanko", "Saelwyn",
                   "Kaelar", "Owly", "Tree", "Gith", "Otadus"]
players = []


@app.route("/", methods=['GET', 'POST'])
def index():
    # First time only
    players.clear()
    for char in character_names:
        players.append(Character(char, 20, 20, True))

    return redirect(url_for('dashboard'))


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        if request.form['button'] == 'add_player':
            return redirect(url_for('add_character'))
        elif request.form['button'] == 'sort':
            players.sort(key=attrgetter('initiative'), reverse=True)
        elif request.form['button'] == 'reset':
            players.clear()
        else:
            pass  # unknown
        return render_template("dyn.html", content=players)
    elif request.method == 'GET':
        return render_template("dyn.html", content=players)


@app.route("/add_character", methods=['GET', 'POST'])
def add_character():
    if request.method == 'POST':
        selected = request.form.getlist('enabled-input')
        any_selected = bool(selected)

        players.append(Character(
            request.form['name-input'],
            int(request.form['initiative-input']),
            int(request.form['health-input']),
            any_selected
        ))
        return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        return render_template("add_characters.html")


if __name__ == "__main__":
    app.run(debug=True)
