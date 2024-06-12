from database.connection import get_db_connection

class Author:
    def __init__(self, id=None, name=None):
        if id is None and name is not None:
            self._name = name
            self._id = self.create_author_in_db(name)
        elif id is not None:
            self._id = id
            author_data = self.get_author_from_db(id)
            if author_data is None:
                raise ValueError("Author with given ID does not exist")
            self._name = author_data['name']
        else:
            raise ValueError("Either id or name must be provided")

    def create_author_in_db(self, name):
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Name must be of type str and longer than 0 characters")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (name,))
        conn.commit()
        author_id = cursor.lastrowid
        conn.close()
        return author_id

    def get_author_from_db(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        author = cursor.fetchone()
        conn.close()
        return author

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise AttributeError("Cannot change the name after the author is instantiated")

    def __repr__(self):
        return f'<Author {self._name}>'