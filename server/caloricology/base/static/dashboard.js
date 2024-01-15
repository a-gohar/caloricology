function getWeights() {
    return new Promise((resolve, reject) => {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', 'get-weights', true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    // Parse the JSON response
                    try {
                        var response = JSON.parse(xhr.responseText);
                        const weight = [];
                        const dates = [];
                        response.weights.forEach(entry => {
                            weight.push(entry.weight);
                            dates.push(entry.Date);
                        });

                        resolve({ weight, dates });
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
function get_user_information() {
    return new Promise((resolve, reject) => {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', 'get-goals', true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    // Parse the JSON response
                    try {
                        var response = JSON.parse(xhr.responseText);
                        var tdee = response.goals.tdee;
                        var pRatio = response.goals.pRatio;
                        var weekly_target = response.goals.target;
                        const caloricDays = [];
                        response.days.forEach(entry => {
                            caloricDays.push(entry.cal)
                        });

                        resolve({ tdee, pRatio, weekly_target, caloricDays });
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
console.log(5);
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
function pRatioCalculator(){
    return (pRatio*800)+(1-pRatio)*4000
}
function updateTDEE() {
    const minEntries = 3;
    const minDaysWithCaloricInfo = 19;
    const caloriesPerPound = pRatioCalculator(); // 
    const divId = 'td';
    document.getElementById(divId).innerText = `TDEE: ${tdee.toFixed(2)}`;

    // Check if there are enough weight entries in the last 3 weeks
    const recentWeights = weightData.slice(-minEntries);
    if (recentWeights.filter(weight => weight !== null).length < minEntries) {
        console.log("Not enough weight entries in the last 3 weeks.");
        return;
    }

    // Check if there are enough days with non-zero caloric information
    const recentCaloricData = caloricData.slice(-minDaysWithCaloricInfo);
    const daysWithCaloricInfo = recentCaloricData.filter(calories => calories !== 0).length;
    if (daysWithCaloricInfo < minDaysWithCaloricInfo) {
        console.log("Not enough days with non-zero caloric information.");
        return;
    }

    // Calculate weight change and calories consumed
    const weightChange = recentWeights[recentWeights.length - 1] - recentWeights[0];
    const caloriesConsumed = recentCaloricData.reduce((totalCalories, calories) => totalCalories + calories, 0);

    // Calculate average TDEE
    const averageTDEE = (weightChange * caloriesPerPound + caloriesConsumed) / daysWithCaloricInfo;

    // Update the div with the calculated average TDEE
    document.getElementById(divId).innerText += `${averageTDEE.toFixed(2)}`;
}

function runningWeight(mArray, mRange) {
    var k = 2 / (mRange + 1);
    emaArray = [mArray[0]];
    for (var i = 1; i < mArray.length; i++) {
        emaArray.push(mArray[i] * k + emaArray[i - 1] * (1 - k));
    }
    return emaArray;
}

const fetchData = async () => {
    try {
        const { weight, dates } = await getWeights();
        const w2 = runningWeight(weight, weight.length);
        console.log(w2)
        plotWeightTrend(weight, w2, dates);
    } catch (error) {
        // Handle errors
        console.error('Error:', error);
    }
};


const fetchTdee = async () => {
    try {
        const { tdee, pRatio, weekly_target, caloricData } = await get_user_information();
        updateTDEE();
        var weight = w2[w2.length-1] - w2[0]
    }
    catch (error) {
        console.error("error:", error);
    }
}
fetchData();