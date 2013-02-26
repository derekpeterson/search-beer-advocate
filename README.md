search-beer-advocate
====================

##BeerAdvocate search project for SI 650##

Supply a URL to the script on the command line

	$ python search.py http://beeradvocate.com/beer/profile/1199/47658
	
and you'll get back a pretty-printed JSON object with the page URL, the beer name, a list of the reviews on that page with their text and score, the overall BeerAdvocate score, and a list of similar beers with their name and URL like this:

	{
	    "url": "http://beeradvocate.com/beer/profile/1199/47658", 
	    "reviews": [
	        {
	            "text": "justyouraveragebeerguy 4.79 /5 rDev +2.6% look: 5 | smell: 4.75 | taste: 4.75 | feel: 5 |  overall: 4.75 Had on tap at founders 15th anniversary party A- Pitch black, no light can pass through this monster. A finger of a mocha/kacki head. S- Wow. Big vanilla, molasses, dark chocolate, coffee, some sweetness coming through Taste- Exactly how it smells. Right up front you get a sweetness immediately cut with a roasted coffee bitterness. Big vanilla, molasses and dark chocolate notes. The roast and coffee come through later on. O- I really don't know what more you can ask from a BA stout. This beer is absolutely amazing. By far the best beer I have ever had. Serving type: on-tap 02-26-2013 04:17:03&nbsp| More by justyouraveragebeerguy", 
	            "score": "4.79"
	        },
	        {...}
	    ], 
	    "score": "100", 
	    "similar": [
	        {
	            "url": "/beer/style/157", 
	            "name": "American Double / Imperial Stout"
	        },
	        {...}
	    ], 
	    "name": "Founders CBS Imperial Stout - Founders Brewing Company"
	}
