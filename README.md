# Library Service


## Description
This project upgrades the library system, enabling users to borrow books and pay in cash based on reading duration. It replaces outdated manual tracking with an online management system, improving efficiency, inventory visibility, and user experience.


## Technologies Used
- Python
- Django ORM
- Django
- DRF


## Features
API with Books data
Borrowing feature
Filtering Borowwings list


## Setup
To install the project locally on your computer, execute the following commands in a terminal:
```bash
git clone https://github.com/Illya-Maznitskiy/library-service.git
cd library-service
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
```


## Commands to test the project:
You can run the tests and check code style using `flake8` with the following commands:

```
python manage.py test
flake8
```


## Configuration .env
1. Create a .env file in the root directory of the project and add the necessary configuration by the [sample.env](sample.env) file.


## Access
- **Superusers**: Can modify all data (e.g., add, update, delete entries) in the Theatre API.
- **Authenticated Users**: Can view data and create reservations and tickets but cannot modify existing data.
To create a superuser, use the following command:

```bash
python manage.py createsuperuser
```
After creating the superuser, you can log in using these credentials on the /api/user/login/ page to get your authentication token. This token can be used for authorized access to the Library API.


## API Endpoints
- api/books/


## Screenshots:
![Library Structure](screenshots/library_structure.png)
