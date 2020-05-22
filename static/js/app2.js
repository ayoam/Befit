document.getElementById("newpassword").addEventListener("keyup",function(){
    let newpassword = document.getElementById("newpassword");
    if (newpassword.value.length < 8) {
        if (newpassword.classList.contains("sucess-input")){
            newpassword.classList.remove("sucess-input")
        }
        newpassword.classList.add("error-input")
    } else {
        newpassword.classList.remove("error-input")
        newpassword.classList.add("sucess-input")
    }
})

document.getElementById("newpassword2").addEventListener("keyup",function(){
    let newpassword = document.getElementById("newpassword");
    let newpassword2 = document.getElementById("newpassword2");
    if (newpassword2.value != newpassword.value) {
        if (newpassword2.classList.contains("sucess-input")){
            newpassword2.classList.remove("sucess-input")
        }
        newpassword2.classList.add("error-input")
    } else {
        newpassword2.classList.remove("error-input")
        newpassword2.classList.add("sucess-input")
    }
})