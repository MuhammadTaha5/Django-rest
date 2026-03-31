async function checkAuth(){
    let access = sessionStorage.getItem('accesstoken')
    let refresh = sessionStorage.getItem('refreshtoken')
    if(!access){
        if(refresh){
            let res = await fetch("http://127.0.0.1:8000/api/v1/api/token/refresh/", {
                method: 'POST',
                headers: {'Content-Type': 'application/josn'},
                body: JSON.stringify({
                    'refresh': refresh
                })
            })
            const data = await res.json()
            if (data.access){
                sessionStorage.setItem('accesstoken', data.access)
                return true
            }
        }

    }
    window.location.href = 'login.html'
    return false
}