async function fetch_user_status(game_id, user_id){
    const response = await fetch("/api/game/"+game_id + "/"+user_id, {
        method: "GET",
        headers: {
            'Content-Type': 'application/json'
        }
    })

    if(!response.ok){
        throw new Error("Failed")
    }

    const resp = await response.json()
    return resp
}

async function flip_likes(game_id, user_id){
    const response = await fetch("/api/game/likes/"+game_id + "/"+user_id, {
        method: "GET",
        headers: {
            'Content-Type': 'application/json'
        }
    })

    if(!response.ok){
        throw new Error("Failed")
    }

    const resp = await response.json()
    return resp
}

document.getElementById("like_button").addEventListener("click", function(){
    let user_id = JSON.parse(localStorage.getItem("gamedb_auth"))['user_id']
    let game_id = document.getElementById("game_id").innerText;
    flip_likes(game_id, user_id).then(function(resp){
        window.location.reload()
    })    
})

document.getElementById("unlike_button").addEventListener("click", function(){
    let user_id = JSON.parse(localStorage.getItem("gamedb_auth"))['user_id']
    let game_id = document.getElementById("game_id").innerText;
    flip_likes(game_id, user_id).then(function(resp){
        window.location.reload()
    })    
})



if ("gamedb_auth" in localStorage){
    let user_id = JSON.parse(localStorage.getItem("gamedb_auth"))['user_id']
    let game_id = document.getElementById("game_id").innerText;

    fetch_user_status(game_id, user_id).then(function(resp){
        
        let like = resp[like]
        if (!like){
            document.getElementById("like_button").classList.remove("hide")
        }else{
            document.getElementById("unlike_button").classList.remove("hide")
        }


        document.getElementById("like_status_div").classList.remove("hide")

        
    })
}