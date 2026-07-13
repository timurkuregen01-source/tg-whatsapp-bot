from flask import Flask, render_template
from services.database import get_representatives

app = Flask(__name__)


@app.route("/")
def index():
    reps = get_representatives()
    return render_template("index.html", representatives=reps)


if __name__ == "__main__":
    app.run(debug=True)