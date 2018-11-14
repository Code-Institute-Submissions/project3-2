import os 
from flask import Flask,render_template, redirect, request, url_for 
from flask_pymongo import PyMongo 
from bson.objectid import ObjectId
import re


app=Flask(__name__)  

app.config["MONGO_DBNAME"] = "app-boakread" 
app.config["MONGO_URI"] = "mongodb://admin:admin1@ds161751.mlab.com:61751/app-boakread"

mongo=PyMongo(app)

@app.route('/') 
@app.route('/get_tasks') 
def get_tasks(): 
    _tasks=mongo.db.tasks.find() 
    task_list=[task for task in _tasks]
    return render_template("tasks.html", tasks=task_list )

@app.route('/add_task') 
def add_task(): 
    return render_template("addtask.html", 
    categories=mongo.db.categories.find(), genres=mongo.db.genre.find(),taskdescs=mongo.db.taskdesc.find() )  

@app.route('/insert_task', methods=['POST'])  
def insert_task():  
    task=mongo.db.tasks 
    task.insert_one(request.form.to_dict()) 
    return redirect(url_for('get_tasks'))  

@app.route("/edit_task/<task_id>")
def edit_task(task_id):
    the_task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    categories = mongo.db.categories.find()
    return render_template("edittask.html", task=the_task, categories=categories)  
    
@app.route("/update_task/<task_id>", methods=['POST'])
def update_task(task_id):
    print( request.form.to_dict())
    tasks = mongo.db.tasks
    tasks.update({"_id": ObjectId(task_id)}, request.form.to_dict())
    return redirect(url_for("get_tasks"))
    
    
@app.route("/delete_task/<task_id>")
def delete_task(task_id):
    mongo.db.tasks.remove({"_id": ObjectId(task_id)})
    return redirect(url_for("get_tasks"))    


    
@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
    categories=mongo.db.categories.find()) 
    
@app.route('/new_category')
def new_category():
    return render_template('addcategory.html')


@app.route('/insert_category', methods=['POST'])
def insert_category():
    categories = mongo.db.categories
    categories.insert_one(request.form.to_dict())
    return redirect(url_for('get_categories'))
    
@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
    category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))

@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form['category_name']})
    return redirect(url_for('get_categories'))

@app.route('/confirm_delete_category/<category_id>') 
def confirm_delete_category(category_id): 
    category = mongo.db.categories.find_one({'_id': ObjectId(category_id)})
    return render_template('confirm_delete_category.html', category=category)

@app.route('/search_task') 
def search_task(): 
    search_term = request.args.get("search_term")
    filtered_tasks = mongo.db.tasks.find({"task_name":{"$regex": "(?i)(" + search_term + ")"}})
    return render_template("tasks.html", tasks=filtered_tasks)
  
    
@app.route('/delete_category/<category_id>') 
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for("get_categories")) 

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)



