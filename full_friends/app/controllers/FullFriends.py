from system.core.controller import *

class FullFriends(Controller):
    def __init__(self, action):
        super(FullFriends, self).__init__(action)
        self.load_model('FullFriend')

    def index(self):
        friends = self.models['FullFriend'].get_friends()
        return self.load_view('index.html', friends=friends)

    def show(self, id):
        friend = self.models['FullFriend'].get_friend(id)
        return self.load_view('show.html', friend=friend)

    def edit(self, id):
        friend = self.models['FullFriend'].get_friend(id)
        return self.load_view('edit.html', friend=friend)

    def update(self, id):

        data = {
            "first_name" : request.form['first_name'],
            "last_name" : request.form['last_name'],
            "email" : request.form['email'],
            "occupation" : request.form['occupation']
        }
        self.models['FullFriend'].update_friend(id, first_name, last_name, email, occupation)
        return redirect('/')

    def delete(self, id):
        friend = self.models['FullFriend'].get_friend(id)
        return self.load_view('delete.html', friend=friend)

    def delete_confirm(self, id):
        self.models['FullFriend'].delete_friend(id)
        return redirect('/')

    def add(self):
        return self.load_view('add.html')

    def add_friend(self):
        data = {
            "first_name" : request.form['first_name'],
            "last_name" : request.form['last_name'],
            "email" : request.form['email'],
            "occupation" : request.form['occupation']
        }

        self.models['FullFriend'].add_friend(data)
        return redirect('/')

