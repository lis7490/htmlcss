from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    text = db.Column(db.String(256), nullable=False)
    def __repr__(self):
        return f'<Note {self.title}>'


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/дневник_программиста", methods=['POST', 'GET'])
def diary():
    if request.method == 'POST':
        # Создание новой записи
        title = request.form.get('title', '').strip()
        text = request.form.get('text', '').strip()

        if title and text:
            new_note = Notes(title=title, text=text)
            db.session.add(new_note)
            db.session.commit()
            return redirect(url_for('diary'))  # Перенаправление чтобы избежать повторной отправки формы

    # Получение всех записей из базы данных
    all_notes = Notes.query.order_by(Notes.id.desc()).all()  # Сортировка по ID в обратном порядке

    return render_template("notes.html", notes=all_notes)


@app.route("/удалить_запись/<int:note_id>", methods=['POST'])
def delete_note(note_id):
    # Находим запись по ID
    note_to_delete = Notes.query.get_or_404(note_id)

    # Удаляем запись
    db.session.delete(note_to_delete)
    db.session.commit()

    return redirect(url_for('diary'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)