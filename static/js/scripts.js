function editEquipment(id) {
    fetch(`/equipo/${id}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('edit_name').value = data.name;
            document.getElementById('edit_status').value = data.status;
            document.getElementById('edit_location').value = data.location;
            document.getElementById('edit_user_id').value = data.user_id;
            document.getElementById('editEquipmentForm').action = `/equipo/${id}/edit`;
            new bootstrap.Modal(document.getElementById('editEquipmentModal')).show();
        });
}

function editarPanel(id) {
    fetch(`/laboratorio/${id}/data`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('edit_nombre').value = data.nombre;
            document.getElementById('edit_desc').value = data.descripcion;
            document.getElementById('editPanelForm').action = `/laboratorio/${id}/edit`;
            new bootstrap.Modal(document.getElementById('editPanelModal')).show();
        });
}

function editUser(id) {
    fetch(`/usuarios/${id}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('edit_username').value = data.username;
            document.getElementById('edit_rol').value = data.rol;
            document.getElementById('editUserForm').action = `/usuarios/${id}/edit`;
            new bootstrap.Modal(document.getElementById('editUserModal')).show();
        });
}

function generateQR(equipmentId) {
    fetch(`/equipo/${equipmentId}/qr`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('qrMensaje').innerText = data.mensaje;
            document.getElementById('qrImagen').src = data.qr_image;
            document.getElementById('qrFilename').innerText = data.nombre_archivo;
            document.getElementById('btnGuardarQR').href = `/equipo/guardar_qr/${equipmentId}`;
            new bootstrap.Modal(document.getElementById('GenerarQRModal')).show();
        })
        .catch(err => {
            console.error('Error al generar el QR:', err);
            alert('Ocurrió un error al generar el código QR.');
        });
}
  
function openMoveModal(equipmentId) {
    const form = document.getElementById("moveEquipmentForm");
    form.action = "/equipo/" + equipmentId + "/mover";

    const modal = new bootstrap.Modal(document.getElementById("MoverPanelModal"));
    modal.show();
}
