import sqlite3
from math import ceil
from os.path import expanduser


class Database:
    def __init__(self, db_file: str):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS channels("
                            "channel_id TEXT, channelTitle TEXT, publishedAt TEXT, description TEXT, thumbnails TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS playlists(playlist_id TEXT, title TEXT, published_at TEXT, "
                            "description TEXT, thumbnails TEXT, channel_id TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS videos(video_id TEXT, title TEXT, description TEXT, "
                            "author TEXT, publishedAt DATETIME, thumbnails TEXT, playlist_id TEXT, channel_id TEXT, "
                            "viewed BOOLEAN DEFAULT (0))")

    def save_temp_channel(self, channel_id, channel_title, publishedat, description, thumbnails):
        with self.connection:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS temp_channel_search(channel_id TEXT,  
            channelTitle TEXT, publishedAt DATETIME, description TEXT, thumbnails TEXT)""")

            self.cursor.execute("INSERT INTO temp_channel_search (channel_id, channelTitle, publishedAt, "
                                " description, thumbnails) VALUES (?, ?, ?, ?, ?)",
                                (channel_id, channel_title, publishedat, description, thumbnails,))

    def show_temp_channels(self, page, show_results):
        with self.connection:
            pages = ceil(self.cursor.execute("SELECT COUNT(*) FROM temp_channel_search").fetchone()[0] / show_results)
            offset = (page - 1) * show_results
            return self.cursor.execute("SELECT channel_Id, channelTitle, publishedAt, description FROM temp_channel_search LIMIT ? OFFSET ?", (show_results, offset,)).fetchall(), pages

    def show_my_channels(self, page, show_results):
        with self.connection:
            pages = ceil(self.cursor.execute("SELECT COUNT(*) FROM channels").fetchone()[0] / show_results)
            offset = (page - 1) * show_results
            return self.cursor.execute("SELECT channel_Id, channelTitle, publishedAt, description FROM channels LIMIT ? OFFSET ?", (show_results, offset,)).fetchall(), pages

    def clear_temp_channel(self):
        with self.connection:
            self.cursor.execute("DROP TABLE IF EXISTS temp_channel_search")

    def get_channel_from_temp(self, channel_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM temp_channel_search WHERE channel_id = ?",
                                       (channel_id,)).fetchone()

    def check_channel_in_fav(self, channel_id):
        with self.connection:
            return self.cursor.execute("SELECT EXISTS (SELECT * FROM channels WHERE channel_id = ?)", (channel_id,)).fetchone()

    def add_channel(self, channel_id, channel_title, publishedat, description, thumbnails):
        with self.connection:
            self.cursor.execute("INSERT INTO channels (channel_Id, channelTitle, publishedAt, description, thumbnails) "
                                "VALUES (?, ?, ?, ?, ?)",
                                (channel_id, channel_title, publishedat, description, thumbnails,))

    def rm_channel(self, channel_id):
        with self.connection:
            self.cursor.execute("DELETE FROM channels WHERE channel_id = ?", (channel_id,))
            self.cursor.execute("DELETE FROM videos WHERE channel_id = ?", (channel_id,))
            self.cursor.execute("DELETE FROM playlists WHERE channel_id = ?", (channel_id,))

    def add_playlist(self, playist_id, title, published_at, description, thumbnails, channel_id):
        with self.connection:
            self.cursor.execute(
                "INSERT INTO playlists (playlist_id, title, published_at, description, thumbnails, channel_id) "
                "VALUES (?, ?, ?, ?, ?, ?)", (playist_id, title, published_at, description, thumbnails, channel_id,))

    def show_channel_playlists(self, page, show_results, channel_id):
        with self.connection:
            pages = ceil(self.cursor.execute("SELECT COUNT(*) FROM playlists WHERE channel_Id = ?", (channel_id,)).fetchone()[0] / show_results)
            offset = (page - 1) * show_results
            return self.cursor.execute("SELECT playlist_id, title, published_at FROM playlists WHERE channel_id = ? LIMIT ? OFFSET ?", (channel_id, show_results, offset,)).fetchall(), pages

    def mark_videos_in_playlist(self, playist_id, video_id):
        with self.connection:
            self.cursor.execute("UPDATE videos SET playlist_id = ? WHERE video_id = ?", (playist_id, video_id,))

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
                "SELECT video_id, title, publishedAt FROM videos WHERE channel_id = ? LIMIT ? OFFSET ? ",
                (channel_id, show_results, offset, )).fetchall(), pages


db = Database(f'{expanduser("~")}/youtube_client/my_favorites.db')
