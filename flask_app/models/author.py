from pickle import FALSE
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book
#from datetime import datetime

class Author:

    DB = 'books'

    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.fav_books = []

    @classmethod
    def get_all_authors(cls):
        query = """
        SELECT * FROM authors
        ;"""
        results = connectToMySQL(cls.DB).query_db(query)
        authors = []
        for author in results:
            authors.append( cls(author) )
        return authors

    @classmethod
    def get_author_with_books(cls, data):
        query = """
        SELECT * FROM authors 
        LEFT JOIN favorites ON favorites.author_id = authors.id 
        LEFT JOIN books ON favorites.book_id = books.id 
        WHERE authors.id = %(id)s;
        ;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        author = cls( results[0] )
        for row in results:
            book_data = {
                "id" : row["books.id"],
                "title" : row["title"],
                "num_of_pages" : row["num_of_pages"],
                "created_at" : row["books.created_at"],
                "updated_at" : row["books.updated_at"]
            }
            author.fav_books.append( book.Book( book_data ) )
        return author
    
    @classmethod
    def create_author(cls, data ):
        query = """
        INSERT INTO authors 
        ( name , created_at, updated_at ) 
        VALUES ( %(name)s , NOW() , NOW() )
        ;"""
        connectToMySQL(cls.DB).query_db( query, data )

    @classmethod
    def create_author_with_books(cls, data):
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
            return data['author_id']
        else:
            return results[0]['author_id']

#    @classmethod
#    def update(cls, data, userId):
#        query = "Update users SET first_name = %(fname)s, last_name = %(lname)s, email = %(email)s, updated_at = NOW() where id=" + userId + ";"
#        return connectToMySQL('users').query_db( query, data )
#    @classmethod
#    def delete(cls, userId):
#        query = "DELETE FROM users WHERE id =%s;" %userId
#        return connectToMySQL('users').query_db( query )