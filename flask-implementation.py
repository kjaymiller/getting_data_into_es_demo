import os
from connection import client
from elasticsearch_dsl import (
    Document,
    Search,
    Text,
    Date,
)
from elasticsearch_dsl.query import MultiMatch
from flask import (
    Flask,
    render_template,
    request,
)
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    DateTimeField,
)
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField

from datetime import datetime
from dateutil import parser

app = Flask(__name__)
app.secret_key = os.urandom(16)


@app.template_filter("datetime")
def format_datetime(value):
    dt = parser.parse(value)
    return datetime.strftime(dt, "%Y %b %d %X")


class CatReport(Document):
    cat = Text()
    action = Text()
    comment = Text()
    date = Date()

    class Index:
        name = "cat_data"
        using = client


class MyForm(FlaskForm):
    cat = StringField("cat", validators=[DataRequired()])
    comment = TextAreaField("comment", validators=[DataRequired()])
    date = DateTimeField(
        validators=[DataRequired()],
        default=datetime.today,
    )
    action = SelectField("action", choices=["good", "bad"])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search")
def search():
    query = request.args.get("query")
    s = Search(using=client, index="cat_data").sort('-date')
    m = MultiMatch(query=query, fields=["cat", "comment", "action"])
    s = s.query(m)
    results = s.execute()
    return render_template(
        "search.html",
        results=results,
        query=query,
    )


@app.route("/create", methods=["GET", "POST"])
def create():
    form = MyForm()
    if request.method == "POST":
        if form.validate_on_submit():
            report = CatReport(
                cat=form.cat.data,
                action=form.action.data,
                comment=form.comment.data,
                date=form.date.data,
            )
            report.save()

            return render_template("edit_entry.html", form=form)

    else:

        return render_template("edit_entry.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
