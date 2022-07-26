console.log('a21321321sd123123213123asad123432123212sdass')

document.addEventListener("DOMContentLoaded", function(){
    let btn = document.querySelector('input[type=submit]');
    btn.style.backgroungColor = "yellow";
    console.log('1212213123123123123123213')
    console.log(btn)
    btn.addEventListener('click', async function(e){
        e.preventDefault()
        let username = document.querySelector('input[name=username]').value
        let password = document.querySelector('input[name=password]').value
        console.log(username, password)
        let response = await fetch("/login", {
            method: "POST",
            body: new FormData(document.querySelector('form'))
        })
        let response_text = await response.text()
        console.log(response, response_text)

    })
    
})