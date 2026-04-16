import sqlite3
import os

os.makedirs('instance', exist_ok=True)
conn = sqlite3.connect('instance/database.db')
conn.executescript(open('database/schema.sql', encoding='utf-8').read())
c = conn.cursor()
c.execute('SELECT COUNT(*) FROM fortunes')
count = c.fetchone()[0]

if count == 0:
    c.execute('INSERT INTO fortunes (category, title, content, interpretation) VALUES (?, ?, ?, ?)', (
        '觀音靈籤', 
        '第一籤 上上', 
        '開天闢地作良緣\n吉日良時萬物全', 
        '萬事如意，皆能順利。'
    ))
    c.execute('INSERT INTO fortunes (category, title, content, interpretation) VALUES (?, ?, ?, ?)', (
        '觀音靈籤', 
        '第二籤 中平', 
        '靜心等待時機至\n凡事莫求太急進', 
        '需等待時機成熟。'
    ))
    conn.commit()
conn.close()
print("Database initialized successfully.")
