// Function to map intensity based on the count of cases
function getMuniColorByCases(count) {
    var intensityColors = [
        '#6DA9FF', // Medium-light blue
        '#6DA9FF', // Medium-light blue
        '#3399FF', // Medium blue
        '#3399FF', // Medium blue
        '#007BFF', // Primary blue (Bootstrap primary)
        '#007BFF', // Primary blue (Bootstrap primary)
        '#0069D9', // Dark blue
        '#0069D9', // Dark blue
        '#0056B3', // Darker blue
        '#0056B3', // Darker blue
        '#004085',  // Darkest blue
        '#004085',  // Darkest blue
    ];

    if (count < 50) {
        return intensityColors[0];
    } else if (count < 100) {
        return intensityColors[1];
    } else if (count < 200) {
        return intensityColors[2];
    } else if (count < 300) {
        return intensityColors[3];
    } else if (count < 400) {
        return intensityColors[4];
    } else if (count < 500) {
        return intensityColors[5];
    } else {
        return intensityColors[6];
    }
}

// Initialize Municipality Chart
function initMunicipalityChart(municipalities, municipality_case_counts) {
    var ctx = document.getElementById('municipalityChart').getContext('2d');
    var totalCasesPerMuni = municipality_case_counts.reduce((acc, val) => acc + val, 0); // Calculate total cases
    var backgroundColors = municipality_case_counts.map(count => getMuniColorByCases(count));
    var borderColors = backgroundColors;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: municipalities,
            datasets: [{
                label: 'Number of Cases per Municipality',
                data: municipality_case_counts,
                backgroundColor: backgroundColors,
                borderColor: borderColors,
                borderWidth: 1,
                borderRadius: 30,
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Municipality'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Cases'
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top'
                },
                datalabels: {
                    formatter: (value) => value,
                    color: '#fff',
                    font: {
                        weight: 'bold',
                        size: 14
                    }
                }
            }
        },
        plugins: [ChartDataLabels]
    });
}

// Initialize Gender Chart
function initGenderChart(genderLabels, genderData) {
    var ctxGender = document.getElementById('genderChart').getContext('2d');
    new Chart(ctxGender, {
        type: 'pie',
        data: {
            labels: genderLabels,
            datasets: [{
                label: 'Number of Cases',
                data: genderData,
                backgroundColor: [
                    'rgba(54, 162, 235, 1)', // Color for males
                    'rgba(255, 99, 132, 1)'  // Color for females
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)', // Border color for males
                    'rgba(255, 99, 132, 1)'  // Border color for females
                ],
                borderWidth: 1,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                datalabels: {
                    formatter: (value, ctx) => {
                        let sum = ctx.dataset.data.reduce((a, b) => a + b, 0);
                        let percentage = (value * 100 / sum).toFixed(2) + "%";
                        return percentage;
                    },
                    color: '#fff',
                    font: {
                        weight: 'bold',
                        size: '14'
                    }
                }
            }
        },
        plugins: [ChartDataLabels]
    });
}

// Initialize Animal Chart
function initAnimalChart(animalLabels, animalData) {
    var ctxAnimal = document.getElementById('animalChart').getContext('2d');
    new Chart(ctxAnimal, {
        type: 'pie',
        data: {
            labels: animalLabels,
            datasets: [{
                label: 'Number of Cases',
                data: animalData,
                backgroundColor: [
                    'rgba(255, 165, 0, 1)', 
                    'rgba(255, 0, 0, 1)',   
                    'rgba(128, 128, 128, 1)' 
                ],
                borderColor: [
                    'rgba(255, 165, 0, 1)', 
                    'rgba(255, 0, 0, 1)',  
                    'rgba(128, 128, 128, 1)' 
                ],
                borderWidth: 1,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                datalabels: {
                    formatter: (value, ctx) => {
                        let sum = ctx.dataset.data.reduce((a, b) => a + b, 0);
                        let percentage = (value * 100 / sum).toFixed(2) + "%";
                        return percentage;
                    },
                    color: '#fff',
                    font: {
                        weight: 'bold',
                        size: '14'
                    }
                }
            }
        },
        plugins: [ChartDataLabels]
    });
}
