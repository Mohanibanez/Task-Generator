#Importing Modules and the functions
#In line 11 you are making available the code you need to build web apps with flask.
#flask is the framework here(library), while Flask is a Python class datatype(specific class).
#In other words, Flask  is the prototype used to create instances of web application or web applications if you want to put it simple.
#What we also did is we imported the render_template method from the flask framework and then we passed an HTML file(line 47 and line 75)
#to that method.
#The method will generate a jinja2 template object out of that HTML and return it to the browser when the user visits associated URL.



from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


#So, once we import Flask, we need to create an instance of the Flask class for our web app.
#That’s what line 18 does. __name__ is a special variable that gets as value the string "__main__" when you’re executing the script.
app = Flask(__name__)      #__name__ becomes __main__ when executed.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #The database URI that should be used for the connection.
db = SQLAlchemy(app)

#The baseclass for all your models is called db.Model. It’s stored on the SQLAlchemy instance you have to create.
#Use Column to define a column.
#The name of the column is the name you assign it to.
#If you want to use a different name in the table you can provide an optional first argument which is a string with the desired column name.
#Primary keys are marked with primary_key=True.
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)                               #Number of tasks
    content = db.Column(db.String(200), nullable=False)                        #Task description
    date_created = db.Column(db.DateTime, default=datetime.utcnow)             #Date created

    def __repr__(self):
        return '<Task %r>' % self.id
#That index function is mapped to the home ‘/’ URL.
#That means when the user navigates to localhost:5000, the home function will run and it will return its output on the webpage.
#If the input to the route method was something else, let’s say ‘/about/’, the function output would be shown when the user visited localhost:5000/about/.

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':                  #If the request is provided by the User, I.e.,Inputting data, the below code is followed
        task_content = request.form['content']    #Iniliazing a variable to save the contents in the "contents" field.
        new_task = Todo(content=task_content)     #creating a Todo object(a new task)

        try:
            db.session.add(new_task)    #adding data to our model
            db.session.commit()         #commiting the data to our model
            return redirect('/')        #redirect it back to index page
        except:
            return 'There was an issue adding your task'  #if it fails(above 3 lines)

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()     #To display all current tasks in table
        return render_template('index.html', tasks=tasks)        #Returning the tasks to template


@app.route('/delete/<int:id>')   #New route to delete a Task
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)   #Gets the Task by id, else it 404s

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')    #Redirect back to home page
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)

#Something you should know is that Python assigns the name "__main__" to the script when the script is executed.
#If the script is imported from another script, the script keeps it given name (e.g. hello.py).
#In our case we are executing the script. Therefore, __name__ will be equal to "__main__".
#That means the if conditional statement is satisfied and the app.run() method will be executed.
#This technique allows the programmer to have control over script’s behavior.

if __name__ == "__main__":
    app.run(debug=True)

#The Python script handles the communication between the web server and the web client (i.e. browser)
#while the HTML documents are responsible for the structure of the page content.
