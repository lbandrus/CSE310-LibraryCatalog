from select import select
import sqlite3

#
class Database:

    def __init__(self, location):
        """Creates a database at the location given if a database does not exist
        otherwise connects to the database that exists.
        
        Args:
            location: A string that gives the location of the database.
        """
        self.database = sqlite3.connect(location)
        self.c = self.database.cursor()

    def create_table(self, name, columns):
        """Creates a table in the selected database
        
        Args:
            name: A string that gives the table its name.
            columns: A string the gives the columns its names. (seperate with commas)
        """
        try:
            all_columns = "".join(str(f"{i}, ") for i in columns)
            self.c.execute(f"""
            CREATE TABLE {name} (
                {all_columns}
            )""")
        except:
            pass

    def delete_table(self, table):
        """Deletes a table in the selected database
        
        Args:
            table: A String of the name of the table being deleted
        """
        self.c.execute(f"""DROP TABLE {table}""")

    def print_all(self, table):
        """Prints all of the data from a table.
        
        Args:
            table: A String that is used to query all of the data from the given table.
        """
        self.c.execute(f"""SELECT *
                            FROM {table}""")
        data = self.c.fetchall()
        for row in data:
            for value in row:
                print(f"| {value} |", end=" ")
            print()

    def insert_row(self, table, row_data):
        """Inserts a row into the selected table.
        
        Args:
            table: A String that tells the query where the data is being inserted.
            row_data: A Tuple that adds the data to a single row of data.
        """
        row = "(" +"".join(f"\'{str(i)}\', " for i in row_data)[0:-2] + ")"
        print(row)
        self.c.execute(f"""INSERT INTO {table} VALUES {row}""")

    def insert_many_rows(self, table, data):
        """Inserts many rows into the selected table.
        
        Args:
            table: A String that tells the query where the data is being inserted.
            data: List of Tuples adds each tuple of data into its own row.
        """
        num_of_columns = "(" + "".join(str(f"?,") for i in data[0])[0:-1] + ")"
        self.c.executemany(f"INSERT INTO {table} VALUES {num_of_columns}", books_authors)

    def add_column(self, table, column, datatype=None):
        """Adds a new column to the table selected
        
        Args:
            table: A String that tells what what table the column will be added to.
            column: A String that names the column being added.
        """
        command = f"""ALTER TABLE {table}
                            ADD {column}"""
        if datatype != None:
            command += f" {datatype}"

        self.c.execute(command)

    def select(self, table, columns="All", condition=None):
        """Selects data from the table
        
        Args:
            table: A String that selects the table to be queried from.
            columns: A string that selects what columns should be queried.
            condition: If a string is added it will add a where clause.
        """
        command = ""
        if columns == "All":
            command += f"""SELECT * FROM {table}"""
        else:
            command += f"""SELECT {columns} FROM {table}"""
        if condition is not None:
            command += f" WHERE {condition}"
        
        self.c.execute(command)

        return self.c.fetchall()
        
    def custom_query(self, query, many=False):
        """Allows custom queries to be made to a database.
        
        Args:
            query: A String the is the SQL query
            many: Boolean the sets the mode for the query.
        """
        if many:
            self.c.executemany(query)
        else:
            self.c.execute(query)
        return self.c.fetchall()

    def connect(self, location):
        """Connects to a different database with the location given. If no 
        database matching the location exists then it will create a database.
        
        Args:
            location: A string stating the location of the database.
        """
        self.database.close()
        self.database = location
        self.c = self.database.cursor()

    def close(self):
        """Closes the connection to the selected database."""
        self.database.close()

    

books_authors = []

with open("files/books.csv") as books:
    for line in books:
        book, author = line.strip().strip("\n").split(", ")
        books_authors.append((book, author))


lib = Database('files/Library.db') 
lib.create_table("books", ('book_name', 'book_authors'))
lib.insert_many_rows("books", books_authors)
lib.print_all("books")
lib.insert_row("books", ('The Hobbit', 'J. R. R. Tolkien'))
lib.print_all("books")