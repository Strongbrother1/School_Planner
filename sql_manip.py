import os
import pandas as pd 
import sqlite3
import scraper
import requisites
class SqlManip():
    file_path = os.path.join("turtle_database.db")
    def __init__(self):
        self.conn = sqlite3.connect(self.file_path)
        self.c = self.conn.cursor()
    
    def _initiate(self):
        df = scraper.scrape_classes()
        df.to_sql("classes", self.conn, if_exists = "replace", index = False)
        self._initiate_requisite()
        
    def _initiate_requisite(self, ):
        df = requisites.make_math_req()
        df.to_sql("math_req", self.conn, if_exists="replace", index=False)
    
    def close(self):
        self.conn.commit()
        self.c.close()
        self.conn.close()
    
    def get_desc(self, class_id, dept):
        query = '''SELECT desc, requisites, corequisites FROM classes WHERE class_id = ? AND dept = ?;'''
        self.c.execute(query, (class_id, dept))
        desc_req = self.c.fetchone()
        self.close() 
        return desc_req
    
    def get_grade_type_units_hours(self, class_id, dept):
        query = '''SELECT grade_type, units, hours  FROM classes WHERE class_id = ? AND dept = ?;'''
        self.c.execute(query, (class_id, dept))
        info = self.c.fetchone()
        self.close() 
        return info
    
    def get_classes(self):
        query ='''SELECT dept, class_id FROM classes'''
        self.c.execute(query)
        classes = self.c.fetchall()
        self.close()
        return classes # list of tuples [('MATH', '1')]
            
# ooga = SqlManip()
# ooga.get_desc('31A', 'MATH')
# SqlManip().get_classes()

if __name__ == "__main__":
    SqlManip()._initiate()
    # SqlManip()._initiate_requisite()

