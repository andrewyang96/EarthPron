# EarthPron
Fetches hot posts in /r/earthporn and related subreddits and maps them onto a webpage with Google maps background. Uses [Alchemy API](http://www.alchemyapi.com/) to parse relevant entities in post titles and feeds them to Google's Geocoding API to fetch coordinates that appear on the map.

[Link to Multireddit](http://www.reddit.com/user/theyangmaster/m/earthporns)

[Link to Website](http://earthpron.rocks)

## Process
1. Fetch hot posts from Reddit.
2. For each new post, extract entities from the post title using AlchemyAPI.
3. Feed the entity words into Google Reverse Geocoding API to get a coordinate.
4. Collect all coordinates from the posts and update the database.
