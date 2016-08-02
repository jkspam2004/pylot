from system.core.router import routes

routes['default_controller'] = 'Products'
routes['/products/new'] = 'Products#new'
routes['/products/show/<product_id>'] = 'Products#show'
routes['/products/edit/<product_id>'] = 'Products#edit'
routes['POST']['/products/create'] = 'Products#create'
routes['POST']['/products/destroy/<product_id>'] = 'Products#destroy'
routes['POST']['/products/update/<product_id>'] = 'Products#update'
