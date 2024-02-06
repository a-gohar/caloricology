async function updateFoodResults(form, e) {
    e.preventDefault()
    var serializedForm = new FormData(form);
    var formData = JSON.stringify(Object.fromEntries(serializedForm));
    console.log(formData)
    const response = await fetch('/commonfood', {
        method: 'POST',
        body: formData,
        credentials: "same-origin",
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": getCookie('csrftoken')
        }
    });
    

    const data = await response.json();
    console.log(data)
    if ("error" in data) {
        alert("There was an error.")
        return false;
    }
    const resultsDiv = document.getElementById('foodResults');
    resultsDiv.innerHTML = '';  // Clear previous results

    for (const food of data.foods) {
        const foodItem = document.createElement('div');
        foodItem.classList.add('food-item');

        const nameElement = document.createElement('p');
        nameElement.textContent = `Name: ${food.name}`;
        foodItem.appendChild(nameElement);

        const caloriesElement = document.createElement('p');
        caloriesElement.textContent = `Calories: ${food.calories}`;
        foodItem.appendChild(caloriesElement);

        const proteinElement = document.createElement('p');
        proteinElement.textContent = `Protein: ${food.protein}`;
        foodItem.appendChild(proteinElement);

        const fatElement = document.createElement('p');
        fatElement.textContent = `Fat: ${food.fat}`;
        foodItem.appendChild(fatElement);

        const carbElement = document.createElement('p');
        carbElement.textContent = `Carbohydrates: ${food.carb}`;
        foodItem.appendChild(carbElement);


        // Add "Log Food" button and log form next to it
        const logFoodContainer = document.createElement('div');

        const logFoodButton = document.createElement('button');
        logFoodButton.textContent = 'Log Food';

        const logForm = document.createElement('div');
        logForm.style.display = 'none';  // Hide the form initially



        const dateLabel = document.createElement('label');
        dateLabel.textContent = 'Date:';
        const dateInput = document.createElement('input');
        dateInput.setAttribute('type', 'date');
        dateInput.setAttribute('name', 'date');
        dateInput.setAttribute('required', true);

        const weightLabel = document.createElement('label');
        weightLabel.textContent = 'Weight:';
        const weightInput = document.createElement('input');
        weightInput.setAttribute('type', 'text');
        weightInput.setAttribute('name', 'weight');
        weightInput.setAttribute('required', true);

        const foodNameInput = document.createElement('input');
        foodNameInput.setAttribute('type', 'hidden');
        foodNameInput.setAttribute('name', 'food_name');
        foodNameInput.setAttribute('value', food.name);

        const caloriesInput = document.createElement('input');
        caloriesInput.setAttribute('type', 'hidden');
        caloriesInput.setAttribute('name', 'calories');
        caloriesInput.setAttribute('value', food.calories);

        const proteinInput = document.createElement('input');
        proteinInput.setAttribute('type', 'hidden');
        proteinInput.setAttribute('name', 'protein');
        proteinInput.setAttribute('value', food.protein);

        const fatInput = document.createElement('input');
        fatInput.setAttribute('type', 'hidden');
        fatInput.setAttribute('name', 'fat');
        fatInput.setAttribute('value', food.fat);

        const carbInput = document.createElement('input');
        carbInput.setAttribute('type', 'hidden');
        carbInput.setAttribute('name', 'carb');
        carbInput.setAttribute('value', food.carb);

        const submitButton = document.createElement('button');
        submitButton.setAttribute('type', 'submit');
        submitButton.textContent = 'Submit';

        logForm.appendChild(dateLabel);
        logForm.appendChild(dateInput);
        logForm.appendChild(weightLabel);
        logForm.appendChild(weightInput);
        logForm.appendChild(foodNameInput);
        logForm.appendChild(caloriesInput);
        logForm.appendChild(proteinInput);
        logForm.appendChild(fatInput);
        logForm.appendChild(carbInput);
        logForm.appendChild(submitButton);
        logFoodButton.addEventListener('click', function () {
            logForm.style.display = (logForm.style.display === 'none') ? 'block' : 'none';
        });
        submitButton.addEventListener('click', async function (e) {
            e.preventDefault();

            const logData = {
                date: dateInput.value,
                weight: weightInput.value,
                food_name: foodNameInput.value,
                calories: caloriesInput.value,
                protein: proteinInput.value,
                fat: fatInput.value,
                carb: carbInput.value,
            };
            console.log(logData)

            try {
                const logResponse = await fetch('/commonfoodlog', {
                    method: 'POST',
                    body: JSON.stringify(logData),
                    credentials: "same-origin",
                    headers: {
                        'Content-Type': 'application/json',
                        "X-CSRFToken": getCookie('csrftoken')
                    },
                });

                const responseData = await logResponse.json();
                if (!("error" in responseData)) {
                    resultsDiv.innerHTML = '';
                }
                else {
                    console.error('Log food error:', responseData);
                    alert('Error logging food. Please try again.');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
        logFoodContainer.appendChild(logFoodButton);
        logFoodContainer.appendChild(logForm);

        foodItem.appendChild(logFoodContainer);

        resultsDiv.appendChild(foodItem);
    }
}

document.getElementById('commonfood').addEventListener('submit', function (e) {
    e.preventDefault();
    updateFoodResults();
});
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
