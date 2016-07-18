from system.core.router import routes

routes['default_controller'] = 'Courses'
routes['/courses/destroy/<id>'] = 'Courses#confirm_delete'
routes['POST']['/courses/delete_confirmed/<id>'] = 'Courses#delete'
routes['POST']['/courses/add'] = 'Courses#add'
