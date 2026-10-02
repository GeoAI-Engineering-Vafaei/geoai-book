// ۵-۷) داده‌های مکان-زمانمند
var s2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
  .filterDate("2024-03-01", "2024-09-30")
  .filterBounds(geometry)                                   // your AOI
  .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20));

// add an NDVI band to every image: (NIR - Red) / (NIR + Red)
var withNDVI = s2.map(function (img) {
  return img.addBands(img.normalizedDifference(["B8", "B4"]).rename("NDVI"));
});
