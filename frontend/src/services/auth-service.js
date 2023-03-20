
export const authService = {
    loginUser,
    logoutUser
}

function loginUser(email, password) {
    const requestOptions = {
        crossDomain: false,
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
        body: JSON.stringify({ email, password })
    };

    return fetch(`https://mnmdev1.truestreamz.com/api/net-tv/login`, requestOptions)
        .then((response) => {
            return response.json().then(text => {
                if (!response.ok) {
                    if (response.status === 401) {
                        localStorage.removeItem('user');
                    }
        
                    const error = (text && text.message) || response.statusText;
                    return Promise.reject(error)
                }
                localStorage.setItem('user', JSON.stringify(text));
                return text;
            });
        });
}

function logoutUser() {
    localStorage.removeItem('user');
}