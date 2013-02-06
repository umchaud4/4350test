from flask import render_template
from lumberjack import app
from lumberjack.models.user import User

@app.route("/")
def home_index():
    return render_template("test.html")

@app.route("/users/")
def users_index():
    users = User.all()
    output = ""
    for user in users:
        output += user.user_name + "\n"
    return output
