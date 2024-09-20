
window.onload = init;


function init(){
    
    // Get total_cases from the data attribute in HTML
    const totalCasesElement = document.getElementById('total-cases-data');
    const totalCases = parseInt(totalCasesElement.getAttribute('data-total-cases'), 10);

    // Check for screen width to adjust zoom and control sizes for mobile
    const isMobile = window.innerWidth <= 600;
    const minZoom = isMobile ? 9 : 10; // Set lower zoom for smaller screens

    // Debug the value
    console.log("Total Cases: ", totalCases);

    // Check if the value is valid
    if (isNaN(totalCases)) {
        console.error("Total cases value is NaN!");
        return;
    }



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
        zoom: isMobile ? 9 : 10.8,  // Adjust default zoom based on screen size
        minZoom: minZoom, // Dynamic min zoom 
        zoomSnap:0.75,
        zoomDelta:1,
        layers:[Dark],
        zoomControl:false,
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


    // Define the bounds for each image
    const heatbounds = [[11.816501751176341, 124.27882890611566], [11.468813149687769, 124.62549853623533]];

    // Create image overlays
    const heatOverlayImage = L.imageOverlay(heatOverlay, heatbounds);


    //object in baselayers
    const baselayers = {
        'Dark':Dark,
        'Street Map':StreetMap,
        'Light':Light
    }
    
    // Adding layer control with expanded option
    L.control.layers(baselayers, {
        'Heat Overlay': heatOverlayImage,
    }, {
        collapsed: false,
        position: 'topright' // Adjust position of layer control
    }).addTo(mymap);


    // Create a heatmap layer and add it to the map
    var heat = L.heatLayer(heatmapData, {
        radius: 3,
        blur: 1,
        maxZoom: 20,
        gradient: {
            0.0: 'blue',     // Lowest intensity
            0.2: 'cyan',
            0.4: 'lime',
            0.6: 'yellow',
            0.8: 'orange',  
            1.0: 'red',
   
        },
        minOpacity: 0.5,
        maxIntensity: 100,
        opacity: 0.1
        
    }).addTo(mymap);

    // Create a custom control to display total cases
    var totalCasesControl = L.control({ position: 'topleft' });

    totalCasesControl.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'total-cases-control'); 
        div.innerHTML = `
        <div style="text-align: center;">
            <h2 style="color: red; margin: 0;">${totalCases}</h2> 
            <h4 style="color: black; margin: 0;">Total Patients</h4>  
        </div>
        `;
        div.style.backgroundColor = 'rgba(255, 255, 255, 1)';
        div.style.padding = isMobile ? '5px' : '10px'; // Adjust padding for mobile
        div.style.borderRadius = '8px';
        div.style.fontFamily = 'Arial, sans-serif';
        div.style.fontSize = '14px';
        div.style.boxShadow = '0 0 5px rgba(0, 0, 0, 0.3)'; // Optional: Add shadow
        return div;
    };

    // Add the custom control to the map
    totalCasesControl.addTo(mymap);
    


    //function to view latlng
    mymap.on('click',function(e){
        console.log(e.latlng)
    })



    
    
}