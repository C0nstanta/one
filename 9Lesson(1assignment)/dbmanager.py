import sqlite3
import os
from flask import jsonify


class MyDBManager:
    base_dir = os.getcwd()
    db_path = os.path.join(base_dir, "9lessondb.db")

    def __init__(self, db):
        self._db = db

    def __enter__(self):
        self.conn = sqlite3.connect(self._db)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        if exc_val:
            raise Exception("MyDBManager error!")


class DBManager(object):

    db_path = MyDBManager.db_path

    def faculty(self, status, fac_id=None, fac_name=None):
        with MyDBManager(self.db_path) as conn:
            cursor = conn.cursor()

            if status == 'GET':
                if fac_id:
                    row_query = "SELECT fac_name FROM faculty_tbl WHERE id=?"
                    value_query = (fac_id,)
                else:
                    row_query = "SELECT fac_name FROM faculty_tbl"
                    value_query = ()
                res = cursor.execute(row_query, value_query)
                return jsonify(res.fetchall())

            if status == 'POST' and fac_name:
                print("From db:",fac_name)
                row_query = f"INSERT INTO  faculty_tbl ('fac_name') VALUES (?)"
                value_query = (fac_name,)
                cursor.execute(row_query, value_query)
                conn.commit()
                return f"Faculty:{fac_name} was added!"

            if status == 'PUT' and fac_name and fac_id:
                row_query = "UPDATE faculty_tbl SET fac_name=? WHERE id=?"
                value_query = (fac_name, fac_id)
                cursor.execute(row_query, value_query)
                conn.commit()
                return f'New fac_id:{fac_id} was changed!'

            if status == 'DELETE' and fac_id:
                row_query = "DELETE FROM faculty_tbl WHERE id=?"
                value_query = (fac_id,)
                cursor.execute(row_query, value_query)
                conn.commit()
                return f'fac_id:{fac_id} was deleted!'

            else:
                return "Something wrong with your request, check all carefully "

    def curators(self,status, cur_id=None, **kwargs):
        with MyDBManager(self.db_path) as conn:
            cursor = conn.cursor()

            if status == 'GET':
                if cur_id:
                    row_query = "SELECT fname, lname FROM curators_tbl WHERE id=?"
                    value_query = (cur_id,)
                else:
                    row_query = "SELECT fname, lname FROM curators_tbl"
                    value_query = ()
                res = cursor.execute(row_query, value_query)
                return jsonify(res.fetchall())

            if status == 'POST':
                row_query = f"INSERT INTO  curators_tbl ('fname', 'lname') VALUES (?, ?)"
                value_query = (kwargs['fname'], kwargs['lname'])
                cursor.execute(row_query, value_query)
                conn.commit()
                return f"Curator:{kwargs['fname']}, {kwargs['lname']} was added!"

            if status == 'PUT' and cur_id:
                row_query = "UPDATE curators_tbl SET fname=?, lname=? WHERE id=?"
                value_query = (kwargs['fname'], kwargs['lname'], cur_id)
                cursor.execute(row_query, value_query)
                conn.commit()
                return f'New cur_id:{cur_id} was changed!'

            if status == 'DELETE' and cur_id:
                row_query = "DELETE FROM curators_tbl WHERE id=?"
                value_query = (cur_id,)
                cursor.execute(row_query, value_query)
                conn.commit()
                return f'cur_id:{cur_id} was deleted!'

            else:
                return "Something wrong with your request, check all carefully "

    def students(self,status, stud_id=None, **kwargs):
        with MyDBManager(self.db_path) as conn:
            cursor = conn.cursor()

            if status == 'GET':
                if stud_id:
                    row_query = "SELECT students_tbl.fname, students_tbl.lname, faculty_tbl.fac_name, " \
                                "curators_tbl.fname, curators_tbl.lname FROM students_tbl  INNER JOIN faculty_tbl ON " \
                                "students_tbl.faculty_id=faculty_tbl.id INNER JOIN curators_tbl ON " \
                                "students_tbl.curator_id=curators_tbl.id WHERE students_tbl.id=?"
                    value_query = (stud_id,)

                else:
                    row_query = "SELECT students_tbl.fname, students_tbl.lname, faculty_tbl.fac_name, " \
                                "curators_tbl.fname, curators_tbl.lname FROM students_tbl  INNER JOIN faculty_tbl ON " \
                                "students_tbl.faculty_id=faculty_tbl.id INNER JOIN curators_tbl ON " \
                                "students_tbl.curator_id=curators_tbl.id"
                    value_query = ()
                res = cursor.execute(row_query, value_query)
                return jsonify(res.fetchall())

            if status == 'POST':#реализовано 2 способа добавления, через id факультета и куратора и через из названия.
                if 'fname_cur' and'fac_name' and 'lname_cur' in kwargs:
                    row_query_cur = f"SELECT id FROM curators_tbl WHERE curators_tbl.fname='{kwargs['fname_cur']}' AND " \
                                    f"curators_tbl.lname='{kwargs['lname_cur']}'"
                    row_query_fac = f"SELECT id FROM faculty_tbl WHERE faculty_tbl.fac_name='{kwargs['fac_name']}'"

                    res_cur = cursor.execute(row_query_cur)
                    cur_id = int(res_cur.fetchone()[0])
                    res_fac = cursor.execute(row_query_fac)
                    fac_id = int(res_fac.fetchone()[0])
                elif kwargs['fac_id'] and kwargs['cur_id']:
                    cur_id = kwargs['cur_id']
                    fac_id = kwargs['fac_id']

                else:
                    return "Add the necessary variables"
                row_query_stud = f"INSERT INTO students_tbl('fname', 'lname', 'curator_id', 'faculty_id') " \
                                 f"VALUES('{kwargs['fname']}', '{kwargs['lname']}', {cur_id}, {fac_id})"
                cursor.execute(row_query_stud)
                conn.commit()
                return f"Student:{kwargs['fname']}, {kwargs['lname']} was added!"

            if status == 'PUT' and stud_id:
                row_query = "UPDATE students_tbl SET fname=?, lname=?, curator_id=?, faculty_id=?  WHERE id=?"
                value_query = (kwargs['fname'], kwargs['lname'], kwargs['cur_id'], kwargs['fac_id'], stud_id)
                cursor.execute(row_query, value_query)
                conn.commit()
                return f'New stud_id:{stud_id} was changed!'

            if status == 'DELETE' and stud_id:
                row_query = "DELETE FROM students_tbl WHERE id=?"
                value_query = (stud_id,)
                cursor.execute(row_query, value_query)
                conn.commit()
                return f'cur_id:{stud_id} was deleted!'

            else:
                return "Something wrong with your request, check all carefully "

    def grades(self, status, grade_id=None, **kwargs):
        with MyDBManager(self.db_path) as conn:
            cursor = conn.cursor()
            if status == 'GET':

                if grade_id:
                    row_query = "SELECT grades_tbl.grade, students_tbl.fname, students_tbl.lname, faculty_tbl.fac_name"\
                                "  FROM grades_tbl  INNER JOIN students_tbl ON grades_tbl.student_id=students_tbl.id " \
                                "INNER JOIN faculty_tbl ON grades_tbl.faculty_id=faculty_tbl.id WHERE grades_tbl.id=?"
                    value_query = (grade_id,)

                else:
                    row_query = "SELECT grades_tbl.grade, students_tbl.fname, students_tbl.lname, faculty_tbl.fac_name"\
                                "  FROM grades_tbl  INNER JOIN students_tbl ON grades_tbl.student_id=students_tbl.id " \
                                "INNER JOIN faculty_tbl ON grades_tbl.faculty_id=faculty_tbl.id"
                    value_query = ()
                res = cursor.execute(row_query, value_query)
                return jsonify(res.fetchall())

            if status == 'POST':#реализовано 2 способа добавления, через id студента и факультета и через их названия.

                if 'fname_stud' and 'lname_stud' and'fac_name' in kwargs:
                    row_query_stud = f"SELECT id FROM students_tbl WHERE students_tbl.fname='{kwargs['fname_stud']}' " \
                        f"AND students_tbl.lname='{kwargs['lname_stud']}'"
                    row_query_fac = f"SELECT id FROM faculty_tbl WHERE faculty_tbl.fac_name='{kwargs['fac_name']}'"

                    res_stud = cursor.execute(row_query_stud)
                    stud_id = int(res_stud.fetchone()[0])
                    res_fac = cursor.execute(row_query_fac)
                    fac_id = int(res_fac.fetchone()[0])

                elif kwargs['fac_id'] and kwargs['stud_id']:
                    stud_id = kwargs['stud_id']
                    fac_id = kwargs['fac_id']

                else:
                    return "Add the necessary variables"
                row_query_grade = f"INSERT INTO grades_tbl('grade','student_id', 'faculty_id') " \
                                 f"VALUES('{kwargs['grade']}', {stud_id}, {fac_id})"
                cursor.execute(row_query_grade)
                conn.commit()
                return f"Grade:{kwargs['grade']} was added!"

            if status == 'PUT' and grade_id:
                row_query = "UPDATE grades_tbl SET grade=?, student_id=?, faculty_id=?  WHERE id=?"
                value_query = (kwargs['grade'], kwargs['stud_id'], kwargs['fac_id'], grade_id)
                cursor.execute(row_query, value_query)
                conn.commit()
                return f'New grade_id:{grade_id} was changed!'

            if status == 'DELETE' and grade_id:
                row_query = "DELETE FROM grades_tbl WHERE id=?"
                value_query = (grade_id,)
                cursor.execute(row_query, value_query)
                conn.commit()
                return f'grade_id:{grade_id} was deleted!'

            else:
                return "Something wrong with your request, check all carefully "
