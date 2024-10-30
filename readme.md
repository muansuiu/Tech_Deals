
# Tech Deals

## Overview

This is an application designed to help users compare various PC components (e.g., keyboards, GPUs, etc.) from different vendors. (Till now only keyboards comparison is available). 
 The application scrapes product data using Selenium, stores it in a PostgreSQL database, and exposes a Django REST API for comparison based on features and prices.

## Features

- Scrapes product information (name, features, price, etc.) from multiple vendors.
- Stores the scraped data in a PostgreSQL database.
- Provides a RESTful API for comparing components.
- Supports filtering component according to their name.

## Technologies Used

- **Python**: Programming language used for scraping and building the API.
- **Selenium**: Tool for automating web browsers to scrape product data.
- **Django**: Web framework for building the RESTful API.
- **Django REST Framework**: Toolkit for building Web APIs in Django.
- **PostgreSQL**: Relational database management system to store scraped data.

## Installation

### Prerequisites

- Python 3.10
- PostgreSQL
- pip (Python package installer)
- Docker and Docker Compose (Optional)

### Steps to Install

 1.  **Clone the repository:**
    [https://github.com/muansuiu/Tech_Deals](https://github.com/muansuiu/Tech_Deals) \
   Then go to root directory of project `cd tech_deals`\
  **If you have docker and docker compose installed in your host:** \
    Enter this command: ``docker-compose up --build`` \
    Skip steps `(2-8)` and just follow step 9.
 2. **Create a virtual environment and activate:**
`python -m venv venv`
On Linux use `source venv/bin/activate`
On Windows use `venv\Scripts\activate`
 
 3. **Install the required packages:**
`pip install -r requirements.txt`

 4. **Create a postgres database named: `components`**
 5. **Adjust the settings.py file in the project directory with database settings**
 6. **Run the migrations to set up the database tables:** \
`python manage.py makemigrations` \
`python manage.py migrate`
 7. **Run the django admin script to scrape data** \
``python manage.py scrape_components_and_save_into_db startech`` \
``python manage.py scrape_components_and_save_into_db skyland``
 8. **Run the app**
- ``python manage.py runserver``
 9. **Acess the app from your browser or an api client (Postman)**
- API will be available at this: `http://localhost:8000/compare/api/search/`
- To search, add `?query=` any item. Like this url: `http://localhost:8000/compare/api/search/?query=AjazzAK820`
- If the similar product is found it will show the result with comparison, otherwise it'll show the message that the product is not found.
