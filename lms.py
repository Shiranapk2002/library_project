import mysql.connector

connection = mysql.connector.connect (
    host="localhost" ,
    user="root" ,
    password="232003" ,
    database="lms"
)


def create_tables () :
    cursor = connection.cursor ( )
    create_admins_table = """
    CREATE TABLE IF NOT EXISTS admins (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    )
    """

    create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """

    create_books_table = """
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            category VARCHAR(255) NOT NULL,
            status VARCHAR(255) NOT NULL,
            quantity INT NOT NULL
        )
    """

    cursor.execute ( create_admins_table )
    cursor.execute ( create_users_table )
    cursor.execute ( create_books_table )

    connection.commit ( )
    cursor.close ( )


def admin_login ( username , password ) :
    cursor = connection.cursor ( )
    query = "SELECT * FROM admins WHERE username = %s AND password = %s"
    cursor.execute ( query , (username , password) )
    admin = cursor.fetchone ( )
    if admin :
        print ( "Admin login successful!" )
        return True
    else :
        print ( "Admin login failed!" )
        return False


def create_admin_account ( username , password ) :
    cursor = connection.cursor ( )
    query = "INSERT INTO admins (username, password) VALUES (%s, %s)"
    cursor.execute ( query , (username , password) )
    connection.commit ( )
    if cursor.rowcount > 0 :
        print ( "Admin account created successfully!" )
        return True
    else :
        print ( "Admin account creation failed!" )
        return False


def add_book ( title , author , category , quantity ) :
    cursor = connection.cursor ( )
    query = "INSERT INTO books (title, author, category, status, quantity) VALUES (%s, %s, %s, %s, %s)"

    if quantity > 0 :
        status = "available"
    else :
        status = "unavailable"

    cursor.execute ( query , (title , author , category , status , quantity) )
    connection.commit ( )

    print ( "Book added successfully!" )


def delete_book ( book_id ) :
    cursor = connection.cursor ( )
    query = "DELETE FROM books WHERE id = %s"  # Use 'id' as the column name
    cursor.execute ( query , (book_id ,) )
    connection.commit ( )
    if cursor.rowcount > 0 :
        print ( "Book deleted successfully!" )
        return True
    else :
        print ( "Book deletion failed!" )
        return False


def update_book ( book_id , title , author , category ) :
    cursor = connection.cursor ( )
    query = "UPDATE books SET title = %s, author = %s, category = %s WHERE id = %s"  # Change 'id' to 'book_id'
    cursor.execute ( query , (title , author , category , book_id) )
    connection.commit ( )
    if cursor.rowcount > 0 :
        print ( "Book updated successfully!" )
        return True
    else :
        print ( "Book update failed!" )
        return False


def view_books () :
    cursor = connection.cursor ( )
    query = "SELECT * FROM books"
    cursor.execute ( query )
    books = cursor.fetchall ( )
    if cursor.rowcount > 0 :
        for book in books :
            print ( "ID:" , book[0] )
            print ( "Title:" , book[1] )
            print ( "Author:" , book[2] )
            print ( "Category:" , book[3] )
            print ( "Status:" , book[4] )
            print ( "-------" )
    else :
        print ( "No books found." )


def view_users () :
    cursor = connection.cursor ( )
    query = "SELECT * FROM users"
    cursor.execute ( query )
    users = cursor.fetchall ( )
    if cursor.rowcount > 0 :
        for user in users :
            print ( "ID:" , user[0] )
            print ( "Username:" , user[1] )
            print ( "Email:" , user[2] )
            print ( "-------" )
    else :
        print ( "No users found." )


def user_login ( email , password ) :
    cursor = connection.cursor ( )
    query = "SELECT * FROM users WHERE email = %s AND password = %s"
    cursor.execute ( query , (email , password) )
    user = cursor.fetchone ( )
    if user :
        print ( "User login successful!" )
        return user
    else :
        print ( "User login failed!" )
        return None


def register_user ( username , email , password ) :
    cursor = connection.cursor ( )
    query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
    cursor.execute ( query , (username , email , password) )
    connection.commit ( )
    if cursor.rowcount > 0 :
        print ( "Registration successful!" )
        return True
    else :
        print ( "Registration failed!" )
        return False


def search_book ( title ) :
    cursor = connection.cursor ( )
    query = "SELECT * FROM books WHERE title = %s"
    cursor.execute ( query , (title ,) )
    books = cursor.fetchall ( )
    if cursor.rowcount > 0 :
        for book in books :
            print ( "ID:" , book[0] )
            print ( "Title:" , book[1] )
            print ( "Author:" , book[2] )
            print ( "Category:" , book[3] )
            print ( "Status:" , book[4] )
            print ( "-------" )
    else :
        print ( "No matching books found." )


def browse_all_books () :
    cursor = connection.cursor ( )
    query = "SELECT * FROM books"
    cursor.execute ( query )
    books = cursor.fetchall ( )
    if cursor.rowcount > 0 :
        for book in books :
            print ( "ID:" , book[0] )
            print ( "Title:" , book[1] )
            print ( "Author:" , book[2] )
            print ( "Category:" , book[3] )
            print ( "Status:" , book[4] )
            print ( "-------" )
    else :
        print ( "No books found." )


def admin_menu () :
    while True :
        print ( "Admin Menu" )
        print ( "1. Add Book" )
        print ( "2. Delete Book" )
        print ( "3. Update Book" )
        print ( "4. View Books" )
        print ( "5. View Users" )
        print ( "6. Exit" )
        choice = input ( "Enter your choice: " )
        if choice == "1" :
            title = input ( "Enter book title: " )
            author = input ( "Enter book author: " )
            category = input ( "Enter book Category: " )
            quantity = int ( input ( "Enter quantity: " ) )
            add_book ( title , author , category , quantity )
        elif choice == "2" :
            book_id = input ( "Enter book ID to delete: " )
            delete_book ( book_id )
        elif choice == "3" :
            book_id = input ( "Enter book ID to update: " )
            new_title = input ( "Enter new title: " )
            new_author = input ( "Enter new author: " )
            new_category = input ( "Enter new Category: " )
            update_book ( book_id , new_title , new_author , new_category )
        elif choice == "4" :
            view_books ( )
        elif choice == "5" :
            view_users ( )
        elif choice == "6" :
            break
        else :
            print ( "Invalid choice" )


def user_menu ( user_email ) :
    while True :
        print ( "User Menu" )
        print ( "1. Search for a Book" )
        print ( "2. Browse All Books" )
        print ( "3. Exit" )
        choice = input ( "Enter your choice: " )
        if choice == "1" :
            title = input ( "Enter book title to search: " )
            search_book ( title )
        elif choice == "2" :
            browse_all_books ( )
        elif choice == "3" :
            break
        else :
            print ( "Invalid choice" )


def main () :
    while True :
        print ( "1. Admin Login" )
        print ( "2. User Login / Register" )
        print ( "3. Exit" )
        choice = input ( "Enter your choice: " )

        if choice == "1" :
            admin_username = input ( "Admin Username: " )
            admin_password = input ( "Admin Password: " )
            if admin_login ( admin_username , admin_password ) :
                admin_menu ( )
        elif choice == "2" :
            user_choice = input ( "1. Login\n2. Register\nEnter choice: " )
            if user_choice == "1" :
                user_email = input ( "User Email: " )
                user_password = input ( "User Password: " )
                user = user_login ( user_email , user_password )
                if user :
                    print ( "Welcome," , user[1] )
                    user_menu ( user_email )
            elif user_choice == "2" :
                user_username = input ( "User Username: " )
                user_email = input ( "User Email: " )
                user_password = input ( "User Password: " )
                register_user ( user_username , user_email , user_password )
            else :
                print ( "Invalid choice" )
        elif choice == "3" :
            break
        else :
            print ( "Invalid choice" )


if __name__ == "__main__" :
    create_tables ( )
    main ( )
    connection.close ( )
