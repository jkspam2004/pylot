from system.core.controller import *
import inspect

class Books(Controller):
    def __init__(self, action):
        super(Books, self).__init__(action)
        self.load_model('Book')
        self.load_model('User')
        self.load_model('Review')
        self.models['Book'].set_models(self.models['Review'])

    def trace(self):
        return __file__, inspect.stack()[1][2], inspect.stack()[1][3]

    # get recent book reviews and display
    def show(self):
        info = self.models['Book'].get_books_and_reviews()
        return self.load_view('books.html', recent_reviews=info.get('recent_reviews'), all_books=info.get('all_books'))

    # display add book page
    def add(self):
        return self.load_view('new_book.html')

    # process adding new book
    def create(self):
        print("session id: ", session.get('user_id'), "alias: ", session.get('alias'))
        create_status = self.models['Book'].add_book(request.form, session.get('user_id'))
        if create_status['status'] == False:
            for message in create_status['errors']:
                flash(message, 'error')
            return redirect('/books/add')
        else:
            return redirect('/books/' + str(create_status['book']['id']))

    # display reviews for specified book
    def review(self, book_id):
        (book_info, reviews) = self.models['Book'].get_book_reviews(book_id)
        #print "book_info: ", book_info, self.trace()
        #print "reviews: ", reviews, self.trace()
        return self.load_view('book_info.html', book=book_info, reviews=reviews)

    # add a review to a book
    def add_review(self):
        print("session id: ", session.get('user_id'), "alias: ", session.get('alias'))
        print("request_form: ", request.form)
        add_status = self.models['Review'].add_review(request.form, session.get('user_id'))

        return redirect('/books/' + request.form.get('book_id'))

    def delete(self, review_id):
        return self.load_view('delete.html', review_id = review_id)

    def confirm_delete(self, review_id):
        self.models['Review'].delete_review(review_id)
        return redirect('/books')

