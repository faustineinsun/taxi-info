$(document).ready(function() {
    $('#example').dataTable( {
        "aLengthMenu": [[25, 50, 75, -1], [25, 30, 40, 50]],
        "iDisplayLength": 25,
        "ajax": "/static/demo/data/taxiinfo.json",
        "columns": [
            { "data": "hack_license" },
            { "data": "pickup_datetime" },
            { "data": "dropoff_datetime" },
            { "data": "passenger_count" },
            { "data": "trip_distance" },
            { "data": "pickup_longitude" },
            { "data": "pickup_latitude" },
            { "data": "dropoff_longitude" },
            { "data": "dropoff_latitude" }
        ]
    } );
} );

