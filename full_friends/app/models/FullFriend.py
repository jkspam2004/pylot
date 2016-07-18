from system.core.model import Model

class FullFriend(Model):
    def __init__(self):
        super(FullFriend, self).__init__()

    def get_friend(self, id):
        query = 'SELECT * FROM friends WHERE id=:id'
        values = {
            "id": id
        }

        friend = self.db.query_db(query, values)
        return friend[0]

    def get_friends(self):
        query = 'SELECT * FROM friends'
        return self.db.query_db(query)

    def update_friend(self, id, data):
        query = 'UPDATE friends SET first_name=:first_name, last_name=:last_name, email=:email, occupation=:occupation WHERE id=:id'
        data['id'] = id

        self.db.query_db(query, data)
        return True

    def delete_friend(self, id):
        query = 'DELETE FROM friends WHERE id=:id'
        values = {
            "id": id
        }

        self.db.query_db(query, values)
        return True

    def add_friend(self, data):
        query = 'INSERT INTO friends (first_name, last_name, email, occupation, created_at, updated_at) VALUES (:first_name, :last_name, :email, :occupation, NOW(), NOW())'
        self.db.query_db(query, data)