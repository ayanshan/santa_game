import csv
import random
import pandas as pd
import sys

class Employee:
    """Represents an employee participating in Secret Santa."""
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.secret_child = None  # Will be assigned later

    def assign_secret_child(self, child):
        """Assign a secret child to this employee."""
        self.secret_child = child

    def __repr__(self):
        return f"Employee({self.name}, {self.email})"

class SecretSantaAssigner:
    """Manages Secret Santa assignments while ensuring constraints are met."""
    def __init__(self, employees, last_year_assignments):
        self.employees = employees
        self.last_year_assignments = last_year_assignments

    def _is_valid_assignment(self, giver, child):
        """Checks if the assignment is valid."""
        return (
            giver.email != child.email and  # No self-assignment
            self.last_year_assignments.get(giver.email) != child.email  # No repeat from last year
        )

    def assign(self):
        """Assigns secret children to employees while following constraints."""
        random.shuffle(self.employees)  # Shuffle employees for randomness

        while True:
            assignments = {}
            available_children = set(self.employees)

            for giver in self.employees:
                possible_children = [
                    child for child in available_children if self._is_valid_assignment(giver, child)
                ]

                if not possible_children:
                    break  # Restart assignment if no valid choices exist

                chosen_child = random.choice(possible_children)
                assignments[giver] = chosen_child
                available_children.remove(chosen_child)  # Remove assigned child

            if len(assignments) == len(self.employees):  # Ensure valid assignment
                break

        for giver, child in assignments.items():
            giver.assign_secret_child(child)

    def get_assignments(self):
        """Returns a list of Secret Santa assignments."""
        return [(emp.name, emp.email, emp.secret_child.name, emp.secret_child.email) for emp in self.employees]

class FileHandler:
    """Handles reading and writing of CSV and Excel files."""
    
    @staticmethod
    def read_employees(file_path):
        """Reads employee data from CSV or Excel and returns a list of Employee objects."""
        employees = []
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Use CSV or Excel.")

        for _, row in df.iterrows():
            employees.append(Employee(row["Employee_Name"], row["Employee_EmailID"]))
        return employees

    @staticmethod
    def read_last_year_assignments(file_path):
        """Reads last year's assignments from CSV or Excel and returns a dictionary."""
        assignments = {}
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Use CSV or Excel.")

        for _, row in df.iterrows():
            assignments[row["Employee_EmailID"]] = row["Secret_Child_EmailID"]
        return assignments

    @staticmethod
    def save_assignments(file_path, employees):
        """Saves Secret Santa assignments to CSV or Excel."""
        data = [
            [emp.name, emp.email, emp.secret_child.name, emp.secret_child.email]
            for emp in employees
        ]
        df = pd.DataFrame(data, columns=["Employee_Name", "Employee_EmailID", "Secret_Child_Name", "Secret_Child_EmailID"])

        if file_path.endswith('.csv'):
            df.to_csv(file_path, index=False)
        elif file_path.endswith('.xlsx'):
            df.to_excel(file_path, index=False)
        else:
            raise ValueError("Unsupported file format. Use CSV or Excel.")

        print(f"✅ Secret Santa assignments saved to {file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python santa_game.py <employees_file> <last_year_file> <output_file>")
        sys.exit(1)
    
    EMPLOYEE_FILE = sys.argv[1]
    LAST_YEAR_FILE = sys.argv[2]
    OUTPUT_FILE = sys.argv[3]

    # Load employees and last year's assignments
    employees = FileHandler.read_employees(EMPLOYEE_FILE)
    last_year_assignments = FileHandler.read_last_year_assignments(LAST_YEAR_FILE)

    # Perform Secret Santa assignment
    santa_assigner = SecretSantaAssigner(employees, last_year_assignments)
    santa_assigner.assign()

    # Save results
    FileHandler.save_assignments(OUTPUT_FILE, employees)

