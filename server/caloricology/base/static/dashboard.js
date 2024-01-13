function getWeights(weight, dates) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'get-weights', true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                // Parse the JSON response
                try {
                    var response = JSON.parse(xhr.responseText);

                    // Assuming weight and dates are arrays declared outside this function
                    
                    weight.length = 0;
                    dates.length = 0;
                    response.weights.forEach(entry => {
                        weight.push(entry.weight);
                        dates.push(entry.Date);
                    });
                } catch (error) {
                    console.error('Error parsing JSON:', error.message);
                    // Handle the JSON parsing error as needed
                }
            } else {
                console.error('HTTP error! Status:', xhr.status);
                // Handle the HTTP error as needed
            }
        }
    };
    xhr.send();
}
function plotWeightTrend(weightData, dateLabels) {
    // Get the reference to the "weighTrend" div
    // Create a canvas element to render the chart
    // Get the 2D context of the canvas
    console.log(weightData)
    console.log(dateLabels)
    console.log(5)
    new Chart(
        document.getElementById('weightChart'),
        {
            type: 'line',
            data: {
                labels: dateLabels,
                datasets: [
                    {
                        label: 'Weight',
                        data: weightData
                    }
                ]
            },
            options: {
                scales: {
                  y: {
                    beginAtZero: false
                  }
                }
              }
            });
    }



const w = [1,2, 3];
const d = [1, 2, 3];
getWeights(w,d);
plotWeightTrend(w, d);