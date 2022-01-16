from flask import Flask, jsonify, request

stores = [
    {
        'name': 'My Wonderfull Store',
        'items': [
            {
                'name': 'Axe',
                'price': 23.50
            }
        ]
    }
]

app = Flask(__name__)

#POST - used to receive data
#GET - used to send data back only

#POST /store data: {name:}
@app.route('/store', methods = ['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': request_data['items']
    }
    stores.append(new_store)
    return jsonify(new_store)

#GET /store/<string:name>
@app.route('/store/<string:name>', methods = ['GET'])
def get_store(name):
    for store in stores:
        print(store.get('name'))
        if(store.get('name') == name):
            print("Store found")
            return jsonify(store)
    return jsonify({'message': 'No such store available.'})

#GET /store
@app.route('/store', methods = ['GET'])
def get_all_stores():
    return jsonify({'stores': stores})

#POST /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods = ['POST'])
def create_item_for_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            store['items'] = store['items'] + [request_data]
            return jsonify(request_data)
    return jsonify({'message': 'No such store available.'})

#GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_items_for_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': 'No such store available.'})


#start server
app.run(port = 5000)