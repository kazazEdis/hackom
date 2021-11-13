from flask import Flask, render_template, request
import hakom
# from flask_sslify import SSLify

app = Flask(__name__)
# sslify = SSLify(app)


@app.route("/", methods=["GET","POST"])
def hackom():
    if request.method == "POST":
        msisdn = request.form.get("msisdn")
        if len(msisdn) >= 10:
            results = hakom.operator(msisdn)
            return render_template("mnp_results.html", results = results)
    else:
        return render_template("mnp.html")


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)
