import sqlite3

def main():
    # Connect to the book database if it does not exist it will create one.
    database = sqlite3.connect('files/Library.db')
    
    # create a data cursor
    data = database.cursor()

    # create book table
    try:
        data.execute("""
        CREATE TABLE books (
            book_name,
            book_author
        )""")
    except:
        pass

    #get book names and authors from text file.
    books_authors = []
    with open("files/books.csv") as books:
        for line in books:
            book, author = line.strip().strip("\n").split(",")
            books_authors.append((book, author))
    
    #insert book names and authors into books table
    data.executemany("INSERT INTO books VALUES (?,?)", books_authors)

    #view the first element from the database
    data.execute("SELECT * FROM books")
    print(data.fetchone(), end= "\n\n")

    #Insert a rating column into the book table.
    data.execute("""ALTER TABLE books
        ADD book_rating INTEGER""")

    #Add the ratings to the book table
    data.execute('''UPDATE books SET book_rating = abs(random() % 5) + 1''')

    #Get only the books that have a five star rating and print them to the console
    data.execute("""SELECT book_name, book_author
                    FROM books
                    WHERE book_rating = 5""")
    recomendations = data.fetchall()

    print("Your book recomendations are: ")
    for book in recomendations:
        print(f'{book[0]} by{book[1]}')

    # Add your favorite book to the database
    data.execute("""INSERT INTO books VALUES ('The Hobbit', 'J. R. R. Tolkien', 5)""")
    
    
    # delete all books that have a rating of 1
    # data.execute("""DELETE FROM books WHERE book_rating = 1""")

    # # delete the books table
    # data.execute("""DROP TABLE books""")
    
if __name__ == "__main__":
    main()