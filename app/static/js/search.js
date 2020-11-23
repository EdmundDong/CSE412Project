document.getElementById("search_button").addEventListener("click", function(){
    let text = document.getElementById("search_field").value
    window.location.href += "?type=word&query=" + text

    window.location.reload()
})

document.getElementById("sort_alph_button").addEventListener("click", function(){
    window.location.href += "?type=name_asc"

    window.location.reload()
})