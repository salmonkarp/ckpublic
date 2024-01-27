from flask import *
from openpyxl import load_workbook
import os

#helper functions

#get image url from static folder
def get_image_url(product_name, images_folder):
    for filename in os.listdir(images_folder):
        if filename.startswith(product_name + ' #'):
            return os.path.join('images', filename)
    return None

#process all data from workbook before app is running
def process_excel_file():
    excel_file_path = 'static/products.xlsx'
    images_folder_path = 'static/images'
    wb = load_workbook(excel_file_path)
    sheet = wb['Signature']
    products_list = []

    for row in sheet.iter_rows(min_row=2, values_only=True):
        product_name, price, description = row
        image_url = get_image_url(product_name, images_folder_path)
        product_dict = {
            'name': product_name,
            'price': price,
            'description': description,
            'image_url': image_url
        }
        products_list.append(product_dict)

    return products_list

#get image url from cover folder
def get_all_cover_image_urls():
    cover_folder_path = 'static/cover'
    image_urls = []

    for filename in os.listdir(cover_folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image_urls.append(cover_folder_path + '/' + filename)

    return image_urls

app = Flask(__name__)

@app.route('/',methods=['GET'])
def root():
    cover_image_urls = get_all_cover_image_urls()
    print(cover_image_urls)
    return render_template('home.html', cover_image_urls = cover_image_urls)

@app.route('/signature',methods=['GET'])
def signature():
    return render_template('signature.html')


#TODO
# Informasi produk kurang lengkap, bisa ditambah:
# - Signature products: kastengel, nastar, sagu keju
# - Cookies: nastar, kastengel, sagu keju, lidah kucing, kenari, choco chip, dll
# - Hampers: lebaran, natal, chinese new year
# - Snack: soesring, mieting, almond crispy
# Ditambah menu sertifikasi yg kita punya: PIRT dan Halal
# Ditambah menu produk kita bisa dibeli dimana saja:
# - Store: Hoky, Ranch Market, Transmart, Lottemart, Chicco, Bilka, dll
# - Online: Grab, Gojek, Shopee, Tokopedia (kl bisa kl di klik bisa langsung link ke online shop kita)
# Contact us: ditambah IG & WA (kl di klik bisa langsung link ke IG/WA tsb)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)