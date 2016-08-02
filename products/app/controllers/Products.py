from system.core.controller import *

class Products(Controller):
    def __init__(self, action):
        super(Products, self).__init__(action)
        self.load_model('Product')

    # display all the products with options to show, edit, remove, and add new product
    def index(self):
        products = self.models['Product'].get_products()
        return self.load_view('index.html', products=products)

    # add a new product
    def new(self):
        return self.load_view('new.html') 

    # display edit page for one product
    def edit(self, product_id):
        product = self.models['Product'].get_product_by_id(product_id)
        return self.load_view('edit.html', product=product)

    # show info for one product
    def show(self, product_id):
        product = self.models['Product'].get_product_by_id(product_id)
        return self.load_view('show.html', product=product)

    # add one product to our database
    def create(self):
        data = {
            'name'       : request.form.get('name', ''),
            'description': request.form.get('description', ''),
            'price'      : request.form.get('price', 0)
        }
        create_status = self.models['Product'].create_product(data)
        if create_status['status'] == False:
            for error in create_status['errors']:
                flash(error, 'error')
            return redirect('/products/new')
        return redirect('/') 

    # remove one product from our database
    def destroy(self, product_id):
        destroy_status = self.models['Product'].remove_product(product_id)
        return redirect('/')

    # update one product
    def update(self, product_id):
        data = {
            'name'        : request.form.get('name', ''),
            'description' : request.form.get('description', ''),
            'price'       : request.form.get('price', 0),
            'id'          : product_id
        }
        update_status = self.models['Product'].update_product(data)
        if update_status['status'] == False:
            for error in update_status['errors']:
                flash(error, 'error')
            return redirect('/products/edit/' + product_id) 
        return redirect('/')

