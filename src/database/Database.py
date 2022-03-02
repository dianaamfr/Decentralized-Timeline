import sqlite3
import json
from ..consts import DATABASE_FILE_PATH, GARBAGE_COLLECTOR_FREQUENCY, POST_LIFETIME
from os.path import exists
from ..utils import get_post_args, post_tuple_to_dict, get_time


class Database:
    # -------------------------------------------------------------------------
    # Creation
    # -------------------------------------------------------------------------

    def __init__(self, username):
        self.database_file_path = f"{DATABASE_FILE_PATH}/{username}.db"
        exists_db = exists(self.database_file_path)

        self.connection = sqlite3.connect(self.database_file_path, check_same_thread=False, isolation_level=None)
        self.cursor = self.connection.cursor()
        if not exists_db:
            self.create_table()

    # -------------------------------------------------------------------------
    # SQL interaction
    # ------------------------------------------------------------------------- 

    def execute(self, command, arguments=None):
        if arguments is None:
            self.cursor.execute(command)
        else:
            self.cursor.execute(command, arguments)
        self.connection.commit()

    def fetch(self, command, arguments=None):
        if arguments is None:
            self.cursor.execute(command)
        else:
            self.cursor.execute(command, arguments)
        return self.cursor.fetchall()

    def fetch_one(self, command, arguments=None):
        if arguments is None:
            self.cursor.execute(command)
        else:
            self.cursor.execute(command, arguments)
        return self.cursor.fetchone()

    def create_table(self):
        self.execute("""
            CREATE TABLE posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            user VARCHAR(20) NOT NULL,
            timestamp DATETIME NOT NULL,
            body VARCHAR(50) NOT NULL,
            UNIQUE(post_id,user)
        );""")

    # -------------------------------------------------------------------------
    # Insert functions
    # -------------------------------------------------------------------------

    def insert_post(self, post):
        post_id, user, timestamp, body = get_post_args(post)
        try:
            self.execute("""
                INSERT INTO posts(post_id, user, timestamp, body) 
                VALUES(?,?,?,?)
            """, [post_id, user, timestamp, body])
        except sqlite3.Error as e:
            print("Duplicate message discarded.")

    def insert_posts(self, posts_list):
        for post in posts_list:
            self.insert_post(post)

    # -------------------------------------------------------------------------
    # Update functions
    # -------------------------------------------------------------------------
    
    def update_post(self, post_id, username, new_timestamp, new_post_id):
        self.cursor.execute("""
                UPDATE posts
                SET timestamp = ?, post_id = ? 
                WHERE post_id = ? AND user = ?
            """, [new_timestamp, new_post_id, post_id, username])    

    # -------------------------------------------------------------------------
    # Delete functions
    # -------------------------------------------------------------------------

    def delete_post(self, username):
        timestamp_now = get_time()
        self.execute("""
            DELETE FROM posts 
            WHERE user != ?
            AND timestamp < datetime(?, ?)
        """, [username, timestamp_now, f"-{POST_LIFETIME} seconds"])

    def delete_all(self, username):
        self.execute("""
            DELETE FROM posts 
            WHERE user == ?
        """, [username])
        
    # -------------------------------------------------------------------------
    # Get functions
    # ------------------------------------------------------------------------- 

    def get_timeline_posts(self):
        """
        Get all the posts ordered by timestamp
        """
        return self.fetch("""
            SELECT post_id, user, timestamp, body
            FROM posts
            ORDER BY timestamp
        """)

    def get_expired_posts(self, username): 
        """
        Get all the posts from the user that already expired the lifetime.
        """
        timestamp_now = get_time()

        return self.fetch("""
            SELECT post_id, user, timestamp, body
            FROM posts 
            WHERE user = ?
            AND timestamp < datetime(?, ?)
            ORDER BY timestamp
        """, [username, timestamp_now, f"-{POST_LIFETIME + GARBAGE_COLLECTOR_FREQUENCY} seconds"])
    
    def get_not_expired_posts(self, username):
        """
        Get posts from a specific user that are still within the lifetime.
        """
        timestamp_now = get_time()
        posts = self.fetch("""
            SELECT post_id, user, timestamp, body
            FROM posts
            WHERE user = ?
            AND timestamp > datetime(?, ?)
            ORDER BY timestamp
        """, [username, timestamp_now, f"-{POST_LIFETIME} seconds"])

        return [post_tuple_to_dict(post) for post in posts]
    
    def get_posts_after(self, username, last_post_id):
        """
        Get posts from a specific user that were made after the post with the id `last_post_id` and that have not expired.
        Used to send posts that were created while a user was offline.
        """
        timestamp_now = get_time()
        posts = self.fetch("""
            SELECT post_id, user, timestamp, body
            FROM posts
            WHERE user = ?
            AND post_id > ?
            AND timestamp > datetime(?, ?)
            ORDER BY timestamp
        """, [username, last_post_id, timestamp_now, f"-{POST_LIFETIME} seconds"])

        return [post_tuple_to_dict(post) for post in posts] 

    def get_last_post(self, username):
        """
        Get the last post from a user that is stored in the database.
        """

        max_id = self.fetch_one("""
            SELECT MAX(post_id)
            FROM posts
            WHERE user == ?
        """, [username])
 
        if max_id[0] is None:
            return -1 

        return max_id[0]

    def get_post(self, username, post_id):
        """
        Get post with a specific id
        """

        post = self.fetch_one("""
            SELECT post_id, user, timestamp, body
            FROM posts
            WHERE post_id = ? AND user = ?
        """, [post_id, username])

        if post is None:
            return None 
        return post_tuple_to_dict(post)
