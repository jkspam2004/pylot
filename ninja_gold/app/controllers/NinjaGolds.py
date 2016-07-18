from system.core.controller import *
from datetime import datetime
import random


class NinjaGolds(Controller):
    def __init__(self, action):
        self.activity = ''
        self.status = ''
        super(NinjaGolds, self).__init__(action)

    def index(self):
        # let's initialize some session variables
        if not 'gold' in session:
            session['gold'] = 0
        if not 'activities' in session:
            session['activities'] = ''   
            
        return self.load_view('index.html')

    # reset the session
    def reset(self):
        print "index - method: " + request.method

        session.clear()	

        return redirect('/')

    # process_money route to handle the calculations for money processing and set results in 
    # activities key in the session. redirects back to index /
    def process_money(self):
        print 'got info - method: ' + request.method

        if request.form.get('action') == 'play_farm':
            self.play_time('farm', 10, 21)
        elif request.form.get('action') == 'play_cave':
            self.play_time('cave', 5, 11)
        elif request.form.get('action') == 'play_house':
            self.play_time('house', 2, 6)
        elif request.form.get('action') == 'play_casino':
            self.play_time('casino', -50, 51)

        # store the result string, the current time, and the gain/loss status for css color rendering
        # add to existing activities
        time = datetime.now().strftime("%Y/%m/%d %-I:%M %p")
        session['activities'] += "<p class='" + self.status + "'>" + self.activity + " (" + time + ")</p>"	

        return redirect('/')

    def play_time(self, place, start, end):
        rand_num = random.randint(start, end)
        print('rand_num: ', rand_num)

        session['gold'] += rand_num # add/subtract to the running gold total
        self.status = 'gain'
        if place == 'casino' and rand_num < 0:
            self.activity = 'Entered a ' + place + ' and lost ' + str(abs(rand_num)) + ' golds... Ouch..'
            self.status = 'loss'
        else:
            self.activity = 'Earned ' + str(rand_num) + ' golds from the ' + place + '! '

        return

        
