from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:<password>@localhost:5432/test_library'
db = SQLAlchemy(app)


class Author(db.Model):
	"""Represent Authors data.
	To avoid situation when deletin Author who has Book,
	there is 'saved' flag. This flag show if Author is saved or deleted."""
	__tablename__ = 'authors'
	__table_args__ = {'sqlite_autoincrement': True}
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30))
	surname = db.Column(db.String(30))
	saved = db.Column(db.Boolean)

	def __init__(self, name, surname):
		self.name = name
		self.surname = surname
		self.saved = True

	def __repr__(self):
		return '<Id %s, Name %s, Surname %s>' % \
			(self.id, self.name, self.surname)

	def _to_dict(self):
		"""All data returns as dict. It prowide flaxebility 
		when migrate from ORM to standat SQL requests."""
		return {'id': self.id,
				'name': self.name,
				'surname': self.surname}

	@classmethod
	def get_all(cls):
		"""Return all Authors marked as `saved=True`"""
		res = Author.query.filter_by(saved=True) or []
		return [el._to_dict() for el in res]

	@classmethod
	def add_new(cls, name, surname):
		"""Create new Author record or restore old if coresponding
		exists with flag `saved=False`."""
		author = Author.query.filter_by(name=name, surname=surname).first()
		if author:
			# Restore old.
			author.saved = True
		else:
			# Create new record.
			author = Author(name, surname)
			db.session.add(author)
		db.session.commit()
		return author.id

	@classmethod
	def update_by_id(cls, id, name, surname):
		"""Update Authors data by ID."""
		author = Author.query.get(id)
		author.name = name
		author.surname = surname
		db.session.commit()

	@classmethod
	def delete_by_id(cls, id):
		"""Set flag `saved` to False by ID."""
		author = Author.query.get(id)
		author.saved = False
		db.session.commit()


class Book(db.Model):
	"""Represent Books data."""
	__tablename__ = 'books' 
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30))
	authors_id = db.Column(db.Integer, db.ForeignKey("authors.id"))

	def __init__(self, name, author_id):
		self.name = name
		self.authors_id = author_id

	def __repr__(self):
		return '<ID %s, Name %s, AuthorID %s>' % \
			(self.id, self.name, self.authors_id)

	def _to_dict(self):
		"""Book object to dict."""
		author = Author.query.get(self.authors_id)
		return {'id': self.id,
				'name': self.name,
				'author_id': self.authors_id,
				'author_name': author.name,
				'author_surname': author.surname}

	@classmethod
	def get_all(cls):
		"""Return all Book data."""
		return [el._to_dict() for el in Book.query.all()]

	@classmethod
	def add_new(cls, name, author_id):
		"""Create new Book record."""
		book = Book(name, author_id)
		db.session.add(book)
		db.session.commit()
		return book.id

	@classmethod
	def update_by_id(cls, id, name, author_id):
		"""Update Book data  by ID."""
		book = Book.query.get(id)
		book.name = name
		book.authors_id = author_id
		db.session.commit()

	@classmethod
	def delete_by_id(cls, id):
		"""Delete Book data by ID."""
		book = Book.query.get(id)
		db.session.delete(book)
		db.session.commit()

# EOF