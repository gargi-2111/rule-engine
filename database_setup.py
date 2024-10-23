import sqlite3

def init_db():
    conn = sqlite3.connect('rule_engine.db')
    cursor = conn.cursor()

    # Create rules table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rules (
            rule_id INTEGER PRIMARY KEY,
            rule_string TEXT,
            ast_json TEXT
        )
    ''')

    # Create metadata table for attributes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metadata (
            attribute TEXT,
            type TEXT
        )
    ''')

    # Insert some example metadata
    cursor.execute('INSERT OR IGNORE INTO metadata (attribute, type) VALUES (?, ?)', ('age', 'integer'))
    cursor.execute('INSERT OR IGNORE INTO metadata (attribute, type) VALUES (?, ?)', ('salary', 'integer'))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized!")
