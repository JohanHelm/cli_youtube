import sqlite3
from math import ceil


class Database:
    def __init__(self, db_file: str):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS channels("
                            "channelTitle TEXT, publishedAt TEXT, channelId TEXT, description TEXT, thumbnails TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS playlists("
                            "title TEXT, description TEXT, thumbnails TEXT, playlist_id TEXT, channel_id TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS videos(title TEXT, description TEXT, author TEXT, "
                            "publishedAt DATETIME, thumbnails TEXT, video_id TEXT, playlist_id TEXT, channel_id TEXT, "
                            "viewed BOOLEAN DEFAULT (0))")

    def save_temp_channel(self, num, channeltitle, publishedat, channelid, description, thumbnails):
        with self.connection:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS temp_channel_search(num INTEGER, 
            channelTitle TEXT, publishedAt DATETIME, channelId TEXT, description TEXT, thumbnails TEXT)""")

            self.cursor.execute("INSERT INTO temp_channel_search (num, channelTitle, publishedAt, channelId,"
                                " description, thumbnails) VALUES (?, ?, ?, ?, ?, ?)",
                                (num, channeltitle, publishedat, channelid, description, thumbnails,))

    def show_temp_channels(self, page):
        with self.connection:
            pages = ceil(self.cursor.execute("SELECT COUNT(*) FROM temp_channel_search").fetchone()[0] / 5)
            offset = (page - 1) * 5
            return self.cursor.execute("SELECT channelTitle, publishedAt, description FROM temp_channel_search LIMIT 5 OFFSET ?", (offset,)).fetchall(), pages

    def clear_temp_channel(self):
        with self.connection:
            self.cursor.execute("DROP TABLE IF EXISTS temp_channel_search")

    def get_channel_from_temp(self, num_in_temporary):
        with self.connection:
            return self.cursor.execute("SELECT * FROM temp_channel_search WHERE num = ?",
                                       (num_in_temporary,)).fetchone()

    def add_channel(self, channeltitle, publishedat, channelid, description, thumbnails):
        with self.connection:
            self.cursor.execute("INSERT INTO channels (channelTitle, publishedAt, channelId, description, thumbnails) "
                                "VALUES (?, ?, ?, ?, ?)",
                                (channeltitle, publishedat, channelid, description, thumbnails,))

    def add_playlist(self, title, description, thumbnails, playist_id, channel_id):
        with self.connection:
            self.cursor.execute(
                "INSERT INTO playlists (title, description, thumbnails, playlist_id, channel_id) "
                "VALUES (?, ?, ?, ?, ?)", (title, description, thumbnails, playist_id, channel_id,))

    def add_video(self, title, description, author, published_at, thumbnails, video_id, channel_id):
        with self.connection:
            self.cursor.execute("INSERT INTO videos (title, description, author, publishedAt, thumbnails, video_id, "
                                " channel_id) VALUES (?, ?, ?, ?, ?, ?, ?)", (title, description, author, published_at,
                                                                              thumbnails, video_id, channel_id,))


db = Database('my_favorites.db')
# print([' '.join(i) for i in db.show_temp_channels()])
# print(db.show_temp_channels(2))
