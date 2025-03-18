window.fbAsyncInit = function() {
    FB.init({
        appId      : '1359722371958371',
        cookie     : true,
        xfbml      : true,
        version    : 'v22.0'
    });
        
    FB.AppEvents.logPageView();   
        
    };

    (function(d, s, id){
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) {return;}
    js = d.createElement(s); js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));


var finished_rendering = function() {
    console.log("finished rendering plugins");
}



function statusChangeCallback(response) {
    console.log('statusChangeCallback', response);
    if (response.status === 'connected') {
        // User is logged in and authorized.
        console.log('Welcome! Fetching your information...');
        FB.api('/me', function(response) {
            console.log('Successful login for: ' + response.name);
            // ... use the user's data ...
        });
    } else {
        // User is not logged in or not authorized.
        console.log('Please log into this app.');
    }
}


function checkLoginState() {
    FB.getLoginStatus(function(response) {
      statusChangeCallback(response);
    });
}

