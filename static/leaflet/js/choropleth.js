window.onload = init;

function init() {
    const totalCasesRabies = document.getElementById('total-rabies-data');
    const totalRabibesCases = parseInt(totalCasesRabies.getAttribute('data-rabies-cases'), 10);
    

    const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    });

    const Light = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
    });

    const maxBounds = L.latLngBounds(
        L.latLng(11.358607609157232, 123.91744935882099), // Southwest corner
        L.latLng(11.897821676214718, 125.01560057070333) // Northeast corner
    );

    const mymap = L.map('choropleth', {
        center: [11.6400, 124.4642],
        zoom: 11,
        minZoom: 10,
        layers: [Light],
        zoomControl: false,
        gestureHandling:true,
        
    }).setMaxBounds(maxBounds);

    L.control.zoom({
        position: 'bottomright'
    }).addTo(mymap);

    function highlightFeature(e) {
        var layer = e.target;
        layer.setStyle({
            weight: 1,
            color: '#FF0000',
            dashArray: '',
            fillOpacity: 0.7
        });
        if (!L.Browser.ie && !L.Browser.edge) {
            layer.bringToFront();
        }
    
        // Retrieve the patient count for the current barangay
        var patientCount = densityData[layer.feature.properties.pk];
    
        // If patientCount is 0 or undefined, show "No Patient"
        var patientDisplay = (patientCount && patientCount > 0) ? patientCount : "No Patient";
    
        // Update the tooltip with the barangay's patient data
        layer.bindTooltip(
            "<b>Barangay: " + layer.feature.properties.brgy_name + "</b>" + 
            "<br><span style='color:red;'>Patients: " + patientDisplay + "</span>"
        )
        .openTooltip()
        .setOffset([20, 20]);  // Offset the tooltip by 20px on the X-axis (to the right)
    }
    
    
    function resetHighlight(e) {
        geojson.resetStyle(e.target); // 'geojson' is our L.geoJson layer
        e.target.closeTooltip(); // Close the tooltip when mouseout
    }
    

    function zoomToFeature(e) {
        mymap.fitBounds(e.target.getBounds());
    }

    // Define onEachFeature to bind events and tooltip
    function onEachFeature(feature, layer) {
        layer.on({
            mouseover: highlightFeature,
            mouseout: resetHighlight,
            click: zoomToFeature
        });

        // Check if the patient count exists and is greater than 0, otherwise display "No Patient"
        var patientCount = densityData[feature.properties.pk];
        var patientText = (patientCount > 0) ? "Patients: " + patientCount : "No Patient";

        // Show the patient's count (or "No Patient") on hover
        layer.bindTooltip(
            "<b>Barangay: " + feature.properties.brgy_name + "</b>" +
            "<br><span style='color:red;'>Patients: " + patientCount + "</span>"
        );
    }

    // Load and style the GeoJSON data
    var geojson = L.geoJson(biliranData, {
        style: function(feature) {
            var density = densityData[feature.properties.pk] || 0; // Default to 0 if no data
            return {
                color: 'black',
                weight: 0.2,
                fillOpacity: 0.7,
                fillColor: getColor(density) // Color based on density
            };
        },
        onEachFeature: onEachFeature
    }).addTo(mymap);

    // Color function to return color based on density
    function getColor(d) {
        return d > 1000 ? '#ff3333' :   // Bright red
               d > 500  ? '#ff6666' :   // Light red
               d > 300  ? '#ff9999' :   // Soft red
               d > 200  ? '#fdbb84' :   // Soft peach
               d > 150  ? '#fdd49e' :   // Creamy peach
               d > 100  ? '#fee8c8' :   // Very light peach
               d > 50   ? '#fff0e0' :   // Pale peach
               d > 10   ? '#fff5eb' :   // Almost white
               '#ffffff';               // Pure white for the lowest range
    }

    // Create a control for displaying barangay patient data
    var info = L.control({ position: 'topright' });

    // Create the div for the custom info control
    info.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'hoverBarangay'); // create a div with class "info"
        this.update(); // Initialize the control with a placeholder
        return this._div;
    };

    // Update the control when a barangay is hovered over
    info.update = function (props) {
        this._div.innerHTML = 'Hover over a barangay';  // Static message, no dynamic changes
    };

    info.addTo(mymap);

    // Total Patients Control in the Top-Left
    var totalPatientsControl = L.control({ position: 'topleft' });

    // Create the div for the total patients control
    totalPatientsControl.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'totalPatients'); // create a div with class "totalPatients"
        this.update(); // Initialize the control with the total patients and rabies cases
        return this._div;
    };

    // Update the total patients control
    totalPatientsControl.update = function () {
        var totalPatients = 0;
        var totalRabiesCases = totalRabibesCases;  // Get the rabies cases count (from your data)

        // Calculate total patients from the densityData
        for (var key in densityData) {
            if (densityData.hasOwnProperty(key)) {
                totalPatients += densityData[key]; // Sum up the values for total patients
            }
        }

        // Update the inner HTML of the control to display total patients and total rabies cases
        this._div.innerHTML = `
            <div style="text-align: center;">
            <h2 style="color: red; margin: 0; font-size: 20px;">${totalPatients}</h2> 
            <h4 style="color: black; margin: 0; font-size: 12px;">
                Total Patients with <span style="color: red; font-size: 16px;">${totalRabiesCases}</span> Rabies Cases
            </h4>
        </div>`;
    };

    // Add the control to the map
    totalPatientsControl.addTo(mymap);


    var legend = L.control({ position: 'bottomleft' });

    legend.onAdd = function (map) {
        // Create a container div with class 'info legend'
        var div = L.DomUtil.create('div', 'info legend'),
            grades = [0, 1, 10, 50, 100, 150, 200, 300, 500, 1000], // Correct intervals
            labels = [];

        // Add a title for the legend
        div.innerHTML += '<h4 style="text-align: center; margin-bottom: 10px;">Patient Density</h4>';

        // Loop through the density intervals in **reverse order** (from top to bottom)
        for (var i = grades.length - 1; i > 0; i--) {
            div.innerHTML +=
            '<i style="background:' + getColor(grades[i]) + '; width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 0.9;"></i>' +
            '<span style="line-height: 18px;">' + grades[i - 1] + '&ndash;' + grades[i] + (grades[i + 1] ? '' : '+') + '</span><br>';
        }

        // Handle the last range (0) separately so it appears only once at the bottom
        div.innerHTML +=
            '<i style="background:' + getColor(grades[0]) + '; width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 0.9;"></i>' +
            '<span style="line-height: 18px;">0</span><br>';

        // Add additional inline styles for the legend
        div.style.padding = '10px';
        div.style.background = 'white'; // Background for the legend
        div.style.borderRadius = '5px';
        div.style.boxShadow = '0 0 10px rgba(0, 0, 0, 0.3)';
        div.style.fontSize = '14px';
        div.style.lineHeight = '18px';
        div.style.color = '#333';
        div.style.color = 'black'; // Adjusted text color for visibility

        return div;
    };

    // Add the legend to the map
    legend.addTo(mymap);

    // Get rabies heatmap data from script tag
    var rabiesHeatmapDataScript = document.getElementById('rabies-heatmap-data');
    var rabiesHeatmapData = JSON.parse(rabiesHeatmapDataScript.textContent);

    // Create a heatmap layer for human rabies cases
    var rabiesHeat = L.heatLayer(rabiesHeatmapData, {
        radius: 5,  // Smaller radius for heatmap
        blur: 1,    // Increase blur for softness
        maxZoom: 10,
        gradient: {
            0.0: 'red',
            0.5: 'red',
            1.0: 'red',
        },
        minOpacity: 0.5,
        maxIntensity: 100,
        opacity: 0.7,
    }).addTo(mymap);  // Add heatmap as the last layer

}
