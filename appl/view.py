from flask import render_template, redirect, url_for, flash, request
from appl.acccount_serv import create_user, verify_hash
from appl.app import app,graph
from flask_login import current_user, login_user, logout_user, login_required
from appl.models import repo,Movie,Actor,User,Director,Genre
from werkzeug.urls import url_parse
from random import randint



@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    movie = list()
    q = list()
    while len(q) < 5:
        b = randint(1,4364)
        if not b in q:
            q.append(b)
    for i in q:
        a = f's{i}'
        b = repo.match(Movie, a).first()
        movie.append(b)
    return render_template("index.html",movie = movie)


@app.route('/register', methods=['GET'])
def register_get():
    return render_template("register.html")


@app.route('/register', methods=['POST'])
def register_post():
    name = request.form.get('name')
    email = request.form.get('email').lower().strip()
    password = request.form.get('password').strip()
    confirm = request.form.get('confirm').strip()
    if not name or not email or not password or not confirm:
        flash("Please populate all the registration fields", "error")
        return render_template("register.html", name=name, email=email, password=password, confirm=confirm)
    if password != confirm:
        flash("Passwords do not match")
        return render_template("register.html", name=name, email=email)
    user = create_user(name, email,password)
    if not user:
        flash("A user with that email already exists.")
        return render_template("register.html", name=name, email=email)
    return render_template("register.html")


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.form != {}:
        email = request.form['email']
        password = request.form['password']
        if not email or not password:
            return render_template("login.html", email=email, password=password)
        user = repo.match(User, email).first()
        if not user:
            return render_template("login.html")
        if not verify_hash(user.hashed_password, password):
            return render_template("login.html")
        login_user(user, remember=True)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("login.html")



@app.route('/logout')
def logout():
    logout_user()
    return redirect (url_for ("index"))


@login_required
@app.route('/item/<id>', methods=['post', 'get'])
def movie_page(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    d = repo.match(Movie, id).first()
    if request.form != {}:
        b = repo.match(User, current_user.email).first()
        for q in b.rated_in:
            if q.show_id == id:
                return redirect(url_for("index"))
        b.rated_in.add(d)
        graph.push(b)
        return redirect(url_for("index"))
    return render_template("movie_page.html",movie = d)


@login_required
@app.route('/recomend', methods=['post', 'get'])
def recomend():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    b = repo.match(User, current_user.email).first()
    a = list()
    a1 = list()
    for q in b.rated_in:
        a1.append(q.show_id)
        dir = repo.match(Director, q.director).first()
        for mov in dir.directed:
            if not mov.show_id in a1:
                a1.append(mov.show_id)
                a.append(mov)
        i = 0
        for cast in mov.cast.split(', '):
            if i == 3:
                break
            dir = repo.match(Actor, cast).first()
            for mov in dir.acted_in:
                if not mov.show_id in a1:
                    a1.append(mov.show_id)
                    a.append(mov)
            i+=1
        for cast in mov.genre.split(', '):
            i = 0
            dir = repo.match(Genre, cast).first()
            for mov in dir.genre_in:
                if i == 3:
                    break
                if not mov.show_id in a1:
                    a1.append(mov.show_id)
                    a.append(mov)
                i += 1

    result= list()
    q = list()
    count = 10
    if len(a)<10:
        count = len(a)
    while len(q) < count:
        b = randint(0, count-1)
        if not b in q:
            q.append(b)
    for i in q:
        result.append(a[i])
    return render_template("recomend.html",movie = result)




