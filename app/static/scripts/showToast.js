var options = {
    animation: true,
    autohide: true,
    delay: 5000
};
var toastElList = [].slice.call(document.querySelectorAll('.toast'));
var toastList = toastElList.map(function (toastEl) {
    return new bootstrap.Toast(toastEl, options)
});

toastList.forEach(toast => toast.show());