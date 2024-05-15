
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

    // スライド画像のクリックイベント
    const slideImages = document.querySelectorAll(".swiper-slide");
    let selectedSlide = null;

    slideImages.forEach((image) => {
        image.addEventListener("click", function() {
            const selectedImage = image.getAttribute("data-image");
            document.getElementById("selected_image").value = selectedImage;
            console.log(selectedImage);

            // 以前選択されたスライドから選択クラスを削除
            if (selectedSlide) {
                selectedSlide.classList.remove("selected-image");
            }

            // 現在のスライドに選択クラスを追加
            image.classList.add("selected-image");

            // 現在のスライドを記録
            selectedSlide = image;
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