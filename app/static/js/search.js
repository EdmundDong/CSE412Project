console.log(document.getElementById("searchform"))
document.getElementById("searchform").addEventListener("submit", function(e){
    e.preventDefault()
    let text = document.getElementById("game").value
    
    console.log("/search/?type=word&query=" + text)
    window.location.href = "/search/?type=word&query=" + text
	
})

document.getElementById("sort_likes").addEventListener("click", function(e){
    e.preventDefault()
    window.location.href = "/search/?type=likes_desc"
})

document.getElementById("sort_name").addEventListener("click", function(e){
    e.preventDefault()
    window.location.href = "/search/?type=name_asc"
})
document.getElementById("sort_release").addEventListener("click", function(e){
    e.preventDefault()
    window.location.href = "/search/?type=release_desc"
})

document.getElementById("sort_user").addEventListener("click", function(e){
    e.preventDefault()
    window.location.href = "/search/?type=user_rating_desc"
})
document.getElementById("sort_critic").addEventListener("click", function(e){
    e.preventDefault()
    window.location.href = "/search/?type=critic_rating_desc"
})


if(document.getElementById("previous") != null){
    document.getElementById("previous").addEventListener("click", function(){
        let page_num = parseInt(document.getElementById("page_num").innerText)
        const params = new URLSearchParams(window.location.search)
        params.set("page", page_num-1)

        querystring = params.toString()

        window.location.href = "/search/?" + querystring
    })
}

if(document.getElementById("next") != null){
    document.getElementById("next").addEventListener("click", function(){
        let page_num = parseInt(document.getElementById("page_num").innerText)
        const params = new URLSearchParams(window.location.search)
        params.set("page", page_num+1)

        querystring = params.toString()

        window.location.href = "/search/?" + querystring
    })
}


/*
document.getElementById("sort_alph_button").addEventListener("click", function(){
    window.location.href += "?type=name_asc"

    window.location.reload()
})
*/