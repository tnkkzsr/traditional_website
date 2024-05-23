document.addEventListener("DOMContentLoaded", function() {

    //スライダー機能の実装
    const swipers = new Swiper("#swiper-container-1", {
            slidesPerView: 1,
            loop: true,
            breakpoints: {
                768: {
                    slidesPerView: 5,
                },
            },
            pagination: {
                el: ".swiper-pagination",
                type: "fraction",
            },
            navigation: {
                nextEl: ".swiper-button-next",
                prevEl: ".swiper-button-prev",
            },
        });

    //画像選択機能の実装
    const imageItems = document.querySelectorAll(".image-item-1");
    const slideImages = document.querySelectorAll("#swiper-container-1 .swiper-slide");
    let selectedSlide = null;
    let selectedItem = null;

    function addSelectedClass(element) {
        element.classList.add("selected-image");
    }

    function removeSelectedClass(element) {
        if (element) {
            element.classList.remove("selected-image");
        }
    }

    function handleClick(imageId, element, isSlide) {
        document.getElementById(`selected_image`).value = imageId;
        
        if (isSlide) {
            removeSelectedClass(selectedSlide);
            selectedSlide = element;
        } else {
            removeSelectedClass(selectedItem);
            selectedItem = element;
        }
        addSelectedClass(element);
        if (isSlide) {
            imageItemsA.forEach(item => {
                if (item.getAttribute("data-image-item") === imageId) {
                    removeSelectedClass(selectedItem);
                    addSelectedClass(item);
                    selectedItem = item;
                }
            });
        } else {
            slideImagesA.forEach((slide, index) => {
                if (slide.getAttribute("data-image") === imageId) {
                    removeSelectedClass(selectedSlide);
                    addSelectedClass(slide);
                    selectedSlide = slide;
                    swipers.a.slideTo(index);
                }
            });
        }
        
    }

    imageItems.forEach(image => {
        image.addEventListener("click", function() {
            const imageId = this.getAttribute("data-image-item");
            handleClick(imageId, this, false);
        });
    });

    slideImages.forEach(slide => {
        slide.addEventListener("click", function() {
            const imageId = this.getAttribute("data-image");
            handleClick(imageId, this, true);
        });
    });
});