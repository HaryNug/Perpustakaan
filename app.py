from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:hary300697@localhost:5432/Perpustakaan'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.String, unique=True, primary_key=True, nullable=False)
    type = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    telp = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<User{self.id}>"


class Author(db.Model):
    __tablename__ = "author"

    id = db.Column(db.String, unique=True, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    list_book = db.relationship("Book", backref="author")

    def __repr__(self):
        return f"<Author{self.id}>"


class Genre(db.Model):
    __tablename__ = "genre"

    id = db.Column(db.String, unique=True, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    list_Book = db.relationship("Book", backref="genre")

    def __repr__(self):
        return f"<Genre{self.id}>"


class Book(db.Model):
    __tablename__ = "book"

    id = db.Column(db.String, unique=True, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    genre_id = db.Column(db.String, db.ForeignKey('genre.id'), nullable=False)
    author_id = db.Column(db.String, db.ForeignKey(
        'author.id'), nullable=False)

    def __repr__(self):
        return f"<Book{self.id}>"


class Transaction(db.Model):
    __tablename__ = "transaction"

    id = db.Column(db.String, unique=True, primary_key=True, nullable=False)
    book_id = db.Column(db.String, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String, nullable=False)
    admin_approve = db.Column(db.String, nullable=True) 
    admin_return = db.Column(db.String, nullable=True)
    requested_date = db.Column(db.DateTime, nullable=False)
    approve_date = db.Column(db.DateTime, nullable=True)
    return_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<Transaction{self.id}>"


def login():
    data_email = request.authorization.username
    data_password = request.authorization.password
    user = User.query.filter_by(
        email=data_email, password=data_password).first()

    if user.type == "admin":
        return "admin"
    elif user.type == "member":
        return "member"


@app.get('/books')
def get_books():
    if login() == "admin" or login() == "member":
        book = Book.query.all()
        results = [
            {
                "id": b.id,
                "name": b.name,
                "author_id": b.author_id,
                "author_name": b.author.name,
                "genre_id": b.genre_id,
                "genre_name": b.genre.name
            }for b in book]
        return jsonify(results)
    return {"message": "invalid request"}


@app.get('/book')
def get_book():
    if login() == "admin" or login() == "member":
        data_id = request.args.get("id")
        b = Book.query.get(data_id)
        if not b:
            return {"message": "invalid request"}
        # available_id = Book.query.filter_by(id=data_id).first()
        # if not available_id:
        #     return {"error": f"book with id {data_id} not available"}
        response = {
            "id": b.id,
            "name": b.name,
            "author_id": b.author_id,
            "author_name": b.author.name,
            "genre_id": b.genre_id,
            "genre_name": b.genre.name
        }
        return {"message": "success", "book": response}
    return {"message": "invalid request"}


@app.post('/book')
def post_book():
    if login() == "admin":
        data = request.get_json()
        if any(
            [
                not "id" in data,
                not "name" in data,
                not "author_id" in data,
                not "genre_id" in data
            ]
        ):
            return {"error": "invalid request"}
        already_id = Book.query.get(data["id"])
        if already_id:
            return {"error": f"book with id {already_id.id} is available"}
        already_name = Book.query.filter_by(name=data["name"]).first()
        if already_name:
            return {"error": f"book with name {already_name.name} is available"}
        already_author_id = Author.query.get(data["author_id"])
        if not already_author_id:
            return {"error": "book with that author id not available"}
        already_genre_id = Genre.query.get(data["genre_id"])
        if not already_genre_id:
            return {"error": "book with that genre id not available"}
        new_book = Book(
            id=data['id'],
            name=data['name'],
            author_id=data['author_id'],
            genre_id=data['genre_id'])
        db.session.add(new_book)
        db.session.commit()
        return {"message": f"the book with id {new_book.id} has been successfully entered"}

    return {"message": "invalid request"}

@app.put('/book')
def put_book():
    if login()== "admin":
        data_id = request.args.get("id")
        b = Book.query.get(data_id)
        data = request.get_json()

        if not b :
            return {"error": "invalid request"}
        Author_id = Author.query.get(data["author_id"])
        if not Author_id :
            return {"error": "id with that author id not available"}
        already_genre_id = Genre.query.get(data["genre_id"])
        if not already_genre_id:
            return {"error": "id with that genre id not available"}
        # default value
        # b.id = data.get("id", b.id)
        b.name = data.get("name", b.name)
        b.author_id = data.get("author_id", b.author_id)
        b.genre_id = data.get("genre_id", b.genre_id)
        db.session.commit()
        return {"message": f"book with id {b.id} successfully updated"}
    
@app.delete('/book')
def delete_book():
    if login()== "admin":
        data_id = request.args.get("id")
        b = Book.query.get(data_id)
        if not b :
            return {"error": "invalid request"}
        db.session.delete(b)
        db.session.commit()
        return {"message": f"book with id {b.id} successfully deleted."}

@app.post('/author')
def post_author():
    if login() == "admin":
        data = request.get_json()
        if any(
            [
                not "id" in data,
                not "name" in data
                
            ]
        ):
            return {"error": "invalid request"}
        already_id = Author.query.get(data["id"])
        if already_id:
            return {"error": f"author with id {already_id.id} is already exists"}
        already_name = Author.query.filter_by(name=data["name"]).first()
        if already_name:
            return {"error": f"author with name {already_name.name} is already exists"}
        new_author = Author(
            id=data['id'],
            name=data['name'])
        db.session.add(new_author)
        db.session.commit()
        return {"message": f"author with id {new_author.id} has been successfully entered"}

    return {"message": "invalid request"}

@app.put('/author')
def put_author():
    if login()== "admin":
        data_id = request.args.get("id")
        b = Author.query.get(data_id)
        data = request.get_json()

        if not b :
            return {"error": "invalid request"}
        # already_id = Author.query.get(data["id"])
        # # if not already_id :
        # #     return {"error": "id with that author id not available"}
        already_name = Author.query.filter_by(name=data["name"]).first()
        if already_name:
            return {"error": "author name already exists"}
        # default value
        b.name = data.get("name", b.name)
        db.session.commit()
        return {"message": f"author with id {b.id} successfully updated"}
    return {"message": "invalid request"}
    
@app.delete('/author')
def delete_author():
    if login()== "admin":
        data_id = request.args.get("id")
        b = Author.query.get(data_id)
        if not b :
            return {"error": "invalid request"}
        db.session.delete(b)
        db.session.commit()
        return {"message": f"author with id {b.id} successfully deleted."}
    return {"message": "invalid request"}

@app.post('/genre')
def post_genre():
    if login() == "admin":
        data = request.get_json()
        if any(
            [
                not "id" in data,
                not "name" in data
                
            ]
        ):
            return {"error": "invalid request"}
        already_id = Genre.query.get(data["id"])
        if already_id:
            return {"error": f"genre with id {already_id.id} is already exists"}
        already_name = Genre.query.filter_by(name=data["name"]).first()
        if already_name:
            return {"error": f"genre with name {already_name.name} is already exists"}
        new_genre = Genre(
            id=data['id'],
            name=data['name'])
        db.session.add(new_genre)
        db.session.commit()
        return {"message": f"genre with id {new_genre.id} has been successfully entered"}

    return {"message": "invalid request"}

@app.put('/genre')
def put_genre():
    if login()== "admin":
        data_id = request.args.get("id")
        b = Genre.query.get(data_id)
        data = request.get_json()

        if not b :
            return {"error": "invalid request"}
        already_name = Genre.query.filter_by(name=data["name"]).first()
        if already_name:
            return {"error": "genre name already exists"}
        b.name = data.get("name", b.name)
        db.session.commit()
        return {"message": f"genre with id {b.id} successfully updated"}
    return {"message": "invalid request"}

@app.delete('/genre')
def delete_genre():
    if login()== "admin":
        data_id = request.args.get("id")
        b = Genre.query.get(data_id)
        if not b :
            return {"error": "invalid request"}
        db.session.delete(b)
        db.session.commit()
        return {"message": f"genre with id {b.id} successfully deleted."}
    return {"message": "invalid request"}

@app.post('/user')
def post_user():
    if login() == "admin":
        data = request.get_json()
        if any(
            [
                not "id" in data,
                not "type" in data,
                not "name" in data,
                not "telp" in data,
                not "email" in data,
                not "password" in data,
            ]
        ):
            return {"error": "invalid request"}
        
        already_id = User.query.get(data["id"])
        if already_id:
            return {"error": f"User with id {already_id.id} already exists"}
        
        if data["type"] not in ("admin", "member"):
            return {"error": "type is invalid"}
        
        already_telp = User.query.filter_by(telp=data["telp"]).first()
        if already_telp:
            return {"error": f"telp with number {already_telp.telp} already exists"}
        
        already_email = User.query.filter_by(email=data["email"]).first()
        if already_email:
            return {"error": f"email with {already_email.email} already exists"}
        new_user = User(
            id=data['id'],
            type = data['type'],
            name=data['name'],
            telp=data['telp'],
            email=data['email'],
            password=data['password'])
        db.session.add(new_user)
        db.session.commit()
        return {"message": f"user with id {new_user.id} has been successfully entered"}

    return {"message": "invalid request"}

@app.put('/user')
def put_user():
    if login()== "admin":
        data_id = request.args.get("id")
        b = User.query.get(data_id)
        data = request.get_json()

        if not b :
            return {"error": "invalid request"}
        
        if data["type"] not in ("admin", "member"):
            return {"error": "type is invalid"}
        
        # default value
        b.type = data.get("type", b.type)
        b.name = data.get("name", b.name)
        b.telp = data.get("telp", b.telp)
        b.email = data.get("email", b.email)
        b.password = data.get("password", b.password)
        db.session.commit()
        return {"message": f"user with id {b.id} successfully updated"}

@app.delete('/user')
def delete_user():
    if login()== "admin":
        data_id = request.args.get("id")
        b = User.query.get(data_id)
        if not b :
            return {"error": "invalid request"}
        db.session.delete(b)
        db.session.commit()
        return {"message": f"user with id {b.id} successfully deleted."}

@app.post('/transaction')
def post_transaction():
    if login() == "member":
        data = request.get_json()
        email = request.authorization.username
        member = User.query.filter_by(email=email).first_or_404()
        if any(
            [
                not "id" in data,
                not "book_id" in data
            ]
        ):
            return {"error": "invalid request"}
        
        new_transaction = Transaction(
            id=data['id'],
            book_id = data['book_id'],
            user_id=member.id,
            requested_date = datetime.today(),
            status = "Requested")
        db.session.add(new_transaction)
        db.session.commit()
        return {"message": f"Transaction with id {new_transaction.id} has been successfully entered"}

    return {"message": "invalid request"}



if (__name__) == ("__main__"):
    app.run(debug=True)
