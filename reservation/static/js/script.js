setTimeout(function () {
    document.querySelectorAll('.alert').forEach(function (alert) {
        alert.remove(); // Remove the alert element
    });
}, 5000); // 5 seconds
