d3.json("/titles").then(function(details) {
    

    mapboxgl.accessToken = 'pk.eyJ1IjoidGhpZW5hbmdpYW8iLCJhIjoiY2twM3NoMzYzMWp3YjJ3dGFqcjRubzJxeCJ9.m3xA8TgUpzdbFjLLeOBnMg';
    var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/light-v10',
    center: [12, 15],
    zoom: 1.63
    });

    map.addControl(new mapboxgl.FullscreenControl());

     // Add the control to the map.
     map.addControl(
        new MapboxGeocoder({
        accessToken: mapboxgl.accessToken,
        mapboxgl: mapboxgl
        })
        );  

    var country = []
    
    var data = []
    Object.entries(details).forEach(([key, value]) => {
        if(key === "Country") {
            country.push(value)
        }
        else {
            data.push(value)
        }
    })  
    console.log(data)
    ;

    
    map.on('load', function () {
// Add source for country polygons using the Mapbox Countries tileset
// https://docs.mapbox.com/vector-tiles/reference/mapbox-countries-v1
    map.addSource('countries', {
    type: 'vector',
    url: 'mapbox://mapbox.country-boundaries-v1'
    });
 
// Build a GL match expression that defines the color for every vector tile feature
// Use the ISO 3166-1 (Alpha-2) code as the lookup key for the country shape
    var matchExpression = ['match', ['get', 'iso_3166_1']];
 
// Calculate color values for each country based on 'titles' value
    data.forEach(function (row) {
// Convert the range of data values to a suitable color
    var red = -((row['Titles'] / 50)-170);
    var green = -((row['Titles'] / 50)-170);  
    var blue = 255;     
    var color = 'rgb('+ red + ',' + green + ',' + blue +')';
 
    matchExpression.push(row['Country'], color);
});
 
// Last value is the default, used where there is no data
    matchExpression.push('rgba(0, 0, 0, 0)');
 
// Add layer from the vector tile source to create the choropleth
// Insert it below the 'admin-1-boundary-bg' layer in the style
    map.addLayer(
    {
    'id': 'countries-join',
    'type': 'fill',
    'source': 'countries',  
    'source-layer': 'country_boundaries',
    'paint': {
    'fill-color': matchExpression
    }
    },
    'admin-1-boundary-bg'
);
});
})
