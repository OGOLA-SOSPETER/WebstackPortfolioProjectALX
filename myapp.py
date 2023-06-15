import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

def get_db_connection():
    conn = sqlite3.connect('recipedatabase.db')
    conn.row_factory = sqlite3.Row
    return conn
def wait_db_connection():
    conn = sqlite3.connect('waitlistdatabase.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        useremail = request.form['email']
        userpassword = request.form['password']

        conn = get_db_connection()

        # Check if the email or password already exists in the database
        result = conn.execute('SELECT * FROM loggedUsers WHERE useremail = ? OR userpassword = ?', (useremail, userpassword))
        existing_user = result.fetchone()

        if existing_user:
            # Email or password already registered, display error message
            flash('Email or password already registered!', 'error')
            conn.close()
            return redirect(url_for('register'))
        else:
            # Register the new user
            result = conn.execute('INSERT INTO loggedUsers (useremail, userpassword) VALUES (?, ?)', (useremail, userpassword))
            conn.commit()
            conn.close()

            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        

    return render_template('register.html')

@app.route('/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        useremail = request.form['email']
        userpassword = request.form['password']
  
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM loggedUsers WHERE useremail = ? AND userpassword = ?',
                            (useremail, userpassword)).fetchone()
        conn.close()

        if user:
            # User credentials are correct, redirect to the main page
            # flash('Login successful!')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password!')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about_us.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/breakfast')
def breakfast():
    return render_template('breakfast.html')

@app.route('/lunch')
def lunch():
    return render_template('lunch.html')

@app.route('/dinner')
def dinner():
    return render_template('dinner.html')

@app.route('/salad')
def salad():
    return render_template('salads.html')

@app.route('/index')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM recipes').fetchall()
    conn.close()
    return render_template('index.html', posts = posts)

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM recipes WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


def get_moduled_post(post_cat):
    conn = get_db_connection()
    cats = conn.execute('SELECT * FROM recipes WHERE rcategory = ?',
                        (post_cat,)).fetchall()
    conn.close()
    if cats is None:
        abort(404)
    return cats

@app.route('/moduled_cat/<post_cat>')
def moduled_cat(post_cat):
    cats = get_moduled_post(post_cat)
    return render_template('moduled.html',cats=cats,post_cat=post_cat)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        rimage = request.form['rimage']
        img1 = request.form['img1']
        img2 = request.form['img2']
        img3 = request.form['img3']

        rname = request.form['rname']
        category = request.form['rcategory']
        description = request.form['description']
        ingredients = request.form['ingredient']
        procedure = request.form['procedure']

        con = wait_db_connection()
        con.execute('INSERT INTO awaitrecipes (rname,rcategory,rimage,rdescription,ringredients,rprocedure,image1,image2,image3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (rname,category,rimage,description,ingredients,procedure,img1,img2,img3))
        con.commit()
        con.close()
        return redirect(url_for('index'))

            

    return render_template('create.html')

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM recipes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['rname']))
    return redirect(url_for('index'))

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        image = request.form['rimage']
        name = request.form['rname']
        category = request.form['rcategory']
        description = request.form['description']
        ingredients = request.form['ingredient']
        procedure = request.form['procedure']
        img1 = request.form['img1']
        img2 = request.form['img2']
        img3 = request.form['img3']

        conn = get_db_connection()
        conn.execute('UPDATE recipes SET  rname = ?, rcategory = ?, rimage = ?, rdescription = ?, ringredients = ?, rprocedure = ?, image1 = ?, image2 = ?, image3 = ? WHERE id = ?',(name,category,image,description,ingredients,procedure,img1,img2,img3, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))


    return render_template('edit.html', post=post)

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form.get('search_term')
    # Perform the search logic here based on the search_term
    conn = get_db_connection()
    search_results = conn.execute('SELECT * FROM recipes WHERE rname = ?',
                        (search_term)).fetchall()
    conn.close()

    return {'results': search_results}



@app.route('/await_list')
def await_list():
    conn = wait_db_connection()
    waitposts = conn.execute('SELECT * FROM awaitrecipes').fetchall()
    conn.close()
    if waitposts is None:
        return redirect(url_for('error'))
    return render_template('awaitList.html',waitposts=waitposts)

@app.route('/error')
def error():
    return render_template('error.html')

def get_wait_post(wait_id):
    conn = wait_db_connection()
    waitpost = conn.execute('SELECT * FROM awaitrecipes WHERE id = ?',
                        (wait_id,)).fetchone()
    conn.close()
    if waitpost is None:
        abort(404)
    return waitpost

@app.route('/<int:wait_id>')
def waitpost(wait_id):
    waitpost = get_wait_post(wait_id)
    return render_template('viewWaitList.html', waitpost=waitpost,)