
import os
import json

from flask import Flask, Response, render_template, \
				request, jsonify, url_for, send_from_directory
from db.db_models import Author, Book

app = Flask(__name__, static_folder='static', template_folder='templates')

# Common view methods.
@app.route('/')
@app.route('/index/')
def index_page():
	"""Render main (index) page."""
	return render_template('main.html')


# Methods for handlong authors.
@app.route('/xhr/html/authors/', methods=['GET'])
def prepare_authors_table():
	"""Render table with authors."""
	row_data = Author.get_all()
	rows = [{'id': el.get('id'), 'cells': [el.get('name'), el.get('surname')]} for el in row_data]
	table = {'headers': ['Name', 'Surname'],
			 'rows': rows}
	return render_template('table.html', table=table)

@app.route('/xhr/html/select/authors/', methods=['GET'])
def prepare_authors_select():
	"""Render Select-Box wirh authors."""
	data = Author.get_all()
	options = [{'id': el.get('id'), 'text': '%s %s' % (el.get('name'), el.get('surname'))} for el in data]
	select = {'id': 'book_author', 'options': options}
	return render_template('select.html', select=select)
	
@app.route('/xhr/json/authors/new/', methods=['POST'])
def new_author():
	"""POST method for handling new Author request."""
	name = request.form['name']
	surname = request.form['surname']
	id = Author.add_new(name, surname)
	return Response(json.dumps({'id': id}), mimetype='application/json')

@app.route('/xhr/json/authors/edit/', methods=['POST'])
def edit_author():
	"""POST method for handling edit Author request."""
	id = request.form['id']
	name = request.form['name']
	surname = request.form['surname']
	Author.update_by_id(id, name, surname)
	return Response(json.dumps({'ok': 'true'}), mimetype='application/json')
	
@app.route('/xhr/json/authors/delete/', methods=['POST'])
def delete_author():
	"""POST method for handling delete Author request."""
	id = request.form['id']
	Author.delete_by_id(id)
	return Response(json.dumps({'ok': 'true'}), mimetype='application/json')


#Methods for handlong Books.
@app.route('/xhr/html/books/', methods=['GET'])
def prepare_books_table():
	"""Render table with Books."""
	row_data = Book.get_all()
	rows = [{'id': el.get('id'), 'cells': [el.get('name'), '%s %s' % (el.get('author_name'), el.get('author_surname'))]} for el in row_data]
	table = {'headers': ['Name', 'Author'],
			 'rows': rows}
	return render_template('table.html', table=table)

@app.route('/xhr/json/books/new/', methods=['POST'])
def new_book():
	"""POST method for handling new Books request."""
	name = request.form['name']
	author_id = request.form['author_id']
	id = Book.add_new(name, author_id)
	return Response(json.dumps({'id': id}), mimetype='application/json')

@app.route('/xhr/json/books/edit/', methods=['POST'])
def edit_book():
	"""POST method for handling edit Books request."""
	id = request.form['id']
	name = request.form['name']
	author_id = request.form['author_id']
	Book.update_by_id(id, name, author_id)
	return Response(json.dumps({'ok': 'true'}), mimetype='application/json')
	
@app.route('/xhr/json/books/delete/', methods=['POST'])
def delete_book():
	"""POST method for handling delete Books request."""
	id = request.form['id']
	Book.delete_by_id(id)
	return Response(json.dumps({'ok': 'true'}), mimetype='application/json')


#Other methds.
@app.route('/static/css/base.css', methods=['GET'])
def base_css():
	"""Return base.css file."""
	return send_from_directory(os.path.join(app.root_path, 'static/css'),
						'base.css', mimetype='text/css')

@app.route('/static/js/book.js', methods=['GET'])
def jquery_book():
	"""Return book.js file."""
	return send_from_directory(os.path.join(app.root_path, 'static/js'),
						'book.js', mimetype='text/javascript')

@app.route('/static/images/favicon.ico')
def favicon():
	"""Return facivon.icon file."""
	return send_from_directory(os.path.join(app.root_path, 'static/images'),
						'favicon.jpeg', mimetype='image/vnd.microsoft.icon')

@app.errorhandler(404)
def page_not_found(error):
	"""Render page_not_found page in case 404 error."""
	return render_template('page_not_found.html'), 404

@app.errorhandler(500)
def page_not_found(error):
	"""Render internal_servere_error page in case 500 error."""
	return render_template('error_page.html'), 500

if __name__ == '__main__':
	app.debug = True
	app.run()

# EOF