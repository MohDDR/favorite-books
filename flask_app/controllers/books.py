from flask_app import app
from flask import Flask, render_template, redirect, request, session
from flask_app.models import book, author

@app.route('/books', methods = ['POST', 'GET'])
def all_books_page():
    if request.method == 'POST':
        book.Book.create_book(request.form)
        return redirect('/books')
    if request.method == 'GET':
        books = book.Book.get_all_books()
        return render_template("all_books.html", books=books)

@app.route('/view/book/<id>', methods = ['POST', 'GET'])
def view_book(id):
    data = {'id' : id}
    if request.method == 'POST':
        id = book.Book.create_book_with_authors(request.form)
        print('hdidhcisbhbidshi ',id)
        data = { 'id' : id }
        return redirect('/view/book/%s' %(data['id']))
    if request.method == 'GET':
        authors = author.Author.get_all_authors()
        this_book = book.Book.get_book_with_authors(data)
        return render_template("view_book.html", book=this_book, authors=authors)
