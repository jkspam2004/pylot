from system.core.model import *

class Quote(Model):
    def __init__(self):
        super(Quote, self).__init__()

    # add: add a quote by poster
    # if invalid input, return error status
    # if valid input, add the quote to the database
    def add(self, poster_id, form):
        errors = self.validate_input(form)

        if errors:
            return { 'status' : False, 'errors' : errors }
        else:
            row_id = self.insert_quote(poster_id, form)
            return { 'status' : True }

    # add_favorite: add a quote to favorites
    def add_favorite(self, quote_id, user_id):
        query = "INSERT INTO favorites (quote_id, user_id, created_at, updated_at) \
            VALUES (:quote_id, :user_id, NOW(), NOW())"
        values = {
            'quote_id' : quote_id,
            'user_id'  : user_id
        }
        return self.db.query_db(query, values)

    # remove_favorite: remove quote from favorites
    def remove_favorite(self, favorite_id):
        query = "DELETE FROM favorites WHERE id = :id"
        return self.db.query_db(query, { 'id' : favorite_id })

    # get_quotes: get all quotes not in the favorites section
    # return list of quotes
    # hmm..subquery..will think of better way
    def get_quotes(self, user_id):
        query = "SELECT q.id AS quote_id, q.quoted_by, q.message, q.poster_id, u.alias AS poster_alias \
            FROM quotes q LEFT JOIN users u ON (q.poster_id = u.id )\
            WHERE q.id NOT IN (SELECT quote_id FROM favorites WHERE user_id = :id)"
        return self.db.query_db(query, { 'id' : user_id })

    # get_favorites: get my favorite quotes
    # return list of favorite quotes
    def get_favorites(self, user_id):
        query = "SELECT  q.id AS quote_id, q.quoted_by, q.message, q.poster_id, u.alias AS poster_alias, f.id AS favorite_id \
            FROM favorites f \
            LEFT JOIN quotes q ON (f.quote_id = q.id ) \
            LEFT JOIN users u ON (q.poster_id = u.id) \
            WHERE f.user_id = :id"
        return self.db.query_db(query, { 'id' : user_id })

    # get_quotes_by_id: get quotes posted by specified user
    # return list of quotes
    def get_quotes_by_id(self, user_id):
        query = "SELECT * FROM quotes WHERE poster_id = :id"
        print("user_id: ", user_id)
        return self.db.query_db(query, { 'id' : user_id })

    # insert_quote: insert a quote into quotes table
    # return row id of inserted row
    def insert_quote(self, poster_id, form):
        query = "INSERT INTO quotes (quoted_by, message, poster_id, created_at, updated_at) \
            VALUES (:quoted_by, :message, :poster_id, NOW(), NOW())"
        values = {
            'quoted_by' : form.get('quoted_by'),
            'message'   : form.get('message'),
            'poster_id' : poster_id
        }
        return self.db.query_db(query, values)

    # validate_input: validate form inputs
    # return error list
    def validate_input(self, form):
        errors = []

        if not form.get('quoted_by'): 
            errors.append("Quoted By cannot be blank")
        elif len(form.get('quoted_by')) < 3:
            errors.append("Quoted By must be at least 3 characters")

        if not form.get('message'):
            errors.append("Message cannot be blank")
        elif len(form.get('message')) < 10:
            errors.append("Message must be at least 10 characters")

        return errors 
