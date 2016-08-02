from system.core.router import routes

routes['default_controller']           = 'FullFriends'                # default route
routes['/add']                         = 'FullFriends#add'            # display add page to add friend
routes['/show/<id>']                   = 'FullFriends#show'           # show one friend info
routes['/edit/<id>']                   = 'FullFriends#edit'           # display edit page for one friend
routes['/delete/<id>']                 = 'FullFriends#delete'         # confirmation page for delete
routes['POST']['/add_friend']          = 'FullFriends#add_friend'     # add one friend to db
routes['POST']['/update/<id>']         = 'FullFriends#update'         # update friend info
routes['POST']['/delete_confirm/<id>'] = 'FullFriends#delete_confirm' # send id for removing friend
