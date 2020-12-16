from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# we can use mysql or any other db we want here instead of sqlite
# /// is for relative path and //// for absolute path

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class TODO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    # utcnow is for universl time and for local time use datetime.now
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        "everytime we make an element in db it returns id of that task"
        return '<Task $r>' % self.id
    

@app.route('/', methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        taskCotent = request.form['content']
        newTask = TODO(content=taskCotent)
        
        try:
            db.session.add(newTask)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error"

    else:
        tasks = TODO.query.order_by(TODO.date_created).all()
        return render_template('index.html',tasks = tasks)
    

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = TODO.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        print("there was a problem deleting")
        
        
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task = TODO.query.get_or_404(id)
    
    if request.method == 'POST':
        task.content = request.form['content']
        
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            print("Error in updating")
    else:
        return render_template('update.html',task=task)
        
if __name__ == "__main__":
    app.run(debug=True)