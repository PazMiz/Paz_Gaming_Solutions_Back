Set Up the Backend:

Navigate to the backend directory.

Install the required Python packages using pip.

shell
Copy code
pip install -r requirements.txt
Create and apply migrations to set up the database.

shell
Copy code
python manage.py makemigrations
python manage.py migrate
Start the Django development server.

shell
Copy code
python manage.py runserver
API Endpoints: Your Django backend is now running, and you can access the API endpoints at http://localhost:8000.

