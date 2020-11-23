async function auth_fetch(username, password, method){
    const response = await fetch("/api/" + method, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })

    if(!response.ok){
        throw new Error("Failed")
    }

    const resp = await response.json()
    return resp
}

function auth(username, password, method){
    auth_fetch(username, password, method).then(function(resp){
        if ("error"  in resp){
            console.log(resp["error"])
        }else{
            localStorage.setItem("gamedb_auth", JSON.stringify(resp))
        }
    })
}

