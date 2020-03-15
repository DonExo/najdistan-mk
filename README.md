# Najdistan.mk

An early implementation of my Najdistan.mk project, which was initially intended to be released on the Macedonian web space, and potentially to be used as a place where you can rent or buy your next apartment.

This project was actually built in 2015-16, but came on GitHub in 2017. The project has room for lots of improvements, but eventually I've decided to rework it in a more modern framework.

It is using a very obsolete version of Flask (v0.12) - a now popular Python framework for building web applications. [Flask](https://flask.palletsprojects.com/en/1.1.x/) can now be considered a mature and reliable framework, as it has grown tremendously and has given a lot of importance in the python-web world.

This application is hosted on Heroku. It is using a free-tier package, which makes services slow on the initial request (when landing on the web page). Subsequent requests work normally. It can be found at: [Najdistan.mk](http://najdistan-mk.herokuapp.com)
(The database of the project is intentionally left in the project to provide some initial data in it. As you can see, there are lots of test/dummy names and images in the project itself. You can still register at the site, create your listing and play around with it).

Some of the functionalites are:
  * User registration, login and password reset
* User create, view, update and delete listings.
* "Interested In" functionality. You will receive an e-mail whenever there is a new listing submitted that match your pre-defined criteria.
* Apartment search.
* Comments
* Admin dashboard (can only be viewed by an Admin user)
* Updating user profile and more...
