// General functions.
function loadTables(){
	//Reload all data.
	validateAuthorForm();
	validateBookForm();
	loadAuthorsTable();
	loadBooksTable();
};

function onClickTbl(table, callback_func){
	// onClick handler for table rows.
	$(table.find('tr')).click(function(event) {
		$(table.find('.selected')).removeClass('selected');
		$(this).addClass('selected');
		callback_func();
	});
};

// Function related to Authors.
function loadAuthorsTable(){
	// Load Authors table.
	$('#authors_table').load('/xhr/html/authors/', function(){
		$('#author_editor').css('display', 'none');
		$('#author_editor_fields input').val('');
		$('#edit_btn_author').attr('disabled', 'disabled');
		$('#delete_btn_author').attr('disabled', 'disabled');
		onClickTbl($('#authors_table'), openEditBtnAuthor);
	});
};

function validateAuthorForm(){
	$("#edit_author_form").validate({
	rules: {
		author_name: "required",
		author_surname: "required"
	},
	submitHandler: function(form) {
		saveAuthor();
	}});
};

function openEditBtnAuthor(){
	// Callback for selecting row in Authors table.
	$('#edit_btn_author').removeAttr('disabled');
	$('#delete_btn_author').removeAttr('disabled');
	$('#author_id').val($('#authors_table tr.selected').attr('id'));
};

function newAuthor(){
	// New Author button click. 
	$('#author_editor').css('display', 'block');
	$('#author_editor_fields input').val('');
	$('#author_id').val('');
};

function editAuthor(){
	// Edit Author button click. 
	var row = $('#authors_table tr.selected');
	$('#author_editor').css('display', 'block');
	$('#author_id').val($(row).attr('id'));
	$('#author_name').val($(row.find('td')[0]).text());
	$('#author_surname').val($(row.find('td')[1]).text());
};

function deleteAuthor(){
	// Delete Author button click. 
	if(confirm('Do you really want to delete this Author?')){
		$.post('/xhr/json/authors/delete/', {'id': $('#author_id').val()}, function(data){
			loadTables();
		});
	};
};

function cancelAuthor(){
	// Cancel Author button click. 
	$('#author_editor').css('display', 'none');
	$('#author_editor_fields input').val('');
};

function saveAuthor(){
	// Save Author button click. 
	var id = $('#author_id').val();
	data = {'name': $('#author_name').val(),
			'surname': $('#author_surname').val()}
	if(id){
		// Editing.
		data['id'] = id;
		$.post('/xhr/json/authors/edit/', data, function(data){
			loadTables();
		});
	} else {
		// Saving new.
		$.post('/xhr/json/authors/new/', data, function(data){
			loadTables();
		});
	};
};


// Functions for handling Books;
function loadBooksTable(){
	// Load Books table.
	$('#books_table').load('/xhr/html/books/', function(){
		$('#book_editor').css('display', 'none');
		$('#book_editor_fields input').val('');
		$('#edit_btn_book').attr('disabled', 'disabled');
		$('#delete_btn_book').attr('disabled', 'disabled');
		onClickTbl($('#books_table'), openEditBtnBook);
	});
	// Load Authors select-box.
	$('#book_author_div').load('/xhr/html/select/authors/');
};

function validateBookForm(){
	$("#edit_book_form").validate({
	rules: {
		book_name: "required",
		book_author: "required"
	},
	submitHandler: function(form) {
		saveBook();
	}});
};

function openEditBtnBook(){
	// Callback for selecting row in Book table.
	$('#edit_btn_book').removeAttr('disabled');
	$('#delete_btn_book').removeAttr('disabled');
	$('#book_id').val($('#books_table tr.selected').attr('id'));
};

function newBook(){
	// New Book button click. 
	$('#book_id').val('');
	$('#book_editor').css('display', 'block');
	$('#book_editor_fields input').val('');
	$('#book_author option').removeAttr('selected');
};

function editBook(){
	// Edit Book button click. 
	var row = $('#books_table tr.selected');
	$('#book_editor').css('display', 'block');
	$('#book_id').val($(row).attr('id'));
	$('#book_name').val($(row.find('td')[0]).text());
	$('#book_author option[value="'+$(row.find('td')[1]).text()+'"]').attr('selected', 'selected');
};

function deleteBook(){
	// Delete Book button click. 
	if(confirm('Do you really want to delete this Book?')){
		$.post('/xhr/json/books/delete/', {'id': $('#book_id').val()}, function(data){
			loadTables();
		});
	};
};

function cancelBook(){
	// Cancel Book button click. 
	$('#book_editor').css('display', 'none');
	$('#book_editor_fields input').val('');
	$('#book_editor select').removeAttr('selected');
};

function saveBook(){
	// Save Book button click. 
	var id = $('#book_id').val();
	var sel_id = $('#book_author option:selected').attr('id');
	data = {'name': $('#book_name').val(), 'author_id': sel_id};
	if(id){
		// Editing.
		data['id'] = id;
		$.post('/xhr/json/books/edit/', data, function(data){
			loadTables();
		});
	} else {
		// Saving new.
		$.post('/xhr/json/books/new/', data, function(data){
			loadTables();
		});
	};
};

// EOF