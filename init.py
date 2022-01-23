from flask import Flask, redirect, render_template, url_for, request

app = Flask(__name__)


class Players:
    shanko = 1
    saelwyn = 1
    kaelar = 1
    owl = 1
    tree = 1
    gith = 1
    otadus = 1
    mon1 = 1
    mon2 = 1
    mon3 = 1
    mon4 = 1
    mon5 = 1
    mon6 = 1
    mon7 = 1


class Enabled:
    shanko = 1
    saelwyn = 1
    kaelar = 1
    owl = 0
    tree = 1
    gith = 1
    otadus = 1
    mon1 = 1
    mon2 = 1
    mon3 = 1
    mon4 = 0
    mon5 = 0
    mon6 = 0
    mon7 = 0


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        if "shanko" in request.form:
            shanko = request.form["shanko"]
            Players.shanko = shanko
            print("Shanko: " + shanko)
        if "saelwyn" in request.form:
            saelwyn = request.form["saelwyn"]
            Players.saelwyn = saelwyn
            print("Saelwyn: " + saelwyn)
        if "kaelar" in request.form:
            kaelar = request.form["kaelar"]
            Players.kaelar = kaelar
            print("Kaelar: " + kaelar)
        if "owl" in request.form:
            owl = request.form["owl"]
            Players.owl = owl
            print("Owl: " + owl)

        if "enable_shanko" in request.form:
            if Enabled.shanko == 0:
                print("Enabled")
                Enabled.shanko = 1
            else:
                print("Disabled")
                Enabled.shanko = 0

        return render_template("index.html", content=Players, enabled=Enabled)
    else:
        return render_template("index.html", content="Testing")

        if __name__ == "__main__":
            app.run(debug=True)
