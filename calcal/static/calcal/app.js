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

function showSection(day) {
    document.querySelector('#b-content').innerHTML = "";
    document.querySelector('#l-content').innerHTML = "";
    document.querySelector('#d-content').innerHTML = "";
    document.querySelector('#single-day').value = `${day}`;
    fetch(`/weekday/${day}`)
    .then(response => response.json())
    .then(meals => {
        console.log(meals)
        var counter = 0;
        meals.forEach(meal => {
            meal.forEach(product => {
                
                const element = document.createElement('div');
                element.innerHTML = `<div id="meal${counter}id${product.id}" class="card-body"><h5><b>${product.product}</b>   <i>${product.gram}g</i>
                <button class="btn btn-outline-danger" type="submit" onclick="deleteProduct(${counter}, ${product.id})">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">
                <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
                </svg>
                </button></h5>
                
                <h6>${product.caloric}kcal    fat: ${product.fat}g  carbs: ${product.carbs}g  protein: ${product.protein}g</h6>
                </div>`;
                if (counter === 0) {
                    document.querySelector('#b-content').append(element);
                } else if (counter === 1) {
                    document.querySelector('#l-content').append(element);
                } else {
                    document.querySelector('#d-content').append(element);
                }
                
                
            })
            counter++;
        });
    })
}

function showPage(page) {
    document.querySelectorAll('.day').forEach(div => {
        div.style.display = 'none';
    });
    document.querySelectorAll('.btn-day').forEach(btn => {
                btn.classList = "btn-day btn btn-secondary";
    })
    document.querySelector(`#btn-${page}`).classList = "btn-day btn btn-light";
    document.querySelector(`#${page}`).style.display = 'block';
    
}

document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('.btn-day').forEach(button => {
        button.onclick = function() {
            const section = this.dataset.section;
            
            showSection(section);
            
            showPage(this.dataset.page);
            console.log(this.dataset.page);
        }
    })
});

function thisDay() {
    const d = new Date();
    let day = d.getDay()
    showSection(day);
    day = "day" + day;
    showPage(day);
}

window.onload = thisDay;

function deleteProduct(meal, id) {
    //niech usuwa tez tego diva js
    let div = document.getElementById(`meal${meal}id${id}`);
    div.replaceChildren();
    fetch(`/delete/${meal}/${id}`)
}