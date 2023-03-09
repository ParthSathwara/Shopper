# Shopper
## E-Commerce app built using Django
This is an e-commerce web application built using the Django web framework. The application allows users to browse, search, and purchase products from the website.
Getting Started

#### Demo of: 
   home, products, product detail, filter and search functionality
   https://user-images.githubusercontent.com/87648167/223929822-5d0652ed-430a-491b-8e03-1e427a100f46.mp4


#### Demo of:
   login form, user profile form, addresses form, change password form, cart, checkout, orders 
   https://user-images.githubusercontent.com/87648167/223936601-ccf64c18-7973-404c-b95b-d0efb35764df.mp4



These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

   - Python 3.6 or higher
   - Django 3.0 or higher
   - Sqlite3 database

### Clone the repository:

In bash type:

    git clone https://github.com/ParthSathwara/Shopper.git


## Running this project

To get this project up and running you should start by having Python installed on your computer. It's advised you create a virtual environment to store your projects dependencies separately. You can install virtualenv with

```
pip install virtualenv
```

Clone or download this repository and open it in your editor of choice. In a terminal (mac/linux) or windows terminal, run the following command in the base directory of this project

```
virtualenv env
```

That will create a new folder `env` in your project directory. Next activate it with this command on mac/linux:

```
source env/bin/active
```

Then install the project dependencies with

```
pip install -r requirements.txt
```

Now you can run the project with this command

```
python manage.py runserver
```

## Features

The following features are available in the application:

 - User authentication: users can create an account and login/logout the website
 - User profile: user can add addresses and change password of his account
 - Product browsing: users can browse products by category or search for products by name or description
 - Product details: users can view detailed information about a product, including images, description, and price
 - Cart management: users can add products to their cart, increase/decrease items, view the cart, and checkout to place an order
 - Order history: users can view their order history and the status of their orders

## Architecture

- Shopper is built using the Django web framework, which follows the Model-View-Controller (MVC) architecture pattern. The database is implemented using Sqlite3, and the        front-end is implemented using HTML, CSS, Bootstrap, JavaScript and Ajax.

- The Shopper directory contains the main settings file and URL configuration. The app directory contains the application for managing products, users and authentication. The templates directory contains the HTML templates, the static directory contains the CSS and JavaScript files, and the media directory contains the uploaded images.
