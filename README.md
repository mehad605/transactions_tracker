# Transactions Tracker

A comprehensive Django-based personal finance application for tracking expenses and income.

## Features

- **User Authentication**: Secure registration and login system
- **Transaction Management**: Add, edit, and delete financial transactions
- **Categorization**: Organize transactions with customizable categories
- **Balance Tracking**: Automatically updated account balance
- **Filtering & Search**: Find transactions by date range, category, or keyword
- **Data Visualization**: View spending patterns through interactive charts
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

- **Framework**: Django 5.1.1
- **Database**: SQLite (default), with PostgreSQL support
- **Frontend**: HTML, CSS, JavaScript
- **Data Visualization**: Chart.js (via JavaScript)
- **Authentication**: Django's built-in authentication system with social auth options

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/transactions_tracker.git
   cd transactions_tracker
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser (for admin access):
   ```
   python manage.py createsuperuser
   ```

6. Start the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at http://127.0.0.1:8000/

## Project Structure

- **tracker/**: Core application with models, views, and templates
  - `models.py`: Defines UserProfile, Category, and Transaction models
  - `views.py`: Contains all view functions for handling requests
  - `forms.py`: Form definitions for user input
  - `templates/tracker/`: HTML templates for rendering pages
  - `static/tracker/`: CSS and JavaScript files
- **transactions_tracker/**: Project configuration
  - `settings.py`: Django settings
  - `urls.py`: URL routing configuration

## Usage

1. Register a new account or log in to an existing one
2. Set your initial account balance
3. Add income and expense transactions with categories
4. View your transaction history on the home page
5. Filter transactions by date range, type, or category
6. Manage categories through the category management page

## Deployment

This Django application can be deployed on:
- Heroku
- PythonAnywhere
- DigitalOcean
- AWS
- Any platform supporting Django applications

Note: For production deployment, make sure to:
1. Set `DEBUG = False` in settings.py
2. Configure a secure `SECRET_KEY`
3. Set up proper database credentials
4. Configure allowed hosts
5. Use HTTPS

## License

[MIT License](LICENSE)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request