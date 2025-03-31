/**
 * Hides all alert messages on the page after a 5 second delay.
 */
setTimeout(function () {
    document.querySelectorAll('.alert').forEach(function (alert) {
        alert.remove();
    });
}, 5000);


/**
* Navigates the browser back to the previous page in history after confirmation.
*/
function goBack() {
    if (confirm("Are you sure you want to go back? Any unsaved changes may be lost.")) {
        window.history.back();
    }
}


document.addEventListener('DOMContentLoaded', function() {
    /**
     * Adds event listeners to handle the password reset flow.
     */
    document.getElementById('reset-password-button').addEventListener('click', function() {
        document.getElementById('reset-password-message').style.display = 'block';
        document.getElementById('reset-password-button').style.display = 'none';
        document.getElementById('go-home-button').style.display = 'block';
    });

    /**
    * Event listener for the 'go-home-button' click.
    * Redirects the user to the home page.
    */
    document.getElementById('go-home-button').addEventListener('click', function() {
        window.location.href = '/';
    });
});