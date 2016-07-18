from system.core.controller import *

class Courses(Controller):
    def __init__(self, action):
        super(Courses, self).__init__(action)
        self.load_model('Course')

    def index(self):
        courses = self.models['Course'].get_courses()
        return self.load_view('index.html', courses=courses) 

    # adds a single course
    def add(self):
        data = {
            'title'       : request.form.get('title', ''),
            'description' : request.form.get('description', '')
        }

        error = False
        if len(data.get('title')) < 1:
            flash("Please enter course title")
            error = True
        elif len(data.get('title')) < 15:
            flash("Course title must be at least 15 characters")
            error = True

        if not error: 
            row_id = self.models['Course'].add_course(data)

        return redirect('/')

    # print the confirm delete page
    def confirm_delete(self, id):
        course = self.models['Course'].get_course_by_id(id)
        return self.load_view('delete.html', course=course[0])

    # do the delete
    def delete(self, id):
        self.models['Course'].remove_course_by_id(id)
        return redirect('/')
