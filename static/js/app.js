document.getElementById("password").addEventListener("keyup",function(){
    let password = document.getElementById("password");
    if (password.value.length < 8) {
        if (password.classList.contains("sucess-input")){
            password.classList.remove("sucess-input")
        }
        password.classList.add("error-input")
    } else {
        password.classList.remove("error-input")
        password.classList.add("sucess-input")
    }
})

document.getElementById("password2").addEventListener("keyup",function(){
    let password = document.getElementById("password");
    let password2 = document.getElementById("password2");
    if (password2.value != password.value) {
        if (password2.classList.contains("sucess-input")){
            password2.classList.remove("sucess-input")
        }
        password2.classList.add("error-input")
    } else {
        password2.classList.remove("error-input")
        password2.classList.add("sucess-input")
    }
})
