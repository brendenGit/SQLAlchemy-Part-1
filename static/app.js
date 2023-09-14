document.addEventListener('DOMContentLoaded', function() {
    const cancelButton = document.getElementById('cancelButton');
    const addButton = document.getElementById('addButton');
    const form = document.getElementById('form');

    cancelButton.addEventListener('click', function(e) {
        window.history.back();
        e.preventDefault();
    });

    addButton.addEventListener('click', function() {
        form.submit();
    });
});