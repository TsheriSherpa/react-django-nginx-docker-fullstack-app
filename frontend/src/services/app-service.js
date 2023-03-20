const saveApp = (name, username, secret) => {
    const requestOptions = {
        crossDomain: false,
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
        body: JSON.stringify({ name, username, secret })
    };

    return fetch(`https://mnmdev1.truestreamz.com/api/net-tv/login`, requestOptions)
        .then((response) => {
            return response.json().then(text => {
                if (!response.ok) {
                    const error = (text && text.message) || response.statusText;
                    return Promise.reject(error)
                }
                return text;
            });
        });
}