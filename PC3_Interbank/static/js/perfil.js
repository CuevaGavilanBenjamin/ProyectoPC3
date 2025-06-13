// static/js/perfil.js

document.addEventListener('DOMContentLoaded', function () {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/login/';
        return;
    }

    // Cargar datos del perfil de la empresa
    fetch('/empresas/api/perfil/', {
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
            document.getElementById('razon_social').value = data.razon_social || '';
            document.getElementById('ruc').value = data.ruc || '';
            document.getElementById('representante').value = data.representante || '';
            document.getElementById('correo').value = data.correo || '';
            document.getElementById('direccion').value = data.direccion || '';
            document.getElementById('telefono').value = data.telefono || '';
        });

    // Guardar cambios en el perfil
    document.getElementById('perfilForm').addEventListener('submit', async function (e) {
        e.preventDefault();
        const formData = new FormData(this);
        const mensaje = document.getElementById('perfilMensaje');
        mensaje.className = 'mensaje';
        mensaje.style.display = 'none';
        try {
            const response = await fetch('/empresas/api/perfil/', {
                method: 'POST',
                body: formData,
                headers: {
                    'Authorization': 'Bearer ' + token,
                    'Accept': 'application/json'
                }
            });
            const result = await response.json();
            if (response.ok) {
                mensaje.textContent = result.mensaje;
                mensaje.classList.add('success');
            } else {
                mensaje.textContent = result.error || 'Error al actualizar.';
                mensaje.classList.add('error');
            }
            mensaje.style.display = 'block';
        } catch {
            mensaje.textContent = 'Error de conexión.';
            mensaje.classList.add('error');
            mensaje.style.display = 'block';
        }
    });
});