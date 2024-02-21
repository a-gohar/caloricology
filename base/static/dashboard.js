function runningWeight(mArray, mRange) {
    var k = 2 / (mRange + 1);
    const emaArray = [mArray[0]];
    for (var i = 1; i < mArray.length; i++) {
        emaArray.push(mArray[i] * k + emaArray[i - 1] * (1 - k));
    }
    return emaArray;
}

function getWeights() {
    return new Promise((resolve, reject) => {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', 'get-weights', true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    try {
                        var response = JSON.parse(xhr.responseText);
                        const weight = [];
                        const total_caloric_data = [];
                        const protein = []
                        const dates = [];
                        const weightDates = []
                        response.weights.forEach(entry => {
                            if (entry.weight > 0) {
                                weight.push(entry.weight);
                                weightDates.push(entry.Date);
                            }
                            if (entry.calories > 0) {
                                dates.push(entry.Date)
                                total_caloric_data.push(entry.calories)
                                protein.push(entry.protein)
                            }
                        });

                        resolve({ weight, total_caloric_data, protein, dates, weightDates });
                    } catch (error) {
                        console.error('Error parsing JSON:', error.message);
                        reject('Error parsing JSON');
                    }
                } else {
                    console.error('HTTP error! Status:', xhr.status);
                    reject('HTTP error');
                }
            }
        };
        xhr.send();
    });
}


function plotWeightTrend(weightData, weightTrend, dateLabels) {
    new Chart(
        document.getElementById('weightChart'),
        {
            type: 'line',
            data: {
                labels: dateLabels,
                datasets: [
                    {
                        label: 'Weight (Scale)',
                        data: weightData,
                    }, {
                        label: "Weight (Average)",
                        data: weightTrend
                    }
                ]
            },
        });
}
function plotCalorieChart(totalCaloricData, dateLabels) {
    new Chart(
        document.getElementById('calorieChart'),
        {
            type: 'bar',
            data: {
                labels: dateLabels,
                datasets: [
                    {
                        label: 'Consumed Calories',
                        data: totalCaloricData,
                    }
                ]
            },

        });
}
function plotProteinChart(protein, dateLabels) {
    new Chart(
        document.getElementById('proteinChart'),
        {
            type: 'bar',
            data: {
                labels: dateLabels,
                datasets: [
                    {
                        label: 'Consumed Protein (g)',
                        data: protein,
                    }
                ]
            },
        });
}
function pRatioCalculator(p) {
    return (p * 1800) + (1 - p) * 9250
}



const fetchData = async () => {
    try {
        const { weight, total_caloric_data, protein, dates, weightDates } = await getWeights();
        console.log(total_caloric_data)
        const w2 = runningWeight(weight, weight.length);
        plotWeightTrend(weight, w2, weightDates);
        plotCalorieChart(total_caloric_data, dates)
        plotProteinChart(protein, dates)
    } catch (error) {
        console.error('Error:', error);
    }
};




fetchData();
//fetchTdee();