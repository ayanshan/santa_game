```markdown
# 🎁 Secret Santa Assignment Automation

This project automates the **Secret Santa** assignment process for employees in a company. It ensures that:
- Each employee gets exactly **one** secret child.
- No employee is assigned **to themselves**.
- No employee is assigned **the same secret child as last year**.
- The system handles **both CSV and Excel (XLSX) formats**.

---

## 🚀 Features
- **Fully Object-Oriented** implementation.
- **Prevents self-assignment** and **repetitions from last year**.
- **Ensures uniqueness**—every employee is assigned a different secret child.
- **Handles both CSV & Excel files** for input/output.
- **Modular design** for easy extension.
- **Automated tests** for validation.

---

## 🛠 Installation

### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/yourusername/secret-santa.git
cd secret-santa
```

Ensure you have Python **3.7+** installed. Then, install required packages:
```bash
pip install pandas openpyxl
```

---

## 📌 Usage

### 🎯 **Running the Secret Santa Assignment**
1. Prepare an **employee list** as a CSV or Excel file (`employees.csv` or `employees.xlsx`).
2. If applicable, prepare last year's assignment file (`last_year.csv` or `last_year.xlsx`).
3. Run the script:
```bash
python santa_game.py employees.csv last_year.csv output.csv
```
or for Excel:
```bash
python santa_game.py employees.xlsx last_year.xlsx output.xlsx
```

### 📂 **Input File Format**
| Employee_Name | Employee_EmailID |
|--------------|------------------|
| Alice        | alice@example.com |
| Bob          | bob@example.com   |

### 📂 **Last Year's Assignments**
| Employee_Name | Employee_EmailID | Secret_Child_Name | Secret_Child_EmailID |
|--------------|------------------|-------------------|----------------------|
| Alice        | alice@example.com | Bob              | bob@example.com      |

### 📂 **Generated Output File**
| Employee_Name | Employee_EmailID | Secret_Child_Name | Secret_Child_EmailID |
|--------------|------------------|-------------------|----------------------|
| Alice        | alice@example.com | Charlie          | charlie@example.com  |

---

## ✅ Running Tests

To ensure everything works correctly, run:
```bash
python -m unittest test_santa_game.py
```

### 🧪 **What is tested?**
✔ Employee objects are correctly created.  
✔ Secret children are assigned properly.  
✔ No employee is assigned themselves.  
✔ No repeat assignments from last year.  
✔ File handling works correctly for both CSV & Excel.

