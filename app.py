""" Entrypoint file """
import io
import json

import pandas
from flask import Flask, render_template, request, send_file
# from flask_sslify import SSLify

import hakom

APP = Flask(__name__)
#sslify = SSLify(APP)



@APP.route("/", methods=["GET", "POST"])
def hackom():
    """ Get the data from the form and send it to the hakom module """
    if request.method == "POST":
        msisdn = request.form.get("msisdn")

        if len(msisdn) == 0:
            return render_template("mnp_results.html", results=[
                {"Success": False, "Reason": "Please enter MSISDN!"}
                ])

        if "," in msisdn:
            return render_template("mnp_results.html", results=hakom.batch_operator(msisdn))

        return render_template("mnp_results.html", results=hakom.operator(msisdn))

    return render_template("mnp.html")


@APP.route("/json_to_xlsx", methods=["POST"])
def json_to_xlsx():
    """ Convert the json data to an xlsx file """
    mnp_results = request.form.get("mnp_results")
    data_frame = pandas.DataFrame.from_dict(json.loads(mnp_results))
    data_frame.drop("Success", axis=1, inplace=True)
    out = io.BytesIO()
    data_frame.to_excel(out, index=False, sheet_name="Sheet1")
    out.seek(0)
    return send_file(out, as_attachment=True, download_name="mnp_results.xlsx")




if __name__ == "__main__":
    APP.run(
        host="0.0.0.0",
        port=8080,
        debug=False
    )
