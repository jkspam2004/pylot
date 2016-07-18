from system.core.controller import *

class Logins(Controller):
    def __init__(self, action):
        super(Logins, self).__init__(action)
        self.load_model('Login')

    def index(self):
        return self.load_view('index.html')

    # register: validates input 
    # if valid input, insert into db, and set session
    # redirects to index page if invalid input
    def register(self):
        user_info = {
            'first_name' : request.form.get('first_name', ''),
            'last_name'  : request.form.get('last_name', ''),
            'email'      : request.form.get('email', ''),
            'password'   : request.form.get('password', ''),
            'confirm_pw' : request.form.get('confirm_pw', ''),
        }
        create_status = self.models['Login'].create_user(user_info)
        if create_status['status'] == True:
            session['id'] = create_status['user']['id']
            session['name'] = create_status['user']['first_name']
            flash('Successfully registered!', 'success')
            return redirect('/success')
        else:
            for message in create_status['errors']:
                flash(message, 'error')
            return redirect('/')

    # login: validates input 
    # if valid input, insert into db, and set session
    # redirects to index page if invalid input
    def login(self):
        data = {
            'email' : request.form.get('email', ''),
            'password' : request.form.get('password', '')
        }
        login_status = self.models['Login'].login_user(data)
        print('login_status', login_status)
        if login_status['status'] == True:
            session['id'] = login_status['user']['id']
            session['name'] = login_status['user']['first_name']
            flash('Successfully logged in!', 'success')
            return redirect('/success')
        else: 
            for message in login_status['errors']:
                flash(message, 'error')
            return redirect('/')

    # prints success page
    def success(self):
        return self.load_view('success.html')
