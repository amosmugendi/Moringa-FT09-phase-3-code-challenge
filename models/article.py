from database.connection import get_db_connection
from models.author import Author 
from models.magazine import Magazine 

class Article:
    def __init__(self, id=None, title=None, content=None, author_id=None, magazine_id=None):
        if id is None and title is not None and content is not None and author_id is not None and magazine_id is not None:
            self._title = title
            self._content = content
            self._author_id = author_id
            self._magazine_id = magazine_id
            self._id = self.create_article_in_db(title, content, author_id, magazine_id)
        elif id is not None:
            self._id = id
            article_data = self.get_article_from_db(id)
            if article_data is None:
                raise ValueError("Article with given ID does not exist")
            self._title = article_data['title']
            self._content = article_data['content']
            self._author_id = article_data['author_id']
            self._magazine_id = article_data['magazine_id']
        else:
            raise ValueError("Either id or (title, content, author_id, magazine_id) must be provided")

    def create_article_in_db(self, title, content, author_id, magazine_id):
        if not isinstance(title, str) or len(title) == 0:
            raise ValueError("Title must be of type str and longer than 0 characters")
        if not isinstance(content, str) or len(content) == 0:
            raise ValueError("Content must be of type str and longer than 0 characters")
        if not isinstance(author_id, int):
            raise ValueError("Author ID must be of type int")
        if not isinstance(magazine_id, int):
            raise ValueError("Magazine ID must be of type int")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
                       (title, content, author_id, magazine_id))
        conn.commit()
        article_id = cursor.lastrowid
        conn.close()
        return article_id

    def get_article_from_db(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
        article = cursor.fetchone()
        conn.close()
        return article

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def content(self):
        return self._content

    @property
    def author_id(self):
        return self._author_id

    @property
    def magazine_id(self):
        return self._magazine_id

    @property
    def author(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT authors.* FROM articles
            JOIN authors ON articles.author_id = authors.id
            WHERE articles.id = ?
        """, (self._id,))
        author_data = cursor.fetchone()
        conn.close()
        if author_data:
            return Author(id=author_data['id'])
        return None

    @property
    def magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT magazines.* FROM articles
            JOIN magazines ON articles.magazine_id = magazines.id
            WHERE articles.id = ?
        """, (self._id,))
        magazine_data = cursor.fetchone()
        conn.close()
        if magazine_data:
            return Magazine(id=magazine_data['id'])
        return None

    def __repr__(self):
        return f'<Article {self._title}>'
