from flask import Flask, render_template, request
app = Flask(__name__)
notes = []
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/дневник_программиста", methods=['POST', 'GET'])
def diary():
    form_data = {
        "Содержание": request.form.get('data')
    }
    return render_template("notes.html", form_data=form_data)
if __name__ == "__main__":
    app.run(debug = True)