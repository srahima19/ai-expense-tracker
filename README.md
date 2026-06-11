# 💰 AI Expense Tracker

A smart console-based Python application to record, manage, analyze, and monitor daily expenses — built using **Core Python only** (no frameworks or external libraries).

---

## 📋 Features

### Core Features
- ➕ **Add Expense** — Enter title, amount, category, and date
- 📋 **View All Expenses** — Clean tabular display of all records
- 🧮 **Total Expenses** — Total spending, transaction count, and average
- 📊 **Category Analysis** — Per-category breakdown with mini bar chart, highest & lowest spending
- 🔍 **Search** — Search by title keyword, category, or date
- 🗑️ **Delete Expense** — Remove any record by number
- 💾 **File Handling** — Auto-saves and loads data using JSON
- 🤖 **AI Suggestions** — Budget warnings, saving tips, top spending day, category-based advice

### Bonus Features
- 💰 Set custom monthly budget at runtime
- 📤 Export all expenses to CSV
- 🔃 Sort expenses by amount or date
- 📅 Filter expenses by date range

---

## 🐍 Python Concepts Used

| Concept | Where Used |
|---|---|
| Variables & Data Types | Throughout |
| Conditional Statements | Budget warnings, validation |
| Loops | Menu, data processing |
| Functions | Every feature is modular |
| Lists | Storing expense records |
| Dictionaries | Individual expense objects |
| String Handling | Search, formatting |
| File Handling | JSON save/load, CSV export |
| Exception Handling | Input validation, file errors |

---

## 🚀 How to Run

**Requirements:** Python 3.x — no external libraries needed.

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ai-expense-tracker.git

# Navigate into the folder
cd ai-expense-tracker

# Run the program
python ai_expense_tracker.py
```

---

## 📁 Project Structure

```
ai-expense-tracker/
│
├── ai_expense_tracker.py   # Main application file
├── expenses.json           # Auto-generated data file (created on first run)
├── expenses_export.csv     # CSV export (created when you use Export feature)
└── README.md               # Project documentation
```

---

## 🖥️ Menu Overview

```
===========================================================
          💰  AI EXPENSE TRACKER  💰
===========================================================
  1.  Add New Expense
  2.  View All Expenses
  3.  Calculate Total Expenses
  4.  Category-Based Analysis
  5.  Search Expense
  6.  Delete Expense
  7.  AI Spending Insights
  8.  Set Monthly Budget
  ──  BONUS  ──────────────────────────────────────────────
  9.  Export to CSV
  10. Sort Expenses
  11. Filter by Date Range
  0.  Exit
===========================================================
```

---

## 📸 Sample Output

```
  #    Title                Category       Date          Amount
  ────────────────────────────────────────────────────────────
  1    Lunch                Food           2026-05-12  PKR     350.00
  2    Uber Ride            Transport      2026-05-12  PKR     250.00
  3    Groceries            Food           2026-05-13  PKR    2500.00
  ────────────────────────────────────────────────────────────
  TOTAL                                               PKR    3100.00
```

---

## 🤖 AI Insights Example

```
  Monthly Budget   : PKR 30,000.00
  Total Spent      : PKR 24,500.00
  Remaining        : PKR 5,500.00
  Budget Used      : 81.7%

  🟡 WARNING: You have used 81.7% of your budget.
     Tip: Try to limit non-essential spending for the rest of the month.

  📅 Highest Spending Day : 2026-05-13 — PKR 5,200.00
  💸 Top Category : Food (43.2% of total spending)
     Tip: Consider meal-prepping at home to cut food costs.
  💡 Saving Suggestion: Put PKR 2,750.00 (50% of remaining) into savings.
```

---

## 👨‍💻 Author

- **Your Name**
- Course / Institute Name
- Project Submission — May 2026

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
