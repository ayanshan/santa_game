import unittest
from santa_game import Employee, SecretSantaAssigner, FileHandler
import os
import pandas as pd

class TestSecretSanta(unittest.TestCase):

    def setUp(self):
        """Setup test data for each test."""
        self.employees = [
            Employee("Alice", "alice@example.com"),
            Employee("Bob", "bob@example.com"),
            Employee("Charlie", "charlie@example.com"),
            Employee("David", "david@example.com")
        ]
        self.last_year_assignments = {
            "alice@example.com": "bob@example.com",
            "bob@example.com": "charlie@example.com",
            "charlie@example.com": "david@example.com",
            "david@example.com": "alice@example.com"
        }

    def test_employee_creation(self):
        """Test if Employee objects are created correctly."""
        alice = Employee("Alice", "alice@example.com")
        self.assertEqual(alice.name, "Alice")
        self.assertEqual(alice.email, "alice@example.com")
        self.assertIsNone(alice.secret_child)

    def test_secret_child_assignment(self):
        """Test secret child assignment to an employee."""
        self.employees[0].assign_secret_child(self.employees[1])
        self.assertEqual(self.employees[0].secret_child, self.employees[1])

    def test_no_self_assignment(self):
        """Ensure no employee is assigned to themselves."""
        assigner = SecretSantaAssigner(self.employees, self.last_year_assignments)
        assigner.assign()
        for emp in self.employees:
            self.assertNotEqual(emp.email, emp.secret_child.email)

    def test_no_repeat_assignment_from_last_year(self):
        """Ensure no one gets the same secret child as last year."""
        assigner = SecretSantaAssigner(self.employees, self.last_year_assignments)
        assigner.assign()
        for emp in self.employees:
            self.assertNotEqual(self.last_year_assignments.get(emp.email), emp.secret_child.email)

    def test_all_unique_assignments(self):
        """Ensure each secret child is assigned only once."""
        assigner = SecretSantaAssigner(self.employees, self.last_year_assignments)
        assigner.assign()
        assigned_children = {emp.secret_child.email for emp in self.employees}
        self.assertEqual(len(assigned_children), len(self.employees))

    def test_file_handler_read_write_csv(self):
        """Test reading and writing CSV files."""
        test_csv = "test_employees.csv"
        test_output_csv = "test_output.csv"

        # Write test CSV
        with open(test_csv, "w", newline="") as f:
            f.write("Employee_Name,Employee_EmailID\n")
            f.write("Alice,alice@example.com\n")
            f.write("Bob,bob@example.com\n")
            f.write("Charlie,charlie@example.com\n")
            f.write("David,david@example.com\n")

        # Read employees
        employees = FileHandler.read_employees(test_csv)
        self.assertEqual(len(employees), 4)

        # Assign Secret Santa
        assigner = SecretSantaAssigner(employees, {})
        assigner.assign()
        FileHandler.save_assignments(test_output_csv, employees)

        # Ensure output file exists
        self.assertTrue(os.path.exists(test_output_csv))

        # Cleanup
        os.remove(test_csv)
        os.remove(test_output_csv)

    def test_file_handler_read_write_excel(self):
        """Test reading and writing Excel files."""
        test_xlsx = "test_employees.xlsx"
        test_output_xlsx = "test_output.xlsx"

        # Create test Excel file
        df = pd.DataFrame({"Employee_Name": ["Alice", "Bob", "Charlie", "David"],
                           "Employee_EmailID": ["alice@example.com", "bob@example.com", "charlie@example.com", "david@example.com"]})
        df.to_excel(test_xlsx, index=False)

        # Read employees
        employees = FileHandler.read_employees(test_xlsx)
        self.assertEqual(len(employees), 4)

        # Assign Secret Santa
        assigner = SecretSantaAssigner(employees, {})
        assigner.assign()
        FileHandler.save_assignments(test_output_xlsx, employees)

        # Ensure output file exists
        self.assertTrue(os.path.exists(test_output_xlsx))

        # Cleanup
        os.remove(test_xlsx)
        os.remove(test_output_xlsx)

if __name__ == "__main__":
    unittest.main()

