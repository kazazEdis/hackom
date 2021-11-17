const batch = document.querySelector("body > form > input[type=checkbox]");
const form = document.querySelector("body > form");
const msisdn = document.getElementsByName("msisdn");

let batchBox = document.createElement("textarea");
batchBox.type = "text";
batchBox.name = "msisdn";

let inputBox = document.createElement("input");
inputBox.type = "text";
inputBox.name = "msisdn";
inputBox.value = "385";

batch.addEventListener('click', function(){
    msisdn[0].remove()
    if (batch.checked == true){
        form.insertBefore(batchBox, form.firstChild);
    } else {
        form.insertBefore(inputBox, form.firstChild);
    }
})
