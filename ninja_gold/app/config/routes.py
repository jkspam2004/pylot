from system.core.router import routes

routes['default_controller'] = 'NinjaGolds'
routes['POST']['/reset'] = 'NinjaGolds#reset'
routes['POST']['/process_money'] = 'NinjaGolds#process_money'
