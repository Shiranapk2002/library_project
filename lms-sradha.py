import mysql.connector

# Connect to the database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="232003",
    database="lib_mng"
)
cursor = db.cursor()


def admin_menu():
    while True:
        print("\n\t\tAdmin Menu")
        print("1. Add Book")
        print("2. Delete Book")
        print("3. Update Book")
        print("4. View Book Details")
        print("5. View User Details")
        print("6. Back to main menu ")
        choice = input("Enter your choice: ")
        if choice == "1":
            add_book()
        elif choice == "2":
            delete_book()
        elif choice == "3":
            update_book()
        elif choice == "4":
            view_books()
        elif choice == "5":
            view_users()
        elif choice == "6":
            print("Logging out.")
            break
        else:
            print("Invalid choice. Please choose a valid option.")


def admin_login():
    admin_username = input("Admin Username: ")
    admin_password = input("Admin Password: ")

    query = "SELECT * FROM admin WHERE username = %s AND password = %s"
    values = (admin_username, admin_password)
    cursor.execute(query, values)

    admin_data = cursor.fetchone()
    if admin_data:
        print("Admin login successful.")
        admin_menu()
    else:
        print("Invalid admin credentials.")
        create_account = input("Do you want to create an admin account? (yes/no): ")
        if create_account.lower() == "yes":
            create_admin()


def create_admin():
    admin_username = input("Enter a new admin username: ")
    admin_password = input("Enter a new admin password: ")

    query = "INSERT INTO admin (username, password) VALUES (%s, %s)"
    values = (admin_username, admin_password)
    cursor.execute(query, values)
    db.commit()
    print("Admin account created successfully!")


def user_login():
    username = input("Username: ")
    password = input("Password: ")

    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    values = (username, password)
    cursor.execute(query, values)

    user_data = cursor.fetchone()
    if user_data:
        print("User login successful.")
        user_menu(user_data[0])
    else:
        print("Invalid user credentials.")


def register_user():
    username = input("Enter a username: ")
    password = input("Enter a password: ")

    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    values = (username, password)
    cursor.execute(query, values)
    db.commit()
    print("User registered successfully!")


def user_menu(user_id):
    while True :
        print("\n\t\t WELCOME  ")
        print("1. Search Books")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            search_books()
        elif choice == "2":
            issue_book(user_id)
        elif choice == "3":
            return_book(user_id)
        elif choice == "4":
            print("Logging out....HAVE A NICE DAY")
            break
        else:
            print("Invalid choice. Please choose a valid option.")


def search_books():
    title_keyword = input("Enter a keyword in the title: ")

    query = "SELECT * FROM books WHERE title LIKE %s"
    values = ('%' + title_keyword + '%',)
    cursor.execute(query, values)

    books = cursor.fetchall ( )
    if books :
        print ( "Search results:" )
        for book_id , title , author , category_id , quantity , available in books :
            print ( "Book ID:" , book_id )
            print ( "Title:" , title )
            print ( "Author:" , author )
            print ( "Category ID:" , category_id )
            print ( "Quantity:" , quantity )
            print ( "Available:" , available )
            print ( )

    else :
        print ( "No matching books found." )


def issue_book(user_id):
    book_id = input("Enter the Book ID you want to issue: ")

    query = "SELECT * FROM books WHERE book_id = %s"
    values = (book_id,)
    cursor.execute(query, values)

    book_data = cursor.fetchone()
    if book_data:
        if book_data[4] > 0:  # Check quantity
            query = "UPDATE books SET quantity = quantity - 1 WHERE book_id = %s"
            cursor.execute(query, (book_id,))
            db.commit()

            query = "INSERT INTO issued_books (user_id, book_id) VALUES (%s, %s)"
            values = (user_id, book_id)
            cursor.execute(query, values)
            db.commit()
            print("Book issued successfully!")

            update_available_column()  # Update the 'available' column
        else:
            print("Sorry, the book is not available.")
    else:
        print("Book not found.")


