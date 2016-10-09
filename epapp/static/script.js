var iconURLPrefix = 'http://maps.google.com/mapfiles/ms/icons/';

var icons = [
    iconURLPrefix + 'red-dot.png',
    iconURLPrefix + 'green-dot.png',
    iconURLPrefix + 'blue-dot.png',
    iconURLPrefix + 'orange-dot.png',
    iconURLPrefix + 'purple-dot.png',
    iconURLPrefix + 'pink-dot.png',
    iconURLPrefix + 'yellow-dot.png'
];

function showGoogleMaps(locations) {
    'use strict';

    var mapOptions = {
        zoom: 2, // initialize zoom level - the max value is 21
        center: new google.maps.LatLng(0, 0),
        streetViewControl: false, // hide the yellow Street View pegman
        scaleControl: true, // allow users to zoom the Google Map
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    var map = new google.maps.Map(document.getElementById('googlemaps'),
        mapOptions);

    var infowindow = new google.maps.InfoWindow({
        maxWidth: 500
    });

    var markers = [];

    var iconCounter = 0;

    // Add the markers and infowindows to the map
    for (var i = 0; i < locations.length; i++) {  
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(locations[i]['lat'], locations[i]['lng']),
            map: map,
            icon: icons[iconCounter]
        });

        markers.push(marker);

        google.maps.event.addListener(marker, 'click', (function(marker, i) {
            return function() {
                infowindow.setContent(generateContent(locations[i]));
                    infowindow.open(map, marker);
                }
        })(marker, i));
      
      	iconCounter++;
      	// We only have a limited number of possible icon colors, so we may have to restart the counter
      	if (iconCounter >= icons.length) {
      		iconCounter = 0;
      	}
    }
}

function generateContent(location) {
    return '<h3><a target="_blank" href="' + location.url + '">' + location.title + '</a></h3>' +
    '<div><a target="_blank" href="http://www.reddit.com/r/' + location.subreddit + '">/r/' + location.subreddit + '</a></div>' +
    '<img alt="' + location.query + '" src="' + location.image_url + '" class="featured-img">';
}

$(document).ready(function () {
	$.getJSON('/data', function (data) {
        var localTimestamp = data['last_updated'] + (moment().utcOffset() * 60);
        $('#timestamp').html(moment.utc(localTimestamp * 1000).fromNow());
		showGoogleMaps(data['results']);
	});
});
