import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()

DATABASE_NAME = os.getenv('DB_NAME')

class Database:
    
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_NAME)
        self.cursor = self.conn.cursor()
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pictures (
                name TEXT,
                generation INT NOT NULL,
                done BOOLEAN
            ) 
        """)

    def insert_new_picture(self, name, generation):
        sql = "INSERT INTO pictures(name, generation, done) VALUES (?, ?, ?)"
        data_tuple = (name, generation, 0)
        self.cursor.execute(sql, data_tuple)
        self.conn.commit()
    
    def load_initial_data(self, originals):
        for pict in originals:
            self.insert_new_picture(pict, 0)
            
    def get_current_generation(self):
        self.cursor.execute('select generation from pictures where done = 0 group by generation order by generation')
        generation = self.cursor.fetchone()
       
        return generation[0] if generation else -1
    
    def get_current_pictures(self, generation):
        self.cursor.execute('select name from pictures where done = 0 and generation = ?', (generation,))
        pictures = self.cursor.fetchall()
        
        return pictures
    
    def get_all_pictures(self):
        self.cursor.execute('select name, generation, done from pictures')
        pictures = self.cursor.fetchall()
        
        return pictures
    
    def update_picture(self, name, state):
        sql = "Update pictures set done = ? where name = ?"
        data_tuple = (state, name)
        self.cursor.execute(sql, data_tuple)
        self.conn.commit()