// ۱۶-۶) لایه‌ی نمایش: نقشه‌ی وب با Leaflet
const map = L.map("map").setView([35.72, 51.40], 12);
L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);

map.on("click", async (e) => {
  const { lat, lng } = e.latlng;

  const url = "http://localhost:8000/flood/classify-point"
            + `?lat=${lat}&lon=${lng}`;
  const res = await fetch(url);          // a read -> a plain GET
  const data = await res.json();

  L.popup()
    .setLatLng([lat, lng])
    .setContent("flood risk: " + data.risk_level)
    .openOn(map);
});
