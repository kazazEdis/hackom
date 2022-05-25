from urllib import response
from flask import Flask, render_template, request, make_response, jsonify, send_file
import hakom
import pandas, io, json
from flask_sslify import SSLify

app = Flask(__name__)
#sslify = SSLify(app)


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


@app.route("/json_to_xlsx", methods=["POST"])
def json_to_xlsx():
    if request.method == "POST":
        mnp_results = request.form.get("mnp_results")
        df = pandas.DataFrame.from_dict(json.loads(mnp_results))
       	df.drop('Success', axis=1, inplace=True)
        out = io.BytesIO()
        df.to_excel(out, index=False, sheet_name='Sheet1')
        out.seek(0)
        return send_file(out, as_attachment=True, download_name="mnp_results.xlsx")
  

         

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=False
    )
