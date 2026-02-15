# AI-Powered Playwright Automation Framework

This project is a robust test automation framework built with **Python** and **Playwright**. It features a unique **AI-powered self-healing mechanism** that uses Google's Gemini models to automatically recover from locator failures during test execution.

## 🚀 Key Features

*   **Self-Healing Tests**: If a selector fails (e.g., changed ID or Class), the framework captures a screenshot and page source, sends it to the Gemini AI, and dynamically receives a corrected locator to continue the test.
*   **Auto-Correction Logging**: Suggested locator updates are logged in `locator_updates.txt` for easy maintenance.
*   **Page Object Model (like) Structure**: Reusable common functions and utilities.
*   **HTML Reporting**: Generates detailed HTML test reports with screenshots and videos.
*   **Data-Driven Testing**: Supports reading data from CSV files.
*   **Parallel Execution**: Integrated with `pytest-xdist`.

## 🛠️ Prerequisites

*   Python 3.8+
*   Google Gemini API Key

## 📦 Installation

1.  **Clone the repository**
    ```bash
    git clone <repository_url>
    cd playwrightProject
    ```

2.  **Create and activate a virtual environment**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Mac/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Playwright browsers**
    ```bash
    playwright install
    ```

## ⚙️ Configuration

1.  Create a `.env` file in the root directory.
2.  Add your Google Gemini API key:
    ```env
    GEMINI_API_KEY=your_actual_api_key_here
    ```

## ▶️ How to Run Tests

Run the tests using `pytest`. The following command runs tests with tracing enabled and generates an HTML report:

```bash
pytest -n=1 --tracing on --html=report.html Tests/test.py -v
```

*   `-n=1`: Number of parallel workers (via pytest-xdist).
*   `--tracing on`: Captures trace files for debugging.
*   `--html=report.html`: Generates a standalone HTML report.

## 🤖 How AI Recovery Works

1.  **Detection**: When a specific action (like `click_element` or `enter_text`) fails with a mismatch or timeout, the `CommonFunctions` wrapper catches the exception.
2.  **Analysis**:
    *   The system captures a screenshot of the failure state.
    *   It extracts the current page source.
    *   It constructs a prompt for the Gemini AI model ("gemini-2.5-flash").
3.  **Healing**: The AI analyzes the UI and suggests a robust locator.
4.  **Resume**: The test attempts to perform the action again with the new locator.
5.  **Log**: The change is recorded in `locator_updates.txt` in the format:
    `Test: <test_name> | Old: <old_locator> | New: <new_locator>`

## 📂 Project Structure

```
playwrightProject/
├── .venv/                   # Virtual environment
├── AutomationResults/       # Screenshots captured during exec
├── Data/                    # Test data (e.g., login_data.csv)
├── Resources/
│   ├── Common/
│   │   └── CommonFunctions.py  # Wrappers for Playwright actions & AI logic
│   └── Utilities/
│       └── Gen_AI.py           # Gemini API integration via requests
├── Tests/
│   └── test.py              # Test scripts
├── locator_updates.txt      # Log of AI-suggested locator repairs
├── report.html              # Test execution report
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables (API Key)
```

## 📝 Dependencies

*   `pytest-playwright`
*   `pytest-html`
*   `pytest-xdist`
*   `python-dotenv`
*   `requests`

## 📊 Reports

After execution, open `report.html` in any browser to view detailed test results, logs, and screenshots.
