console.log(document.getElementById("searchform"))
document.getElementById("searchform").addEventListener("submit", function(e){
    e.preventDefault()
    let text = document.getElementById("game").value
    

    window.location.href = "/search/?type=word&query=" + text
	console.log(window.location.href)
    //window.location.reload()
})
/*
document.getElementById("sort_alph_button").addEventListener("click", function(){
    window.location.href += "?type=name_asc"

    window.location.reload()
})
*/