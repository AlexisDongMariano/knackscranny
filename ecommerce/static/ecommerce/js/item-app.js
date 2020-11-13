// ==============================
//         UI ELEMENTS
// ==============================

const stars = document.querySelectorAll('.star-rating .fa');
const rating = document.querySelector('#rating-value');


// ==============================
//         EVENT LISTENERS
// ==============================



// ==============================
//         GLOBAL FUNCTIONS
// ==============================
function setRating(index) {
    stars.forEach((star,i) => {
        if(i <= index){
            star.classList.remove('fa-star-o');
            star.classList.add('fa-star');
        }
        else{
            star.classList.remove('fa-star');
            star.classList.add('fa-star-o');
        }
    });  
    rating.value = index+1;
}


// ==============================
//         RUNTIME LOGIC
// ==============================

stars.forEach((star, i) => {
    star.addEventListener('click', e => {
        stars[i].index = i;
        setRating(stars[i].index);
    });
});