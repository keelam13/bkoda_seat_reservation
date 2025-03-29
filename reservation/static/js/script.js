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


document.getElementById('reset-password-button').addEventListener('click', function() {
    document.getElementById('reset-password-message').style.display = 'block';
    document.getElementById('reset-password-button').style.display = 'none';
    document.getElementById('go-home-button').style.display = 'block';
});

document.getElementById('go-home-button').addEventListener('click', function() {
    window.location.href = '/'; // Replace with your home page URL
});