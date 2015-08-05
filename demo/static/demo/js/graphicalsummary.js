var map = L.map('map');
var layer = Tangram.leafletLayer({
    scene: '/static/demo/data/scene.yaml',
    attribution: '<a href="https://mapzen.com/tangram" target="_blank">Tangram</a> '
    +'| &copy; OSM contributors '
    +'| <a href="https://mapzen.com/" target="_blank">Mapzen</a> '
    +'| <a href="https://github.com/tangrams/tangram-sandbox" target="_blank">tangram-sandbox</a>'
});

layer.addTo(map);
map.setView([40.78,-14.06], 3)
