#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import os
import time
from flask.helpers import flash, send_file
from werkzeug import secure_filename


#Initialize the app from Flask
app = Flask(__name__)
app.config['IMAGE_UPLOADS'] = r"C:\Users\giana\Documents\CS3083Project\Finstagram\Flask\static"
#Configure MySQL
conn = pymysql.connect(host='localhost',
                       port = 3306,
                       user='root',
                       password='',
                       db='finstagram',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
    return render_template('index.html')

#Define route for login
@app.route('/login')
def login():
    return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
    return render_template('register.html')

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM user WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in
        session['username'] = username
        return redirect(url_for('home'))
    else:
        #returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login.html', error=error)

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM user WHERE username = %s'
    cursor.execute(query, (username))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register.html', error = error)
    else:
        ins = 'INSERT INTO user VALUES(%s, %s,%s,%s,%s)'
        cursor.execute(ins, (username, password,first_name,last_name,""))
        conn.commit()
        cursor.close()
        return render_template('index.html')


@app.route('/home')
def home():
    user = session['username']
    cursor = conn.cursor();
    query = "SELECT * FROM Photo JOIN user ON Photo.photoPoster=user.username WHERE (photoPoster IN (SELECT username_followed FROM Follow WHERE " \
            "username_follower = %s and followstatus = 1) and allFollowers = 1) OR (photoID IN (SELECT photoID FROM " \
            "belongto NATURAL JOIN sharedwith WHERE member_username = %s)) OR (photoPoster = %s) ORDER BY postingdate DESC"
    cursor.execute(query, (user,user,user))
    data = cursor.fetchall()
    cursor.close()
    return render_template("home.html", user=user, images=data)

@app.route("/upload_image", methods=["GET"])
def upload_image():
    return render_template("upload.html")

app.secret_key = "super secret key"
app.config["IMAGES_DIR"] = r"C:\Users\giana\Documents\CS3083Project\Finstagram\Flask\static"
ALLOWED_EXTENSIONS = {'png','jpg','jpeg','gif'}

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/post', methods=['GET', 'POST'])
def post():

    user = session['username']

    cursor = conn.cursor()

    if request.method == 'POST':
        file = request.files['file']

        filename = file.filename

        filepath = os.path.join(app.config["IMAGES_DIR"], filename)

        file.save(filepath)

        if request.form:
            requestData = request.form

            allFollowers = requestData["public"]

            query = "INSERT INTO photo (filePath,photoPoster, allFollowers) VALUES ( %s, %s,%s)"

            cursor.execute(query, (filename, user,allFollowers))

            conn.commit()
    
        query = "SELECT * FROM Photo JOIN user ON Photo.photoPoster=user.username WHERE (photoPoster IN (SELECT username_followed FROM Follow WHERE " \
            "username_follower = %s and followstatus = 1) and allFollowers = 1) OR (photoID IN (SELECT photoID FROM " \
            "belongto NATURAL JOIN sharedwith WHERE member_username = %s)) OR (photoPoster = %s) ORDER BY postingdate DESC"

        cursor.execute(query, (user,user,user))

        data = cursor.fetchall()

        cursor.close()
        
    return render_template("home.html", user=user, images=data)

        # username = session['username']
        # cursor = conn.cursor();
        # blog = request.form['blog']
        # query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
        # cursor.execute(query, (blog, username))
        # conn.commit()
        # cursor.close()
        # return redirect(url_for('home'))

@app.route('/search_by_tag', methods=['GET', 'POST'])
def search_by_tag():
    user = session['username']
    cursor = conn.cursor()
    if request.method=='POST':
        keyword=request.form['keyword']
        sql="SELECT * FROM Photo NATURAL JOIN tagged WHERE tagstatus=true AND username=%s AND " \
            "photoID IN (SELECT photoID FROM Photo JOIN user ON Photo.photoPoster=user.username " \
            "WHERE (photoPoster IN (SELECT username_followed FROM Follow WHERE " \
            "username_follower = %s and followstatus = 1) and allFollowers = 1) OR (photoID IN (SELECT photoID FROM " \
            "belongto NATURAL JOIN sharedwith WHERE member_username = %s)) OR (photoPoster = %s)) "
        cursor.execute(sql, (keyword, user, user, user))
        data=cursor.fetchall()
        return render_template('search_result.html', user=user, images=data)
    return render_template('home.html')

@app.route('/search_by_poster', methods=['GET', 'POST'])
def search_by_poster():
    user = session['username']
    cursor = conn.cursor()
    if request.method=='POST':
        keyword=request.form['keyword']
        sql="SELECT * FROM Photo WHERE photoPoster=%s AND " \
            "photoID IN (SELECT photoID FROM Photo JOIN user ON Photo.photoPoster=user.username " \
            "WHERE (photoPoster IN (SELECT username_followed FROM Follow WHERE " \
            "username_follower = %s and followstatus = 1) and allFollowers = 1) OR (photoID IN (SELECT photoID FROM " \
            "belongto NATURAL JOIN sharedwith WHERE member_username = %s)) OR (photoPoster = %s)) "
        cursor.execute(sql, (keyword, user, user, user))
        data=cursor.fetchall()
        return render_template('search_result.html', user=user, images=data)
    return render_template('home.html')

@app.route('/select_blogger')
def select_blogger():
    #check that user is logged in
    #username = session['username']
    #should throw exception if username not found
    
    cursor = conn.cursor();
    query = 'SELECT DISTINCT username FROM blog'
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return render_template('select_blogger.html', user_list=data)

@app.route('/show_posts', methods=["GET", "POST"])
def show_posts():
    poster = request.args['poster']
    cursor = conn.cursor();
    query = 'SELECT postingdate, photoPoster FROM blog WHERE username = %s ORDER BY postingdate DESC'
    cursor.execute(query, poster)
    data = cursor.fetchall()
    cursor.close()
    return render_template('show_posts.html', poster_name=poster, posts=data)

@app.route("/like", methods = ["GET","POST"])
def likes():
    photoID = request.args.get("photoID")

    user = session['username']

    rating = request.form['rating']

    cursor = conn.cursor();

    query = "INSERT INTO likes (username, photoID,rating) VALUES (%s, %s,%s) "

    cursor.execute(query,(user, photoID,rating))

    query = "SELECT * FROM likes NATURAL JOIN user WHERE photoID = %s ORDER BY liketime DESC"

    cursor.execute(query,photoID)

    data = cursor.fetchall()

    cursor.close()

    return render_template("likes.html",likes = data)

@app.route("/comment", methods = ["GET","POST"])
def comment():
    photoID = request.args.get("photoID")

    user = session['username']

    comment = request.form['comment']

    cursor = conn.cursor();

    query = "INSERT INTO comment (username, photoID, comment) VALUES (%s, %s,%s)"

    cursor.execute(query,(user, photoID,comment))

    query = "SELECT * FROM comment NATURAL JOIN user WHERE photoID = %s"

    cursor.execute(query,photoID)

    data = cursor.fetchall()

    cursor.close()

    return render_template("comment.html",comments = data)


@app.route("/tag", methods = ["GET","POST"])
def tag():
    photoID = request.args.get("photoID")
    query = "SELECT * FROM tagged NATURAL JOIN user WHERE tagged.photoID = %s AND tagged.tagstatus = 1"
    cursor = conn.cursor();
    cursor.execute(query, photoID)
    data = cursor.fetchall()
    cursor.close()
    return render_template("tag.html", tagPage = data)

@app.route("/tagged",methods = ["GET","POST"])
def tagged():
    photoID = request.args.get("photoID")
    taggee = request.form['taggee']
    cursor = conn.cursor();
    query = "SELECT photoPoster from photo WHERE photoID = %s"
    cursor.execute(query, (photoID))
    data = cursor.fetchall()
    if session['username'] == data[0]['photoPoster']:
        if session["username"] == taggee:
                query = "INSERT INTO Tagged (username, photoID, tagstatus) VALUES (%s, %s, %s)"
                cursor.execute(query, (session["username"], photoID, 1))
        else:
            query = "SELECT * FROM Photo JOIN user ON Photo.photoPoster=user.username WHERE photoID=%s AND " \
                    "(photoPoster IN (SELECT username_followed FROM Follow WHERE " \
                "username_follower = %s and followstatus = 1) and allFollowers = 1) OR (photoID IN (SELECT photoID FROM " \
                "belongto NATURAL JOIN sharedwith WHERE member_username = %s)) OR (photoPoster = %s) ORDER BY postingdate DESC"
            cursor.execute(query, (photoID, taggee, taggee, taggee))
            data = cursor.fetchall()
            if data:
                query = "INSERT INTO tagged (username, photoID, tagstatus) VALUES (%s, %s, %s)"
                cursor.execute(query, (taggee, photoID, 0))
            else:
                return render_template("error.html", message="Invalid Tag")
    else:
        return render_template("error.html",message = "This picture does not belong to you!")
    query = "SELECT * FROM tagged NATURAL JOIN user WHERE tagged.photoID = %s AND tagged.tagstatus = 1"
    cursor.execute(query, photoID)
    data = cursor.fetchall() 
    return render_template("tag.html",tagPage = data)

@app.route("/tagRequest",methods = ["GET","POST"])
def tagRequest():
    user = session['username']
    query = "SELECT * FROM tagged NATURAL JOIN user WHERE username = %s AND tagged.tagstatus = 0"
    cursor = conn.cursor();
    cursor.execute(query, user)
    data = cursor.fetchall()
    return render_template("tagRequest.html",tagRequest = data)

@app.route("/updateTag",methods = ["GET","POST"])
def updateTag():
    user = session['username']
    photoID = request.args.get("photoID")
    if request.form['options']:
        option = request.form['options']
        if option == '1':
            query = "UPDATE tagged SET tagstatus = %s WHERE username = %s AND photoID = %s"
            cursor = conn.cursor();
            cursor.execute(query, (option,user,photoID))
            query = "SELECT * FROM tagged NATURAL JOIN user WHERE tagged.photoID = %s AND tagged.tagstatus = 1"
            cursor.execute(query, photoID)
            data = cursor.fetchall() 
            return render_template("tag.html",tagPage = data)
        else:
            pass
    else:
        pass
    

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')
        
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)
