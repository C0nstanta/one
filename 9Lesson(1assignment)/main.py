#делаем базу данных.
# для каждой сущности пишем по контроллеру. В каждом контроллере все типы запросов. GET POST PUT DELETE
# и еще один отдельный роут для вывода списка отличников по какому то отдельному факультету
#
# создаем базу данных студентов. у студентов будут следующие поля:
# (ФИО, группа, оценки, куратор студента, факультет).
# эти поля нужно будет придумать как по разным таблицам разбить.
# Описан список сущностей(студенты, оценки, кураторы, факультет)
# Создать базу данных студентов (ФИО, группа, оценки, куратор
# студента, факультет). Написать CRUD ко всем полям.
# ===============================================================


from flask import Flask, request
from dbmanager import DBManager

app = Flask(__name__)

dbmanager = DBManager()


@app.route('/faculty/<int:faculty_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/faculty', methods=['GET', 'POST'])
def faculty_control(faculty_id=None):
    if request.method == 'GET':
        if faculty_id:
            result = dbmanager.faculty('GET', faculty_id)
        else:
            result = dbmanager.faculty('GET')
        return result
    if request.method == 'POST':
        data = request.json
        if data['fac_name']:
            fac_name = (data['fac_name'])
            print(fac_name)
            result = dbmanager.faculty('POST', fac_name=fac_name)
        return result
    if request.method == 'PUT' and faculty_id:
        data = request.json
        fac_name = (data['fac_name'])
        print(f'From put db fac_id:{faculty_id}, fac_name:{fac_name}')
        result = dbmanager.faculty('PUT', fac_id=faculty_id, fac_name=fac_name)
        return result
    if request.method == 'DELETE' and faculty_id:
        result = dbmanager.faculty('DELETE', fac_id=faculty_id)
        return result
    else:
        return "Wrong request type"


@app.route('/curators/<int:curator_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/curators', methods=['GET', 'POST'])
def curator_control(curator_id=None):
    if request.method == 'GET':
        if curator_id:
            result = dbmanager.curators('GET', curator_id)
        else:
            result = dbmanager.curators('GET')
        return result
    if request.method == 'POST':
        data = request.json
        result = dbmanager.curators('POST', **data)
        return result
    if request.method == 'PUT' and curator_id:
        data = request.json
        result = dbmanager.curators('PUT', curator_id,  **data)
        return result
    if request.method == 'DELETE' and curator_id:
        result = dbmanager.curators('DELETE', curator_id)
        return result
    else:
        return "Wrong request type"


@app.route('/students/<int:student_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/students', methods=['GET', 'POST'])
def students_control(student_id=None):
    if request.method == 'GET':
        if student_id:
            result = dbmanager.students('GET', stud_id=student_id)
        else:
            result = dbmanager.students('GET')
        return result
    if request.method == 'POST':
        data = request.json
        result = dbmanager.students('POST', **data)
        return result
    if request.method == 'PUT' and student_id:
        data = request.json
        result = dbmanager.students('PUT', student_id,  **data)
        return result
    if request.method == 'DELETE' and student_id:
        result = dbmanager.students('DELETE', student_id)
        return result
    else:
        return "Wrong request type"


@app.route('/grades/<int:grade_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/grades', methods=['GET', 'POST'])
def grades_control(grade_id=None):
    if request.method == 'GET':
        if grade_id:
            result = dbmanager.grades('GET', grade_id=grade_id)
        else:
            result = dbmanager.grades('GET')
        return result
    if request.method == 'POST':
        data = request.json
        result = dbmanager.grades('POST', **data)
        return result
    if request.method == 'PUT' and grade_id:
        data = request.json
        result = dbmanager.grades('PUT', grade_id,  **data)
        return result
    if request.method == 'DELETE' and grade_id:
        result = dbmanager.grades('DELETE', grade_id)
        return result
    else:
        return "Wrong request type"

#Можем регулировать в ручном режиме минимальный СРЕДНИЙ балл попадания в отличники
@app.route('/a_grades/<int:faculty_id>', methods=['GET'])
@app.route('/a_grades/<int:faculty_id>/<int:min_grade>', methods=['GET'])
@app.route('/a_grades/<string:faculty_name>', methods=['GET'])
@app.route('/a_grades/<string:faculty_name>/<int:min_grade>', methods=['GET'])
def a_grade_control(min_grade=None, faculty_id=None, faculty_name=None):
    if request.method == 'GET':
        result = dbmanager.get_a_grades('GET', faculty_id=faculty_id, min_grade=min_grade, faculty_name=faculty_name)
    return result


@app.route('/cur_stud/<int:curator_id>', methods=['GET'])
@app.route('/cur_stud/<string:curator_fname>/<string:curator_surname>', methods=['GET'])
def get_cur_stud(curator_id=None, curator_fname=None, curator_surname=None):
    if request.method == 'GET':
        print(f'cur_id_func:{curator_id}')
        result = dbmanager.get_curators_stud('GET', curator_id=curator_id, curator_fname=curator_fname,
                                             curator_surname=curator_surname)
    return result


if __name__ == "__main__":
    app.run(debug=True)