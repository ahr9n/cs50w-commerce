<div align="center">
 <img style="width: 20%;" src="https://github.com/ahr9n/cs50w-commerce/blob/master/auctions/static/auctions/img/icon.png" alt="Best Place to Bid!">
</div>

# Commerce
Project 2 for CS50’s Web Programming with Python and JavaScript.

## Overview
An eBay-like e-commerce auction site design that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”

## Specification
This project fulfills the following requirements:

* **Models**: the application has at least three models in addition to the `User` model: one for auction listings, one for bids, and one for comments made on auction listings. Also, I add fields for each model as needed.
* **Create Listing**: Users are able to visit a page to create a new listing. They are able to specify a title for the listing, a text-based description, and what the starting bid should be. Users also are optionally able to provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).
* **Active Listings Page**: The default route of the web application lets users view all of the currently active auction listings. For each active listing, this page should display (at minimum) the title, description, current price, and photo (if one exists for the listing).
* **Listing Page**: Clicking on a listing takes users to a page specific to that listing. On that page, users are able to view all details about the listing, including the current price for the listing.
  * If the user is signed in, the user is able to add the item to their “Watchlist.” If the item is already on the watchlist, the user is able to remove it.
  * If the user is signed in, the user is able to bid on the item. The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any). If the bid doesn’t meet those criteria, the user is presented with an error.
  * If the user is signed in and is the one who created the listing, the user has the ability to “close” the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.
  * If a user is signed in on a closed listing page, and the user has won that auction, the page will say so.
  * Users who are signed in are able to add comments to the listing page. The listing page displays all comments that have been made on the listing.
* **Watchlist**: Users who are signed in are able to visit a Watchlist page, which displays all of the listings that a user has added to their watchlist. Clicking on any of those listings takes the user to that listing’s page.
* **Categories**: Users are able to visit a page that displays a list of all listing categories. Clicking on the name of any category takes the user to a page that displays all of the active listings in that category.
* **Django Admin Interface**: Via the Django admin interface, a site administrator is able to view, add, edit, and delete any listings, comments, and bids made on the site.

## Setup
Requires Python3 and the package installer for Python (pip) to run:

* Install requirements (Django4): `pip install -r requirements.txt`
* After cloning the repository, refer to the project folder and:
  1. Create new migrations based on the changes in models: `python3 manage.py makemigrations`
  2. Apply the migrations to the database: `python3 manage.py migrate`
  3. Create a superuser to be able to use Django Admin Interface: `python3 manage.py createsuperuser`
  4. Run the app locally: `python3 manage.py runserver`
  5. Visit the site: `http://localhost:8000`
  6. Enjoy!

## Topics
Built with [`Python`](https://www.python.org/downloads/), [`Django`](https://www.djangoproject.com/), and HTML/CSS.

## Future Work
Some challenges I would make in my free-time:
* Make nicer front-end design.
