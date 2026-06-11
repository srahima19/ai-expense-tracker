# ============================================================
#   AI Expense Tracker
#   A console-based Python application for managing expenses
#   Uses: Variables, Data Types, Conditionals, Loops,
#         Functions, Lists, Dictionaries, File Handling,
#         String Handling, Exception Handling
# ============================================================

import json
import os
import datetime

# ──────────────────────────────────────────────────────────────
# CONSTANTS
# ──────────────────────────────────────────────────────────────
DATA_FILE = "expenses.json"

CATEGORIES = [
    "Food", "Transport", "Shopping", "Entertainment",
    "Health", "Education", "Utilities", "Other"
]

MONTHLY_BUDGET = 30000   # default budget (PKR) – user can change at runtime
WARNING_THRESHOLD = 0.80  # warn when 80 % of budget is used


# ══════════════════════════════════════════════════════════════
# FILE HANDLING
# ══════════════════════════════════════════════════════════════

def load_expenses():
    """Load expenses from JSON file. Returns a list of dicts."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        print("  [Warning] Could not read data file. Starting fresh.")
        return []


def save_expenses(expenses):
    """Save the expenses list to a JSON file."""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(expenses, f, indent=4)
        print("  [✓] Data saved successfully.")
    except IOError as e:
        print(f"  [Error] Could not save data: {e}")


# ══════════════════════════════════════════════════════════════
# HELPER / VALIDATION FUNCTIONS
# ══════════════════════════════════════════════════════════════

def get_valid_amount():
    """Keep asking until the user enters a positive number."""
    while True:
        raw = input("  Enter amount (PKR): ").strip()
        try:
            amount = float(raw)
            if amount <= 0:
                print("  [!] Amount must be greater than 0.")
            else:
                return round(amount, 2)
        except ValueError:
            print("  [!] Invalid input. Please enter a numeric value.")


def get_valid_date():
    """Keep asking until the user enters a date in YYYY-MM-DD format."""
    while True:
        raw = input("  Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
        if raw == "":
            return str(datetime.date.today())
        try:
            datetime.datetime.strptime(raw, "%Y-%m-%d")
            return raw
        except ValueError:
            print("  [!] Invalid date format. Use YYYY-MM-DD.")


def get_valid_category():
    """Display category menu and return the chosen category string."""
    print("\n  Categories:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"    {i}. {cat}")
    while True:
        choice = input("  Choose category number: ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(CATEGORIES):
                return CATEGORIES[idx]
            print(f"  [!] Please enter a number between 1 and {len(CATEGORIES)}.")
        except ValueError:
            print("  [!] Invalid input. Enter a number.")


def print_separator(char="─", width=56):
    print("  " + char * width)


def print_expense_row(idx, exp):
    """Print a single expense in a formatted row."""
    print(
        f"  {idx:<4} {exp['title']:<20} {exp['category']:<14} "
        f"{exp['date']:<12} PKR {exp['amount']:>10.2f}"
    )


# ══════════════════════════════════════════════════════════════
# CORE FEATURES
# ══════════════════════════════════════════════════════════════

# ── 1. Add New Expense ────────────────────────────────────────

def add_expense(expenses):
    """Collect expense details from user and append to the list."""
    print("\n  ── ADD NEW EXPENSE ──────────────────────────────")
    title = input("  Enter expense title: ").strip()
    if not title:
        print("  [!] Title cannot be empty.")
        return

    amount   = get_valid_amount()
    category = get_valid_category()
    date     = get_valid_date()

    expense = {
        "id":       len(expenses) + 1,
        "title":    title,
        "amount":   amount,
        "category": category,
        "date":     date,
    }

    expenses.append(expense)
    save_expenses(expenses)
    print(f"\n  [✓] Expense '{title}' of PKR {amount:.2f} added under {category}.")

    # AI suggestion: instant overspend check
    ai_instant_check(expenses, MONTHLY_BUDGET)


# ── 2. View All Expenses ──────────────────────────────────────

def view_all_expenses(expenses):
    """Display every stored expense in a tabular layout."""
    print("\n  ── ALL EXPENSES ─────────────────────────────────")
    if not expenses:
        print("  No expenses recorded yet.")
        return

    print_separator()
    print(f"  {'#':<4} {'Title':<20} {'Category':<14} {'Date':<12} {'Amount':>14}")
    print_separator()

    for i, exp in enumerate(expenses, 1):
        print_expense_row(i, exp)

    print_separator()
    total = sum(e["amount"] for e in expenses)
    print(f"  {'TOTAL':<50} PKR {total:>10.2f}")
    print_separator()


# ── 3. Total Expenses ─────────────────────────────────────────

def calculate_total(expenses):
    """Show total spending and transaction count."""
    print("\n  ── TOTAL EXPENSES ───────────────────────────────")
    if not expenses:
        print("  No expenses recorded yet.")
        return

    total  = sum(e["amount"] for e in expenses)
    count  = len(expenses)
    avg    = total / count

    print(f"  Total Transactions : {count}")
    print(f"  Total Spending     : PKR {total:,.2f}")
    print(f"  Average per Entry  : PKR {avg:,.2f}")


# ── 4. Category Analysis ──────────────────────────────────────

def category_analysis(expenses):
    """Show per-category totals, highest and lowest spending."""
    print("\n  ── CATEGORY-BASED ANALYSIS ──────────────────────")
    if not expenses:
        print("  No expenses recorded yet.")
        return

    # Build totals dict
    cat_totals = {}
    for exp in expenses:
        cat = exp["category"]
        cat_totals[cat] = cat_totals.get(cat, 0) + exp["amount"]

    sorted_cats = sorted(cat_totals.items(), key=lambda x: x[1], reverse=True)
    grand_total = sum(cat_totals.values())

    print_separator()
    print(f"  {'Category':<20} {'Total (PKR)':>14}  {'% of Spend':>10}")
    print_separator()

    for cat, amt in sorted_cats:
        pct = (amt / grand_total) * 100
        bar = "█" * int(pct // 5)   # mini bar chart (each block = 5 %)
        print(f"  {cat:<20} {amt:>14,.2f}  {pct:>9.1f}%  {bar}")

    print_separator()

    highest = sorted_cats[0]
    lowest  = sorted_cats[-1]
    print(f"  Highest Spending: {highest[0]} — PKR {highest[1]:,.2f}")
    print(f"  Lowest  Spending: {lowest[0]}  — PKR {lowest[1]:,.2f}")
    print_separator()


# ── 5. Search Expense ─────────────────────────────────────────

def search_expense(expenses):
    """Search expenses by title keyword, category, or date."""
    print("\n  ── SEARCH EXPENSE ───────────────────────────────")
    print("  1. Search by Title")
    print("  2. Search by Category")
    print("  3. Search by Date")

    choice = input("  Choose option: ").strip()

    results = []

    if choice == "1":
        keyword = input("  Enter keyword: ").strip().lower()
        results = [e for e in expenses if keyword in e["title"].lower()]

    elif choice == "2":
        category = get_valid_category()
        results = [e for e in expenses if e["category"] == category]

    elif choice == "3":
        date = get_valid_date()
        results = [e for e in expenses if e["date"] == date]

    else:
        print("  [!] Invalid option.")
        return

    if not results:
        print("  No matching expenses found.")
    else:
        print(f"\n  Found {len(results)} result(s):\n")
        print(f"  {'#':<4} {'Title':<20} {'Category':<14} {'Date':<12} {'Amount':>14}")
        print_separator()
        for i, exp in enumerate(results, 1):
            print_expense_row(i, exp)
        print_separator()
        print(f"  Sub-total: PKR {sum(e['amount'] for e in results):,.2f}")


# ── 6. Delete Expense ─────────────────────────────────────────

def delete_expense(expenses):
    """Let the user remove an expense by its display number."""
    print("\n  ── DELETE EXPENSE ───────────────────────────────")
    if not expenses:
        print("  No expenses to delete.")
        return

    view_all_expenses(expenses)

    try:
        idx = int(input("\n  Enter the # of the expense to delete (0 to cancel): "))
        if idx == 0:
            print("  Cancelled.")
            return
        if 1 <= idx <= len(expenses):
            removed = expenses.pop(idx - 1)
            save_expenses(expenses)
            print(f"  [✓] Deleted: '{removed['title']}' — PKR {removed['amount']:.2f}")
        else:
            print("  [!] Invalid number.")
    except ValueError:
        print("  [!] Please enter a valid number.")


# ══════════════════════════════════════════════════════════════
# AI-BASED SUGGESTIONS
# ══════════════════════════════════════════════════════════════

def ai_suggestions(expenses, budget):
    """Display intelligent spending insights and saving tips."""
    print("\n  ── AI SPENDING INSIGHTS ─────────────────────────")

    if not expenses:
        print("  Add some expenses first to get personalised insights.")
        return

    total = sum(e["amount"] for e in expenses)
    remaining = budget - total
    usage_pct = (total / budget) * 100 if budget > 0 else 0

    # ── Budget Status ──
    print(f"\n  Monthly Budget   : PKR {budget:,.2f}")
    print(f"  Total Spent      : PKR {total:,.2f}")
    print(f"  Remaining        : PKR {remaining:,.2f}")
    print(f"  Budget Used      : {usage_pct:.1f}%")

    if usage_pct >= 100:
        print("\n  🔴 ALERT: You have EXCEEDED your monthly budget!")
        print("     Tip: Review your 'Shopping' and 'Entertainment' expenses first.")
    elif usage_pct >= WARNING_THRESHOLD * 100:
        print(f"\n  🟡 WARNING: You have used {usage_pct:.1f}% of your budget.")
        print("     Tip: Try to limit non-essential spending for the rest of the month.")
    else:
        print(f"\n  🟢 Good job! You are within budget ({usage_pct:.1f}% used).")

    # ── Top spending day ──
    day_totals = {}
    for exp in expenses:
        day_totals[exp["date"]] = day_totals.get(exp["date"], 0) + exp["amount"]

    if day_totals:
        top_day   = max(day_totals, key=day_totals.get)
        top_day_amt = day_totals[top_day]
        print(f"\n  📅 Highest Spending Day : {top_day} — PKR {top_day_amt:,.2f}")

    # ── Category advice ──
    cat_totals = {}
    for exp in expenses:
        cat_totals[exp["category"]] = cat_totals.get(exp["category"], 0) + exp["amount"]

    if cat_totals:
        top_cat = max(cat_totals, key=cat_totals.get)
        top_amt = cat_totals[top_cat]
        top_pct = (top_amt / total) * 100

        print(f"\n  💸 Top Category : {top_cat} ({top_pct:.1f}% of total spending)")

        if top_cat == "Food" and top_pct > 40:
            print("     Tip: Consider meal-prepping at home to cut food costs.")
        elif top_cat == "Entertainment" and top_pct > 25:
            print("     Tip: Look for free or low-cost entertainment alternatives.")
        elif top_cat == "Shopping" and top_pct > 30:
            print("     Tip: Try a 24-hour rule before impulse purchases.")
        elif top_cat == "Transport" and top_pct > 20:
            print("     Tip: Carpooling or public transport can reduce costs.")
        else:
            print("     Tip: Keeping a diverse spend spread is a great habit!")

    # ── Saving suggestion ──
    if remaining > 0:
        save_suggestion = remaining * 0.50
        print(f"\n  💡 Saving Suggestion: Put PKR {save_suggestion:,.2f} (50% of remaining)"
              " into savings before month-end.")

    print()


def ai_instant_check(expenses, budget):
    """Quick AI check called right after adding a new expense."""
    total = sum(e["amount"] for e in expenses)
    usage_pct = (total / budget) * 100 if budget > 0 else 0

    if usage_pct >= 100:
        print(f"  🔴 AI Alert: Budget exceeded! Total: PKR {total:,.2f}")
    elif usage_pct >= WARNING_THRESHOLD * 100:
        print(f"  🟡 AI Warning: {usage_pct:.1f}% of monthly budget used.")


# ══════════════════════════════════════════════════════════════
# BONUS FEATURES
# ══════════════════════════════════════════════════════════════

def set_budget():
    """Let the user update the monthly budget at runtime."""
    global MONTHLY_BUDGET
    print(f"\n  Current monthly budget: PKR {MONTHLY_BUDGET:,.2f}")
    while True:
        raw = input("  Enter new monthly budget (PKR): ").strip()
        try:
            new_budget = float(raw)
            if new_budget <= 0:
                print("  [!] Budget must be positive.")
            else:
                MONTHLY_BUDGET = round(new_budget, 2)
                print(f"  [✓] Monthly budget updated to PKR {MONTHLY_BUDGET:,.2f}")
                return
        except ValueError:
            print("  [!] Invalid input. Enter a number.")


def export_to_csv(expenses):
    """Export all expenses to a CSV file."""
    filename = "expenses_export.csv"
    try:
        with open(filename, "w") as f:
            f.write("ID,Title,Amount,Category,Date\n")
            for exp in expenses:
                f.write(
                    f"{exp['id']},{exp['title']},{exp['amount']},"
                    f"{exp['category']},{exp['date']}\n"
                )
        print(f"  [✓] Exported to '{filename}' successfully.")
    except IOError as e:
        print(f"  [Error] Could not export: {e}")


def sort_expenses(expenses):
    """Sort expenses by amount or date and display them."""
    print("\n  Sort by:")
    print("  1. Amount (High → Low)")
    print("  2. Amount (Low → High)")
    print("  3. Date   (Newest first)")
    print("  4. Date   (Oldest first)")

    choice = input("  Choose option: ").strip()

    if choice == "1":
        sorted_exp = sorted(expenses, key=lambda x: x["amount"], reverse=True)
    elif choice == "2":
        sorted_exp = sorted(expenses, key=lambda x: x["amount"])
    elif choice == "3":
        sorted_exp = sorted(expenses, key=lambda x: x["date"], reverse=True)
    elif choice == "4":
        sorted_exp = sorted(expenses, key=lambda x: x["date"])
    else:
        print("  [!] Invalid option.")
        return

    print(f"\n  {'#':<4} {'Title':<20} {'Category':<14} {'Date':<12} {'Amount':>14}")
    print_separator()
    for i, exp in enumerate(sorted_exp, 1):
        print_expense_row(i, exp)
    print_separator()


def filter_by_date(expenses):
    """Show expenses between a start and end date."""
    print("\n  ── DATE FILTER ──────────────────────────────────")
    print("  Start date:")
    start = get_valid_date()
    print("  End date:")
    end   = get_valid_date()

    if start > end:
        print("  [!] Start date cannot be after end date.")
        return

    filtered = [e for e in expenses if start <= e["date"] <= end]

    if not filtered:
        print(f"  No expenses found between {start} and {end}.")
        return

    print(f"\n  Expenses from {start} to {end}:\n")
    print(f"  {'#':<4} {'Title':<20} {'Category':<14} {'Date':<12} {'Amount':>14}")
    print_separator()
    for i, exp in enumerate(filtered, 1):
        print_expense_row(i, exp)
    print_separator()
    print(f"  Sub-total: PKR {sum(e['amount'] for e in filtered):,.2f}")


# ══════════════════════════════════════════════════════════════
# MAIN MENU
# ══════════════════════════════════════════════════════════════

def print_menu():
    print("\n" + "=" * 58)
    print("          💰  AI EXPENSE TRACKER  💰")
    print("=" * 58)
    print("  1.  Add New Expense")
    print("  2.  View All Expenses")
    print("  3.  Calculate Total Expenses")
    print("  4.  Category-Based Analysis")
    print("  5.  Search Expense")
    print("  6.  Delete Expense")
    print("  7.  AI Spending Insights")
    print("  8.  Set Monthly Budget")
    print("  ──  BONUS  ──────────────────────────────────")
    print("  9.  Export to CSV")
    print("  10. Sort Expenses")
    print("  11. Filter by Date Range")
    print("  0.  Exit")
    print("=" * 58)


def main():
    expenses = load_expenses()

    print("\n  Welcome to AI Expense Tracker!")
    print(f"  Data file : {DATA_FILE}")
    print(f"  Records loaded : {len(expenses)}")

    while True:
        print_menu()
        choice = input("  Enter your choice: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_all_expenses(expenses)
        elif choice == "3":
            calculate_total(expenses)
        elif choice == "4":
            category_analysis(expenses)
        elif choice == "5":
            search_expense(expenses)
        elif choice == "6":
            delete_expense(expenses)
        elif choice == "7":
            ai_suggestions(expenses, MONTHLY_BUDGET)
        elif choice == "8":
            set_budget()
        elif choice == "9":
            export_to_csv(expenses)
        elif choice == "10":
            sort_expenses(expenses)
        elif choice == "11":
            filter_by_date(expenses)
        elif choice == "0":
            print("\n  Goodbye! Keep tracking your expenses. 👋\n")
            break
        else:
            print("  [!] Invalid choice. Please select from the menu.")


# ══════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()
