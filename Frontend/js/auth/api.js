const BASE_URL = 'http://127.0.0.1:8000'
export async function fetchwithAuth(url, options={}){
    token = sessionStorage.getItem('accesstoken')
    options.headers = {
        ...options.headers,
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    }
    let response = await fetch(BASE_URL+url, options)

    if(response.status===401){
        let refresh = sessionStorage.getItem('refreshtoken')
        if(!refresh){
            window.location.href = 'login.html'
            return
        }
        let RefreshAccessToken = await fetch(BASE_URL+'/api/v1/api/token/refresh/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }, 
            body: {
                'refresh': refresh
            }
        })
        data = await RefreshAccessToken.json()
        if (data.access){
            sessionStorage.setItem('accesstoken', data.access)
            

        }
    }


}