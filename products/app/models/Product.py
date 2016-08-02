from system.core.model import *
import re

class Product(Model):
    def __init__(self):
        super(Product, self).__init__()

    def get_products(self):
        query = "SELECT * FROM products"
        return self.db.query_db(query)

    def create_product(self, args):
        errors = self.validate_input(args)
        if errors:
            return { 'status' : False, 'errors' : errors }
        else:
            return { 'status' : True, 'result' : self.do_insert(args) }

    def get_product_by_id(self, id):
        query = "SELECT * FROM products WHERE id = :id"
        result = self.db.query_db(query, { 'id' : id })
        return result[0]

    def update_product(self, args):
        errors = self.validate_input(args)
        if errors:
            return { 'status' : False, 'errors' : errors }
        else:
            return { 'status' : True, 'result': self.do_update(args) }

    def remove_product(self, id):
        query = "DELETE FROM products WHERE id = :id"
        return self.db.query_db(query, { 'id' : id })

    ### Helper functions ###    

    def do_insert(self, data):   
        query = "INSERT INTO products (name, description, price, created_at, updated_at) \
            VALUES (:name, :description, :price, NOW(), NOW())"
        return self.db.query_db(query, data)

    def do_update(self, data):
        query = "UPDATE products SET name = :name, description = :description, price = :price, \
            updated_at = NOW() WHERE id = :id"
        return self.db.query_db(query, data)

    def validate_input(self, data):
        errors = []
        if not data['name']:
            errors.append("Enter product name")
        if not data['description']:
            errors.append("Enter a description")
        if not data['price']:
            errors.append("Enter a price")
        elif not re.match(r'^[0-9]*\.[0-9]{2}$', data['price']): 
            errors.append("Invalid price. Enter a valid number with 2 digits after decimal point ")
        else:
            print("type of price before converting: ", type(data['price']))
            data['price'] = float(data['price'])
        return errors
   

