def insert_patient_date(name: str, age: int):
    if type(name) == str and type(age) == int:
        print(name)
        print(age)
        print("inserted into db.")
    else:
        raise TypeError("type error occured!!")


def update_patient_date(name: str, age: int):
    if type(name) == str and type(age) == int:
        print(name)
        print(age)
        print("updated the record!!!")
    else:
        raise TypeError("type error occured!!")


insert_patient_date("sarvesh", 25)
update_patient_date("sarvesh", 25)
