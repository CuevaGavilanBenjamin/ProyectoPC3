// static/js/documentos.js

document.addEventListener('DOMContentLoaded', function () {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/login/';
        return;
    }

    // ===================== LISTAR DOCUMENTOS =====================
    function cargarDocumentos() {
        fetch('/documentos/empresa/', {
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
                const contenedor = document.getElementById('listaDocumentos');
                contenedor.innerHTML = '';
                data.forEach(doc => {
                    contenedor.innerHTML += `
                    <div class="documento-item">
                        <span>${doc.nombre} (${doc.tipo_documento})</span>
                        <span class="etiquetas">${doc.etiquetas || ''}</span>
                        <button class="verPdfBtn" data-id="${doc.id}">PDF</button>
                        <button class="editarDocBtn" data-id="${doc.id}">Editar</button>
                        <button class="eliminarDocBtn" data-id="${doc.id}">Eliminar</button>
                    </div>
                `;
                });
            });
    }

    cargarDocumentos();

    // ===================== SUBIR / CREAR DOCUMENTO =====================
    document.getElementById('nuevoDocumentoBtn').addEventListener('click', function () {
        document.getElementById('documentoForm').reset();
        document.getElementById('documento_id').value = '';
        document.getElementById('documentoModal').style.display = 'flex';
    });

    document.getElementById('cerrarDocumentoModalBtn').addEventListener('click', function () {
        document.getElementById('documentoModal').style.display = 'none';
    });

    document.getElementById('documentoForm').addEventListener('submit', function (e) {
        e.preventDefault();
        const docId = document.getElementById('documento_id').value;
        const url = docId ? `/documentos/empresa/${docId}/` : '/documentos/empresa/';
        const method = docId ? 'PUT' : 'POST';
        const formData = {
            nombre: document.getElementById('titulo').value,
            tipo_documento: document.getElementById('tipo_documento').value,
            contenido: document.getElementById('contenido').value,
            etiquetas: document.getElementById('etiquetas').value
        };
        const mensaje = document.getElementById('documentoMensaje');
        mensaje.className = 'mensaje';
        mensaje.style.display = 'none';

        fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token,
                'Accept': 'application/json'
            },
            body: JSON.stringify(formData)
        })
            .then(r => r.json().then(data => ({ status: r.status, data })))
            .then(res => {
                if (res.status >= 200 && res.status < 300) {
                    mensaje.textContent = res.data.mensaje || 'Documento guardado correctamente.';
                    mensaje.classList.add('success');
                    cargarDocumentos();
                    setTimeout(() => {
                        document.getElementById('documentoModal').style.display = 'none';
                    }, 1000);
                } else {
                    mensaje.textContent = res.data.error || 'Error al guardar documento.';
                    mensaje.classList.add('error');
                }
                mensaje.style.display = 'block';
            })
            .catch(() => {
                mensaje.textContent = 'Error de conexión.';
                mensaje.classList.add('error');
                mensaje.style.display = 'block';
            });
    });

    // Mostrar/ocultar formulario de subir documento
    document.getElementById('mostrarSubirDocBtn').addEventListener('click', function () {
        document.getElementById('subirDocForm').style.display = 'block';
    });
    document.getElementById('cancelarSubirDocBtn').addEventListener('click', function () {
        document.getElementById('subirDocForm').reset();
        document.getElementById('subirDocForm').style.display = 'none';
    });

    // Subir documento existente
    document.getElementById('subirDocForm').addEventListener('submit', async function (e) {
        e.preventDefault();
        const formData = new FormData();
        formData.append('archivo', document.getElementById('archivo').files[0]);
        formData.append('nombre', document.getElementById('tituloArchivo').value);
        formData.append('tipo_documento', document.getElementById('tipoArchivo').value);
        formData.append('etiquetas', document.getElementById('etiquetasArchivo').value);

        const mensaje = document.getElementById('docMensaje');
        mensaje.className = 'mensaje';
        mensaje.style.display = 'none';

        try {
            const response = await fetch('/documentos/empresa/', {
                method: 'POST',
                body: formData,
                headers: {
                    'Authorization': 'Bearer ' + token,
                    'Accept': 'application/json'
                }
            });
            const result = await response.json();
            if (response.ok) {
                mensaje.textContent = result.mensaje || 'Documento subido correctamente.';
                mensaje.classList.add('success');
                cargarDocumentos();
                setTimeout(() => {
                    document.getElementById('subirDocForm').reset();
                    document.getElementById('subirDocForm').style.display = 'none';
                }, 1000);
            } else {
                mensaje.textContent = result.error || 'Error al subir.';
                mensaje.classList.add('error');
            }
            mensaje.style.display = 'block';
        } catch {
            mensaje.textContent = 'Error de conexión.';
            mensaje.classList.add('error');
            mensaje.style.display = 'block';
        }
    });

    // ===================== GENERAR Y PREVISUALIZAR PDF =====================
    document.getElementById('listaDocumentos').addEventListener('click', function (e) {
        if (e.target.classList.contains('verPdfBtn')) {
            const docId = e.target.getAttribute('data-id');
            fetch(`/documentos/generar-pdf/${docId}/`, {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + token,
                    'Accept': 'application/pdf'
                }
            })
                .then(response => response.blob())
                .then(blob => {
                    const url = URL.createObjectURL(blob);
                    document.getElementById('pdfPreview').src = url;
                    document.getElementById('descargarPdfBtn').href = url;
                    document.getElementById('pdfModal').style.display = 'flex';
                });
        }
        // Puedes agregar aquí editar/eliminar documento
    });

    document.getElementById('cerrarPdfModalBtn').addEventListener('click', function () {
        document.getElementById('pdfModal').style.display = 'none';
        document.getElementById('pdfPreview').src = '';
    });

    // ===================== FILTROS Y BÚSQUEDA =====================
    document.getElementById('busquedaDocumento').addEventListener('input', function () {
        // Puedes implementar búsqueda local o volver a llamar a la API con el filtro
        // Por simplicidad, recarga la lista (mejorar según tu backend)
        cargarDocumentos();
    });
    document.getElementById('tipoDocumentoFiltro').addEventListener('change', function () {
        cargarDocumentos();
    });

    // ===================== ELIMINAR DOCUMENTO =====================
    document.getElementById('listaDocumentos').addEventListener('click', function (e) {
        if (e.target.classList.contains('eliminarDocBtn')) {
            const docId = e.target.getAttribute('data-id');
            if (confirm('¿Seguro que deseas eliminar este documento?')) {
                fetch(`/documentos/empresa/${docId}/`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': 'Bearer ' + token,
                        'Accept': 'application/json'
                    }
                })
                    .then(r => r.json())
                    .then(data => {
                        alert(data.mensaje || 'Documento eliminado');
                        cargarDocumentos();
                    });
            }
        }
        // Puedes agregar aquí lógica para editar documento
        if (e.target.classList.contains('editarDocBtn')) {
            const docId = e.target.getAttribute('data-id');
            fetch(`/documentos/empresa/${docId}/`, {
                headers: {
                    'Authorization': 'Bearer ' + token,
                    'Accept': 'application/json'
                }
            })
                .then(r => r.json())
                .then(doc => {
                    document.getElementById('documento_id').value = doc.id;
                    document.getElementById('tipo_documento').value = doc.tipo_documento;
                    document.getElementById('titulo').value = doc.nombre;
                    document.getElementById('contenido').value = doc.contenido;
                    document.getElementById('etiquetas').value = doc.etiquetas || '';
                    document.getElementById('documentoModal').style.display = 'flex';
                });
        }
    });
});