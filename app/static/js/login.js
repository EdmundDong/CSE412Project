document.getElementById("login_button").addEventListener("click", function(e){
    e.preventDefault()
    
    let username = document.getElementById("username_field").value;
    let password = document.getElementById("password_field").value;

    auth(username, password, "login")
})