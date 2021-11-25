import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import json
from time import sleep
import tensorflow as tf
import model as m

model, prediction_model = m.build_model()
model.load_weights('my_model.hdf5')


def ocr():
    dataset = tf.data.Dataset.from_tensor_slices((['test.jpeg'], None))
    dataset = (
        dataset.map(m.encode_single_sample,
                    num_parallel_calls=tf.data.AUTOTUNE)
        .batch(16)  # batch size
        .prefetch(buffer_size=tf.data.AUTOTUNE)
    )

    out = prediction_model.predict(dataset)
    out = m.decode_batch_predictions(out, 6)  # max length = 6

    return out[0]


def reformat_phone_number(phone_number: str):
    phone_number = str(phone_number)
    while phone_number[0] == "0":
        phone_number = phone_number.lstrip("0")

    if not phone_number.startswith("385"):
        phone_number = "385" + phone_number

    return phone_number


def operator(phone_number):
    phone_number = reformat_phone_number(str(phone_number))

    try:
        session = requests.session()
        response = session.get('https://app.hakom.hr/captcha.aspx')
        if response.status_code != 200:
            raise Exception(f'Returned status code {response.status_code}')
        with open('test.jpeg', 'wb') as file:
            file.write(response.content)

        url = "https://app.hakom.hr/default.aspx?id=62&iframe=yes"
        captcha = ocr()
        payload = f'brojTel={phone_number}&cp={captcha}&iframe=yes&sto=prijenosBroja'
        headers = {
            'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        }

        response = session.request(
            "POST", url, headers=headers, data=payload)

        soup = BeautifulSoup(response.text, 'html.parser')

        try:
            results = soup.find_all("td")

            if len(results[0].text) == 0:
                return [{"Success": False, "Reason": f"Invalid MSISDN: {phone_number} !"}]

            results = [{"Success": True, "Operator": results[0].text,
                        "Broj": results[1].text, "Status": results[2].text}]
            return results

        except Exception:
            status = soup.find(id="brojRez").text
            timeout = "Molimo pokušajte ponovo za 1 minutu..."
            bad_captcha = "Greška, provjerite unos kontrolne vrijednosti"
            if status == bad_captcha:
                return operator(phone_number)

            elif status == timeout:
                sleep(60)
                return operator(phone_number)

    except ConnectionError:
        return [{"Success": False, "Reason": "ConnectionError. Are you online?"}]

    except Exception as e:
        return [{"Success": False, "Reason": e}]


def batch_operator(phone_numbers: str):
    phone_numbers = json.loads("[" + phone_numbers + "]")
    preneseno = open('preneseno.json', "r")
    preneseno = json.load(preneseno)
    telemach = "Telemach Hrvatska d.o.o."
    statuses = {
        "completed": "Broj je prenesen",
        "gave_up": "Zahtjev za prijenos broja je napušten, broj nije u postupku prijenosa",
        "in_process": "Zahtjev za prijenos broja je otvoren, broj je u postupku prijenosa",
        "accepted": "Zahtjev za prijenos broja je prihvaćen, broj je u postupku prijenosa",
        "not_in_transfer": "Broj nije u postupku prijenosa"
    }

    results = []
    for i in phone_numbers:
        if i not in preneseno:
            res = operator(i)[0]
            res_broj = res.get("Broj")
            res_status = res.get("Status")
            res_operator = res.get("Operator")
            if res_operator != None:
                if res_operator != telemach or res_status == statuses.get("gave_up"):
                    results.append(res)

                else:
                    preneseno.append(int(res_broj))

            elif res_operator == None:
                results.append(res)


    with open("preneseno.json", "w") as f:
        json.dump(preneseno, f)

    return results
