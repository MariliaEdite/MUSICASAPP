import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "musicadatabase.db"))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Musica(db.Model):
    
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    
    def __repr__(self):
        return "<Title: {}>".format(self.title)
    
@app.route('/', methods=["GET", "POST"])
def home():
    musicas = ''
    if request.form:
        try:
            musica = Musica(title=request.form.get("title"))
            db.session.add(musica)
            db.session.commit()
        except Exception as e:
            print("Failed to add musica")
            print(e)
    musicas = Musica.query.all()
    return render_template("index.html", musicas=musicas)
    
@app.route("/update", methods=["POST"])
def update():
    try:
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        musica = Musica.query.filter_by(title=oldtitle).first()
        musica.title = newtitle
        db.session.commit()
    except Exception as e:
        print("Couldn't update musica title")
        print(e)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    musica = Musica.query.filter_by(title=title).first()
    db.session.delete(musica)
    db.session.commit()
    return redirect("/")

if __name__ == '__main__':
      app.run(debug=True, port=5000)
