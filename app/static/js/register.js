document.getElementById("register_button").addEventListener("click", function(){
    let username = document.getElementById("username_field").value;
    let password = document.getElementById("password_field").value;

    auth(username, password, "register")
})