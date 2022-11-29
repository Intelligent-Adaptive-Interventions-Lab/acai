new EmojiPicker({
    trigger: [
        {
            selector: '.emoji',
            insertInto: ['.send__box'] // '.selector' can be used without array
        }
    ],
    closeButton: true,
    //specialButtons: green
});