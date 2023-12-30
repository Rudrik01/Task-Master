from flask import Flask, render_template ,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
import pytz
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

def get_current_time():
    return datetime.now(pytz.timezone('Asia/Kolkata')).time()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200),nullable=False)
    completed = db.Column(db.Integer,default=0)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)
    time_created = db.Column(db.Time)


    def __init__(self, content):
        self.content = content
        self.time_created = get_current_time()

    def __repr__(self):
        return '<Task %r>'% self.id 
    

with app.app_context():
    # Create all tables in the database
    db.create_all()




@app.route('/',methods =['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        
        except:
            return 'There was an issue adding your task'
        
    else:
        tasks = Todo.query.order_by(Todo.time_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'
@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue in updating the task'
    else:
        return render_template('update.html',task=task)


