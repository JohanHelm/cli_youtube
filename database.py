import sqlite3
from math import ceil


class Database:
    def __init__(self, db_file: str):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS channels("
                            "channelId TEXT, channelTitle TEXT, publishedAt TEXT, description TEXT, thumbnails TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS playlists("
                            "playlist_id TEXT, title TEXT, description TEXT, thumbnails TEXT, channel_id TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS videos(video_id TEXT, title TEXT, description TEXT, "
                            "author TEXT, publishedAt DATETIME, thumbnails TEXT, playlist_id TEXT, channel_id TEXT, "
                            "viewed BOOLEAN DEFAULT (0))")

    def save_temp_channel(self, channelid, channeltitle, publishedat, description, thumbnails):
        with self.connection:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS temp_channel_search(channelId TEXT,  
            channelTitle TEXT, publishedAt DATETIME, description TEXT, thumbnails TEXT)""")

            self.cursor.execute("INSERT INTO temp_channel_search (channelId, channelTitle, publishedAt, "
                                " description, thumbnails) VALUES (?, ?, ?, ?, ?)",
                                (channelid, channeltitle, publishedat, description, thumbnails,))

    def show_temp_channels(self, page, results_amount):
        with self.connection:
            pages = ceil(self.cursor.execute("SELECT COUNT(*) FROM temp_channel_search").fetchone()[0] / 5)
            offset = (page - 1) * results_amount
            return self.cursor.execute("SELECT channelId, channelTitle, publishedAt, description FROM temp_channel_search LIMIT ? OFFSET ?", (results_amount, offset,)).fetchall(), pages

    def show_my_channels(self, page, results_amount):
        with self.connection:
            pages = ceil(self.cursor.execute("SELECT COUNT(*) FROM channels").fetchone()[0] / 5)
            offset = (page - 1) * results_amount
            return self.cursor.execute("SELECT channelId, channelTitle, publishedAt, description FROM channels LIMIT ? OFFSET ?", (results_amount, offset,)).fetchall(), pages

    def clear_temp_channel(self):
        with self.connection:
            self.cursor.execute("DROP TABLE IF EXISTS temp_channel_search")

    def get_channel_from_temp(self, num_in_temporary):
        with self.connection:
            return self.cursor.execute("SELECT * FROM temp_channel_search WHERE num = ?",
                                       (num_in_temporary,)).fetchone()

    def check_channel_in_fav(self, channelid):
        with self.connection:
            return self.cursor.execute("SELECT EXISTS (SELECT * FROM channels WHERE channelid = ?)", (channelid,)).fetchone()

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
# print(db.check_channel_in_fav('UCN3nx9hIzgItJeDb5FFfy0Q'))
# a, *b = db.show_my_channels(1, 5)[0][2]
# print(db.show_my_channels(1, 5)[0][2])
# print(a, b)