//if user want to maintain his weight, this function disable few options
function disableSlider() {
    const x = document.getElementById("goal-select").value;
    const rate = document.querySelector("#rate");
    const gw = document.querySelector("#gw");
    if (x == "Maintain weight") {
        rate.style.display = 'none';
        gw.style.display = 'none';
        rate.value = '0';
    } else {
        rate.style.display = 'flex';
        gw.style.display = 'flex';
        rate.value = '100';
        gw.value = 'maintain';
    }
}

// function show current day menu
function showSection(day) {
    document.querySelectorAll('.btn-day').forEach(btn => {
                btn.classList = "btn-day btn btn-outline-secondary";
    })
    document.querySelector(`#btn-day${day}`).classList = "btn-day btn btn-light";
    document.querySelector('#b-content').innerHTML = "";
    document.querySelector('#l-content').innerHTML = "";
    document.querySelector('#d-content').innerHTML = "";
    document.querySelector('#single-day').value = `${day}`;
    // request for data
    fetch(`/weekday/${day}`)
    .then(response => response.json())
    .then(meals => {
        var counter = 0;
        var allCalories = 0;
        var allFat = 0;
        var allCarbs = 0;
        var allProtein = 0;
        meals.forEach(meal => {
            var calories = 0;
            var fat = 0;
            var carbs = 0;
            var protein = 0;
            meal.forEach(product => {
                let x = Math.round(product.gram/100);
                calories = calories + product.caloric*x;
                fat = fat + product.fat*x;
                carbs = carbs + product.carbs*x;
                protein = protein + product.protein*x;
                const element = document.createElement('div');
                element.innerHTML = `<div id="meal${counter}id${product.id}" class="card-body single-product"><h5><b>${product.product}</b>   <i>${product.gram}g</i>
                <button class="btn btn-outline-danger" type="submit" onclick="deleteProduct(${counter}, ${product.id}, ${day})">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">
                <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
                </svg>
                </button></h5>
                
                <h6>${product.caloric*x}kcal    fat: ${product.fat*x}g  carbs: ${product.carbs*x}g  protein: ${product.protein*x}g</h6>
                </div>`;
                if (counter === 0) {
                    document.querySelector('#b-content').append(element);
                } else if (counter === 1) {
                    document.querySelector('#l-content').append(element);
                } else {
                    document.querySelector('#d-content').append(element);
                }
                
                
            })
            // print the main values of the meal 
            if (counter === 0) {
                document.querySelector('#b-caloric-head').innerHTML = `${calories}kcal fat: ${fat}g carbs: ${carbs}g protein: ${protein}g`;
            } else if (counter === 1) {
                document.querySelector('#l-caloric-head').innerHTML = `${calories}kcal fat: ${fat}g carbs: ${carbs}g protein: ${protein}g`;
            } else {
                document.querySelector('#d-caloric-head').innerHTML = `${calories}kcal fat: ${fat}g carbs: ${carbs}g protein: ${protein}g`;
            }
            counter++;
            allCalories = allCalories + calories;
            allCarbs = allCarbs + carbs;
            allFat = allFat + fat;
            allProtein = allProtein + protein;
            // print values of the whole day
            document.querySelector('#day-caloric-head').innerHTML = `${allCalories}kcal fat: ${allFat}g carbs: ${allCarbs}g protein: ${allProtein}g`
        });
    })
}


document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.btn-day').forEach(button => {
        button.onclick = function() {
            const section = this.dataset.section;
            showSection(section);
        }
    })
});

// after page was realoaded, show current day
function thisDay() {
    const d = new Date();
    let day = d.getDay()
    showSection(day);
    day = "day" + day;
}
window.onload = thisDay;

// function that deletes product
function deleteProduct(meal, id, day) {
    fetch(`/delete/${meal}/${id}`)
    setTimeout(() => {showSection(day);}, 100)
}