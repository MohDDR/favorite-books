from flask_app import app
from flask import Flask, render_template, redirect, request, session
from flask_app.models import book, author

@app.route('/authors', methods = ['POST', 'GET'])
def all_authors_page():
    if request.method == 'POST':
        author.Author.create_author(request.form)
        return redirect('/authors')
    if request.method == 'GET':
        authors = author.Author.get_all_authors()
        return render_template("all_authors.html", authors=authors)

@app.route('/view/author/<id>', methods = ['POST', 'GET'])
def view_author(id):
    data = {'id' : id}
    if request.method == 'POST':
        id = author.Author.create_author_with_books(request.form)
        data = { 'id' : id }
        return redirect('/view/author/%s' %(data['id']))
    if request.method == 'GET':
        books = book.Book.get_all_books()
        this_author = author.Author.get_author_with_books(data)
        return render_template("view_author.html", author=this_author, books=books)

