from system.core.model import *
import inspect

class Book(Model):
    def __init__(self):
        super(Book, self).__init__()
        self.review_obj = None

    def trace(self):
        return __file__, inspect.stack()[1][2], inspect.stack()[1][3]

    # set the model objects from other models
    def set_models(self, review_obj):
        self.review_obj = review_obj

    # get_books_and_reviews: get recent reviews and all books with reviews for display
    def get_books_and_reviews(self):
        data = {
            'recent_reviews' : self.get_recent_reviews(),
            'all_books'      : self.get_all_books()
        }
        return data

    # get_book_reviews: get all reviews for specified book
    def get_book_reviews(self, id):
        book_info = self.get_book_by_id(id)
        book = book_info[0] if book_info else {}
        reviews = self.get_reviews_by_book_id(id)
        return (book, reviews)

    # add_book: process adding book
    # if input validation fails, return errors
    # if successful, return one book info
    def add_book(self, form, user_id):
        data = {
            'title'  : form.get('title'),
            'author' : form.get('author'),
            'review' : form.get('review'),
            'rating' : form.get('rating')
        } 
        errors = self.validate_input(data)

        if errors:
            return { 'status' : False, 'errors' : errors }
        else:
            book_id = self.insert_book(data) 
            review_data = {
                'review'  : form.get('review'),
                'rating'  : form.get('rating'),
                'book_id' : book_id,
                'user_id' : user_id
            } 
            review_id = self.review_obj.insert_review(review_data)
            return { 'status' : True, 'book' : self.get_book_by_id(book_id)[0] }

    #### Helper Functions ####

    # get all reviews for specified book
    def get_reviews_by_book_id(self, id):
        query = "SELECT u.id AS user_id, u.alias, \
            r.id AS review_id, r.rating, r.review, r.updated_at AS review_updated_at \
            FROM reviews r \
            LEFT JOIN users u ON (u.id = r.user_id) \
            WHERE book_id = :id ORDER BY review_updated_at DESC"
        return self.db.query_db(query, { 'id' : id })

    # get_book_by_id: get book info for specified book
    def get_book_by_id(self, id):
        query = "SELECT * FROM books WHERE id = :id"
        return self.db.query_db(query, { 'id' : id })

    # get_recent_reviews: join books, users, and reviews tables to get recent reviews on books
    # return list
    def get_recent_reviews(self):
        query = "SELECT b.id AS book_id, b.title, u.id AS user_id, u.alias, \
            r.id AS review_id, r.rating, r.review, r.updated_at AS review_updated_at \
            FROM reviews r LEFT JOIN books b ON (b.id = r.book_id) \
            LEFT JOIN users u ON (u.id = r.user_id) \
            ORDER BY review_updated_at DESC LIMIT 3"
        return self.db.query_db(query)

    # get_all_books: get all books from books table
    def get_all_books(self):
        query = "SELECT * FROM books"
        return self.db.query_db(query) 

    # insert_book: insert one book into books table
    # returns book id
    def insert_book(self, data):
        query = "INSERT INTO books (title, author, created_at, updated_at) \
            VALUES (:title, :author, NOW(), NOW())"
        return self.db.query_db(query, data)


    # get_book_by_title: get book info for specified title
    def get_book_by_title(self, title):
        query = "SELECT * FROM books WHERE title = :title"
        return self.db.query_db(query, { 'title' : title })

    # validate_input: validate input prior to adding book
    # returns errors array
    def validate_input(self, data):
        errors = []
        # if the book exists, error

        if  not data['title']:
            errors.append("Title cannot be blank")
        else:
            book = self.get_book_by_title(data.get('title'))
            print("book: ", book)
            if book:
                errors.append("Book has already been added")
                return errors

        if not data['author']:
            errors.append("Author cannot be blank")
        if not data['review']:
            errors.append("Please write review") 
     
        rating = int(data.get('rating'))
        if rating < 0 or rating > 5:
            errors.append("Invalid rating") 
 
        return errors

   
