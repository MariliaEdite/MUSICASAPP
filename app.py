import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# Configuração do diretório do projeto e do banco de dados
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "seriedatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class Serie(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Serie: {}>".format(self.title)

# Inicializa o banco de dados e cria as tabelas
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    series = Serie.query.all()
    return render_template("index.html", series=series)

@app.route('/index', methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form.get("title")
        if title:
            try:
                serie = Serie(title=title)
                db.session.add(serie)
                db.session.commit()
            except Exception as e:
                print("Failed to add serie:", e)
    return render_template("im.html")

@app.route("/update", methods=["GET", "POST"])
def update():
    if request.method == "POST":
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        serie = Serie.query.filter_by(title=oldtitle).first()
        if serie and newtitle:
            serie.title = newtitle
            db.session.commit()
    series = Serie.query.all()
    return render_template("update.html", series=series)

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    serie = Serie.query.filter_by(title=title).first()
    if serie:
        db.session.delete(serie)
        db.session.commit()
    return redirect("/update")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
