from flask import Flask, redirect, render_template, url_for, request, session

app = Flask(__name__)
app.secret_key = "hello"


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
    session['players'] = Players.to_json
    session['enabled'] = Enabled

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
        if "tree" in request.form:
            tree = request.form["tree"]
            Players.tree = tree
            print("Tree: " + tree)
        if "gith" in request.form:
            gith = request.form["gith"]
            Players.gith = gith
            print("Gith: " + gith)
        if "otadus" in request.form:
            otadus = request.form["otadus"]
            Players.otadus = otadus
            print("Otadus: " + otadus)
        if "mon1" in request.form:
            mon1 = request.form["mon1"]
            Players.mon1 = mon1
            print("Monster 1: " + mon1)
        if "mon2" in request.form:
            mon2 = request.form["mon2"]
            Players.mon2 = mon2
            print("Monster 2: " + mon2)
        if "mon3" in request.form:
            mon3 = request.form["mon3"]
            Players.mon3 = mon3
            print("Monster 3: " + mon3)
        if "mon4" in request.form:
            mon4 = request.form["mon4"]
            Players.mon4 = mon4
            print("Monster 4: " + mon4)
        if "mon5" in request.form:
            mon5 = request.form["mon5"]
            Players.mon5 = mon5
            print("Monster 5: " + mon5)
        if "mon6" in request.form:
            mon6 = request.form["mon6"]
            Players.mon6 = mon6
            print("Monster 6: " + mon6)
        if "mon7" in request.form:
            mon7 = request.form["mon7"]
            Players.mon7 = mon7
            print("Monster 7: " + mon7)

        if "enable_shanko" in request.form:
            if Enabled.shanko == 0:
                print("Enabled")
                Enabled.shanko = 1
            else:
                print("Disabled")
                Enabled.shanko = 0
        if "enable_saelwyn" in request.form:
            if Enabled.saelwyn == 0:
                print("Enabled")
                Enabled.saelwyn = 1
            else:
                print("Disabled")
                Enabled.saelwyn = 0
        if "enable_kaelar" in request.form:
            if Enabled.kaelar == 0:
                print("Enabled")
                Enabled.kaelar = 1
            else:
                print("Disabled")
                Enabled.kaelar = 0
        if "enable_owl" in request.form:
            if Enabled.owl == 0:
                print("Enabled")
                Enabled.owl = 1
            else:
                print("Disabled")
                Enabled.owl = 0
        if "enable_tree" in request.form:
            if Enabled.tree == 0:
                print("Enabled")
                Enabled.tree = 1
            else:
                print("Disabled")
                Enabled.tree = 0
        if "enable_gith" in request.form:
            if Enabled.gith == 0:
                print("Enabled")
                Enabled.gith = 1
            else:
                print("Disabled")
                Enabled.gith = 0
        if "enable_otadus" in request.form:
            if Enabled.otadus == 0:
                print("Enabled")
                Enabled.otadus = 1
            else:
                print("Disabled")
                Enabled.otadus = 0
        if "enable_mon1" in request.form:
            if Enabled.mon1 == 0:
                print("Enabled")
                Enabled.mon1 = 1
            else:
                print("Disabled")
                Enabled.mon1 = 0
        if "enable_mon2" in request.form:
            if Enabled.mon2 == 0:
                print("Enabled")
                Enabled.mon2 = 1
            else:
                print("Disabled")
                Enabled.mon2 = 0
        if "enable_mon3" in request.form:
            if Enabled.mon3 == 0:
                print("Enabled")
                Enabled.mon3 = 1
            else:
                print("Disabled")
                Enabled.mon3 = 0
        if "enable_mon4" in request.form:
            if Enabled.mon4 == 0:
                print("Enabled")
                Enabled.mon4 = 1
            else:
                print("Disabled")
                Enabled.mon4 = 0
        if "enable_mon5" in request.form:
            if Enabled.mon5 == 0:
                print("Enabled")
                Enabled.mon5 = 1
            else:
                print("Disabled")
                Enabled.mon5 = 0
        if "enable_mon6" in request.form:
            if Enabled.mon6 == 0:
                print("Enabled")
                Enabled.mon6 = 1
            else:
                print("Disabled")
                Enabled.mon6 = 0
        if "enable_mon7" in request.form:
            if Enabled.mon7 == 0:
                print("Enabled")
                Enabled.mon7 = 1
            else:
                print("Disabled")
                Enabled.mon7 = 0

        return render_template("index.html", content=Players, enabled=Enabled)
    else:
        return render_template("index.html", content="Testing")

        if __name__ == "__main__":
            app.run(debug=True)
