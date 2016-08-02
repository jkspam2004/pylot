from system.core.controller import *
import inspect

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('User')
        self.load_model('Book')
        self.load_model('Review')

    def trace(self):
        return __file__, inspect.stack()[1][2], inspect.stack()[1][3]

    def index(self):
        return self.load_view('index.html')

    # add: validates input 
    # if valid input, insert into db, and set session
    # redirects to index page if invalid input
    def add(self):
        create_status = self.models['User'].create_user(request.form)
        if create_status['status'] == False:
            for message in create_status['errors']:
                flash(message, 'error')
            return redirect('/')
        else:
            session['user_id'] = create_status['user']['id']
            session['alias'] = create_status['user']['alias']
            flash("Successfully registered!", "success")
            return redirect('/books')

    # login: validates input 
    # if valid input, insert into db, and set session
    # redirects to index page if invalid input
    def login(self):
        data = {
            'email' : request.form.get('email', ''),
            'password' : request.form.get('password', '')
        }
        login_status = self.models['User'].login_user(data)
        print('login_status', login_status)
        if login_status['status'] == False:
            for message in login_status['errors']:
                flash(message, 'error')
            return redirect('/')
        else: 
            session['user_id'] = login_status['user']['id']
            session['alias'] = login_status['user']['alias']
            flash('Successfully logged in!', 'success')
            print("session: ", session)
            return redirect('/books')

    # display user info
    def show(self, user_id):
        user = self.models['User'].get_user_by_id(user_id)
        reviews = self.models['Review'].get_reviews_by_user_id(user_id)
        print reviews, self.trace()
        user['review_count'] = len(reviews)
        return self.load_view('user.html', user=user, reviews=reviews)

    # logout: clears session
    def logout(self):
        session.clear()
        return redirect('/')

    ##### end of file ####
