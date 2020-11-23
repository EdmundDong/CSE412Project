document.getElementById("search_button").addEventListener("click", function(){
    let text = document.getElementById("search_field").value
    window.location.href += "?type=search&query=" + text

    window.location.reload()
})