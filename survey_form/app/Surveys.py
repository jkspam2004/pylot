from system.core.controller import *

class Surveys(Controller):
    def __init__(self, action):
    super(Surveys, self).__init__(action)
    self.load_model('Surveys')

    def index(self):


