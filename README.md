This project aims to create a comprehensive data visualization track using a substantial dataset to highlight key insights through various visualizations. The goal is to provide clear, digestible visual narratives that can be interpreted easily by users of all levels, leveraging both common and novel tools in data visualization.

Purpose
The purpose of this project is to demonstrate the power of data visualization in uncovering trends and patterns within a dataset. By utilizing advanced visualization techniques and interactive elements, the project seeks to enhance user engagement and facilitate deeper understanding of the data.




Technology Stack
Frontend:
HTML/CSS:
HTML: Structuring the web pages.
CSS: Styling the web pages (likely served from the static folder).
JavaScript:
Vanilla JavaScript: Handling user interactions and dynamic content updates.
Fetch API: Fetching data from the backend.
Lightweight Charts: Visualizing financial data (TradingView Lightweight Charts library).
UI Frameworks/Libraries:
Lightweight Charts: For interactive financial charts (from TradingView).
Backend:
Python:
Flask: Web framework for building the backend and serving HTML pages and APIs.
Pandas: Data manipulation and analysis (for handling CSV data and generating tick data).
NumPy: Numerical operations (used in generating random tick prices).
Random: For generating random tick data.
Datetime: For date and time manipulations.
Database:
SQLAlchemy: ORM (Object-Relational Mapping) tool for database interactions.
PostgreSQL/MySQL/SQLite: Likely database systems for storing OHLCV data (specific database not mentioned but SQLAlchemy supports various databases).
APIs:
Flask Routes: To serve data and charts.
/cryptos: Provides a list of available symbols.
/ohlcv/<symbol>: Provides OHLCV data for a specific symbol.
/api/get_ticks: Provides generated tick data for a specific symbol.
/chart/<symbol>: Serves chart visualization (if applicable).
Development & Deployment:
Development Tools:
VS Code/PyCharm/IDE: Code editors or IDEs for development.
Git: Version control system for managing code changes.
Deployment:
Heroku/AWS/GCP/Azure: Cloud platforms for deploying your Flask application (based on your deployment choice).
Hosting:
GitHub/Bitbucket: For hosting the source code and version control.
Package Management:
pip: Python package installer for managing Flask, Pandas, NumPy, etc.
requirements.txt: To list the Python dependencies for your Flask app.
Summary
Frontend: HTML, CSS, Vanilla JavaScript, Fetch API, Lightweight Charts.
Backend: Flask, Python, Pandas, NumPy, SQLAlchemy, and potentially PostgreSQL/MySQL/SQLite.
Development & Deployment: IDEs, Git, cloud deployment platforms.
