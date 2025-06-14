document.addEventListener('DOMContentLoaded', function () {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/login/';
        return;
    }
    fetch('/api/panel-empresa/', {
        headers: {
            'Authorization': 'Bearer ' + token,
            'Accept': 'application/json'
        }
    })
        .then(res => {
            if (res.status === 401 || res.status === 403) {
                window.location.href = '/login/';
                return;
            }
            return res.json();
        })
        .then(data => {
            if (data && data.mensaje) {
                document.getElementById('mensaje-bienvenida').textContent = data.mensaje;
            }
        });
});