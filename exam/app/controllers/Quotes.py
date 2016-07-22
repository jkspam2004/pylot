from system.core.controller import *

class Quotes(Controller):
    def __init__(self, action):
        super(Quotes, self).__init__(action)
        self.load_model('Quote')
        self.load_model('User')

    # show: get all quotes and my favorite quotes
    def show(self):
        quotes = self.models['Quote'].get_quotes(session.get('user_id'))
        favorites = self.models['Quote'].get_favorites(session.get('user_id'))
        return self.load_view('quotes.html', favorites=favorites, quotes=quotes)

    # add: add a quote
    def add(self, poster_id):
        create_status = self.models['Quote'].add(poster_id, request.form)
        print("create_status: ", create_status)
        if create_status['status'] == False:
            for message in create_status['errors']:
                flash(message, 'error')
        else:
            flash("Successfully added!", "success")

        return redirect('/quotes')

    # move_to: move quote to favorites list
    def move_to(self, quote_id):
        self.models['Quote'].add_favorite(quote_id, session.get('user_id'))
        return redirect('/quotes')

    # move_from: move quote from favorites list
    def move_from(self, favorite_id):
        self.models['Quote'].remove_favorite(favorite_id)
        return redirect('/quotes')
        
        
