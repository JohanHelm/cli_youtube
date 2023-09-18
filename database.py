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

    def show_temp_channels(self, page, show_results):
        with self.connection:
            pages = ceil(self.cursor.execute("SELECT COUNT(*) FROM temp_channel_search").fetchone()[0] / show_results)
            offset = (page - 1) * show_results
            return self.cursor.execute("SELECT channelId, channelTitle, publishedAt, description FROM temp_channel_search LIMIT ? OFFSET ?", (show_results, offset,)).fetchall(), pages

    def show_my_channels(self, page, show_results):
        with self.connection:
            pages = ceil(self.cursor.execute("SELECT COUNT(*) FROM channels").fetchone()[0] / show_results)
            offset = (page - 1) * show_results
            return self.cursor.execute("SELECT channelId, channelTitle, publishedAt, description FROM channels LIMIT ? OFFSET ?", (show_results, offset,)).fetchall(), pages

    def clear_temp_channel(self):
        with self.connection:
            self.cursor.execute("DROP TABLE IF EXISTS temp_channel_search")

    def get_channel_from_temp(self, channel_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM temp_channel_search WHERE channelId = ?",
                                       (channel_id,)).fetchone()

    def check_channel_in_fav(self, channel_id):
        with self.connection:
            return self.cursor.execute("SELECT EXISTS (SELECT * FROM channels WHERE channelid = ?)", (channel_id,)).fetchone()

    def add_channel(self, channelid, channeltitle, publishedat, description, thumbnails):
        with self.connection:
            self.cursor.execute("INSERT INTO channels (channelId, channelTitle, publishedAt, description, thumbnails) "
                                "VALUES (?, ?, ?, ?, ?)",
                                (channelid, channeltitle, publishedat, description, thumbnails,))

    def add_playlist(self, playist_id, title, description, thumbnails, channel_id):
        with self.connection:
            self.cursor.execute(
                "INSERT INTO playlists (playlist_id, title, description, thumbnails, channel_id) "
                "VALUES (?, ?, ?, ?, ?)", (playist_id, title, description, thumbnails, channel_id,))

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
                "SELECT video_id, title, publishedAt FROM videos WHERE channel_Id = ? LIMIT ? OFFSET ? ",
                (channel_id, show_results, offset, )).fetchall(), pages



db = Database('my_favorites.db')
# print([' '.join(i) for i in db.show_temp_channels()])
# print(db.check_channel_in_fav('UCN3nx9hIzgItJeDb5FFfy0Q'))

# print(db.show_channel_videos(1, 5, 'UCIyLQ6cL0eWj1jT6oyy148w'))
# print(a, b)