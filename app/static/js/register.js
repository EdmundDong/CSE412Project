document.getElementById("register_button").addEventListener("click", function(e){
    e.preventDefault()
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    auth(username, password, "register")
})