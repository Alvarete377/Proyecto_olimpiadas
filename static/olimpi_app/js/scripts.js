// Validación básica de fechas
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const finiEnc = new Date(document.getElementById('finiEnc').value);
            const ffinEnc = new Date(document.getElementById('ffinEnc').value);
            
            if (finiEnc >= ffinEnc) {
                e.preventDefault();
                alert('❌ La fecha de fin debe ser posterior a la fecha de inicio');
                return false;
            }
            
            // Validación de que todos los campos requeridos están llenos
            const requiredFields = form.querySelectorAll('[required]');
            let valid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    valid = false;
                    field.style.borderColor = '#dc3545';
                } else {
                    field.style.borderColor = '#e9ecef';
                }
            });
            
            if (!valid) {
                e.preventDefault();
                alert('⚠️ Por favor, completa todos los campos requeridos');
                return false;
            }
            
            return true;
        });

        // Establecer fecha mínima como hoy
        const today = new Date().toISOString().slice(0, 16);
        const finiEncInput = document.getElementById('finiEnc');
        const ffinEncInput = document.getElementById('ffinEnc');
        
        if (finiEncInput) finiEncInput.min = today;
        if (ffinEncInput) ffinEncInput.min = today;
        
        // Actualizar fecha mínima de fin cuando cambia la fecha de inicio
        if (finiEncInput && ffinEncInput) {
            finiEncInput.addEventListener('change', function() {
                ffinEncInput.min = this.value;
            });
        }
    }

    // Animaciones para las tarjetas de estadísticas
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });

    // Auto-ocultar mensajes después de 5 segundos
    const messages = document.querySelectorAll('.alert');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            message.style.transition = 'opacity 0.5s ease';
            setTimeout(() => message.remove(), 500);
        }, 5000);
    });
});
