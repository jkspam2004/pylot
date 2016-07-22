from system.core.router import routes

routes['default_controller']                      = 'Users'
routes['/index']                                  = 'Users#index'      # main page
routes['/main']                                   = 'Users#main'       # main page
routes['/logout']                                 = 'Users#logout'     # logout
routes['/users/<user_id>']                        = 'Users#show'       # display page of posted quotes by user
routes['/quotes']                                 = 'Quotes#show'      # display page of quotes and my favorites
routes['POST']['/users/add']                      = 'Users#add'        # process registering new user
routes['POST']['/users/login']                    = 'Users#login'      # process login
routes['POST']['/quotes/add/<poster_id>']         = 'Quotes#add'       # process adding a quote
routes['POST']['/quotes/move_to/<quote_id>']      = 'Quotes#move_to'   # process moving a quote to favorites
routes['POST']['/quotes/move_from/<favorite_id>'] = 'Quotes#move_from' # process moving a quote from favorites

