var iconURLPrefix = 'http://maps.google.com/mapfiles/ms/icons/';
    
var icons = [
	iconURLPrefix + 'red-dot.png',
	iconURLPrefix + 'green-dot.png',
	iconURLPrefix + 'blue-dot.png',
	iconURLPrefix + 'orange-dot.png',
	iconURLPrefix + 'purple-dot.png',
	iconURLPrefix + 'pink-dot.png',      
	iconURLPrefix + 'yellow-dot.png'
]

var iconsLength = icons.length;

function showGoogleMaps(locations) {
	var mapOptions = {
		zoom: 2, // initialize zoom level - the max value is 21
		center: new google.maps.LatLng(0, 0),
		streetViewControl: false, // hide the yellow Street View pegman
		scaleControl: true, // allow users to zoom the Google Map
		mapTypeId: google.maps.MapTypeId.ROADMAP,
	};
	 
	map = new google.maps.Map(document.getElementById('googlemaps'),
	mapOptions);

	var infowindow = new google.maps.InfoWindow({
		maxWidth: 500
    });

    var markers = new Array();
    
    var iconCounter = 0;
    
    // Add the markers and infowindows to the map
    for (var i = 0; i < locations.length; i++) {  
		var marker = new google.maps.Marker({
        	position: new google.maps.LatLng(locations[i][1], locations[i][2]),
        	map: map,
        	icon: icons[iconCounter]
      	});

      	markers.push(marker);

      	google.maps.event.addListener(marker, 'click', (function(marker, i) {
        	return function() {
          		infowindow.setContent(locations[i][0]);
          		infowindow.open(map, marker);
        	}
      	})(marker, i));
      
      	iconCounter++;
      	// We only have a limited number of possible icon colors, so we may have to restart the counter
      	if (iconCounter >= iconsLength) {
      		iconCounter = 0;
      	}
    }
}

$(document).ready(function () {
	$.getJSON("/earthporn.json", function (data) {
		showGoogleMaps(data);
	});
});
