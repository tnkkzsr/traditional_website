document.addEventListener("DOMContentLoaded", function() {

    //スライダー機能の実装
    const swipers = {
        a: new Swiper("#swiper-container-a", {
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
        }),
        b: new Swiper("#swiper-container-b", {
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
        }),
        c: new Swiper("#swiper-container-c", {
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
        })
    };

    //画像選択機能の実装
    const imageItemsA = document.querySelectorAll(".image-item-a");
    const slideImagesA = document.querySelectorAll("#swiper-container-a .swiper-slide");
    let selectedSlideA = null;
    let selectedItemA = null;

    const imageItemsB = document.querySelectorAll(".image-item-b");
    const slideImagesB = document.querySelectorAll("#swiper-container-b .swiper-slide");
    let selectedSlideB = null;
    let selectedItemB = null;

    const imageItemsC = document.querySelectorAll(".image-item-c");
    const slideImagesC = document.querySelectorAll("#swiper-container-c .swiper-slide");
    let selectedSlideC = null;
    let selectedItemC = null;

    function addSelectedClass(element) {
        element.classList.add("selected-image");
    }

    function removeSelectedClass(element) {
        if (element) {
            element.classList.remove("selected-image");
        }
    }

    function handleClick(imageId, element, isSlide, formId) {
        document.getElementById(`selected_image_${formId}`).value = imageId;

        if (formId === 'a') {
            if (isSlide) {
                removeSelectedClass(selectedSlideA);
                selectedSlideA = element;
            } else {
                removeSelectedClass(selectedItemA);
                selectedItemA = element;
            }
            addSelectedClass(element);
            if (isSlide) {
                imageItemsA.forEach(item => {
                    if (item.getAttribute("data-image-item") === imageId) {
                        removeSelectedClass(selectedItemA);
                        addSelectedClass(item);
                        selectedItemA = item;
                    }
                });
            } else {
                slideImagesA.forEach((slide, index) => {
                    if (slide.getAttribute("data-image") === imageId) {
                        removeSelectedClass(selectedSlideA);
                        addSelectedClass(slide);
                        selectedSlideA = slide;
                        swipers.a.slideTo(index);
                    }
                });
            }
        } else if (formId === 'b') {
            if (isSlide) {
                removeSelectedClass(selectedSlideB);
                selectedSlideB = element;
            } else {
                removeSelectedClass(selectedItemB);
                selectedItemB = element;
            }
            addSelectedClass(element);
            if (isSlide) {
                imageItemsB.forEach(item => {
                    if (item.getAttribute("data-image-item") === imageId) {
                        removeSelectedClass(selectedItemB);
                        addSelectedClass(item);
                        selectedItemB = item;
                    }
                });
            } else {
                slideImagesB.forEach((slide, index) => {
                    if (slide.getAttribute("data-image") === imageId) {
                        removeSelectedClass(selectedSlideB);
                        addSelectedClass(slide);
                        selectedSlideB = slide;
                        swipers.b.slideTo(index);
                    }
                });
            }
        } else if (formId === 'c') {
            if (isSlide) {
                removeSelectedClass(selectedSlideC);
                selectedSlideC = element;
            } else {
                removeSelectedClass(selectedItemC);
                selectedItemC = element;
            }
            addSelectedClass(element);
            if (isSlide) {
                imageItemsC.forEach(item => {
                    if (item.getAttribute("data-image-item") === imageId) {
                        removeSelectedClass(selectedItemC);
                        addSelectedClass(item);
                        selectedItemC = item;
                    }
                });
            } else {
                slideImagesC.forEach((slide, index) => {
                    if (slide.getAttribute("data-image") === imageId) {
                        removeSelectedClass(selectedSlideC);
                        addSelectedClass(slide);
                        selectedSlideC = slide;
                        swipers.c.slideTo(index);
                    }
                });
            }
        }
    }

    imageItemsA.forEach(image => {
        image.addEventListener("click", function() {
            const imageId = this.getAttribute("data-image-item");
            handleClick(imageId, this, false, 'a');
        });
    });

    slideImagesA.forEach(slide => {
        slide.addEventListener("click", function() {
            const imageId = this.getAttribute("data-image");
            handleClick(imageId, this, true, 'a');
        });
    });

    imageItemsB.forEach(image => {
        image.addEventListener("click", function() {
            const imageId = this.getAttribute("data-image-item");
            handleClick(imageId, this, false, 'b');
        });
    });

    slideImagesB.forEach(slide => {
        slide.addEventListener("click", function() {
            const imageId = this.getAttribute("data-image");
            handleClick(imageId, this, true, 'b');
        });
    });

    imageItemsC.forEach(image => {
        image.addEventListener("click", function() {
            const imageId = this.getAttribute("data-image-item");
            handleClick(imageId, this, false, 'c');
        });
    });

    slideImagesC.forEach(slide => {
        slide.addEventListener("click", function() {
            const imageId = this.getAttribute("data-image");
            handleClick(imageId, this, true, 'c');
        });
    });

    // document.querySelectorAll(".selectionForm").forEach(form => {
    //     form.addEventListener("submit", function(e) {
    //         e.preventDefault();
    //         const formId = this.getAttribute("data-form-id");
    //         const formData = new FormData(this);

    //         fetch("{% url 'save_selection' %}", {
    //             method: "POST",
    //             body: formData,
    //             headers: {
    //                 "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
    //             },
    //         })
    //         .then(response => response.json())
    //         .then(data => {
    //             alert(`選択が保存されました！ (${formId})`);
    //         })
    //         .catch(error => {
    //             alert(`エラーが発生しました。もう一度お試しください。 (${formId})`);
    //         });
    //     });
    // });
});