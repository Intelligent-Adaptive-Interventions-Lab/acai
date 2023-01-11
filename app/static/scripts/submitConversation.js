let btnSubmit = document.getElementById("btn-submit");
let formSubmit = document.getElementById("form-submit");

let textareaMessage = document.getElementById("textarea-message");
btnSubmit.addEventListener('click', function handleClick(event) {
    event.preventDefault();

    let formMessage = document.getElementById("form-message");
    let botNewMessage = document.getElementById("bot-new-message");
    let userNewMessage = document.getElementById("user-new-message");

    if (textareaMessage.value) {
        formMessage.value = textareaMessage.value;
        formSubmit.click();
        textareaMessage.value = '';

        userNewMessage.classList.remove("d-none");
        botNewMessage.classList.add("d-none");

        let tempUserBox = document.getElementById("temp-user-box");
        let tempUserMsg = document.getElementById("temp-user-msg");
        tempUserMsg.insertAdjacentText('afterbegin', formMessage.value);
        tempUserBox.classList.remove("d-none");

        let chatBoxes = document.querySelectorAll('.convo__box'); 
        if (chatBoxes.length > 1) {
            let secondLastChatBox = chatBoxes[chatBoxes.length-2];
            secondLastChatBox.scrollIntoView(alignToTop=false);
        }
        let lastChatBox = chatBoxes[chatBoxes.length-1];  
        lastChatBox.scrollIntoView({behavior: "smooth", block: "start"});

    };
    formMessage.value = '';
});