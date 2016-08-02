from system.core.model import *
import re

class User(Model):
    def __init__(self):
        super(User, self).__init__()
        self.user = []

    # create_user: create user from registration. check for valid input first
    # if input invalid, return errors
    # if success, add and return user info
    def create_user(self, form):
        errors = self.validate_registration(form)
        if errors:
            return {"status": False, "errors": errors}
        else:
            data = {
                'name'     : form.get('name'),
                'alias'    : form.get('alias'),
                'email'    : form.get('email'),
                'password' : self.bcrypt.generate_password_hash(form.get('password'))
            }
            user_id = self.insert_user(data)
            return { 'status': True, 'user': self.get_user_by_id(user_id) }

    # login_user: login user. check for valid input first
    # if invalid inputs, return errors
    # if successful, return user info
    def login_user(self, info):
        errors = self.validate_login(info)
        if errors:
            return { 'status' : False, 'errors' : errors }
        else:
            return { 'status' : True, 'user' : self.user }
        
    #### Helper functions ###

    # do_select: select all rows
    # if column name and value passed in, limit the result in the where clause
    def do_select(self, table_name=None, column_name=None, value=None):
        if column_name and value:
            query = "SELECT * FROM " + table_name + " WHERE " + column_name + " = :" + column_name
            data = { column_name : value }
            results = self.db.query_db(query, data)
        else:
            query = "SELECT * FROM " + table_name
            results = self.db.query_db(query)

        return results

    # get_user_by_id: get info for a specific user
    def get_user_by_id(self, id):
        query = "SELECT * FROM users WHERE id = :id"
        user = self.db.query_db(query, { 'id': id })
        return user[0] 

    # insert_user: insert one row into user
    def insert_user(self, info):
        query = "INSERT INTO users (name, alias, email, password, created_at, updated_at) \
            VALUES (:name, :alias, :email, :password, NOW(), NOW())"
        return self.db.query_db(query, info)

    # validate_login: validate login input
    def validate_login(self, info):
        errors = []
        user_data = self.do_select('users', 'email', info['email']) # get database info associated with email
        print("user_data: ", user_data)
   
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

    # validate_registration: returns errors from basic validation
    def validate_registration(self, info):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        duplicate_email = self.do_select('users', 'email', info['email'])
        errors = []

        # Some basic validation
        if not info['name']:
            errors.append('Name cannot be blank')
        elif len(info['name']) < 2:
            errors.append('Name must be at least 2 characters long')
        if not info['alias']:
            errors.append('Alias cannot be blank')
        elif len(info['alias']) < 2:
            errors.append('Alias must be at least 2 characters long')
        if not info['email']:
            errors.append('Email cannot be blank')
        elif duplicate_email:
            errors.append('Email already in use')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Email format must be valid!')
        if not info['password']:
            errors.append('Password cannot be blank')
        elif len(info['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif info['password'] != info['confirm_pw']:
            errors.append('Password and confirmation must match!')

        return errors

     ######  end of file #####
