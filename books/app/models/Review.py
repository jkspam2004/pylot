from system.core.model import *

class Review(Model):
    def __init__(self):
        super(Review, self).__init__()

    # add_review: add a review if it does not exist
    # update otherwise
    def add_review(self, form, user_id):
        has_review = self.has_review(form.get('book_id'), user_id)
        print("has_review: ", has_review)
        if not has_review:
            data = form.copy()
            data.update({ 'user_id' : user_id })
            review_id = self.insert_review(data)
            print("review_id: ", review_id)
        else:
            data = {
                'review' : form.get('review'),
                'rating' : form.get('rating'),
                'id'     : has_review[0]['id']  # review id
            }
            ret_val = self.update_review(data) 
            print("ret_val: ", ret_val)
            pass

        return True

    # check if user has a review for a particular book
    def has_review(self, book_id, user_id):
        query = "SELECT * FROM reviews WHERE book_id = :book_id AND user_id = :user_id"
        data = {
            'book_id' : book_id,
            'user_id' : user_id
        }
        return self.db.query_db(query, data)

    # get_reviews: get all the reviews and return
    def get_reviews(self):
        query = "SELECT * FROM reviews"
        return self.db.query_db(query)

    # insert_review: insert one review into reviews table
    # returns review id
    def insert_review(self, data):
        query = "INSERT INTO reviews (review, rating, book_id, user_id, created_at, updated_at) \
            VALUES (:review, :rating, :book_id, :user_id, NOW(), NOW())"
        return self.db.query_db(query, data)

    # update
    def update_review(self, data):
        query = "UPDATE reviews SET review = :review, rating = :rating, updated_at = NOW() \
            WHERE id = :id"
        return self.db.query_db(query, data)

    # delete review
    def delete_review(self, id):
        query = "DELETE FROM reviews WHERE id = :id"
        self.db.query_db(query, { 'id' : id })
        return

    # get reviews by user
    def get_reviews_by_user_id(self, id):
        query = "SELECT * FROM reviews, books WHERE user_id = :id AND reviews.book_id = books.id"
        return self.db.query_db(query, { 'id' : id })


