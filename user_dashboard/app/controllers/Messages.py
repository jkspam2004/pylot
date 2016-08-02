from system.core.controller import *
import inspect

class Messages(Controller):
    def __init__(self, action):
        super(Messages, self).__init__(action)
        self.load_model('Message')
        self.load_model('Comment')

    # return a tuple with filename, linenum, and function name for caller
    def trace(self):
        return __file__, + inspect.stack()[1][2], inspect.stack()[1][3]

    def post(self):
        data = request.form.copy()
        print request.form, self.trace()
        print data, self.trace()
        post_status = self.models['Message'].add(data)
        if post_status['status'] == False:
            flash(post_status['error'], "error")
            
        return redirect('/users/show/' + request.form.get('owner_id')) 

    def comment(self):
        data = request.form.copy()
        comment_status = self.models['Comment'].add(data)
        if comment_status['status'] == False:
            flash(comment_status['error'], "error")

        return redirect('/users/show/' + request.form.get('owner_id')) 


