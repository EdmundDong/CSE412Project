function logout(){
    localStorage.removeItem("gamedb_auth")

    window.location.reload()
}
document.getElementById("logout_button").addEventListener("click", logout)


if ("gamedb_auth" in localStorage){
    document.getElementById("nav_login").classList.add("hideElement")
    document.getElementById("nav_register").classList.add("hideElement")
    document.getElementById("nav_logout").classList.remove("hideElement")
}