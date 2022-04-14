from database import *
import requests
import random

jumlah_kota = 501 #sumber https://api.rajaongkir.com/starter/city

def get_random_name():
    data = requests.request("GET", "https://api.namefake.com/")
    data = data.json()
    return data["name"]

def get_random_product(index):
    data = requests.request("GEt", f"https://fakestoreapi.com/products/{index}")
    data = data.json()
    return data

def seed_table_penjual(jumlah_data=10):
    for i in range(jumlah_data):
        data = dict()
        data["nama"] = get_random_name()
        data["id_kota"] = random.randint(1, jumlah_kota)
        print(data) #preview seed data
        insertData("penjual", data)

def seed_table_produk(jumlah_data=19):    
    jumlahPenjual = rowCount(query="SELECT * FROM penjual")
    for i in range(jumlah_data):
        dataProduk = get_random_product(index=i+1)
        data = dict()
        data["id_penjual"]  = random.randint(1, jumlahPenjual)
        data["nama"]        = dataProduk["title"]
        data["harga"]       = dataProduk["price"]
        data["berat"]       = random.randrange(100, 1000)
        data["stok"]        = random.randint(10, 250)
        data["gambar"]      = dataProduk["image"]
        data["deskripsi"]   = dataProduk["description"]
        print(data) #preview seed data
        insertData("produk", data)

# kode ini digunakan untuk membuat data secara otomatis pada database secara random
# seed_table_penjual(10)
# seed_table_produk()