// ==============================
//         UI ELEMENTS
// ==============================

const stars = document.querySelectorAll('.star-rating .fa');
const rating = document.querySelector('#rating-value');
const submit = document.querySelector('#submit-review');
// const submit = document.querySelector('#submit-review');
const reviewRating1 = document.querySelectorAll('.rating-1');
const reviewRating2 = document.querySelectorAll('.rating-2');
const reviewRating3 = document.querySelectorAll('.rating-3');
const reviewRating4 = document.querySelectorAll('.rating-4');
const reviewRating5 = document.querySelectorAll('.rating-5');
// GET rating inside the review modal
let itemRatingValue = document.querySelector('.item-rating'); 


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

if (itemRatingValue){
    itemRatingValue = parseInt(itemRatingValue.innerText);
    setRating(itemRatingValue-1);
    console.log('item rating value:', itemRatingValue);
}
    

starClicked = false;
stars.forEach((star, i) => {
    star.addEventListener('click', e => {
        stars[i].index = i;
        setRating(stars[i].index);
        starClicked = true;

        if (submit)
            submit.disabled = false;
    });
});

if (submit)
    submit.disabled = true;

    

if(reviewRating1){
    reviewRating1.forEach(rating => {
        rating.innerHTML = `
        <span class="fa fa-star"></span>
        <span class="fa fa-star-o"></span>
        <span class="fa fa-star-o"></span>
        <span class="fa fa-star-o"></span>
        <span class="fa fa-star-o"></span>`
    });
}

if(reviewRating2){
    reviewRating2.forEach(rating => {
        rating.innerHTML = `
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star-o"></span>
        <span class="fa fa-star-o"></span>
        <span class="fa fa-star-o"></span>`
    });
}

if(reviewRating3){
    reviewRating3.forEach(rating => {
        rating.innerHTML = `
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star-o"></span>
        <span class="fa fa-star-o"></span>`
    });
}

if(reviewRating4){
    reviewRating4.forEach(rating => {
        rating.innerHTML = `
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star-o"></span>`
    });
}

if(reviewRating5){
    reviewRating5.forEach(rating => {
        rating.innerHTML = `
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>`
    });
}



