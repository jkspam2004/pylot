from system.core.controller import *

class Surveys(Controller):
    def __init__(self, action):
        super(Surveys, self).__init__(action)

    def index(self):
        return self.load_view('index.html')

    def process(self):
        print("process args: ", request.args)
        print("form: ", request.form)

        if not 'counter' in session:
            session['counter'] = 1
        else:
            session['counter'] += 1

        session['name'] = request.form.get('name')
        session['location'] = request.form.get('location')
        session['language'] = request.form.get('language')
        session['comment'] = request.form.get('comment')
        return redirect('/result')

    def result(self):
        return self.load_view('result.html')
