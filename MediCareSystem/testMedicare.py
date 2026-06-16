import unittest
from MediCare import HospitalService, Patient, Doctor, Treatment

class TestHospitalSystem(unittest.TestCase):

    def setUp(self):
        """Initialize service before each test"""
        self.service = HospitalService()

    # Test Patient Module
    def test_add_patient(self):
        patient = Patient("John Doe", 30, "Male", "A+")
        self.service.add_record("Patients", patient)

        self.assertEqual(len(self.service.get_all("Patients")), 1)

    def test_update_patient(self):
        patient = Patient("John Doe", 30, "Male", "A+")
        self.service.add_record("Patients", patient)

        self.service.update_record(
            "Patients",
            patient.id,
            ["Jane Doe", 28, "Female", "B+"]
        )

        updated = self.service.get_all("Patients")[0]
        self.assertEqual(updated.name, "Jane Doe")

    def test_delete_patient(self):
        patient = Patient("John Doe", 30, "Male", "A+")
        self.service.add_record("Patients", patient)

        self.service.remove_record("Patients", patient.id)

        self.assertEqual(len(self.service.get_all("Patients")), 0)

    # Test Doctor Module
    def test_add_doctor(self):
        doctor = Doctor("Dr Smith", "Cardiology")
        self.service.add_record("Doctors", doctor)

        self.assertEqual(len(self.service.get_all("Doctors")), 1)

    # Test Treatment Module
    def test_add_treatment(self):
        treatment = Treatment("John Doe", "Consultation", 1500)
        self.service.add_record("Treatments", treatment)

        self.assertEqual(len(self.service.get_all("Treatments")), 1)

    def test_treatment_cost(self):
        treatment = Treatment("John Doe", "X-Ray", 2000)
        self.assertEqual(treatment.cost, 2000)

    # Test Search Function
    def test_search_patient(self):
        patient = Patient("Alice", 25, "Female", "O+")
        self.service.add_record("Patients", patient)

        results = self.service.search("Patients", "Alice")

        self.assertGreater(len(results), 0)

if __name__ == "__main__":
    unittest.main()
