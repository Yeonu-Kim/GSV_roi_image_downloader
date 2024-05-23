// Load the GAUL Level 2 dataset (administrative boundaries).
var gaul = ee.FeatureCollection("FAO/GAUL/2015/level2");

// Filter the dataset to get the feature for Seoul.
// You can check the city data from "Unique_ADM2.csv"
var seoul = gaul.filter(ee.Filter.eq('ADM2_NAME', 'YOUR_ROI_NAME')).first();

// Print the boundary to the console to verify.
print('roi Boundary:', roi);

// Define the interval (distance between points) in degrees.
var interval = 0.005;  // Adjust this value based on the desired interval.

// Calculate the bounding box of the polygon.
var bounds = roi.bounds();
var coords = bounds.coordinates().get(0);
console.log(coords);
console.log(ee.List(ee.List(coords).get(0)).get(0));
var xmin = ee.Number(ee.List(ee.List(coords).get(0)).get(0));
var ymin = ee.Number(ee.List(ee.List(coords).get(0)).get(1));
var xmax = ee.Number(ee.List(ee.List(coords).get(2)).get(0));
var ymax = ee.Number(ee.List(ee.List(coords).get(2)).get(1));

// Generate a list of x coordinates and y coordinates.
var xPoints = ee.List.sequence(xmin, xmax, interval);
var yPoints = ee.List.sequence(ymin, ymax, interval);

// Create a grid of points within the bounding box.
var gridPoints = xPoints.map(function(x) {
  return yPoints.map(function(y) {
    return ee.Feature(ee.Geometry.Point([x, y]));
  });
}).flatten();

// Filter points to keep only those within the polygon.
var pointsWithinPolygon = ee.FeatureCollection(gridPoints)
  .filterBounds(roi);

// Print the resulting points to the console.
print('Points within roi polygon:', pointsWithinPolygon);

// Display the points on the map.
Map.addLayer(pointsWithinPolygon, {color: 'blue'}, 'Points');

// Convert the points to a string representation of lat, lon.
var pointsString = pointsWithinPolygon.map(function(feature) {
  var coords = ee.Geometry(feature.geometry()).coordinates();
  var lon = ee.Number(coords.get(0));
  var lat = ee.Number(coords.get(1));
  return ee.Feature(null, {'lat': lat, 'lon': lon});
});

// Convert the FeatureCollection to a single Feature.
var pointsFeature = ee.FeatureCollection(pointsString);

// Export the points to a CSV file in Google Drive.
Export.table.toDrive({
  collection: pointsFeature,
  description: 'Points_within_roi',
  fileFormat: 'CSV'
});