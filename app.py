from flask import Flask, render_template, request, make_response, jsonify
import hakom
import json
# from flask_sslify import SSLify

app = Flask(__name__)
# sslify = SSLify(app)


@app.route("/", methods=["GET", "POST"])
def hackom():
    batch = request.form.get("batch")
    if request.method == "POST":
        msisdn = request.form.get("msisdn")
        if batch != None:
            results = hakom.batch_operator(msisdn)
            return render_template("mnp_results.html", results=results)

        if len(msisdn) >= 10:
            results = hakom.operator(msisdn)
            return render_template("mnp_results.html", results=results)

    else:
        return render_template("mnp.html")


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False
    )
