
    jQuery("a").focus(
    function(){
        this.blur();
    });


    var loginBtn = $('.carousel-inner #log-btn');
    var registrationBtn = $('.carousel-inner #reg-button');
    var loginBackBtn = $('.carousel-inner #button-id-auth-back');
    var registrationBackBtn = $('.carousel-inner #button-id-reg-back');

    var home = $('#home');
    var regForm = $('#registration-form');
    var loginFrom = $('#login-form');


    registrationBtn.click(function() {
        swapBlocks(home, regForm)
    });

    loginBtn.click(function(){
        swapBlocks(home, loginFrom)
    });

    loginBackBtn.click(function () {
       swapBlocks(loginFrom, home)
    });

    registrationBackBtn.click(function () {
       swapBlocks(regForm, home)
    });

function swapBlocks(active, passive){
    active.animate({
        opacity: 0
    });
    active.hide();

    passive.show();
    passive.animate({
        opacity: 1
    });
}