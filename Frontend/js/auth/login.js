let loader = document.getElementById('loader')

function showLoader() {
    loader.classList.remove('d-none')
}

function hideLoader() {
    loader.classList.add('d-none')
}
let loginForm = document.getElementById('loginForm')

loginForm.addEventListener('submit', (e) => {
    e.preventDefault()

    let username = document.getElementById('username').value
    let password = document.getElementById('password').value

    let loginData = {
        username: username,
        password: password
    }
    showLoader()
    fetch("http://127.0.0.1:8000/api/v1/login/", {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(loginData)
    }).then(res => res.json())
    .then(data =>{
        hideLoader();
        if(data.access && data.refresh){
            sessionStorage.setItem('accesstoken', data.access)
            sessionStorage.setItem('refreshtoken', data.refresh)
            
            console.log(data.access)
            console.log(data.refresh)
            window.location.href = "../pages/dashboard.html"
            
        }
        
        else{
            alert(data.status)

        }
        
    }).catch(err=>{
        hideLoader()
        alert("Something went wrong")
    })
})