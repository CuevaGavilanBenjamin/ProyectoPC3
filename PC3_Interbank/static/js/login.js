document.getElementById('loginForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    const mensaje = document.getElementById('mensaje');
    mensaje.className = 'mensaje';
    mensaje.style.display = 'none';

    const correo = document.getElementById('correo').value.trim();
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/api/login/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
            body: JSON.stringify({ correo, password })
        });
        const result = await response.json();

        if (response.ok) {
            // Guarda el token JWT
            if (result.access) {
                localStorage.setItem('access_token', result.access);
                localStorage.setItem('refresh_token', result.refresh);
            }
            mensaje.textContent = result.mensaje || 'Login exitoso.';
            mensaje.classList.add('success');
            mensaje.style.display = 'block';
            setTimeout(() => { window.location.href = '/dashboard/'; }, 1200);
        } else {
            mensaje.textContent = result.error || 'Credenciales incorrectas.';
            mensaje.classList.add('error');
            mensaje.style.display = 'block';
        }
    } catch (error) {
        mensaje.textContent = 'Error de conexión. Intenta nuevamente.';
        mensaje.classList.add('error');
        mensaje.style.display = 'block';
    }
});