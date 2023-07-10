let toggleReviewInput = document.getElementById('toggle-review-input');
let addReview = document.getElementById('add-review');

window.addEventListener('load', (e) => {
    e.preventDefault()
    addReview.classList.add('d-none');
});

// for product image gallery

function switchImage(img) {
    let setImage = document.getElementById('set_image');
    setImage.src = img.src;
    setImage.alt = img.alt;
    setImage.parentElement.style.display = 'block';
}


// for the add and remove from cart button toggle



// document.addEventListener('DOMContentLoaded', (e) => {
//     e.preventDefault()
//     removeFromBag.classList.add('d-none');
// });

toggleReviewInput.addEventListener('click', (e) => {
    e.preventDefault()
    addReview.classList.toggle('d-none')
    // addToBag.classList.add('d-none')
})

// removeFromBag.addEventListener('click', (e) => {
//     e.preventDefault()
//     addToBag.classList.remove('d-none')
//     removeFromBag.classList.add('d-none')
// })


// // for the add and remove from cart button toggle

// let addToBag = document.getElementById('add_to_bag');
// let removeFromBag = document.getElementById('remove_from_bag');

// // document.addEventListener('DOMContentLoaded', (e) => {
// //     e.preventDefault()
// //     removeFromBag.classList.add('d-none');
// // });

// addToBag.addEventListener('click', (e) => {
//     e.preventDefault()
//     removeFromBag.classList.remove('d-none')
//     // removeFromBag.style.display = "block";
//     addToBag.classList.add('d-none')
//     // addToBag.style.display = "none";
// })

// removeFromBag.addEventListener('click', (e) => {
//     e.preventDefault()
//     addToBag.classList.remove('d-none')
//     // addToBag.style.display = "block";
//     removeFromBag.classList.add('d-none')
//     // removeFromBag.style.display = "none";
// })