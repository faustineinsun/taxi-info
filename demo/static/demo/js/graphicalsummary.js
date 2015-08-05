var map = L.map('map');
var layer = Tangram.leafletLayer({
    scene: '/static/demo/data/scene.yaml',
    attribution: '<a href="https://mapzen.com/tangram" target="_blank">Tangram</a> '
    +'| &copy; OSM contributors '
    +'| <a href="https://mapzen.com/" target="_blank">Mapzen</a> '
    +'| <a href="https://github.com/tangrams/tangram-sandbox" target="_blank">tangram-sandbox</a>'
});

layer.addTo(map);
map.setView([40.8891, -73.8405], 10) //NYC


///////////////////////////////
//   Chart                   //
///////////////////////////////
// reference: http://bl.ocks.org/mikehadlow/93b471e569e31af07cd3
// modified by faustineinsun
function showChart(data) {
    //var data = [[0,9],[1,9],[1,3],[2,3],[2,8],[3,5],[4,7],[5,3],[6,0]];
    data = JSON.parse(data);
    $("#passengerCountChart").empty();
    var containerHeight = 460;
    var containerWidth = 460;
    var xLabel = "Hour";
    var yLabel = "Passenger Count";

    var svg = d3.select("#passengerCountChart").append("svg")
        .attr("width", containerWidth)
        .attr("height", containerHeight);

    var margin = {
        top: 20,
        left: 40,
        right: 20,
        bottom: 40 
    };

    var height = containerHeight - margin.top - margin.bottom;
    var width = containerWidth - margin.left - margin.right;

    var xDomain = d3.extent(data, function(d) { return d[0]; })
    var yDomain = d3.extent(data, function(d) { return d[1]; });

    var xScale = d3.scale.linear().range([0, width]).domain(xDomain);
    var yScale = d3.scale.linear().range([height, 0]).domain(yDomain);

    var xAxis = d3.svg.axis().scale(xScale).orient('bottom').ticks(7);
    var yAxis = d3.svg.axis().scale(yScale).orient('left');

    var line = d3.svg.line()
        .x(function(d) { return xScale(d[0]); })
        .y(function(d) { return yScale(d[1]); });

    var g = svg.append('g').attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')');
    var xAxisColor='x axisWithoutML';
    var yAxisColor='x axisWithoutML';

    g.append('path')
    .datum(data);

    g.append('g')
    .attr('class', xAxisColor)
    .attr('transform', 'translate(0, ' + height + ')')
    .call(xAxis)
    .append('text')
    .attr('text-anchor', 'middle')
    .attr('x', 180)
    .attr('y', 40)
    .text(xLabel);

    g.append('g')
    .attr('class', yAxisColor)
    .call(yAxis)
    .append('text')
    .attr('transform', 'rotate(-90)')
    .attr('x', -180)
    .attr('y', -40)
    .attr('dy', '.71em')
    .attr('text-anchor', 'end')
    .text(yLabel);

    g.append('path')
    .datum(data)
    .attr('class', 'line')
    .attr('d', line);

    g.selectAll('circle').data(data).enter().append('circle')
        .attr('cx', function(d) {
            return xScale(d[0]);
        })
    .attr('cy', function(d) {
        return yScale(d[1]);
    })
    .attr('r', 5)
        .attr('class', 'circle');

    var focus = g.append('g').style('display', 'none');
    focus.append('line')
        .attr('id', 'focusLineX')
        .attr('class', 'focusLine');
    focus.append('line')
        .attr('id', 'focusLineY')
        .attr('class', 'focusLine');
    focus.append('circle')
        .attr('id', 'focusCircle')
        .attr('r', 5)
        .attr('class', 'circle focusCircle');

    var bisectDate = d3.bisector(function(d) {
        return d[0];
    }).left;
    g.append('rect')
        .attr('class', 'overlay')
        .attr('width', width)
        .attr('height', height)
        .on('mouseover', function() {
            focus.style('display', null);
        })
    .on('mouseout', function() {
        focus.style('display', 'none');
    })
    .on('mousemove', function() {
        var mouse = d3.mouse(this);
        var mouseDate = xScale.invert(mouse[0]);
        var i = bisectDate(data, mouseDate); // returns the index to the current data item
        var d0 = data[i - 1]
        var d1 = data[i];
    var d;
    if (typeof d0 === 'undefined') {
        d=d1;
    }else {
        d = mouseDate - d0[0] > d1[0] - mouseDate ? d1 : d0;
    }

    var x = xScale(d[0]);
    var y = yScale(d[1]);
    focus.select('#focusCircle')
        .attr('cx', x)
        .attr('cy', y);
    focus.select('#focusLineX')
        .attr('x1', x).attr('y1', yScale(yDomain[0]))
        .attr('x2', x).attr('y2', yScale(yDomain[1]));
    focus.select('#focusLineY')
        .attr('x1', xScale(xDomain[0])).attr('y1', y)
        .attr('x2', xScale(xDomain[1])).attr('y2', y);
    });
};
