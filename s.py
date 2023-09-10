# import mysql.connector
#
# # Connect to the MySQL database
# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="232003",
#     database="lms"
# )
#
# # Create a cursor object to interact with the database
# cursor = db.cursor()
#
#
#
# def create_tables():
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS users (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             username VARCHAR(255) NOT NULL,
#             password VARCHAR(255) NOT NULL
#         )
#     """)
#
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS books (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             title VARCHAR(255) NOT NULL,
#             author VARCHAR(255) NOT NULL,
#             available BOOLEAN DEFAULT TRUE
#         )
#     """)
#
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS transactions (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             user_id INT NOT NULL,
#             book_id INT NOT NULL,
#             FOREIGN KEY (user_id) REFERENCES users(id),
#             FOREIGN KEY (book_id) REFERENCES books(id)
#         )
#     """)
#
#
# def add_user(username, password):
#     cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
#     db.commit()
#
#
# def authenticate_user(username, password):
#     cursor.execute("SELECT id FROM users WHERE username = %s AND password = %s", (username, password))
#     user = cursor.fetchone()
#     return user is not None
#
#
# def add_book(title, author):
#     cursor.execute("INSERT INTO books (title, author) VALUES (%s, %s)", (title, author))
#     db.commit()
#
#
# def delete_book(book_id):
#     cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
#     db.commit()
#
#
# def update_book(book_id, title, author):
#     cursor.execute("UPDATE books SET title = %s, author = %s WHERE id = %s", (title, author, book_id))
#     db.commit()
#
#
# def view_books():
#     cursor.execute("SELECT * FROM books")
#     books = cursor.fetchall()
#     for book in books:
#         status = "Available" if book[3] else "Checked Out"
#         print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Status: {status}")
#
#
# def view_users():
#     cursor.execute("SELECT * FROM users")
#     users = cursor.fetchall()
#     for user in users:
#         print(f"ID: {user[0]}, Username: {user[1]}")
#
#
# def buy_book(user_id, book_id):
#     cursor.execute("UPDATE books SET available = FALSE WHERE id = %s", (book_id,))
#     cursor.execute("INSERT INTO transactions (user_id, book_id) VALUES (%s, %s)", (user_id, book_id))
#     db.commit()
#     print("Book purchased successfully.")
#
#
# def return_book(user_id, book_id):
#     cursor.execute("UPDATE books SET available = TRUE WHERE id = %s", (book_id,))
#     cursor.execute("DELETE FROM transactions WHERE user_id = %s AND book_id = %s", (user_id, book_id))
#     db.commit()
#     print("Book returned successfully.")
#
#
# # Create tables if they don't exist
# create_tables()
#
# while True:
#     print("\nLibrary Management System")
#     print("1. Admin Login")
#     print("2. User Login")
#     print("3. Exit")
#     choice = int(input("Enter your choice: "))
#
#     if choice == 1:
#         admin_username = input("Enter admin username: ")
#         admin_password = input("Enter admin password: ")
#         if authenticate_user(admin_username, admin_password):
#             while True:
#                 print("\nAdmin Menu:")
#                 print("1. Add Book")
#                 print("2. Delete Book")
#                 print("3. Update Book")
#                 print("4. View Books")
#                 print("5. View Users")
#                 print("6. Exit")
#                 admin_choice = int(input("Enter your choice: "))
#
#                 if admin_choice == 1:
#                     title = input("Enter title: ")
#                     author = input("Enter author: ")
#                     add_book(title, author)
#                     print("Book added successfully.")
#                 elif admin_choice == 2:
#                     book_id = int(input("Enter book ID to delete: "))
#                     delete_book(book_id)
#                     print("Book deleted successfully.")
#                 elif admin_choice == 3:
#                     book_id = int(input("Enter book ID to update: "))
#                     title = input("Enter new title: ")
#                     author = input("Enter new author: ")
#                     update_book(book_id, title, author)
#                     print("Book updated successfully.")
#                 elif admin_choice == 4:
#                     print("\nAvailable books:")
#                     view_books()
#                 elif admin_choice == 5:
#                     print("\nUsers:")
#                     view_users()
#                 elif admin_choice == 6:
#                     break
#                 else:
#                     print("Invalid choice. Try again.")
#         else:
#             print("Authentication failed. Please try again.")
#     elif choice == 2:
#         user_username = input("Enter user username: ")
#         user_password = input("Enter user password: ")
#         cursor.execute("SELECT id FROM users WHERE username = %s AND password = %s", (user_username, user_password))
#         user = cursor.fetchone()
#         if user:
#             user_id = user[0]
#             while True:
#                 print("\nUser Menu:")
#                 print("1. View Books")
#                 print("2. Buy Book")
#                 print("3. Return Book")
#                 print("4. Exit")
#                 user_choice = int(input("Enter your choice: "))
#
#                 if user_choice == 1:
#                     print("\nAvailable books:")
#                     view_books()
#                 elif user_choice == 2:
#                     book_id = int(input("Enter book ID to buy: "))
#                     buy_book(user_id, book_id)
#                 elif user_choice == 3:
#                     book_id = int(input("Enter book ID to return: "))
#                     return_book(user_id, book_id)
#                 elif user_choice == 4:
#                     break
#                 else:
#                     print("Invalid choice. Try again.")
#         else:
#             print("Authentication failed. Please try again.")
#     elif choice == 3:
#         break
#     else:
#         print("Invalid choice. Try again.")
#
# # Close the database connection
# db.close()

if existing_book:
    print("The book already exists in the database.")
    # Increment the quantity of the existing book
    update_query = "UPDATE book SET quantity = quantity + 1 WHERE book_name = %s AND author_name = %s"
    self.cursor.execute(update_query, (title, author))
    self.db.commit()
else:
    insert_query = "INSERT INTO book (book_name, author_name, quantity) VALUES (%s, %s, %s)"
    self.cursor.execute(insert_query, (title, author, 1))  # Default quantity is 1
    self.db.commit()

