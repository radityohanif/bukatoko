from flask import Flask, request, jsonify, make_response
import requests
import json

app = Flask(__name__)
server1 = "http://127.0.0.1:5001"
server2 = "http://127.0.0.1:5002"

@app.route("/", methods=["GET"])
def index():
    return "welcome to server 3"

@app.route("/order", methods=["POST"])
def order():
    dataPost = request.form.to_dict()
    dataAllowed = [
        "id_produk",
        "jumlah_pembelian",
        "id_kota",
        "kurir",
        "paket_pengiriman"
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
    
    # ========================================
    # Request data produk ke server 2
    dataProduk = requests.request("GET", f"{server2}/produk/{dataPostValid['id_produk']}")
    dataProduk = dataProduk.json()
    # Jika id produk tidak ditemukan
    if dataProduk["status"] != 200:
        return make_response(jsonify(dataProduk))
    # Jika id produk ditemukan
    dataProduk = dataProduk["result"]
    
    # ========================================
    # Request data id_kota penjual ke server 2
    dataKota = requests.request("GET", f"{server2}/penjual/{dataProduk['id_penjual']}")
    dataKota = dataKota.json()
    # Jika id produk tidak ditemukan
    if dataKota["status"] != 200:
        return make_response(jsonify(dataKota))
    # Jika id produk ditemukan
    dataProduk["id_kota_penjual"] = dataKota["result"]["id_kota"]

    # ========================================
    # Request data ongkos kirim ke server 1
    dataOngkir = requests.request(
        "POST", 
        f"{server1}/ongkir",
        data={
            "origin" : dataProduk["id_kota_penjual"],
            "destination" : dataPostValid["id_kota"],
            "weight" : dataProduk["berat"],
            "courier" : dataPostValid["kurir"],
            "service" : dataPostValid["paket_pengiriman"]
        }
    )    
    dataOngkir = dataOngkir.json()
    # Jika request gagal
    if dataOngkir["status"] != 200:
        return make_response(
            jsonify(dataOngkir)
        )
    dataOngkir = dataOngkir["result"]
    
    # ========================================
    # Mempersiapkan format akhir respon 
    total_harga = dataOngkir["ongkos_kirim"] + (int(dataProduk["harga"]) * int(dataPostValid["jumlah_pembelian"]) * 1000.0)
    return make_response(
        jsonify({
            "status" : 200,
            "result" : {
                "total_harga" : total_harga,
                "jumlah_pembelian" : dataPostValid["jumlah_pembelian"],
                "detail" : {
                    "produk" : dataProduk,
                    "ongkos kirim" : dataOngkir
                }
            }
        })
    )
    

if __name__ == "__main__":
    app.run(port=5003, debug=True)