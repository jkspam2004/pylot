from system.core.router import routes

routes['default_controller'] = 'Logins'
routes['POST']['/users/register'] = 'Logins#register'
routes['POST']['/users/login'] = 'Logins#login'
routes['/success'] = 'Logins#success'
