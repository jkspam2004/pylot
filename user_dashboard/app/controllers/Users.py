from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('User')
        self.load_model('Message')
   
    # home page 
    def index(self):
        return self.load_view("index.html")

    # clear session upon logout
    def logout(self):
        session.clear()
        return redirect('/')

    # display signin page
    def signin(self):
        if 'user_id' in session:
            if 'admin' in session:
                return redirect("/dashboard/admin")
            else:
                return redirect("/dashboard")
        return self.load_view("signin.html")

    # process logging in the user
    def login(self):
        login_status = self.models['User'].login_user(request.form) 
        if login_status['status']:
            session['user_id'] = login_status.get('user')['id']
            session['admin'] = 1 if login_status.get('user')['user_level'] == 9 else 0
            session['name'] = login_status.get('user')['first_name']
            print("session user_id:", session.get('user_id'))
            print("session admin:", session.get('admin'))
            if session.get('admin') == 1:
                return redirect("/dashboard/admin")
            else:
                return redirect("/dashboard")
        else: 
            for error in login_status.get('errors'):
                flash(error, "error")
            return redirect("/signin")

    # dislay registration page
    def register(self):
        print("register")
        return self.load_view("register.html")

    # process registration signup
    def signup(self):
        print("signup")
        reg_status = self.models['User'].create_user(request.form)
        if reg_status.get('status') == True:
            session['user_id'] = reg_status.get('user')['id']
            session['admin'] = 1 if reg_status.get('user')['user_level'] == 9 else 0
            session['name'] = reg_status.get('user')['first_name']
            if session.get('admin') == 1:
                return redirect("/dashboard/admin")
            else:
                return redirect("/dashboard")
        else:
            for error in reg_status.get('errors'):
                flash(error, "error")
            return redirect("/register")

    # user and admin dashboard use the same template 
    # template will check for session admin to display or "hide" certain features
    def dashboard_admin(self):
        # non-admin getting here by entering url redirects to user dashboard
        if not session.get('admin'):
            return redirect('/dashboard')
        return self.dashboard()
      
    # dashboard
    def dashboard(self):
        users = self.models['User'].get_all_users()
        for user in users:
            user['level'] = 'admin' if user.get('user_level') == 9 else 'normal'
        return self.load_view("dashboard.html", users=users)

    # display add new user page (admin only)
    def new(self):
        # non-admin getting here by entering url redirects to user dashboard
        if not session.get('admin'):
            return redirect('/dashboard')
        return self.load_view("new.html")

    # process adding new user
    # go back to dashboard if successful
    def create(self):
        create_status = self.models['User'].create_user(request.form)
        if create_status.get('status') == True:
            return redirect("/dashboard/admin")
        else:
            for error in create_status.get('errors'):
                flash(error, "error")
            return redirect("/users/new")

    # display edit profile page. user_id = person logged in
    def edit_profile(self):
        print("edit_profile")
        user = self.models['User'].get_user_by_id(session.get('user_id')) 
        return self.load_view("edit.html", user=user)

    # display edit user page (admin only)
    def edit_user(self, user_id):
        print("edit_user")
        # non-admin getting here by entering url redirects to user dashboard
        if not session.get('admin'):
            return redirect('/dashboard')

        user = self.models['User'].get_user_by_id(user_id) 
        return self.load_view("edit.html", user=user)

    # process update user
    def update_user(self):
        print("update_user")
        edit_status = self.models['User'].edit_user(request.form)
        print("edit status: ", edit_status)
        if edit_status.get('status') == False:
            for error in edit_status.get('errors'):
                flash(error, "error")
        else:
            flash("Successfully updated", "success")

        if int(request.form.get('id')) == session.get('user_id'):
            return redirect("/users/edit")
        else:
            return redirect("/users/edit/" + request.form.get('id'))

    # process update password
    def update_password(self):
        edit_status = self.models['User'].edit_password(request.form)
        if edit_status.get('status') == False:
            for error in edit_status.get('errors'):
                flash(error, "error")
        else:
            flash("Successfully updated", "success")

        if int(request.form.get('id')) == session.get('user_id'):
            return redirect("/users/edit")
        else:
            return redirect("/users/edit/" + request.form.get('id'))

    # process update description
    def update_description(self):
        update_status = self.models['User'].update_description(request.form)
        return redirect("/dashboard")
 
    # displays confirmation page to delete user
    def delete(self, user_id): 
        # non-admin getting here by entering url redirects to user dashboard
        if not session.get('admin'):
            return redirect('/dashboard')

        user = self.models['User'].get_user_by_id(user_id) 
        return self.load_view("delete.html", user=user)

    # process deleting user
    def confirm_delete(self, user_id):
        self.models['User'].delete_user(user_id)
        if session.get('admin') == 1:
            return redirect("/dashboard/admin")
        else:
            return redirect("/dashboard")


    # display user info and wall messages
    def show(self, user_id):
        user = self.models['User'].get_user_by_id(user_id) 
        messages = self.models['Message'].get_wall(user_id)
        return self.load_view("show.html", user=user, messages=messages)




