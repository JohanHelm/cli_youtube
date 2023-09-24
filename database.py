import sqlite3
from math import ceil
from os.path import expanduser
# from pympler import asizeof

class Database:
    __slots__ = ('connection', 'cursor')

    def __init__(self, db_file: str):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS channels("
                            "channel_id TEXT, channelTitle TEXT, publishedAt TEXT, description TEXT, thumbnails TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS videos(video_id TEXT, title TEXT, description TEXT, "
                            "author TEXT, publishedAt DATETIME, thumbnails TEXT, channel_id TEXT, "
                            "viewed BOOLEAN DEFAULT (0))")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS temp_channel_search(channel_id TEXT,  
                    channelTitle TEXT, publishedAt DATETIME, description TEXT, thumbnails TEXT)""")

    def save_temp_channel(self, channel_id, channel_title, publishedat, description, thumbnails):
        with self.connection:
            self.cursor.execute("INSERT INTO temp_channel_search (channel_id, channelTitle, publishedAt, "
                                " description, thumbnails) VALUES (?, ?, ?, ?, ?)",
                                (channel_id, channel_title, publishedat, description, thumbnails,))

    def show_temp_channels(self, page, show_results):
        with self.connection:
            pages = ceil(self.cursor.execute("SELECT COUNT(*) FROM temp_channel_search").fetchone()[0] / show_results)
            offset = (page - 1) * show_results
            return self.cursor.execute(
                "SELECT channel_Id, channelTitle, publishedAt, description FROM temp_channel_search LIMIT ? OFFSET ?",
                (show_results, offset,)).fetchall(), pages

    def show_my_channels(self, page, show_results):
        with self.connection:
            pages = ceil(self.cursor.execute("SELECT COUNT(*) FROM channels").fetchone()[0] / show_results)
            offset = (page - 1) * show_results
            return self.cursor.execute(
                "SELECT channel_Id, channelTitle, publishedAt, description FROM channels LIMIT ? OFFSET ?",
                (show_results, offset,)).fetchall(), pages

    def clear_temp_channel(self):
        with self.connection:
            self.cursor.execute("DELETE FROM temp_channel_search")

    def get_channel_from_temp(self, channel_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM temp_channel_search WHERE channel_id = ?",
                                       (channel_id,)).fetchone()

    def check_channel_in_fav(self, channel_id):
        with self.connection:
            return self.cursor.execute("SELECT EXISTS (SELECT * FROM channels WHERE channel_id = ?)",
                                       (channel_id,)).fetchone()

    def add_channel(self, channel_id, channel_title, publishedat, description, thumbnails):
        with self.connection:
            self.cursor.execute("INSERT INTO channels (channel_Id, channelTitle, publishedAt, description, thumbnails) "
                                "VALUES (?, ?, ?, ?, ?)",
                                (channel_id, channel_title, publishedat, description, thumbnails,))

    def rm_channel(self, channel_id):
        with self.connection:
            self.cursor.execute("DELETE FROM channels WHERE channel_id = ?", (channel_id,))
            self.cursor.execute("DELETE FROM videos WHERE channel_id = ?", (channel_id,))

    def add_video(self, video_id, title, description, author, published_at, thumbnails, channel_id):
        with self.connection:
            self.cursor.execute("INSERT INTO videos (video_id, title, description, author, publishedAt, thumbnails, "
                                " channel_id) VALUES (?, ?, ?, ?, ?, ?, ?)", (video_id, title, description, author,
                                                                              published_at, thumbnails, channel_id,))

    def show_channel_videos(self, page, show_results, channel_id):
        with self.connection:
            pages = ceil(self.cursor.execute("SELECT COUNT(*) FROM videos").fetchone()[0] / show_results)
            offset = (page - 1) * show_results
            return self.cursor.execute(
                "SELECT video_id, title, publishedAt FROM videos WHERE channel_id = ? ORDER BY publishedAt DESC LIMIT ? OFFSET ?",
                (channel_id, show_results, offset,)).fetchall(), pages

    def check_video_in_db(self, video_id):
        with self.connection:
            return self.cursor.execute("SELECT EXISTS (SELECT * FROM videos WHERE video_id = ?)",
                                       (video_id,)).fetchone()

db = Database(f'{expanduser("~")}/youtube_client/my_favorites.db')
# print(asizeof.asizeof(db))
# 824
# 400