def return_book(user_id):
    book_id = input("Enter the Book ID you want to return: ")

    query = "SELECT * FROM issued_books WHERE user_id = %s AND book_id = %s"
    values = (user_id, book_id)
    cursor.execute(query, values)

    issued_book_data = cursor.fetchone()
    if issued_book_data:
        query = "UPDATE books SET quantity = quantity + 1 WHERE book_id = %s"
        cursor.execute(query, (book_id,))
        db.commit()

        query = "DELETE FROM issued_books WHERE user_id = %s AND book_id = %s"
        cursor.execute(query, values)
        db.commit()
        print("Book returned successfully!")

        update_available_column()  # Update the 'available' column
    else:
        print("You have not issued this book.")


def view_users () :
    cursor.execute ( "SELECT id, username FROM users" )
    users = cursor.fetchall ( )

    for user_id , username in users :
        print ( "User ID:" , user_id )
        print ( "Username:" , username )

        # Retrieve issued books for the user
        query_issued = "SELECT books.title FROM books JOIN issued_books ON books.id = issued_books.book_id WHERE issued_books.user_id = %s"
        values_issued = (user_id ,)
        cursor.execute ( query_issued , values_issued )
        issued_books = cursor.fetchall ( )

        if issued_books :
            print ( "Issued Books:" )
            for book_title in issued_books :
                print ( "- " , book_title[0] )
        else :
            print ( "No issued books." )

        # Retrieve returned books for the user
        query_returned = "SELECT books.title FROM books JOIN returned_books ON books.id = returned_books.book_id WHERE returned_books.user_id = %s"
        values_returned = (user_id ,)
        cursor.execute ( query_returned , values_returned )
        returned_books = cursor.fetchall ( )

        if returned_books :
            print ( "Returned Books:" )
            for book_title in returned_books :
                print ( "- " , book_title[0] )
        else :
            print ( "No returned books." )

        print ( )


def add_book():
    title = input("Enter the title of the book: ")
    author = input("Enter the author of the book: ")
    category = input("Enter the category of the book: ")
    quantity = int(input("Enter the quantity of the book: "))
    available = 'yes' if quantity > 0 else 'no'

    query = "INSERT INTO books (title, author, category, quantity, available) VALUES (%s, %s, %s, %s, %s)"
    values = (title, author, category, quantity, available)
    cursor.execute(query, values)
    db.commit()
    print("Book added successfully!")


def update_book():
    book_id = int(input("Enter the ID of the book to update: "))
    new_quantity = int(input("Enter the new quantity of the book: "))

    query = "UPDATE books SET quantity = %s WHERE id = %s"
    values = (new_quantity, book_id)
    cursor.execute(query, values)
    db.commit()
    print("Book quantity updated successfully!")


def view_books():
    cursor.execute ( "SELECT * FROM books" )
    books = cursor.fetchall ( )

    print ( "\nBook Details:" )
    for book in books :
        book_id , title , author , category , quantity , available = book
        print ( "Book ID:" , book_id )
        print ( "Title:" , title )
        print ( "Author:" , author )
        print ( "Category:" , category )
        print ( "Quantity:" , quantity )
        print ( "Available:" , available )
        print ( )


def delete_book():
    book_id = int(input("Enter the ID of the book to delete: "))

    query = "DELETE FROM books WHERE id = %s"
    values = (book_id,)
    cursor.execute(query, values)
    db.commit()
    print("Book deleted successfully!")


def update_available_column():
    query = "UPDATE books SET available = CASE WHEN quantity > 0 THEN 'yes' ELSE 'no' END"
    cursor.execute(query)
    db.commit()
    print("Available column updated successfully!")



while True:
    print("\n---LIBRARY MANAGEMENT SYSTEM--- ")
    print("\t1. The Librarian ")
    print("\t2. User Login")
    print("\t3. Register User")
    print("\t4. Exit")
    print()

    choice = input("Enter your choice: ")

    if choice == "1":
        admin_login()
    elif choice == "2":
        user_login()
    elif choice == "3":
        register_user()
    elif choice == "4":
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please choose a valid option.")


db.close()





