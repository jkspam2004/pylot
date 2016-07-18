from system.core.model import Model

class Course(Model):
    def __init__(self):
        super(Course, self).__init__()

    def get_courses(self):
        return self.db.query_db("SELECT * FROM courses")

    def add_course(self, data):
        query = "INSERT INTO courses (title, description, created_at, updated_at) \
            VALUES (:title, :description, now(), now())"
        return self.db.query_db(query, data)

    def get_course_by_id(self, course_id):
        query = "SELECT * FROM courses WHERE id = :id"
        data = { 'id' : course_id }
        return self.db.query_db(query, data)

    def remove_course_by_id(self, course_id):
        query = "DELETE FROM courses WHERE id = :id"
        data = { 'id' : course_id }
        return self.db.query_db(query, data)
