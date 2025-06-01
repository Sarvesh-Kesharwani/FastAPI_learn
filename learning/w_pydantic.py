from pydantic import BaseModel
from typing import List, Dict, Optional


class Patient(BaseModel):
    name: str
    age: int
    allergies: list
    contacts: Dict[str, int]
    gender: Optional[str] = "M"


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.contacts)
    print(patient.gender)
    print("inserted")


sample_patient_data = {
    "name": "sarvesh",
    "age": "27",
    "allergies": [2, "b"],
    "contacts": {"home": "222"},
}

validated_sample_patient_data = Patient(**sample_patient_data)
insert_patient_data(validated_sample_patient_data)
