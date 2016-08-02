from system.core.model import *
import inspect

class Message(Model):
    def __init__(self):
        super(Message, self).__init__()

    # return a tuple with filename, linenum, and function name for caller
    def trace(self):
        return __file__, + inspect.stack()[1][2], inspect.stack()[1][3]

    # add a message for the user displayed
    def add(self, data):
        if not data['message']:
            return { 'status' : False, 'error' : 'Enter a message' }

        query = "INSERT INTO messages (owner_id, user_id, message, created_at, updated_at) \
            VALUES (:owner_id, :poster_id, :message, NOW(), NOW())" 

        data['id'] = self.db.query_db(query, data)
        print data, self.trace()
        return { 'status' : True, 'message' : data }

    # get messages and comments for user displayed
    def get_wall(self, user_id):
        query = "SELECT messages.id AS message_id, message, messages.created_at AS message_time, \
            concat(owner.first_name, ' ', owner.last_name) AS owner, owner.id AS owner_id, \
            concat(poster.first_name, ' ', poster.last_name) AS poster, poster.id AS poster_id, \
            concat(commenter.first_name, ' ', commenter.last_name) AS commenter, commenter.id AS commenter_id, \
            comment, comments.created_at AS comment_time, comments.id AS comment_id \
            FROM messages \
            LEFT JOIN users owner ON owner.id = messages.owner_id \
            LEFT JOIN comments ON messages.id = comments.message_id \
            LEFT JOIN users poster ON poster.id = messages.user_id \
            LEFT JOIN users commenter ON commenter.id = comments.user_id \
            WHERE owner_id = :owner_id \
            ORDER BY message_time DESC, \
            comment_time ASC"

        result = self.db.query_db(query, { 'owner_id' : user_id })

        if result:
            # do data massaging to prep for displaying the messages and comments
            # set the first message of the message group
            # set the last comment of the message group
            result[0]['last'] = 1
            result[0]['first'] = 1
            for i in range(1, len(result)):
                if result[i]['message_id'] != result[i-1]['message_id']:
                    # different message_id from previous: must be new message, set to first 
                    result[i]['first'] = 1 
                else:
                    # same message id as previous: previous row is not the last then
                    result[i-1]['last'] = 0

                # set current row to be the last
                result[i]['last'] = 1
                
        print result, self.trace()
        return result
        
