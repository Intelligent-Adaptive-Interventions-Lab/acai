var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));

var options = {
    trigger: 'hover focus click',
    title: "<p id='copy-before' class='p-0 m-0'>Copy user name</p> <p id='copy-later' class='d-none p-0 m-0'>User name copied!</p>",
};

var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl, options);
});

tooltipTriggerList.forEach(tooltipTrigger => {
    tooltipList.forEach(tooltip => {
        tooltipTrigger.addEventListener('shown.bs.tooltip', function () {
            // do something...
            setTimeout(() => {
                tooltip.hide();
            }, 1500);
        });

        tooltipTrigger.addEventListener('click', function () {
            var copy_before = document.getElementById('copy-before');
            var copy_later = document.getElementById('copy-later');

            copy_before.classList.add("d-none");
            copy_later.classList.remove("d-none");
        });

        tooltipTrigger.addEventListener('hover', function () {
            var copy_before = document.getElementById('copy-before');
            var copy_later = document.getElementById('copy-later');

            copy_before.classList.remove("d-none");
            copy_later.classList.add("d-none");
            });
    });
});

var clipboard = new ClipboardJS('.user__clipboard');

clipboard.on('success', function (e) {
    console.info('Action:', e.action);
    console.info('Text:', e.text);
    console.info('Trigger:', e.trigger);

    e.clearSelection();
});

clipboard.on('error', function (e) {
    console.error('Action:', e.action);
    console.error('Trigger:', e.trigger);
});