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
    updateFoodLog();
}

// Function to update the food log based on the current date
async function updateFoodLog() {
    // Fetch and display food log data for the current date (from your backend)
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'update-food-log?date=' + currentDate.toISOString(), true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // Parse the JSON response
            consumedCalories = 0;
            remainingCalilories = 0;
            var response = JSON.parse(xhr.responseText);

            // Update the food log based on the fetched content
            const foodLogElement = document.getElementById('food-log');
            foodLogElement.innerHTML = '';

            // Iterate through the received data and update the food log
            response.food_log.forEach(entry => {
                foodLogElement.innerHTML += `<p>${entry.name} - ${entry.calories} calories
            - ${entry.protein}g protein - ${entry.fat}g fat - ${entry.carbs}g carbs </p>`;
            consumedCalories += entry.calories;
            });
        }
        remainingCalories = 2000 - consumedCalories;
        updateCalorieSummary()
    };
    xhr.send();
    return false;
}
function updateCalorieSummary(){
    const consumedCaloriesElement = document.getElementById('consumed-calories');
    const remainingCaloriesElement = document.getElementById('remaining-calories');

    consumedCaloriesElement.innerHTML = `<h3> Consumed Calories: ${consumedCalories} </h3>`;
    remainingCaloriesElement.innerHTML = `<h3> Remaining Calories: ${remainingCalories} </h3>`;
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
// Initial setup
let consumedCalories = 0;
let remainingCalories = 0;
updateCurrentDate();
updateFoodLog();