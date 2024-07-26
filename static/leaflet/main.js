window.onload = init;

function init(){


    //creating variables each baselayers
    const Dark = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',{
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        attribution: 'Animal Bite and Rabies Monitoring with GEO Mappping',
        maxZoom: 19, // Specify maxZoom to prevent users from zooming beyond the max level of the tile layer
    })
    const StreetMap = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{
        attribution: '&copy; <ahref="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        attribution: 'Animal Bite and Rabies Monitoring with GEO Mappping',
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

    //creating the center of the map 
    const mymap = L.map('mama',{
        center:[11.6400,124.4642],
        zoom:10.8,
        zoomSnap:0.75,
        zoomDelta:1,
        layers:[Dark],
        zoomControl:false,
        doubleClickZoom: false,
        
        scrollWheelZoom: false,
        attributionControl:false,
        doubleClickZoom: false,
        dragging: false, // Disable panning
        touchZoom: false, 
        
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
    heatOverlayImage.addTo(mymap);
    foundCasesImage.addTo(mymap);
    legendImage.addTo(mymap);



    //object in baselayers
    const baselayers = {
        'Dark':Dark,
        'Streep Map':StreetMap,
        'Light':Light
    }


    // Adding layer control with expanded option
    L.control.layers(baselayers, {
        'Heat Overlay': heatOverlayImage,
        'Found Cases': foundCasesImage,
        'Legend': legendImage
    }, {
        collapsed: false,
        position: 'topright' // Adjust position of layer control
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
    

    //markers in each municipalities
    /* const naval = L.marker([11.561764897288604,124.39667725158918],{
        icon:myIcon 
    }).addTo(mymap);
    const caibiran = L.marker([11.57217612592074,124.5810353065212],{
        icon:myIcon 
    }).addTo(mymap);
    const cabucgayan = L.marker([11.47299164012432, 124.57429111741462],{
        icon:myIcon 
    }).addTo(mymap);
    const biliran = L.marker([11.466502523017203, 124.47400191198957],{
        icon:myIcon 
    }).addTo(mymap);
    const culaba = L.marker([11.655595334022552, 124.54057110047455],{
        icon:myIcon 
    }).addTo(mymap);
    const almeria = L.marker([11.620206819741039,124.38116267356257],{
        icon:myIcon 
    }).addTo(mymap);
    const kawayan = L.marker([11.679731941619234, 124.35706958965689],{
        icon:myIcon 
    }).addTo(mymap);
    const maripipi = L.marker([11.77825522135924,124.34892830192959],{
        icon:myIcon 
    }).addTo(mymap); */


    //popup and tooltip in each muni
    /* const navalpopup = naval.bindPopup('Lavan');
    const navaltooltip = naval.bindTooltip("Naval");

    const caibiranpopup = caibiran.bindPopup('naribiac');
    const caibirantooltip = caibiran.bindTooltip("Caibiran");

    const cabucgayanpopup = cabucgayan.bindPopup('nayagcubac');
    const cabucgayantooltip = cabucgayan.bindTooltip("Cabucgayan");
    
    const biliranpopup = biliran.bindPopup('narilib');
    const bilirantooltip = biliran.bindTooltip("Biliran");

    const culabapopup = culaba.bindPopup('abaluc');
    const culabatooltip = culaba.bindTooltip("Culaba");

    const almeriapopup = almeria.bindPopup('airemla');
    const almeriatooltip = almeria.bindTooltip("Almeria");

    const kawayanpopup = kawayan.bindPopup('nayawak');
    const kawayantooltip = kawayan.bindTooltip('Kawayan');

    const maripipipopup = maripipi.bindPopup('ipipiram');
    const maripipitooltip = maripipi.bindTooltip('Maripipi'); */


    /* mymap.locate({
        setView:true,
        maxZoom:18
    })
 */























    /* const papa = L.map('papa',{

        
        center:[11.625615518023677,124.49623869990828],
        zoom:10.2,
        zoomControl:false,
        scrollWheelZoom: false,
        attributionControl:false,
        doubleClickZoom: false,
        dragging: false, // Disable panning
        touchZoom: false, 
        layers:[StreetMap]

        
    });
     */
    




/* var maxBounds = L.latLngBounds(
    L.latLng(11.358607609157232, 123.91744935882099), // Southwest corner
    L.latLng(11.897821676214718, 125.01560057070333) // Northeast corner
    );
    
    var map = L.map('mama',{
    //scrollWheelZoom: false,
    doubleClickZoom: false
    }).setView([11.6400,124.4642],11).setMaxBounds(maxBounds);
    
    map.on('dblclick', function(e) {
    map.setZoom(10);
    });
    map.removeControl(map.zoomControl);
    L.control.zoom({
    position: 'bottomright'
    }).addTo(map);
    
    var Dark = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    attribution: 'Animal Bite and Rabies Monitoring with GEO Mappping',
    minZoom: 10,
    maxZoom: 20, 
    //className: 'map-tiles'
    }).addTo(map)
    var OSM = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    minZoom: 10,
    attribution: 'Animal Bite and Rabies Monitoring with GEO Mappping',
    attribution: '&copy; <ahref="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    
    })
    var Light = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    attribution: 'Animal Bite and Rabies Monitoring with GEO Mappping',
    minZoom: 10,
    maxZoom: 20,
    
    }) */