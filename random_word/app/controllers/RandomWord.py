"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *
import string
import random

class RandomWord(Controller):
    def __init__(self, action):
        super(RandomWord, self).__init__(action)
        self.db = self._app.db
   
    def index(self):
        if 'counter' not in session:
            session['counter'] = 1
        else: 
            session['counter'] += 1

        word = ''
        for letter in range(14):
            word += random.choice(string.letters)

        return self.load_view('index.html', word=word)

    def reset(self):
        session.clear()
        return redirect('/');


