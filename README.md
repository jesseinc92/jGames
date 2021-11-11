# [jGames](https://jgames-capstone.herokuapp.com/)

## About

jGames is an app that allows a user to create a personalized profile and then sort their favorite video games into lists! A user can create as many lists as they want and mix and match games as much as they want. The only limit is what games they can think of!

## Features

- Get in-depth video game information from the expansive giantbomb.com API.
- Create individual user profiles where you can choose your own avatar and your own bio.
- Create lists to sort all of your favorite games!
- Get recommended similar game options on every game page.

These features were implemented to give users a well-rounded experience. In order to keep lists organized, they've been attached to individual user profiles by relationships in the database. That way, any one user can only see the lists that they own. 

While searching for games that a user loves can be fun, implementing a recommended "similar games" feature allows the user to explore new titles while staying within their genre interests.

## Flow

First, a user arrives at the homepage, where they will be asked to either Login or Sign up. Once this is done, a search option appears on the homepage that allows them to immediately begin browsing for video games.

If a user finds a game they'd like to add to a list, they are taken to a page with a selection of lists to choose from for addition. If they'd like to create a new list, they can navigate to the user dashboard to create a new one. From the dashboard, a user can also see their profile details (and can navigate to a form that allows them to edit those details).

This is the basic flow of the app. And once the user is finished, they can close the page, or Logout, or both.

Future additions:

- The addition of an "Add List" button from the add-to-list page where a user adds a video game to a list.

## API

This app retrieves data from the giantbomb.com API. All calls for information are GET requests, and these requests are returned in JSON format. The base URL for the calls is https://www.giantbomb.com/api and the app makes use of calls to the /game, /search, and /video endpoints using various parameters. A rate limit of 200 requests per hour exists and the API access is granted with the use of an API key given when a developer signs up for their free service.

## Tech Stack

- HTML/CSS
- Python (Flask with Jinja2)
- JavaScript (Vanilla and Three.js)
- WTForms
- SQLAlchemy
- Bcrypt

## Database Schema

<img width="1333" alt="Screen Shot 2021-11-05 at 2 43 49 PM" src="https://user-images.githubusercontent.com/86806337/140562679-d09e6e92-86ab-4baf-9c72-e8bc1b3f6348.png">

