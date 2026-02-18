let boletoSeleccionado = null;

// Agregar evento click a boletos disponibles
document.querySelectorAll('.boleto-disponible').forEach(boleto => {
    boleto.addEventListener('click', function() {
        boletoSeleccionado = this.dataset.id;
        document.getElementById('modal-reserva').style.display = 'flex';
    });
});

function confirmarReserva() {
    const nombre = document.getElementById('nombre').value;
    const telefono = document.getElementById('telefono').value;
    
    if (!nombre || !telefono) {
        alert('Por favor completa todos los campos');
        return;
    }
    
    fetch(`/reservar/${boletoSeleccionado}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nombre, telefono })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        }
    });
}

function marcarPagado(boletoId) {
    if (confirm('¿Confirmar pago de este boleto?')) {
        fetch(`/pagar/${boletoId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
        });
    }
}

function cerrarModal() {
    document.getElementById('modal-reserva').style.display = 'none';
    boletoSeleccionado = null;
}
