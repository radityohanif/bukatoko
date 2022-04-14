from flask import Flask, request, jsonify, make_response
import requests
import json

app = Flask(__name__)
api_key = "34943098462755445d31e41f9fa7a8db"

@app.route("/", methods=["GET"])
def index():
    return "welcome to server 1"

@app.route("/provinsi", methods=["GET"])
def getProvinsi():
    dataRajaOngkir = requests.request("GET", "https://api.rajaongkir.com/starter/province", headers={"key":api_key})
    dataRajaOngkir = dataRajaOngkir.json()
    if dataRajaOngkir["rajaongkir"]["status"]["code"] != 200:
        return make_response(
            jsonify(dataRajaOngkir)
        )
    else: 
        return make_response(
            jsonify({
                "results" : dataRajaOngkir["rajaongkir"]["results"],
                "status" : 200
            })
        )

@app.route("/kota", methods=["GET"])
def getKota():
    dataRajaOngkir = requests.request("GET", "https://api.rajaongkir.com/starter/city", headers={"key":api_key})
    dataRajaOngkir = dataRajaOngkir.json()
    return make_response(
        jsonify(dataRajaOngkir)
    )

@app.route("/ongkir", methods=["POST"])
def getOngkir():
    dataPost = request.form.to_dict()
    dataAllowed = [
        "origin",
        "destination",
        "weight",
        "courier",
        "service"
    ]
    dataPostEmpty = list()
    dataPostValid = dict()
    for key in dataAllowed:
        if key in dataPost:
            if dataPost[key] == "":
                dataPostEmpty.append(key)
            else:
                dataPostValid[key] = dataPost[key]
        else:
            dataPostEmpty.append(key)
    
    # Validasi form yang belum diisi
    if len(dataPostEmpty) != 0:
        return make_response(
            jsonify({
                "status" : 400,
                "message" : "beberapa form data belum diisi",
                "empty_form" : dataPostEmpty
            })
        )
    
    else:
        # Request data ke API RajaOngkir
        dataRajaOngkir = requests.request(
            "POST", 
            "https://api.rajaongkir.com/starter/cost",
            headers={
                "key" : api_key
            },
            data=dataPostValid
        )
        dataRajaOngkir = dataRajaOngkir.json()

        # Validasi keberhasilan request data ke API RajaOngkir
        serviceList = list()
        if dataRajaOngkir["rajaongkir"]["status"]["description"] == "OK":        
            for data in dataRajaOngkir["rajaongkir"]["results"][0]["costs"]:
                serviceList.append(data["service"].lower())
                if data["service"].lower() == dataPostValid["service"].lower() :
                    dataCost = data

            # Service tidak tersedia
            if dataPostValid["service"] not in serviceList:
                return make_response(
                    jsonify({
                        "status" : 404,
                        "available_service" : serviceList,
                        "message" : f"paket pengiriman {dataPostValid['service']} tidak tersedia pada kurir {dataPostValid['courier']}"
                    })
                )
            
            # Service tersedia, berikan data ongkos kirim
            return make_response(
                jsonify({
                    "status" : 200,
                    "result" : {
                        "kurir" : dataPostValid["courier"],
                        "paket_pengiriman" : dataCost["description"],
                        "ongkos_kirim" : dataCost["cost"][0]["value"],
                        "estimasi_sampai" : dataCost["cost"][0]["etd"]
                    }
                })
            )
        else:
            return make_response(
                jsonify({
                    "status" : 200,
                    "message": "gagal request data ke API RajaOngkir",
                    "description" : dataRajaOngkir["rajaongkir"]["status"]["description"]
                })
            )

if __name__ == "__main__":
    app.run(port=5001, debug=True)