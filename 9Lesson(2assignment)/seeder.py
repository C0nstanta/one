# создаем файл, называем его сидер. и он будет сидить нашу базу случайными валидными
# значениями
# Имена Фамилии Отчества, для кураторов это применяем. Факультеты рандомные
from seeder_lib import DBManager


def main():
    while True:
        dbmanager = DBManager()
        try:
            step1 = int(input("What we will  seed?\n1.Students\n2.Curators\n3.Faculty\n4.Quit\n"))
            if step1 == 1:
                quantity = int(input("Enter the quantity of students:\n"))
                dbmanager.seed_students(num_seed=quantity)

            if step1 == 2:
                quantity = int(input("Enter the quantity of curators:\n"))
                dbmanager.seed_curators(num_seed=quantity)

            if step1 == 3:
                quantity = int(input("Enter the quantity of faculty:\n"))
                dbmanager.seed_faculty(num_seed=quantity)

            if step1 == 4:
                return False

        except ValueError as e:
            print(e)
            continue


if __name__ == "__main__":
    main()
