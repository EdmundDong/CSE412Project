async function get_profile_likes(user_id){
    const response = await fetch("/api/profile/"+user_id, {
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
async function get_recommended(user_id){
    const response = await fetch("/api/profile/recommended/"+user_id, {
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

function populate_profile_likes(games){
    let template = `
        <% for (let game of games){%>
                <div class = "col-md-6" style = "margin-bottom: 20px;">
                    <div class = "row" style="width: 100%; border: 1px solid black; border-radius: 10px; margin: auto; padding: 15px">
                        <div class ="col-md-6" id = "game1">
                            <h3><a href = "<%= "../game/" + game[0] %>"> <%= game[1] %> </a></h3>
                        </div>
                        <div class ="col-md-6">
                            <div class = "row">
                                <h4> Likes: <span><%= game[8] %></span></h4>
                            </div>
                            <div class = "row">
                                <h4> Genre: <span><%= game[9] %></span></h4>
                            </div>
                        </div>
                    </div>
               
            </div>
            </br>
        <% } %>
    `
    htmlout = ejs.render(template, {games: games})

    console.log(games.length)
    if (games.length > 0){
        document.getElementById("liked_games").innerHTML = htmlout
    }else{
        document.getElementById("liked_games").innerHTML = '<h3 style = "width: 100%; text-align: center;">You have not liked a game.</h3>'
    }
    

    
}

function populate_recommended(games){
    let template = `
        <% for (let game of games){%>
                <div class = "col-md-6" style = "margin-bottom: 20px;">
                    <div class = "row" style="width: 100%; border: 1px solid black; border-radius: 10px; margin: auto; padding: 15px">
                        <div class ="col-md-6" id = "game1">
                            <h3><a href = "<%= "../game/" + game[0] %>"> <%= game[1] %> </a></h3>
                        </div>
                        <div class ="col-md-6">
                            <div class = "row">
                                <h4> Likes: <span><%= game[8] %></span></h4>
                            </div>
                            <div class = "row">
                                <h4> Genre: <span><%= game[9] %></span></h4>
                            </div>
                        </div>
                    </div>
               
            </div>
            </br>
        <% } %>
    `
    htmlout = ejs.render(template, {games: games})

    console.log(games.length)
    if (games.length > 0){
        document.getElementById("recommended_games").innerHTML = htmlout
    }else{
        document.getElementById("recommended_games").innerHTML = '<h3 style = "width: 100%; text-align: center;">You have not liked a game.</h3>'
    }
    

    document.getElementById("page").classList.remove("hideElement")
}

if ("gamedb_auth" in localStorage){
    let auth = localStorage.getItem("gamedb_auth")
    let tokenjs = JSON.parse(auth)
    get_profile_likes(tokenjs["user_id"]).then(function(resp){
        
        document.getElementById("username").innerText = tokenjs["username"]
        console.log(resp)
        populate_profile_likes(resp["games"])
        get_recommended(tokenjs["user_id"].then(function(resp){
            populate_recommended(resp["games"])
        }))
    })
    

}else{
    window.location.href = "../"
}