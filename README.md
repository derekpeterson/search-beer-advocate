search-beer-advocate
====================

##BeerAdvocate search project for SI 650##

When run end-to-end, the Python script will work from the BeerAdvocate Styles page, hit every style, collect all of the beer profile URLs from those styles, and pass that list of URLs to a crawler that then collects the name, URL, score, and review text for that beer and drops them into an SQLite database named reviews.db. With a couple of changes, it dumps the URLs into a text file and de-duplicate them. Don't use this script.

The front-end for this thing is [hosted on Heroku](http://beersearchadvocate.herokuapp.com). It's still raw, but usable.
