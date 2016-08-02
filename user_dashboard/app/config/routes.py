from system.core.router import routes

routes['default_controller']       = 'Users'
routes['/logout']                  = 'Users#logout'          # process logout
routes['/signin']                  = 'Users#signin'          # display login page
routes['/register']                = 'Users#register'        # display register page
routes['/dashboard/admin']         = 'Users#dashboard_admin' # display dashboard page for admin
routes['/dashboard']               = 'Users#dashboard'       # display dashboard page
routes['/users/new']               = 'Users#new'             # display add new user page (admin only)
routes['/users/edit']              = 'Users#edit_profile'    # display edit profile page
routes['/users/edit/<user_id>']    = 'Users#edit_user'       # display edit specific user page
routes['/users/delete/<user_id>']  = 'Users#delete'          # display page to confirm delete
routes['/users/show/<user_id>']    = 'Users#show'            # display page to add posts and comments
routes['POST']['/users/login']                    = 'Users#login'              # process logging in user
routes['POST']['/users/signup']                   = 'Users#signup'             # process registering user
routes['POST']['/users/create']                   = 'Users#create'             # create the user (admin only)
routes['POST']['/users/update_user']              = 'Users#update_user'        # process edit user 
routes['POST']['/users/update_password']          = 'Users#update_password'    # process edit password 
routes['POST']['/users/update_description']       = 'Users#update_description' # process edit description 
routes['POST']['/users/confirm_delete/<user_id>'] = 'Users#confirm_delete'     # process user delete 
routes['POST']['/messages/post']                  = 'Messages#post'            # process adding message post
routes['POST']['/messages/comment']               = 'Messages#comment'         # process adding comment

