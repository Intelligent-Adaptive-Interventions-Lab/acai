var curr_id = document.getElementById("page-id").innerHTML;

var breadcrumb_list = document.getElementById("breadcrumb-list");
const breadcrumb = document.createElement('li');
breadcrumb.classList.add("breadcrumb-item");
breadcrumb.classList.add("active");
breadcrumb.innerHTML = `${curr_id}`
breadcrumb_list.appendChild(breadcrumb);
