document.addEventListener('DOMContentLoaded', function () {
    const token = localStorage.getItem('access_token');
    alert('Token: ' + token);
    if (!token) {
        window.location.href = '/login/';
        return;
    }

    fetch('/users/api/cuenta/', {
        headers: {
            'Authorization': 'Bearer ' + token,
            'Accept': 'application/json'
        }
    })
        .then(r => {
            if (r.status === 401 || r.status === 403) {
                window.location.href = '/login/';
                return;
            }
            return r.json();
        })
        .then(data => {
            if (!data) return;
            if (data.rol !== 'editor') {
                window.location.href = '/login/';
                return;
            }
            document.getElementById('bienvenida').textContent = `¡Hola, ${data.nombre}!`;
        });
});