let updateFiles = document.querySelector("#update");
let calcReturn = document.querySelector("#calc");
let createOutput = document.querySelector("#output");
let makeTablData = document.querySelector("#makeTable");
let fixIndex = document.querySelector("#fixIndex");
let groupData = document.querySelector("#groupData");
let alert = document.querySelector("#alert");

// This function is for getting a cookie value.
function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

// This function sends an ajax request to the beta/update page.
let sendWithAjax = function(e) {
    let csrftoken = getCookie("csrftoken");
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            alert.innerHTML = this.responseText;
            return true;
        }
    }
    xhttp.open("POST", "", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.send("action=" + e);
    alert.innerHTML = "...درخواست به سمت سرور فرستاده شد";

}

updateFiles.addEventListener("click", () => {
    sendWithAjax("updateFiles");
});
calcReturn.addEventListener("click", () => {
   sendWithAjax("calcReturn");
});
createOutput.addEventListener("click", () => {
   sendWithAjax("createOutput");
});
makeTablData.addEventListener("click", () => {
    sendWithAjax("makeTable");
});
fixIndex.addEventListener("click", () => {
    sendWithAjax("fixIndex");
})
groupData.addEventListener("click", () => {
    sendWithAjax("groupData");
})









