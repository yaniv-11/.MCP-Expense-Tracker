from fastmcp import FastMCP
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

mcp = FastMCP("ExpenseTracker")

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
        """)

init_db()

@mcp.tool()
def add_expense(date, amount, category, subcategory="", note=""):
    '''Add a new expense entry to the database.'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
            (date, amount, category, subcategory, note)
        )
        return {"status": "ok", "id": cur.lastrowid}
    
@mcp.tool()
def list_expenses(start_date, end_date):
    '''List expense entries within an inclusive date range.'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY id ASC
            """,
            (start_date, end_date)
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    
    
@mcp.tool()
def delete_expense(expense_id: int):
    """Delete an expense entry by ID."""
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        if cur.rowcount == 0:
            return {"status": "error", "message": f"No expense found with id {expense_id}"}
        return {"status": "ok", "deleted": cur.rowcount}


@mcp.tool()
def update_expense(expense_id: int, date=None, amount=None, category=None, subcategory=None, note=None):
    """Update fields of an expense entry by ID."""
    fields, values = [], []
    if date: fields.append("date = ?"); values.append(date)
    if amount is not None: fields.append("amount = ?"); values.append(amount)
    if category: fields.append("category = ?"); values.append(category)
    if subcategory: fields.append("subcategory = ?"); values.append(subcategory)
    if note: fields.append("note = ?"); values.append(note)

    if not fields:
        return {"status": "error", "message": "No fields to update."}

    values.append(expense_id)
    query = f"UPDATE expenses SET {', '.join(fields)} WHERE id = ?"

    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(query, values)
        if cur.rowcount == 0:
            return {"status": "error", "message": f"No expense found with id {expense_id}"}
        return {"status": "ok", "updated": cur.rowcount}

@mcp.tool()
def get_expense(expense_id: int):
    """Fetch a single expense by ID."""
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
        row = cur.fetchone()
        if not row:
            return {"status": "error", "message": f"No expense found with id {expense_id}"}
        cols = [d[0] for d in cur.description]
        return dict(zip(cols, row))


@mcp.tool()
def filter_expenses(category=None, subcategory=None):
    """Filter expenses by category and/or subcategory."""
    query = "SELECT * FROM expenses WHERE 1=1"
    params = []
    if category:
        query += " AND category = ?"
        params.append(category)
    if subcategory:
        query += " AND subcategory = ?"
        params.append(subcategory)
    query += " ORDER BY date ASC"

    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]


@mcp.tool()
def summarize(start_date, end_date, category=None):
    '''Summarize expenses by category within an inclusive date range.'''
    with sqlite3.connect(DB_PATH) as c:
        query = (
            """
            SELECT category, SUM(amount) AS total_amount
            FROM expenses
            WHERE date BETWEEN ? AND ?
            """
        )
        params = [start_date, end_date]

        if category:
            query += " AND category = ?"
            params.append(category)

        query += " GROUP BY category ORDER BY category ASC"

        cur = c.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    # Read fresh each time so you can edit the file without restarting
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    mcp.run()