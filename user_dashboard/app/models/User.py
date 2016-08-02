from system.core.model import *
import re

class User(Model):
    def __init__(self):
        super(User, self).__init__()
        self.user = {}

    # create user from registration
    # if valid inputs, save the information and set the session
    # if invalid, return error
    def create_user(self, form):
        errors = self.validate_reg(form)

        if errors:
           return { 'status' : False, 'errors': errors }
        else:
           data = {
               'email'      : form.get('email'),
               'first_name' : form.get('first_name'),
               'last_name'  : form.get('last_name'),
               'password'   : self.bcrypt.generate_password_hash(form.get('password')),
               'user_level' : self.get_user_level()
           }
           user_id = self.insert_user(data)
           return { 'status' : True, 'user' : self.get_user_by_id(user_id) } 

    # check user credentials for logging in 
    def login_user(self, info):
        errors = self.validate_login(info)
        if errors:
            return { 'status' : False, 'errors' : errors }
        else:
            return { 'status' : True, 'user' : self.user }

    # edit user
    def edit_user(self, form):
        print("model edit_user")
        errors = self.validate_user_info(form)
        print("errors: ", errors)

        if errors:
           return { 'status' : False, 'errors': errors }
        else:
           data = {
               'email'      : form.get('email'),
               'first_name' : form.get('first_name'),
               'last_name'  : form.get('last_name'),
               'user_level' : form.get('user_level'), 
               'id'         : form.get('id')
           }
           update_ret_val = self.update_user(data)
           print("update_ret_val: ", update_ret_val)
           return { 'status' : True, 'user' : self.get_user_by_id(data.get('id')) } 

    # edit password
    def edit_password(self, form):
        errors = self.validate_password(form)

        if errors:
           return { 'status' : False, 'errors': errors }
        else:
           data = {
               'password'   : self.bcrypt.generate_password_hash(form.get('password')),
               'id'         : form.get('id')
           }
           ret_val = self.update_password(data)
           return { 'status' : True, 'user' : self.get_user_by_id(form.get('id')) } 

    # validate reg input
    def validate_reg(self, info):
        print("validate_reg")
        duplicate_email = self.do_select('users', 'email', info['email'])

        user_errors = self.validate_user_info(info)
        # if email isn't blank and it's already in the system, error
        if info['email'] and duplicate_email:
            errors.append('Email cannot be blank')

        password_errors = self.validate_password(info)

        return user_errors + password_errors

    # validate user inputs: first name, last name, and email
    def validate_user_info(self, info):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
        errors = []

        if not info['first_name']:
            errors.append('First Name cannot be blank')
        elif len(info['first_name']) < 2:
            errors.append('First Name must be at least 2 characters long')
        if not info['last_name']:
            errors.append('Last Name cannot be blank')
        elif len(info['last_name']) < 2:
            errors.append('Last Name must be at least 2 characters long')
        if not info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Email format must be valid!')

        return errors

    # validate user input: password
    def validate_password(self, info):
        print("validate_password", info)
        errors = []
        if not info['password']:
            errors.append('Password cannot be blank')
        elif len(info['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif info['password'] != info['confirm_pw']:
            errors.append('Password and confirmation must match!')

        return errors

    # validate login input
    def validate_login(self, info):
        errors = []
        user_data = self.do_select('users', 'email', info['email']) # get database info associated with email
   
        if not info['email']:
            errors.append('Please enter email')
        elif not user_data: # user doesn't exist in database
            errors.append("Hmm, we don't recognize that email")
            return errors

        if not info['password']:
            errors.append('Enter your password') 
        else:
            hash_pw = user_data[0]['password']
            matched = self.bcrypt.check_password_hash(hash_pw, info['password'])
            if not matched:
                errors.append('Check your password')

        if not errors:
            self.user = user_data[0]

        return errors  

    # delete user
    def delete_user(self, user_id):
        query = "DELETE FROM users WHERE id = :id"
        self.db.query_db(query, { 'id' : user_id })
        return

    # update user info
    def update_user(self, data):
        query = "UPDATE users SET email = :email, first_name = :first_name, last_name = :last_name, \
            user_level = :user_level, updated_at = NOW() WHERE id = :id"
        return self.db.query_db(query, data)

    # update password
    def update_password(self, data):
        query = "UPDATE users SET password = :password, updated_at = NOW() WHERE id = :id"
        return self.db.query_db(query, data)

    # update description
    def update_description(self, data):
        query = "UPDATE users SET description = :description, updated_at = NOW() WHERE id = :id"
        return self.db.query_db(query, data)

    # get all users from db
    def get_all_users(self):
        query = "SELECT * FROM users"
        return self.db.query_db(query)

    # get info for specified user
    def get_user_by_id(self, id):
        query = "SELECT * FROM users WHERE id = :id"
        user = self.db.query_db(query, { 'id' : id }) 
        return user[0] if user else {}
   
    # insert one user into users table
    def insert_user(self, data):
        query = "INSERT INTO users SET email = :email, first_name = :first_name, last_name = :last_name, \
            password = :password, user_level = :user_level, created_at = NOW(), updated_at = NOW()"
        return self.db.query_db(query, data)

    # get user level
    # return 9 if first user, otherwise return 0 
    def get_user_level(self):
        query = "SELECT COUNT(1) AS count FROM users"
        result = self.db.query_db(query)
        if result[0]['count'] > 0:
            return 0 
        else:
            # first user that registers is an admin, set user_level=9
            return 9

    # do a database select
    def do_select(self, table_name=None, column_name=None, value=None):
        if column_name and value:
            query = "SELECT * FROM " + table_name + " WHERE " + column_name + " = :" + column_name
            data = { column_name : value }
            results = self.db.query_db(query, data)
        else:
            query = "SELECT * FROM " + table_name
            results = self.db.query_db(query)

        return results


