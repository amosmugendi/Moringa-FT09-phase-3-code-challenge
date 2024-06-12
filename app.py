from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def create_author():
    name = input("Enter author's name: ")
    try:
        author = Author(name=name)
        print(f'Author created: {author}')
    except ValueError as e:
        print(f'Error: {e}')

def create_magazine():
    name = input("Enter magazine name: ")
    category = input("Enter magazine category: ")
    try:
        magazine = Magazine(name=name, category=category)
        print(f'Magazine created: {magazine}')
    except ValueError as e:
        print(f'Error: {e}')

def create_article():
    title = input("Enter article title: ")
    content = input("Enter article content: ")
    author_id = int(input("Enter author ID: "))
    magazine_id = int(input("Enter magazine ID: "))
    try:
        article = Article(title=title, content=content, author_id=author_id, magazine_id=magazine_id)
        print(f'Article created: {article}')
    except ValueError as e:
        print(f'Error: {e}')

def view_authors():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM authors')
    authors = cursor.fetchall()
    conn.close()
    print("\nAuthors:")
    for author in authors:
        print(Author(id=author["id"], name=author["name"]))

def view_magazines():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM magazines')
    magazines = cursor.fetchall()
    conn.close()
    print("\nMagazines:")
    for magazine in magazines:
        print(Magazine(id=magazine["id"], name=magazine["name"], category=magazine["category"]))

def view_articles():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM articles')
    articles = cursor.fetchall()
    conn.close()
    print("\nArticles:")
    for article in articles:
        print(Article(id=article["id"], title=article["title"], content=article["content"], author_id=article["author_id"], magazine_id=article["magazine_id"]))

def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Create Author")
        print("2. Create Magazine")
        print("3. Create Article")
        print("4. View Authors")
        print("5. View Magazines")
        print("6. View Articles")
        print("7. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            create_author()
        elif choice == '2':
            create_magazine()
        elif choice == '3':
            create_article()
        elif choice == '4':
            view_authors()
        elif choice == '5':
            view_magazines()
        elif choice == '6':
            view_articles()
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

def main():
    # Initialize the database and create tables
    create_tables()

    # Display the main menu
    main_menu()

if __name__ == "__main__":
    main()