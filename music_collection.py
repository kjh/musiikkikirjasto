import db

def get_user(user_id):
    sql = "SELECT username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_user_releases(user_id):
    sql = """SELECT r.id,
                    r.collection_id,
                    r.title,
                    r.artist,
                    c.title collection_title,
                    r.sent_at
             FROM collections c, releases r
             WHERE c.id = r.collection_id AND
                   r.user_id = ?
             ORDER BY r.sent_at DESC"""
    return db.query(sql, [user_id])

def search(query):
    sql = """SELECT DISTINCT r.id release_id,
                    r.collection_id,
                    c.title collection_title,
                    r.sent_at,
                    u.username
             FROM collections c, releases r, users u
             LEFT JOIN collection_tags ct ON c.id = ct.collection_id
             LEFT JOIN tags t ON ct.tag_id = t.id
             WHERE c.id = r.collection_id AND
                   u.id = r.user_id AND
                   (r.artist LIKE ? OR r.title LIKE ? OR t.name LIKE ?)
             ORDER BY r.sent_at DESC"""
    return db.query(sql, ["%" + query + "%", "%" + query + "%", "%" + query + "%"])

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

def add_like(user_id, collection_id):
    sql = "INSERT INTO likes (user_id, collection_id) VALUES (?, ?)"
    db.execute(sql, [user_id, collection_id])

def delete_like(user_id, collection_id):
    sql = "DELETE FROM likes WHERE user_id = ? AND collection_id = ?"
    db.execute(sql, [user_id, collection_id])

def has_user_liked(user_id, collection_id):
    sql = "SELECT 1 FROM likes WHERE user_id = ? AND collection_id = ?"
    result = db.query(sql, [user_id, collection_id])
    return result if result else None  

def count_collection_likes(collection_id):
    sql = "SELECT COUNT(*) FROM likes WHERE collection_id = ?"
    result = db.query(sql, [collection_id])
    return result[0][0] if result else 0

def add_collection_tag(tag_id, collection_id):
    sql_check = "SELECT 1 FROM collection_tags WHERE tag_id = ? AND collection_id = ?"
    result = db.query(sql_check, [tag_id, collection_id])
    if not result:
        sql = "INSERT INTO collection_tags (tag_id, collection_id) VALUES (?, ?)"
        db.execute(sql, [tag_id, collection_id])

def get_collection_tags(collection_id):
    sql = """SELECT t.id, t.name
             FROM tags t
             INNER JOIN collection_tags ct ON t.id = ct.tag_id
             WHERE ct.collection_id = ?"""
    result = db.query(sql, [collection_id])
    return result

def delete_collection_tag(tag_id, collection_id):
    sql = "DELETE FROM collection_tags WHERE tag_id = ? AND collection_id = ?"
    db.execute(sql, [tag_id, collection_id])

def add_tag(name):
    sql = "INSERT INTO tags (name) VALUES (?)"
    db.execute(sql, [name])

def get_tag_id(tag_name):
    sql = "SELECT id FROM tags WHERE name = ?"
    result = db.query(sql, [tag_name])
    return result[0][0] if result else None

def delete_tag(tag_id):
    sql = "DELETE FROM tags WHERE tag_id = ?"
    db.execute(sql, [tag_id])


