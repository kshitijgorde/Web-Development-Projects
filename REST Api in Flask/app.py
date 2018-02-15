from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# Every Resource has to be a class
items = []
class Item(Resource):
    def get(self, name):
        #Iterate over the items and return the one with matching name
        item = next(filter(lambda x:x['name']==name, items), None) # None: to handle empty item list
        return {'item':item}, 200 if item is not None else 404

    def post(self, name):
        #Put will create a new resource and add it
        #First check if item already exists
        if next(filter(lambda x:x['name']==name, items), None):
            return {'message':'An item with same name already exists'}, 400 #Bad request
        data = request.get_json()
        item = {'name':name, 'price':data['price']}
        items.append(item)
        return item, 201

class ItemList(Resource):
    def get(self):
        return {'items':items}


api.add_resource(Item, '/items/<string:name>')
api.add_resource(ItemList, '/items')
app.run(port=5000, debug=True)