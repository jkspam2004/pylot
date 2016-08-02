from system.core.model import *
import inspect

class Comment(Model):
    def __init__(self):
        super(Comment, self).__init__()

    # return a tuple with filename, linenum, and function name for caller
    def trace(self):
        return __file__, + inspect.stack()[1][2], inspect.stack()[1][3]


    def add(self, data):
        if not data['comment']:
            return { 'status' : False, 'error' : 'Enter a comment' }

        query = "INSERT INTO comments (message_id, user_id, comment, created_at, updated_at) \
            VALUES (:message_id, :commenter_id, :comment, NOW(), NOW())" 

        data['id'] = self.db.query_db(query, data)
        print data, self.trace()
        return { 'status' : True, 'message' : data }


