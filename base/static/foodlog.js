function openPopupForm() {
    document.getElementById('popup-form').style.display = 'block';
}

function closePopupForm() {
    document.getElementById('popup-form').style.display = 'none';
}

function loadForm(option, event) {
    event.preventDefault()
    // Container for the dynamic form
    var dynamicFormContainer = document.getElementById('dynamic-form-container');

    // Clear any previous form
    dynamicFormContainer.innerHTML = '';

    // Fetch the form content from the server using AJAX
    var xhr = new XMLHttpRequest();
    xhr.open('GET', option, true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // Create and append the form based on the fetched content
            var form = document.createElement('div');
            form.innerHTML = xhr.responseText;
            dynamicFormContainer.appendChild(form);
        }
    };
    xhr.send();
    return false;
}
function addFood() {
    // Add functionality for adding food
    closePopupForm();
}

// Sample food log data (replace this with data from your backend)
const foodLogData = [
    { name: 'Food 1', calories: 300, protein: 0, fat: 0, carbs: 0 },
    { name: 'Food 2', calories: 500, protein: 0, fat: 0, carbs: 0 },
    // Add more food log entries as needed
];

// Initial date
let currentDate = new Date();

// Function to navigate between days
async function navigateDay(offset) {
    currentDate.setDate(currentDate.getDate() + offset);
    updateCurrentDate();
    updateFoodLog(energyExpenditure);
}

// Function to update the food log based on the current date
async function updateFoodLog(energy) {
    // Fetch and display food log data for the current date (from your backend)
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'update-food-log?date=' + currentDate.toISOString(), true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // Parse the JSON response
            consumedCalories = 0;
            remainingCalories = 0;
            dailyProtein = 0;
            dailyFat = 0;
            dailyCarb = 0;
            var response = JSON.parse(xhr.responseText);

            // Update the food log based on the fetched content
            const foodLogContainer = document.getElementById('food-log');
            foodLogContainer.innerHTML = '';

            response.food_log.forEach(entry => {
                const foodEntryElement = document.createElement('p');

                const entryText = document.createTextNode(`${entry.name} - ${entry.calories} calories - ${entry.protein}g protein - ${entry.fat}g fat - ${entry.carbs}g carbs`);
                foodEntryElement.appendChild(entryText);

                const removeButton = document.createElement('button');
                removeButton.className = 'remove-food';
                removeButton.innerText = 'X';
                removeButton.addEventListener('click', () => removeFood(entry.name, currentDate, entry.calories));

                foodEntryElement.appendChild(removeButton);

                foodLogContainer.appendChild(foodEntryElement);

                consumedCalories += entry.calories;
                dailyProtein += entry.protein;
                dailyFat += entry.fat;
                dailyCarb += entry.carbs
            });
        }
        remainingCalories = energy - consumedCalories;
        updateCalorieSummary()
    };
    xhr.send();
    return false;
}

async function removeFood(foodName, foodDate, foodCalories) {
    // Send a POST request to your Django view to remove the specified food
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'remove-food', true);
    xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // Refresh the food log after successful removal
            updateFoodLog();
        }
    };
    console.log(foodDate)
    xhr.send(JSON.stringify({ food_name: foodName, food_date: foodDate, calories: foodCalories }));
}
function updateCalorieSummary() {
    const consumedCaloriesElement = document.getElementById('consumed-calories');
    const remainingCaloriesElement = document.getElementById('remaining-calories');
    consumedCaloriesElement.innerText = ` Consumed : ${consumedCalories}  calories\r\n`;
    consumedCaloriesElement.innerText += `${dailyProtein}g Protein \r\n`;
    consumedCaloriesElement.innerText += `${dailyFat}g Fat\r\n`
    consumedCaloriesElement.innerText += `${dailyCarb}g Carb`
    remainingCaloriesElement.innerText = `Remaining Calories: ${remainingCalories.toFixed(2)} `;
}
// Function to update the displayed current date
function updateCurrentDate() {
    const currentDayElement = document.getElementById('current-day');
    currentDayElement.textContent = currentDate.toDateString();
}
function closePopupForm() {
    updateFoodLog();
    document.getElementById('popup-form').style.display = 'none';
}
function pRatioCalculator(p) {
    return (p * 1800) + (1 - p) * 9250
}
function updateTDEE(tee, p, tdeeCaloricData, tdeeWeight) {
    const minEntries = 3;
    const minDaysWithCaloricInfo = 19; // 
    const recentWeights = tdeeWeight.filter(weight => weight !== 0)
    // Check if there are enough weight entries in the last 3 weeks
    if (recentWeights.length < minEntries) {
        return tee;
    }
    // Check if there are enough days with non-zero caloric information
    const recentCaloricData = tdeeCaloricData.filter(calories => calories !== 0);
    if (recentCaloricData.length < minDaysWithCaloricInfo) {
        return tee;
    }
    const w4 = runningWeight(recentWeights, recentWeights.length)
    // Calculate weight change and calories consumed
    const weightChange = w4[w4.length - 1] - w4[0];
    if (weightChange > 0){
        const caloriesPerPound = pRatioCalculator(0.5);
    }
    else {
        const caloriesPerPound = pRatioCalculator(0.15);
    }
    const caloriesConsumed = recentCaloricData.reduce((totalCalories, calories) => totalCalories + calories, 0);
    const averageTDEE = ((weightChange * caloriesPerPound) + caloriesConsumed) / recentCaloricData.length;
    return averageTDEE.toFixed(2);
}

function runningWeight(mArray, mRange) {
    var k = 2 / (mRange + 1);
    const emaArray = [mArray[0]];
    for (var i = 1; i < mArray.length; i++) {
        emaArray.push(mArray[i] * k + emaArray[i - 1] * (1 - k));
    }
    return emaArray;
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
function get_daily_caloric(week_calories, pRatio) {
    var energyDensity = pRatioCalculator(pRatio);
    energyDensity = energyDensity * week_calories
    energyDensity = energyDensity / 7
    return energyDensity
}
// Initial setup
let consumedCalories = 0;
let remainingCalories = 0;
let dailyProtein = 0;
let dailyCarb = 0;
let dailyFat = 0;
updateCurrentDate();
updateFoodLog(2000);
const fetchData = async () => {
    try {
        const { tdee, pRatio, weekly_target, caloricData, weightInfo } = await get_user_information();
        const energyExpenditure = updateTDEE(tdee, pRatio, caloricData, weightInfo) + get_daily_caloric(weekly_target, pRatio / 100);
        updateFoodLog(energyExpenditure);
    }
    catch (error) {
        console.error("error:", error);
    }
}
fetchData()
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
