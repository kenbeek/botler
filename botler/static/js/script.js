const numItemsToGenerate = 2; //how many gallery items you want on the screen
const numImagesAvailable = 328; //how many total images are in the collection you are pulling from
const imageWidth = 800; //your desired image width in pixels
const imageHeight = 300; //desired image height in pixels
const collectionID = 416021; //the collection ID from the original url
const $galleryContainer = document.querySelector('.gallery-container');

function renderGalleryItem(randomNumber) {
    fetch(`https://source.unsplash.com/collection/${collectionID}/${imageWidth}x${imageHeight}/?sig=${randomNumber}`)
        .then((response) => {
            let galleryItem = document.createElement('div');
            galleryItem.classList.add('gallery-item');
            galleryItem.innerHTML = `
        <img class="gallery-image" src="${response.url}" alt="gallery image"/>
        `
            $galleryContainer.appendChild(galleryItem);
        })
}


let randomImageIndex = Math.floor(Math.random() * numImagesAvailable);
renderGalleryItem(randomImageIndex);