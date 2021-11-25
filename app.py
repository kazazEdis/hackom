from flask import Flask, render_template, request, make_response, jsonify
import hakom
import json
from flask_sslify import SSLify

app = Flask(__name__)
# sslify = SSLify(app)


@app.route("/", methods=["GET", "POST"])
def hackom():
    if request.method == "POST":
        msisdn = request.form.get("msisdn")

        if len(msisdn) == 0:
            return render_template("mnp_results.html", results=[{"Success": False, "Reason": "Please enter MSISDN!"}])

        elif "," in msisdn:
            return render_template("mnp_results.html", results=hakom.batch_operator(msisdn))

        else:
            return render_template("mnp_results.html", results=hakom.operator(msisdn))

    else:
        return render_template("mnp.html")


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False
    )
