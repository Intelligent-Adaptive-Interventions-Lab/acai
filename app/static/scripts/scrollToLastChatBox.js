let chatBoxes = document.querySelectorAll('.convo__box'); 
if (chatBoxes.length > 1) {
    let secondLastChatBox = chatBoxes[chatBoxes.length-2];
    secondLastChatBox.scrollIntoView(alignToTop=false);
}
let lastChatBox = chatBoxes[chatBoxes.length-1];  
lastChatBox.scrollIntoView({behavior: "smooth", block: "start"});
