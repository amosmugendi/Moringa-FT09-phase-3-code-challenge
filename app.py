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

def view_magazine_article_titles():
    magazine_id = int(input("Enter magazine ID: "))
    try:
        magazine = Magazine(id=magazine_id)
        titles = magazine.article_titles()
        if titles:
            print("\nArticle Titles:")
            for title in titles:
                print(title)
        else:
            print("No articles found for this magazine.")
    except ValueError as e:
        print(f'Error: {e}')

def view_magazine_contributing_authors():
    magazine_id = int(input("Enter magazine ID: "))
    try:
        magazine = Magazine(id=magazine_id)
        authors = magazine.contributing_authors()
        if authors:
            print("\nContributing Authors:")
            for author in authors:
                print(author)
        else:
            print("No contributing authors found for this magazine.")
    except ValueError as e:
        print(f'Error: {e}')

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
        print("7. View Magazine Article Titles")
        print("8. View Magazine Contributing Authors")
        print("9. Exit")

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
            view_magazine_article_titles()
        elif choice == '8':
            view_magazine_contributing_authors()    
        elif choice == '9':
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