// ==============================
//         UI ELEMENTS
// ==============================

const stars = document.querySelectorAll('.star-rating .fa');
const rating = document.querySelector('#rating-value');
const submit = document.querySelector('#submit-review');
const reviewRating1 = document.querySelector('.rating-1');
const reviewRating2 = document.querySelector('.rating-2');
const reviewRating3 = document.querySelector('.rating-3');
const reviewRating4 = document.querySelector('.rating-4');
const reviewRating5 = document.querySelector('.rating-5');


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
starClicked = false;
stars.forEach((star, i) => {
    star.addEventListener('click', e => {
        stars[i].index = i;
        setRating(stars[i].index);
        starClicked = true;


        submit.disabled = false;
    });
});

submit.disabled = true;

    


if(reviewRating1){
    reviewRating1.innerHTML = `
        <span class="fa fa-star"></span>
        <span class="fa fa-star-o"></span>
        <span class="fa fa-star-o"></span>
        <span class="fa fa-star-o"></span>
        <span class="fa fa-star-o"></span>`
}

if(reviewRating2){
    reviewRating2.innerHTML = `
        <span class="fa fa-star "></span>
        <span class="fa fa-star "></span>
        <span class="fa fa-star-o "></span>
        <span class="fa fa-star-o "></span>
        <span class="fa fa-star-o "></span>`
}

if(reviewRating3){
    reviewRating3.innerHTML = `
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star-o"></span>
        <span class="fa fa-star-o"></span>`
}

if(reviewRating4){
    reviewRating4.innerHTML = `
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star-o"></span>`
}

if(reviewRating5){
    reviewRating5.innerHTML = `
    <span class="fa fa-star"></span>
    <span class="fa fa-star"></span>
    <span class="fa fa-star"></span>
    <span class="fa fa-star"></span>
    <span class="fa fa-star"></span>`
}



