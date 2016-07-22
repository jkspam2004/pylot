from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('User')
        self.load_model('Quote')

    def index(self):
        return redirect('/main')

    def main(self):
        return self.load_view('index.html')

    # add: validates input 
    # if invalid input, redirect to index page
    # if valid input, insert into db, set session and redirect to
    def add(self):
        print("add")
        create_status = self.models['User'].create_user(request.form)
        print("create_status: ", create_status)
        if create_status['status'] == False:
            for message in create_status['errors']:
                flash(message, 'error')
            return redirect('/main')
        else:
            session['user_id'] = create_status['user']['id']
            session['alias'] = create_status['user']['alias']
            flash("Successfully registered!", "success")
            return redirect('/quotes')

    # login: validates input 
    # if invalid input, redirect to index page 
    # if valid input, insert into db, set session and redirect to
    def login(self):
        data = {
            'email'    : request.form.get('email', ''),
            'password' : request.form.get('password', '')
        }
        login_status = self.models['User'].login_user(data)
        if login_status['status'] == False:
            for message in login_status['errors']:
                flash(message, 'error')
            return redirect('/')
        else: 
            session['user_id'] = login_status['user']['id']
            session['alias'] = login_status['user']['alias']
            flash('Successfully logged in!', 'success')
            print("session: ", session)
            return redirect('/quotes')

    # logout: clears the session
    def logout(self):
        session.clear()
        return redirect('/main')

    # show: display page of quotes posted by user (from GET method)
    def show(self, user_id):
        user = self.models['User'].get_user_by_id(user_id)
        if not user:
            # maybe someone manually entered user)id into url and user does not exist 
            # redirect to dashboard
            return redirect('/quotes')

        quotes = self.models['Quote'].get_quotes_by_id(user_id) 
        count = len(quotes)
        return self.load_view('user.html', quotes=quotes, user=user[0], count=count)


