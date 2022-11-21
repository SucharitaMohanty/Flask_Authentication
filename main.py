from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, UserMixin, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "984rohrjknfr239thjfds"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

login_maganer = LoginManager(app)

@login_maganer.user_loader
def load_user(user_id):
    return User.query.get(user_id)

db = SQLAlchemy(app)

# Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html", user = current_user)

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        if password == confirm_password:
            if not User.query.filter_by(email = email).first():
                new_user = User(
                    email = email,
                    password = generate_password_hash(password=password, salt_length=8),
                )
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for('profile'))
            else:
                return "User already exits"
        else:
            return "<h1>Password Didnot match</h1>"
    return render_template("signup.html")

@app.route("/signin", methods = ["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('profile'))
            else:
                return "Password did't match"
        else:
            return redirect(url_for("signup"))
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user = current_user)

if __name__ == "__main__":
    app.run(debug=True)