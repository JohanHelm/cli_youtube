import sqlite3
from math import ceil


class Database:
    __slots__ = ('connection',)

    def __init__(self, db_file: str):
        self.connection = sqlite3.connect(db_file)
        cursor = self.connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS channels("
                       "channel_id TEXT, channelTitle TEXT, publishedAt TEXT, description TEXT, thumbnails TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS playlists(playlist_id TEXT, title TEXT, published_at TEXT, "
                       "description TEXT, thumbnails TEXT, channel_id TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS videos(video_id TEXT, title TEXT, description TEXT, "
                       "author TEXT, publishedAt DATETIME, thumbnails TEXT, playlist_id TEXT, channel_id TEXT, "
                       "viewed BOOLEAN DEFAULT (0))")
        cursor.execute("""CREATE TABLE IF NOT EXISTS temp_channel_search(channel_id TEXT,  
                    channelTitle TEXT, publishedAt DATETIME, description TEXT, thumbnails TEXT)""")

    def save_temp_channel(self, channel_id: str, channel_title: str, publishedat: str, description: str,
                          thumbnails: str):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO temp_channel_search (channel_id, channelTitle, publishedAt, "
                           " description, thumbnails) VALUES (?, ?, ?, ?, ?)",
                           (channel_id, channel_title, publishedat, description, thumbnails,))

    def show_temp_channels(self, page: int, show_results: int) -> tuple:
        with self.connection:
            cursor = self.connection.cursor()
            pages = ceil(cursor.execute("SELECT COUNT(*) FROM temp_channel_search").fetchone()[0] / show_results)
            offset = (page - 1) * show_results
            return cursor.execute(
                "SELECT channel_Id, channelTitle, publishedAt, description FROM temp_channel_search LIMIT ? OFFSET ?",
                (show_results, offset,)).fetchall(), pages

    def show_my_channels(self, page: int, show_results: int) -> tuple:
        with self.connection:
            cursor = self.connection.cursor()
            pages = ceil(cursor.execute("SELECT COUNT(*) FROM channels").fetchone()[0] / show_results)
            offset = (page - 1) * show_results
            return cursor.execute(
                "SELECT channel_Id, channelTitle, publishedAt, description FROM channels LIMIT ? OFFSET ?",
                (show_results, offset,)).fetchall(), pages

    def show_back_channel(self, channel_id: str) -> tuple:
        with self.connection:
            cursor = self.connection.cursor()
            return cursor.execute(
                "SELECT channel_Id, channelTitle, publishedAt, description FROM channels WHERE channel_id = ?",
                (channel_id,)).fetchone()

    def clear_temp_channel(self):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM temp_channel_search")

    def get_channel_from_temp(self, channel_id: str) -> tuple:
        with self.connection:
            cursor = self.connection.cursor()
            return cursor.execute("SELECT * FROM temp_channel_search WHERE channel_id = ?",
                                  (channel_id,)).fetchone()

    def check_channel_in_fav(self, channel_id: str) -> tuple:
        with self.connection:
            cursor = self.connection.cursor()
            return cursor.execute("SELECT EXISTS (SELECT * FROM channels WHERE channel_id = ?)",
                                  (channel_id,)).fetchone()

    def add_channel(self, channel_id: str, channel_title: str, publishedat: str, description: str, thumbnails: str):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO channels (channel_Id, channelTitle, publishedAt, description, thumbnails) "
                           "VALUES (?, ?, ?, ?, ?)",
                           (channel_id, channel_title, publishedat, description, thumbnails,))

    def rm_channel(self, channel_id: str):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM channels WHERE channel_id = ?", (channel_id,))
            cursor.execute("DELETE FROM videos WHERE channel_id = ?", (channel_id,))

    def add_playlist(self, playist_id, title, published_at, description, thumbnails, channel_id):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO playlists (playlist_id, title, published_at, description, thumbnails, channel_id) "
                "VALUES (?, ?, ?, ?, ?, ?)", (playist_id, title, published_at, description, thumbnails, channel_id,))

    def show_channel_playlists(self, page, show_results, channel_id):
        with self.connection:
            cursor = self.connection.cursor()
            pages = ceil(
                cursor.execute("SELECT COUNT(*) FROM playlists WHERE channel_Id = ?", (channel_id,)).fetchone()[
                    0] / show_results)
            offset = (page - 1) * show_results
            return cursor.execute(
                "SELECT playlist_id, title, published_at FROM playlists WHERE channel_id = ? LIMIT ? OFFSET ?",
                (channel_id, show_results, offset,)).fetchall(), pages

    def mark_videos_in_playlist(self, playlist_id, video_id):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("UPDATE videos SET playlist_id = ? WHERE video_id = ?", (playlist_id, video_id,))

    def add_video(self, video_id: str, title: str, description: str, author: str, published_at: str, thumbnails: str,
                  channel_id: str):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO videos (video_id, title, description, author, publishedAt, thumbnails, "
                           " channel_id) VALUES (?, ?, ?, ?, ?, ?, ?)", (video_id, title, description, author,
                                                                         published_at, thumbnails, channel_id,))

    def show_channel_videos(self, page: int, show_results: int, channel_id: str) -> tuple:
        with self.connection:
            cursor = self.connection.cursor()
            pages = ceil(cursor.execute("SELECT COUNT(*) FROM videos").fetchone()[0] / show_results)
            offset = (page - 1) * show_results
            return cursor.execute(
                "SELECT video_id, title, publishedAt FROM videos WHERE channel_id = ? "
                "ORDER BY publishedAt DESC LIMIT ? OFFSET ?",
                (channel_id, show_results, offset,)).fetchall(), pages

    def check_video_in_db(self, video_id: str) -> tuple:
        with self.connection:
            cursor = self.connection.cursor()
            return cursor.execute("SELECT EXISTS (SELECT * FROM videos WHERE video_id = ?)",
                                  (video_id,)).fetchone()

    def check_playlist_in_db(self, playlist_id: str) -> tuple:
        with self.connection:
            cursor = self.connection.cursor()
            return cursor.execute("SELECT EXISTS (SELECT * FROM playlists WHERE playlist_id = ?)",
                                  (playlist_id,)).fetchone()


    def show_playlist_videos(self, page: int, show_results: int, playlist_id: str) -> tuple:
        with self.connection:
            cursor = self.connection.cursor()
            pages = ceil(cursor.execute("SELECT COUNT(*) FROM videos WHERE playlist_id = ?", (playlist_id,)).fetchone()[
                             0] / show_results)
            offset = (page - 1) * show_results
            return cursor.execute(
                "SELECT video_id, title, publishedAt FROM videos WHERE playlist_id = ? "
                "ORDER BY publishedAt DESC LIMIT ? OFFSET ?",
                (playlist_id, show_results, offset,)).fetchall(), pages
