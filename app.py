from flask import *
from openpyxl import load_workbook
from PIL import Image
import os

#helper functions ========================================

#get image url from static folder
def get_image_url(product_name, images_folder):
    images_url_array = []
    for filename in os.listdir(images_folder):
        if filename.startswith(product_name + '@'):
            images_url_array.append('static/images/' + filename) 
    return images_url_array

#process all data from workbook before app is running
def process_excel_file():
    excel_file_path = 'static/products.xlsx'
    images_folder_path = 'static/images'
    wb = load_workbook(excel_file_path)
    sheet = wb['Products']
    products_list = []
    counter = 0
    for row in sheet.iter_rows(min_row=2, values_only=True):
        product_name, price, description = row
        image_url = get_image_url(product_name, images_folder_path)
        product_dict = {
            'id':counter,
            'name': product_name,
            'price': price,
            'description': description,
            'image_url': image_url
        }
        products_list.append(product_dict)
        counter += 1
    
    sheet = wb['Hampers']
    hampers_list = []
    counter = 0
    for row in sheet.iter_rows(min_row=2, values_only=True):
        product_name, price, description = row
        image_url = get_image_url(product_name, images_folder_path)
        product_dict = {
            'id':counter,
            'name': product_name,
            'price': price,
            'description': description,
            'image_url': image_url
        }
        hampers_list.append(product_dict)
        counter += 1
        
    sheet = wb['Snacks']
    snacks_list = []
    counter = 0
    for row in sheet.iter_rows(min_row=2, values_only=True):
        product_name, price, description = row
        image_url = get_image_url(product_name, images_folder_path)
        product_dict = {
            'id':counter,
            'name': product_name,
            'price': price,
            'description': description,
            'image_url': image_url
        }
        snacks_list.append(product_dict)
        counter += 1
        
    sheet = wb['Signature']
    signature_list = []
    counter = 0
    for row in sheet.iter_rows(min_row=2, values_only=True):
        product_name, price, description = row
        image_url = get_image_url(product_name, images_folder_path)
        product_dict = {
            'id':counter,
            'name': product_name,
            'price': price,
            'description': description,
            'image_url': image_url
        }
        signature_list.append(product_dict)
        counter += 1

    return products_list, hampers_list, snacks_list, signature_list

#get image url from cover folder
def get_all_cover_image_urls():
    cover_folder_path = 'static/cover'
    image_urls = []

    for filename in os.listdir(cover_folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image_urls.append(cover_folder_path + '/' + filename)

    return image_urls

#process too high quality of an image
def process_image(image_path):
    img = Image.open(image_path)
    desired_quality = 50
    
    processed_image_path = f"static/processed/processed_{image_path.split('\\')[-1]}"
    img.save(processed_image_path, format='JPEG', quality=desired_quality)
    return processed_image_path

#jinja format currency
def format_currency(value):
    formatted_currency = "Rp {:,.0f}".format(value).replace(",", ".")
    return formatted_currency

#end of helper functions =================================



#global environments =====================================
app = Flask(__name__)
cover_image_urls = get_all_cover_image_urls()
products_list, hampers_list, snacks_list, signatures_list = process_excel_file()
app.jinja_env.filters['format_currency'] = format_currency

#end of global environments===============================


#image processing routes==================================
@app.route('/static/images/<filename>')
def serve_image(filename):
    image_path = os.path.join('static', 'images', filename)
    max_file_size = 1 * 1024 * 1024
    print(image_path)
    if os.path.getsize(image_path) > max_file_size:
        processed_image_path = process_image(image_path)
    else:
        processed_image_path = image_path
    return send_file(processed_image_path)

@app.route('/static/cover/<filename>')
def serve_cover_image(filename):
    image_path = os.path.join('static', 'cover', filename)
    max_file_size = 2 * 1024 * 1024
    print(image_path)
    if os.path.getsize(image_path) > max_file_size:
        processed_image_path = process_image(image_path)
    else:
        processed_image_path = image_path
    return send_file(processed_image_path)

#end of image processing routes===========================



#
@app.route('/',methods=['GET'])
def root():
    return render_template('home.html', cover_image_urls = cover_image_urls)

@app.route('/products',methods=['GET'])
def signature():
    option = request.args.get('option','cookies')
    cover_image_urls = get_all_cover_image_urls()
    return render_template('products.html',products_list = products_list, hampers_list = hampers_list, snacks_list = snacks_list, signatures_list = signatures_list, option=option, cover_image_urls = cover_image_urls)

@app.route('/wheretobuy',methods=['GET'])
def wheretobuy():
    return render_template('wheretobuy.html')

@app.route('/contactus',methods=['GET'])
def contactus():
    return render_template('contactus.html')


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