function noop(){}

fetch("https://twitter-whereis.glitch.me/codl").then(res => {
    if(res.ok){
        return res.json()
    } else {
        throw "frick!";
    }
}).then(json => {
    document.querySelector("#whereis").textContent = json.full_name.toLowerCase();
}).catch(noop)
