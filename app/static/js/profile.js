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
function populate_profile_likes(games){
    let template = `
        <% for (let game of games){%>
            <div class="row">
                <div class = "col-md-12">
                    <div class = "row" style="width: 100%; border: 1px solid black; border-radius: 10px; margin: auto; padding: 15px">
                        <div class ="col-md-6" id = "game1">
                            <h3>{{game[1]}}</h3>
                        </div>
                        <div class ="col-md-6">
                            <div class = "row">
                                <h4> Likes: <span>{{game[8]}}</span></h4>
                            </div>
                            <div class = "row">
                                <h4> Last Updated: <span>{{game[7]}}</span></h4>
                            </div>
                            <div class = "row">
                                <h4> Genre: <span>{{game[9]}}</span></h4>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            </br>
        <% } %>
    `
    htmlout = ejs.render(template, {games: games})

    document.getElementById("liked_games").innerHTML = htmlout


}
if ("gamedb_auth" in localStorage){
    let auth = localStorage.getItem("gamedb_auth")
    let tokenjs = JSON.parse(auth)
    get_profile_likes(tokenjs["user_id"]).then(function(resp){
        
        
        populate_profile_likes(resp["games"])
    })
}else{
    window.location.href = "../"
}