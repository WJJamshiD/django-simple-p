$(document).ready(function(){
    
    $nav=$('.nav');
    $toggleCollapse=$('.toggle-icons i');
    
    /* click event on toogle menu */

    $toggleCollapse.click(function(){
        $nav.toggleClass('collapse');  
    })

    //owl-carousel for blog
    $('.owl-carousel').owlCarousel({
        loop:true,
        autoplay: false,
        autoplayTimeout:3000,
        dots:false,
        nav:true,
        navText: [$('.owl-navigation .owl-nav-prev'), $('.owl-navigation .owl-nav-next')],
        responsive:{
            320:{
                items:1
            },
            560:{
                items:2
            },
            960:
            {
                items:3
            }
        }

    });

    // click to scroll top
    $('.move-up span').click(function () {
        $('html, body').animate({
            scrollTop: 0
        }, 1000);
    })

    // AOS Instance
    AOS.init();
});