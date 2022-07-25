from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author
#from datetime import datetime

class Book:

    DB = 'books'

    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.authors_who_recommended = []

    @classmethod
    def get_all_books(cls):
        query = """
        SELECT * FROM books
        ;"""
        results = connectToMySQL(cls.DB).query_db(query)
        books = []
        for book in results:
            books.append( cls(book) )
        return books

    @classmethod
    def get_book_with_authors(cls, data):
        query = """
        SELECT * FROM books 
        LEFT JOIN favorites ON favorites.book_id = books.id 
        LEFT JOIN authors ON favorites.author_id = authors.id 
        WHERE books.id = %(id)s;
        ;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        book = cls( results[0] )
        for row in results:
            author_data = {
                'id' : row['authors.id'],
                'name' : row['name'],
                'created_at' : row['authors.created_at'],
                'updated_at' : row['authors.updated_at']
            }
            book.authors_who_recommended.append( author.Author( author_data ) )
        return book

    @classmethod
    def create_book(cls, data ):
        query = """
        INSERT INTO books 
        ( title , num_of_pages , created_at, updated_at ) 
        VALUES ( %(title)s , %(num_of_pages)s , NOW() , NOW() )
        ;"""
        connectToMySQL(cls.DB).query_db( query, data )

    @classmethod
    def create_book_with_authors(cls, data):
        query = """
        SELECT * FROM favorites
        WHERE author_id = %(author_id)s
        && book_id = %(book_id)s
        ;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        if results == ():
            query = """
            INSERT INTO favorites 
            ( author_id, book_id ) 
            VALUES ( %(author_id)s, %(book_id)s )
            ;"""
            connectToMySQL(cls.DB).query_db( query, data )
            return data['book_id']
        else:
            return results[0]['book_id']


#    @classmethod
#    def update(cls, data, userId):
#        query = "Update users SET first_name = %(fname)s, last_name = %(lname)s, email = %(email)s, updated_at = NOW() where id=" + userId + ";"
#        return connectToMySQL('users').query_db( query, data )
#    @classmethod
#    def delete(cls, userId):
#        query = "DELETE FROM users WHERE id =%s;" %userId
#        return connectToMySQL('users').query_db( query )