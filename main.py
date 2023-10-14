from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"

# Create the extension
db = SQLAlchemy()
# Initialise the app with the extension
db.init_app(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'

with app.app_context():
    db.create_all()

# all_books = [{
#     "title": "Harry Potter",
#     "author": "J. K. Rowling",
#     "rating": 9,
# }, {
#     "title": "Jungle Book",
#     "author": "R. Kipling",
#     "rating": 10,
# }]
all_books =[]

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method.upper() == "GET":
        with app.app_context():
            all_books = Book.query.all()
        # for book in all_books:
        #     print(f"Title: {book.title}, Author: {book.author}, Rating: {book.rating}")
        return render_template("index.html",books=all_books)
    elif request.method.upper() == "POST":
        title = request.form.get("Title")
        author = request.form.get("Author")
        rating = request.form.get("Rating")
        with app.app_context():
            new_book = Book(title=title, author=author, rating=rating)
            db.session.add(new_book)
            db.session.commit()

        #print(title,author,rating)

        return render_template("add.html")


@app.route("/add")
def add():
    return render_template("add.html")

@app.route("/delete")
def delete():
    book_id = request.args.get('id')
    with app.app_context():
        book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
        db.session.delete(book_to_delete)
        db.session.commit()

    with app.app_context():
        all_books = Book.query.all()
    return render_template("index.html", books=all_books)

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method.upper() == "GET":
        book_id = request.args.get('id')
        book_selected = db.get_or_404(Book, book_id)
        return render_template("edit.html",book=book_selected)
    elif request.method.upper() == "POST":
        new_rating = request.form.get('new_rating')
        book_id = request.form.get('book_id')

        print(book_id)

        with app.app_context():
            book_to_update = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
            book_to_update.rating = new_rating
            db.session.commit()

            all_books = Book.query.all()
        return render_template("index.html",books=all_books)

if __name__ == "__main__":
    app.run(debug=True)
