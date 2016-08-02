from system.core.router import routes

routes['default_controller']                        = 'Users'
routes['POST']['/users/add']                        = 'Users#add'            # process registering new user
routes['POST']['/users/login']                      = 'Users#login'          # process login
routes['/logout']                                   = 'Users#logout'         # logout
routes['/users/<user_id>']                          = 'Users#show'           # display user page
routes['/books']                                    = 'Books#show'           # display recent book reviews page
routes['/books/add']                                = 'Books#add'            # display add new book page
routes['POST']['/books/create']                     = 'Books#create'         # process adding new book
routes['/books/<book_id>']                          = 'Books#review'         # display book info page
routes['POST']['/books/add_review']                 = 'Books#add_review'     # process adding book review
routes['/books/delete/<review_id>']                 = 'Books#delete'         # display confirmation for delete review
routes['POST']['/books/confirm_delete/<review_id>'] = 'Books#confirm_delete' # process review delete


