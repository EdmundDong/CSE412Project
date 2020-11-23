function logout(){
    localStorage.removeItem("gamedb_auth")

    window.location.reload()
}