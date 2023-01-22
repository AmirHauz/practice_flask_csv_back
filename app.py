import csv
import json

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
MY_FILE='Products_Data.csv'
def load_data():
    json_data = []
    with open(MY_FILE, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            json_data.append(row)
        return json_data

def get_headers():
    with open(MY_FILE, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        return next(csv_reader)

@app.route('/product', methods=['POST'])
def new_product():
    data = request.get_json()   # request data as dict
    existing_data_array = load_data()   # 
    existing_data_array.append(data)
    row = []
    headers = get_headers()
    for l in headers:
        row.append(data[l])
    
    with open(MY_FILE, 'a') as f:
       writer = csv.writer(f)
       writer.writerow(row)

    return data



@ app.route('/product', methods=['GET'])
@ app.route('/product/<int:product_id>', methods=['GET'])
def read_product(product_id = -1):
    json_data = load_data()
    if (product_id == -1):
        return json_data
    else:
        for x in json_data:
            if int(x['pid']) == product_id:
                return x
        return {"msg": "not such product "}



@app.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    json_data = load_data()
    input_data = request.get_json()   
    product_found = False
    for product in json_data:
        if (str(product_id) == product['pid']):
            product_found = True
            product.update(input_data)
            break
    if not product_found: 
        return {"msg": "no such product "}
    headers = get_headers()
    with open(MY_FILE, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(json_data)
    return input_data


@app.route('/product/<int:product_id>', methods=['DELETE'])
def delete_worker(product_id):
    json_data = load_data()
    index = 0
    for product in json_data:
        if (str(product_id) == product['pid']):
            json_data.pop(index)
            break
        else:
            index = index + 1

    headers = get_headers()
    with open(MY_FILE, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(json_data)

    return jsonify({'message': product['pid']})



if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)