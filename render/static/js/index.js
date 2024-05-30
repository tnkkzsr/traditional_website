document.addEventListener("DOMContentLoaded", function() {
    const swipers = {};

    // スライダー機能の実装
    document.querySelectorAll(".swiper-container").forEach((swiperContainer, index) => {
        const swiperId = swiperContainer.id;
        swipers[swiperId] = new Swiper(`#${swiperId}`, {
            slidesPerView: 1,
            loop: true,
            breakpoints: {
                768: {
                    slidesPerView: 3,
                },
            },
            pagination: {
                el: ".swiper-pagination",
                type: "fraction",
            },
            navigation: {
                nextEl: ".swiper-button-next",
                prevEl: ".swiper-button-prev",
            }
        });

        // 画像選択機能の実装
        const imageItems = document.querySelectorAll(`.image-item-${index + 1} .image-item`);
        console.log(imageItems);
        const slideImages = document.querySelectorAll(`#${swiperId} .swiper-slide`);
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
            document.getElementById(`selected_image_${index + 1}`).value = imageId + '.png';
            if (isSlide) {
                removeSelectedClass(selectedSlide);
                selectedSlide = element;
            } else {
                removeSelectedClass(selectedItem);
                selectedItem = element;
            }
            addSelectedClass(element);
                
            if (isSlide) {
                imageItems.forEach(item => {
                    if (item.getAttribute("data-image-item") === imageId) {
                        console.log(imageId);
                        removeSelectedClass(selectedItem);
                        addSelectedClass(item);
                        selectedItem = item;
                    }
                });
            } else {
                slideImages.forEach((slide, idx) => {
                    if (slide.getAttribute("data-image") === imageId) {
                        console.log("slide", slide);
                        removeSelectedClass(selectedSlide);
                        addSelectedClass(slide);
                        selectedSlide = slide;
                        swipers[swiperId].slideTo(idx);
                    }
                });
            }
        }

        imageItems.forEach(image => {
            image.addEventListener("click", function(event) {
                console.log("click image item", this.getAttribute("data-image-item"));
                event.preventDefault(); // デフォルトの動作を防ぐ
                event.stopPropagation(); // イベントの伝搬を停止
                const imageId = this.getAttribute("data-image-item");
                handleClick(imageId, this, false);
            });
        });

        slideImages.forEach(slide => {
            slide.addEventListener("click", function(event) {
                console.log("click slide image", this.getAttribute("data-image"));
                event.preventDefault(); // デフォルトの動作を防ぐ
                event.stopPropagation(); // イベントの伝搬を停止
                const imageId = this.getAttribute("data-image");
                handleClick(imageId, this, true);
            });
        });
    });
});
