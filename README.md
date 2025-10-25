Here's a beautified version of your README, using enhanced Markdown formatting, code blocks, and emojis for better readability.

-----

# ExpenseTracker (FastMCP) 💸

## 📝 Description

This project is a simple, file-based expense tracker application built using the `fastmcp` framework. It uses an SQLite database (`expenses.db`) to store, manage, and query expense data. It exposes several "tools" (functions) that can be called via the FastMCP environment to add, list, update, delete, filter, and summarize expenses.

-----

## ✨ Features

  * **Add Expenses:** Record new expenses with date, amount, category, subcategory, and notes.
  * **List Expenses:** Retrieve a list of all expenses within a specified date range.
  * **Update & Delete:** Modify or remove existing expense entries by their unique ID.
  * **Detailed View:** Fetch all details for a single expense by its ID.
  * **Filtering:** Filter the expense list by category and/or subcategory.
  * **Summarization:** Get a summary of total spending by category within a date range.
  * **Category Management:** Loads expense categories from an external `categories.json` file.

-----

## 🛠️ Requirements

  * Python 3.x
  * `fastmcp`: `pip install fastmcp`
  * `sqlite3` (included in the Python standard library)

-----

## 🚀 Setup & Installation

1.  **Get the code:**
    Clone the repository or save the code as `main.py`.

2.  **Install dependencies:**
    The only external dependency is `fastmcp`.

    ```bash
    pip install fastmcp
    ```

3.  **Create `categories.json`:**
    In the same directory as `main.py`, you **must** create a file named `categories.json`. This file defines the valid categories and subcategories for your expenses.

    *Example `categories.json`:*

    ```json
    {
      "Food": [
        "Groceries",
        "Restaurants",
        "Coffee",
        "Takeaway"
      ],
      "Transport": [
        "Gas",
        "Public Transit",
        "Taxi",
        "Repairs"
      ],
      "Housing": [
        "Rent",
        "Utilities",
        "Insurance"
      ],
      "Entertainment": [
        "Movies",
        "Subscriptions"
      ]
    }
    ```

4.  **Run the application:**

    ```bash
    python main.py
    ```

    This will start the FastMCP service. The script will automatically create the `expenses.db` SQLite database file in the same directory if it doesn't already exist.

-----

## 🗄️ Database Schema

The application uses an SQLite database file (`expenses.db`) with a single table: `expenses`.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Unique identifier for the expense. |
| `date` | `TEXT` | `NOT NULL` | Date of the expense (e.g., "YYYY-MM-DD"). |
| `amount` | `REAL` | `NOT NULL` | The monetary value of the expense. |
| `category` | `TEXT` | `NOT NULL` | The main category (e.g., "Food"). |
| `subcategory` | `TEXT` | `DEFAULT ''` | The optional subcategory (e.g., "Groceries"). |
| `note` | `TEXT` | `DEFAULT ''` | An optional text note for the expense. |

-----

## 🤖 API / Tools Reference

The following tools and resources are exposed by the FastMCP application.

### `add_expense`

Adds a new expense entry to the database.

  * **Tool Name:** `add_expense`
  * **Parameters:**
      * `date` (str): The date of the expense (format `YYYY-MM-DD`).
      * `amount` (float): The expense amount.
      * `category` (str): The main category.
      * `subcategory` (str, optional): The subcategory. Defaults to `""`.
      * `note` (str, optional): A descriptive note. Defaults to `""`.
  * **Returns:** A dictionary with the status and the `id` of the newly created expense.
      * *Success:* `{"status": "ok", "id": 123}`

### `list_expenses`

Lists all expense entries within an inclusive date range, ordered by ID.

  * **Tool Name:** `list_expenses`
  * **Parameters:**
      * `start_date` (str): The start of the date range (format `YYYY-MM-DD`).
      * `end_date` (str): The end of the date range (format `YYYY-MM-DD`).
  * **Returns:** A list of dictionaries, where each dictionary represents an expense.
      * *Example:* `[{"id": 1, "date": "2024-10-25", "amount": 12.50, ...}, ...]`

### `delete_expense`

Deletes a single expense entry by its unique ID.

  * **Tool Name:** `delete_expense`
  * **Parameters:**
      * `expense_id` (int): The ID of the expense to delete.
  * **Returns:** A status dictionary.
      * *Success:* `{"status": "ok", "deleted": 1}`
      * *Error (Not Found):* `{"status": "error", "message": "No expense found with id 404"}`

### `update_expense`

Updates one or more fields of an existing expense entry.

  * **Tool Name:** `update_expense`
  * **Parameters:**
      * `expense_id` (int): The ID of the expense to update.
      * `date` (str, optional): New date.
      * `amount` (float, optional): New amount.
      * `category` (str, optional): New category.
      * `subcategory` (str, optional): New subcategory.
      * `note` (str, optional): New note.
  * **Returns:** A status dictionary.
      * *Success:* `{"status": "ok", "updated": 1}`
      * *Error (Not Found):* `{"status": "error", "message": "No expense found with id 404"}`
      * *Error (No fields):* `{"status": "error", "message": "No fields to update."}`

### `get_expense`

Fetches all details for a single expense by its ID.

  * **Tool Name:** `get_expense`
  * **Parameters:**
      * `expense_id` (int): The ID of the expense to retrieve.
  * **Returns:** A dictionary containing all fields for the expense, or an error message.
      * *Success:* `{"id": 1, "date": "2024-10-25", "amount": 12.50, ...}`
      * *Error (Not Found):* `{"status": "error", "message": "No expense found with id 404"}`

### `filter_expenses`

Filters expenses by category and/or subcategory, ordered by date.

  * **Tool Name:** `filter_expenses`
  * **Parameters:**
      * `category` (str, optional): The category to filter by.
      * `subcategory` (str, optional): The subcategory to filter by.
  * **Returns:** A list of expense dictionaries matching the criteria.

### `summarize`

Calculates the sum of expenses, grouped by category, within a specified date range.

  * **Tool Name:** `summarize`
  * **Parameters:**
      * `start_date` (str): The start of the date range (format `YYYY-MM-DD`).
      * `end_date` (str): The end of the date range (format `YYYY-MM-DD`).
      * `category` (str, optional): If provided, summarizes only for this specific category.
  * **Returns:** A list of dictionaries, each containing a `category` and its `total_amount`.
      * *Example:* `[{"category": "Food", "total_amount": 350.75}, {"category": "Transport", "total_amount": 120.00}]`

### `categories` (Resource)

A read-only resource that provides the contents of the `categories.json` file.

  * **Resource URI:** `expense://categories`
  * **MIME Type:** `application/json`
  * **Returns:** The raw JSON string content of the `categories.json` file.
