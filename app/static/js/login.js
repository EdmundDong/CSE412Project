document.getElementById("login_button").addEventListener("click", function(e){
    e.preventDefault()
    
    let username = document.getElementById("username").value;
    let password = document.getElementById("exampleInputPassword1").value;

    auth(username, password, "login")
})