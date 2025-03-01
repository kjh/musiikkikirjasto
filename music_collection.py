import db

def get_user(user_id):
    sql = "SELECT username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_user_releases(user_id):
    sql = """SELECT r.id,
                    r.collection_id,
                    c.title collection_title,
                    r.sent_at
             FROM collections c, releases r
             WHERE c.id = r.collection_id AND
                   r.user_id = ?
             ORDER BY r.sent_at DESC"""
    return db.query(sql, [user_id])

def search(query):
    sql = """SELECT r.id release_id,
                    r.collection_id,
                    c.title collection_title,
                    r.sent_at,
                    u.username
             FROM collections c, releases r, users u
             WHERE c.id = r.collection_id AND
                   u.id = r.user_id AND
                   (r.artist LIKE ? OR r.title LIKE ?)
             ORDER BY r.sent_at DESC"""
    return db.query(sql, ["%" + query + "%", "%" + query + "%"])

def get_collections():
    sql = """SELECT c.id, c.title, COUNT(r.id) total, MAX(r.sent_at) last, u.username
             FROM collections c, releases r, users u
             WHERE c.user_id = u.id AND c.id = r.collection_id
             GROUP BY c.id
             ORDER BY c.id DESC"""
    return db.query(sql)

def get_collection(collection_id):
    sql = """SELECT c.id, c.title, c.user_id, u.username
             FROM collections c, users u
             WHERE c.user_id = u.id AND c.id = ?"""
    result = db.query(sql, [collection_id])
    return result[0] if result else None


def get_releases(collection_id):
    sql = """SELECT r.id, r.artist, r.title, r.sent_at, r.user_id, u.username
             FROM releases r, users u
             WHERE r.user_id = u.id AND r.collection_id = ?
             ORDER BY r.id"""
    return db.query(sql, [collection_id])

def get_release(release_id):
    sql = "SELECT id, artist, title, user_id, collection_id FROM releases WHERE id = ?"
    result = db.query(sql, [release_id])
    return result[0] if result else None

def add_collection(collection_title, artist, title, user_id):
    sql = "INSERT INTO collections (title, user_id) VALUES (?, ?)"
    db.execute(sql, [collection_title, user_id])
    collection_id = db.last_insert_id()
    add_release(artist, title, user_id, collection_id)
    return collection_id

def add_release(artist, title, user_id, collection_id):
    sql = """INSERT INTO releases (artist, title, sent_at, user_id, collection_id) VALUES
             (?, ?, datetime('now'), ?, ?)"""
    db.execute(sql, [artist, title, user_id, collection_id])

def update_release(release_id, artist, title):
    sql = "UPDATE releases SET artist = ?, title = ? WHERE id = ?"
    db.execute(sql, [artist, title, release_id])

def remove_release(release_id):
    sql = "DELETE FROM releases WHERE id = ?"
    db.execute(sql, [release_id])
