from app import app, db
from flask import render_template, request, Response, json, redirect, flash
from app.models import User, Course, Enrollment
from app.forms import LoginForm, RegisterForm


courseData = [{"courseID":"1111","title":"PHP 111","description":"Intro to PHP","credits":"3","term":"Fall, Spring"},
              {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":"4","term":"Spring"},
              {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":"3","term":"Fall"},
              {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":"3","term":"Fall, Spring"},
              {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":"4","term":"Fall"
             }]


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.objects(email=email).first()
        if user and user.get_password(password):
            flash(f"{user.first_name}, you are successfully logged in!", "success")
            return redirect("/index")
        else:
            flash("Sorry, something went wrong.", "danger")
    return render_template("login.html", title="Login", form=form, login=True)

@app.route("/courses/")
@app.route("/courses/<term>")
def courses(term="Spring 2019"):
    return render_template("courses.html", courseData=courseData, courses=True, term=term )

@app.route("/register")
def register():
    return render_template("register.html", register=True)

@app.route("/enrollment", methods=["GET", "POST"])
def enrollment():
    id = request.form.get('courseID')
    title = request.form['title']
    term = request.form.get('term')
    return render_template("enrollment.html", register=True, enrollment=True, data={"id":id, "title":title, "term":term})

@app.route("/api/")
@app.route("/api/<idx>")
def api(idx=None):
    if (idx == None):
        jdata = courseData
    else:
        jdata = courseData[int(idx)]

    return Response(json.dumps(jdata), mimetype="app/json")


class User(db.Document):
    user_id = db.IntField(unique=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    email = db.StringField(max_length=30)
    password = db.StringField(max_length=30)


@app.route("/user")
def user():
    # User(user_id=1, first_name="Slava", last_name="Lav", email="lav@lav.com", password="12345").save()
    # User(user_id=2, first_name="Dash", last_name="Kol", email="kol@kol.com", password="1234567").save()
    users = User.objects.all()
    return render_template("user.html", users=users)

