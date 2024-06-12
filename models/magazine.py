from database.connection import get_db_connection
from models.author import Author

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        if id is None and name is not None and category is not None:
            self._name = name
            self._category = category
            self._id = self.create_magazine_in_db(name, category)
        elif id is not None:
            self._id = id
            magazine_data = self.get_magazine_from_db(id)
            if magazine_data is None:
                raise ValueError("Magazine with given ID does not exist")
            self._name = magazine_data['name']
            self._category = magazine_data['category']
        else:
            raise ValueError("Either id or (name, category) must be provided")

    def create_magazine_in_db(self, name, category):
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError("Name must be of type str and between 2 and 16 characters")
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("Category must be of type str and longer than 0 characters")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (name, category))
        conn.commit()
        magazine_id = cursor.lastrowid
        conn.close()
        return magazine_id

    def get_magazine_from_db(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        magazine = cursor.fetchone()
        conn.close()
        return magazine

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("Name must be of type str and between 2 and 16 characters")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Category must be of type str and longer than 0 characters")
        self._category = value

    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self._id,))
        articles = cursor.fetchall()
        conn.close()
        if articles:
            return [article['title'] for article in articles]
        return None

    def contributing_authors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT authors.*, COUNT(articles.id) as article_count
            FROM articles
            JOIN authors ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        """, (self._id,))
        authors = cursor.fetchall()
        conn.close()
        if authors:
            return [Author(id=author['id']) for author in authors]
        return None

    def __repr__(self):
        return f'<Magazine {self._name}>'