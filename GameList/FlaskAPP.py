from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
db = SQLAlchemy(app)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        year = request.form['year']
        new_game = Game(name=name, year=year)
        db.session.add(new_game)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        games = Game.query.all()
        return render_template('index.html', games=games)


@app.route('/clear', methods=['POST'])
def clear():
    Game.query.delete()
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)