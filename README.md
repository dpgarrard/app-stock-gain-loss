Stock Portfolio Tracker

A desktop GUI application built with **Python**, **wxPython**, **SQLite**, and the **Finnhub Stock API**. It retrieves stored portfolio holdings from a local database, fetches live market quotes via REST API calls, calculates real-time individual and net portfolio gains/losses, and displays the results in a desktop report table.

---

## Key Technical Highlights

* **Live REST API Integration:** Queries the Finnhub `/api/v1/quote` endpoint via the `requests` library to pull real-time market prices (`c`) for each stock symbol stored in the database.
* **Environment-Based Secret Management:** Uses `python-dotenv` (`load_dotenv()`) to load sensitive API credentials securely from a `.env` file, failing fast with a descriptive `ValueError` if `FINNHUB_API_KEY` is missing.
* **Automated Portfolio Valuation:** Computes per-position profit/loss using `(current_price - purchase_price) * shares` and aggregates total net portfolio performance formatted to two decimal places.
* **Event-Driven Desktop GUI:** Built with `wxPython` (`wx.Frame` and `wx.ListCtrl`), binding UI events to live API/database synchronization and surfacing HTTP or runtime exceptions through modal `wx.MessageDialog` alerts.

---

## Tech Stack

* **Language:** Python 3
* **GUI Framework:** wxPython (`wx`)
* **HTTP Client:** Requests (`requests`)
* **Database:** SQLite (`sqlite3`)
* **Configuration:** `python-dotenv`
* **External API:** [Finnhub Stock API](https://finnhub.io/)

---

## How to Set Up and Run the Application

### 1. Prerequisites

Ensure you have **Python 3.x** installed, then install the required third-party packages:

bash
pip install wxPython requests python-dotenv
2. Configure Your Finnhub API Key
Sign up for a free API key at finnhub.io.

Create a file named .env in the same directory as the Python script (dgarrard-pythonprogram4 (1).py).

Add your API key to the .env file using the exact variable name below:

Code snippet
FINNHUB_API_KEY=your_actual_finnhub_api_key_here
(Note: The application will raise a ValueError on startup if .env or FINNHUB_API_KEY is missing.)

3. Initialize the SQLite Database (tech_stocks.db)
The application reads portfolio holdings from a SQLite database named tech_stocks.db containing a table named dow_stocks. Create the database and populate it with sample holdings before launching the app:

SQL
CREATE TABLE IF NOT EXISTS dow_stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    symbol TEXT NOT NULL,
    purchase_price REAL NOT NULL,
    shares INTEGER NOT NULL
);

-- Example starter portfolio data:
INSERT INTO dow_stocks (company, symbol, purchase_price, shares) VALUES
    ('Apple', 'AAPL', 150.00, 10),
    ('Microsoft', 'MSFT', 280.50, 5),
    ('NVIDIA', 'NVDA', 110.25, 12);
(Tip: You can create tech_stocks.db using the sqlite3 CLI, DB Browser for SQLite, or a quick Python setup script in the same folder.)

4. Run the Application
Confirm that dgarrard-pythonprogram4 (1).py, .env, and tech_stocks.db are all in the same working directory.

Launch the application from your terminal:

Bash
python "dgarrard-pythonprogram4 (1).py"
Click Display Data in the Stock Data window to fetch current share prices, update the timestamp, populate the 6-column table (company, symbol, purchase price, Shares, current price, gain/loss), and view your net gains/losses at the top right.

Click Cancel to close the window.
