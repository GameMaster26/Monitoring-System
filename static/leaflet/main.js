window.onload = init;


function init(){
    
    // Get the total cases from Django context and convert it to a number
    const totalCases = parseInt("{{ total_cases }}", 10);

    // Get heatmap data from script tag
    var heatmapDataScript = document.getElementById('heatmap-data');
    var heatmapData = JSON.parse(heatmapDataScript.textContent);

    //creating variables for each base layer
    const Dark = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',{
        attribution: 'Animal Bite and Rabies Monitoring with GEO Mapping &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        //attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        //attribution: 'Animal Bite and Rabies Monitoring with GEO Mappping',
        maxZoom: 19, // Specify maxZoom to prevent users from zooming beyond the max level of the tile layer
    })
    const StreetMap = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        //attribution: 'Animal Bite and Rabies Monitoring with GEO Mappping',
    })
    const Light = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    attribution: 'Animal Bite and Rabies Monitoring with GEO Mappping',
    })

    const maxBounds = L.latLngBounds(
        L.latLng(11.358607609157232, 123.91744935882099), // Southwest corner
        L.latLng(11.897821676214718, 125.01560057070333) // Northeast corner
        );

    //Creating the center of the map 
    const mymap = L.map('mama',{
        center:[11.6400,124.4642],
        zoom:10.8,
        zoomSnap:0.75,
        zoomDelta:1,
        layers:[Dark],
        /* zoomControl:false,
        doubleClickZoom: false,
        scrollWheelZoom: false,
        attributionControl:false,
        doubleClickZoom: false,
        dragging: false, 
        touchZoom: false,  */
    }).setMaxBounds(maxBounds);

    // Add zoom control manually to the bottom left
    L.control.zoom({
        position: 'bottomright'
    }).addTo(mymap);

    

    
    // Define the image paths
    const heatOverlay = 'static/leaflet/images/over.png';
    const foundCases = 'static/leaflet/images/foundCases.png';
    const legend = 'static/leaflet/images/legend.png';

    // Define the bounds for each image
    const heatbounds = [[11.816501751176341, 124.27882890611566], [11.468813149687769, 124.62549853623533]];
    const foundCasesBounds = [[11.862441599374863, 123.87604124101928], [11.772764806345831, 124.01967042198523]];
    const legendBounds = [[11.463685022849134, 123.88335525231034], [11.426345482253387, 123.9751614939354]];

    // Create image overlays
    const heatOverlayImage = L.imageOverlay(heatOverlay, heatbounds);
    const foundCasesImage = L.imageOverlay(foundCases, foundCasesBounds);
    const legendImage = L.imageOverlay(legend, legendBounds);

    // Add image overlays to the map
    /* heatOverlayImage.addTo(mymap);
    foundCasesImage.addTo(mymap);
    legendImage.addTo(mymap); */

    //object in baselayers
    const baselayers = {
        'Dark':Dark,
        'Street Map':StreetMap,
        'Light':Light
    }
    
    // Adding layer control with expanded option
    L.control.layers(baselayers, {
        'Heat Overlay': heatOverlayImage,
        /* 'Found Cases': foundCasesImage,
        'Legend': legendImage */
    }, {
        collapsed: false,
        position: 'topright' // Adjust position of layer control
    }).addTo(mymap);

    // Example heatmap data from Django context
    /* var heatmapData = {{ heatmap_data|safe }}; */

    // Create a heatmap layer and add it to the map
    var heat = L.heatLayer(heatmapData, {
        radius: 15,
        blur: 5,
        maxZoom: 20,
        gradient: {
            0.1: 'red',
            0.2: 'cyan',
            0.3: 'lime',
            0.4: 'yellow',
            0.5: 'orange',
            1: 'red',
        },
        minOpacity: 0.1,
        maxIntensity: 100,
        opacity: 0.8
        
    }).addTo(mymap);
    


    //function to view latlng
    mymap.on('click',function(e){
        console.log(e.latlng)
    })

    var myIcon = L.icon({
        iconUrl: 'static/assets/images/marker.png',
        iconSize: [20, 30],
        iconAnchor: [5, 30],
        /* popupAnchor: [-3, -76],
        shadowSize: [68, 95],
        shadowAnchor: [22, 94] */
    });

    
    
}
    