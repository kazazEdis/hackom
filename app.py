from flask import Flask, render_template, request
import hakom
# from flask_sslify import SSLify

app = Flask(__name__)
# sslify = SSLify(app)


@app.route("/", methods=["GET","POST"])
def hackom():
    if request.method == "POST":
        results = hakom.operator(request.form.get("msisdn"))
        # return make_response(jsonify(operator), 200)
        return render_template("mnp_results.html", results = results)

    else:
        return render_template("mnp.html")


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)
