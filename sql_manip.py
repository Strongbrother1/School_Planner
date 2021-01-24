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
        
        create_table_query = """CREATE TABLE IF NOT EXISTS finished (course TEXT NOT NULL) """
        self.c.execute(create_table_query)
        self.close()
        
    def _initiate_requisite(self, ):
        df = requisites.make_math_req()
        df.to_sql("math_req", self.conn, if_exists="replace", index=False)
    
    def get_finished(self):
        get_finished_query = """SELECT course FROM finished"""
        self.c.execute(get_finished_query)
        finished = self.c.fetchall()
        self.close()
        
        return finished
    
    def add_finished(self, course):
        insert_query = """INSERT OR REPLACE INTO finished (course) VALUES (?)"""
        self.c.execute(insert_query, (course,))
        self.close()
        
    
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
            
    def get_req_courses_and_type(self):
        query_required = """SELECT requisite_type, course FROM math_req"""
        self.c.execute(query_required)
        required = self.c.fetchall()
        self.close()
        req_dict = {}
        for req in required:
            req_classes = []
            req = req[1].replace(r"'", "").replace(r"[", "").replace(r"]", "").split(r"/")
            req_classes.extend(req)
            req_dict[req[0]] = req_classes
        return req_dict
    
    def get_req_courses(self):
        query_required = """SELECT course FROM math_req"""
        self.c.execute(query_required)
        required = self.c.fetchall()
        self.close()
        req_classes = []
        for req in required:
            req = req[0].replace(r"'", "").replace(r"[", "").replace(r"]", "").split(r"/")
            req_classes.extend(req)
            
        return req_classes
    
    def get_hours_num_prereqs(self, dept, course_id):
        query = """SELECT hours, prereq_score FROM classes WHERE dept = ? AND class_id = ?"""
        self.c.execute(query, (dept, course_id))
        hours_prereq = self.c.fetchone()
        self.close()
        return hours_prereq
# ooga = SqlManip()
# ooga.get_desc('31A', 'MATH')
# SqlManip().get_classes()
# print(SqlManip().get_req_courses())
# print(SqlManip().get_finished())
if __name__ == "__main__":
    SqlManip()._initiate()
# #     # SqlManip()._initiate_requisite()
