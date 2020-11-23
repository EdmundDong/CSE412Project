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
    //todo
}
if ("gamedb_auth" in localStorage){
    let auth = localStorage.getItem("gamedb_auth")
    let tokenjs = JSON.parse(auth)
    get_profile_likes(tokenjs["user_id"]).then(function(resp){
        
        
        populate_profile_likes(resp)
    })
}else{
    window.location.href = "../"
}