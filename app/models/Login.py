from system.core.model import Model 
import re

class Login(Model):
    def __init__(self):
        super(Login, self).__init__()
        self.user = []

    def create_user(self, info):
        errors = self.validate_registration(info)
        # If we hit errors, return them, else return True.
        if errors:
            return {"status": False, "errors": errors}
        else:
            # insert user
            info['password'] = self.bcrypt.generate_password_hash(info['password'])
            row_id = self.do_insert(info)
            # Then retrieve the last inserted user.
            get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            self.user = self.db.query_db(get_user_query)
            return { 'status': True, 'user': self.user[0] }

    def login_user(self, info):
        errors = self.validate_login(info)
        if errors:
            return { 'status' : False, 'errors' : errors }
        else:
            return { 'status' : True, 'user' : self.user }
        
    #### Helper functions ###

    # select all rows
    # if column name and value passed in, limits the result in the where clause
    def do_select(self, table_name=None, column_name=None, value=None):
        if column_name and value:
            query = "SELECT * FROM " + table_name + " WHERE " + column_name + " = :" + column_name
            data = { column_name : value }
            results = self.db.query_db(query, data)
        else:
            query = "SELECT * FROM " + table_name
            results = self.db.query_db(query)

        return results

    # insert one row
    def do_insert(self, info):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) \
            VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())"
        print("info", info)
        return self.db.query_db(query, info)

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

    # returns errors from basic validation
    def validate_registration(self, info):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        duplicate_email = self.do_select('users', 'email', info['email'])
        errors = []

        # Some basic validation
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


