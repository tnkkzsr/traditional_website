
document.addEventListener("DOMContentLoaded", function() {

    // Swiperの初期化
    const swiper = new Swiper(".swiper-container", {
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
        },
    });

    //画像一覧、スライドのクリックイベント
    const ImageItems = document.querySelectorAll(".image-item");
    let selectedItem = null;
    const slideImages = document.querySelectorAll(".swiper-slide");
    let selectedSlide = null;

    ImageItems.forEach((item) => {
        item.addEventListener("click", function() {
            const selectedImage = item.getAttribute("data-image-item");
            // 選択された画像をフォームにセット
            document.getElementById("selected_image").value = selectedImage;
            

            // 以前選択された画像から選択クラスを削除
            if (selectedItem) {
                selectedItem.classList.remove("selected-image");
            }

            // 現在の画像に選択クラスを追加
            item.classList.add("selected-image");

            // 現在の画像を記録
            selectedItem = item;

            // スライドの赤枠も選択画像に合わせて移動
            slideImages.forEach((image,index) => {
                image.classList.remove("selected-image");
                if (image.getAttribute("data-image") === selectedImage) {
                    image.classList.add("selected-image");
                    selectedSlide = image;
                    swiper.slideTo(index-1);
                }
            })
            
        });
    });


    // スライド画像のクリックイベント
    slideImages.forEach((image) => {
        image.addEventListener("click", function() {
            // 選択されたスライドをフォームにセット
            const selectedImage = image.getAttribute("data-image");
            document.getElementById("selected_image").value = selectedImage;
            

            // 以前選択されたスライドから選択クラスを削除
            if (selectedSlide) {
                selectedSlide.classList.remove("selected-image");
            }

            // 現在のスライドに選択クラスを追加
            image.classList.add("selected-image");

            // 現在のスライドを記録
            selectedSlide = image;

            // スライドの赤枠も選択画像に合わせて移動
            ImageItems.forEach((image) => {
                image.classList.remove("selected-image");
                if (image.getAttribute("data-image-item") === selectedImage) {
                    image.classList.add("selected-image");
                    selectedItem = image;
                }
            });
        });
    });

    // // フォーム送信のAjax処理
    // document.getElementById("selectionForm").addEventListener("submit", function(e) {
    //     e.preventDefault();
    //     const formData = new FormData(this);

    //     fetch("{% url 'save_selection' %}", {
    //         method: "POST",
    //         body: formData,
    //         headers: {
    //             "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
    //         },
    //     })
    //     .then(response => response.json())
    //     .then(data => {
    //         alert("選択が保存されました！");
    //     })
    //     .catch(error => {
    //         alert("エラーが発生しました。もう一度お試しください。");
    //     });
    // }); 
});