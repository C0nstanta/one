#Контекстный менеджер у меня реализован в классе class MyDBManager. То есть прошу рассмотреть его , как первое задание.
#Путь к базе данных у меня лежал в отдельной папке. Но его можно поменять вверху.
#Буду благодарен
#
from autoclass import Authorization
from dbmanager import DBManager


def main():

    reg = False
    privileges = 0

    while True:
        try:
            if not reg or privileges == 0:
                press = int(input("1.Enter to account\n2.Exit\n"))

                if press == 1:
                    login = input("Enter your login:\n(letters and numbers only)\n")
                    if login.isalnum():
                        password = input("Enter your password:\n(letters and \
                        numbers only)\n")
                    if password.isalnum():
                        auto = Authorization(login, password)
                        print(auto.login)
                        print(auto.password)
                        reg, privileges = auto.check_log_pass_registration()
                        print(f'privileges:{privileges}, reg:{reg}')

                if press == 2:
                    print("Good buy")
                    break

            if reg and privileges == 1:
                choice = int(input("1.Add student\n2.Change(delete) student\n3.Get full DB info\n4.Login out\n5.Quit\n"))

                if choice == 1:
                    fname = input("Input student first name\n")
                    lname = input("Input student last name\n")
                    stud_card_num = input("Input student card number\n")
                    faculty = input("Input student faculty\n")

                    if fname.isalpha() and lname.isalpha() and stud_card_num.isalnum() and faculty.isalpha():
                        db_manager = DBManager(privileges, choice)
                        reg, privileges = db_manager.add_student(fname, lname, stud_card_num, faculty)
                        print(f'privileges:{privileges}, reg:{reg}')

                if choice == 2:
                    db_manager = DBManager(privileges, choice)
                    reg, privileges = db_manager.change_del_student()

                if choice == 3:
                    db_manager = DBManager(privileges, choice)
                    reg, privileges = db_manager.get_db_info()
                    print(f'privileges:{privileges}, reg:{reg}')

                if choice == 4:
                    reg = False
                    privileges = 0

                if choice == 5:
                    reg = False
                    privileges = 0
                    break

            if reg and privileges == 2:
                choice = int(input("1.Get full DB info\n2.Get a straight-A students list\n3.Get full info about "
                                   "students by ID\n4.Get full info about student by student card number\n5.Login out\n"
                                   "6.Quit\n"))
                if choice == 1:
                    db_manager = DBManager(privileges, choice)
                    reg, privileges = db_manager.get_db_info()
                    print(f'privileges:{privileges}, reg:{reg}')

                if choice == 2:
                    grade = input("Enter a minimum grade(not including it):\n")
                    print("Here is a full A-grade student list:\n")
                    db_manager = DBManager(privileges, choice)
                    reg, privileges = db_manager.get_agrade(grade)

                if choice == 3:
                    stud_id = input("Enter student id:\n")
                    if stud_id.isnumeric():
                        db_manager = DBManager(privileges, choice)
                        reg, privileges = db_manager.get_by_id(stud_id)

                if choice == 4:
                    card_num = input("Enter student card number:\n")
                    if card_num.isnumeric():
                        db_manager = DBManager(privileges, choice)
                        reg, privileges = db_manager.get_by_card(card_num)

                if choice == 5:
                    reg = False
                    privileges = 0

                if choice == 6:
                    reg = False
                    privileges = 0
                    break

        except ValueError as e:
            print("Try once again\n")
            print(e)  


if __name__ == "__main__":
    main()