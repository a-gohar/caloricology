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
                        const caloricData = [];
                        const weightInfo = []
                        response.days.forEach(entry => {
                            caloricData.push(entry.cal)
                            weightInfo.push(entry.weight)
                        });
                        resolve({ tdee, pRatio, weekly_target, caloricData, weightInfo });
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
        options: {
            plugins: {
              datalabels: {
                 display: function(context) {
                    return context.dataset.data[context.dataIndex] !== 0; // or >= 1 or ...
                 }
              }
            }
          }
    });
}
function pRatioCalculator(p){
    return (p*800)+(1-p)*4000
}
function updateTDEE(tee, p, tdeeCaloricData, tdeeWeight) {
    const minEntries = 3;
    const minDaysWithCaloricInfo = 19;
    const caloriesPerPound = pRatioCalculator(p); // 
    const divId = 'td';
    const recentWeights = tdeeWeight.filter(weight => weight !== 0)
    // Check if there are enough weight entries in the last 3 weeks
    if (recentWeights.length < minEntries) {
        console.log("Not enough weight entries in the last 3 weeks.");
        document.getElementById(divId).innerText += ` ${tee.toFixed(2)}`;
        return;
    }
    // Check if there are enough days with non-zero caloric information
    const recentCaloricData = tdeeCaloricData.filter(calories => calories !== 0);
    if (recentCaloricData.length < minDaysWithCaloricInfo) {
        console.log("Not enough days with non-zero caloric information.");
        document.getElementById(divId).innerText += ` ${tee.toFixed(2)}`;
        return;
    }
    const w4 = runningWeight(recentWeights, recentWeights.length)
    // Calculate weight change and calories consumed
    const weightChange = w4[w4.length - 1] - w4[0];
    const caloriesConsumed = recentCaloricData.reduce((totalCalories, calories) => totalCalories + calories, 0);
    const averageTDEE = ((weightChange * caloriesPerPound) + caloriesConsumed) / recentCaloricData.length;
    const sum = recentCaloricData.reduce((partialSum, a) => partialSum + a, 0);
    document.getElementById(divId).innerText += `${averageTDEE.toFixed(0)}`;
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
        plotWeightTrend(weight, w2, dates);
    } catch (error) {
        // Handle errors
        console.error('Error:', error);
    }
};


const fetchTdee = async () => {
    try {
        const { tdee, pRatio, weekly_target, caloricData, weightInfo } = await get_user_information();
        updateTDEE(tdee, pRatio, caloricData, weightInfo);
    }
    catch (error) {
        console.error("error:", error);
    }
}
fetchData();
fetchTdee();