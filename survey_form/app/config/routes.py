from system.core.router import routes

routes['default_controller'] = 'Surveys'
routes['/result'] = 'Surveys#result'
routes['POST']['/surveys/process'] = 'Surveys#process'

