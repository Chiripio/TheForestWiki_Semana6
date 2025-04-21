document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.estrellas').forEach(estrellasDiv => {
      const temaId = estrellasDiv.getAttribute('data-tema');
      const input = document.getElementById(`valor-input-${temaId}`);
      const form = document.getElementById(`form-valoracion-${temaId}`);
  
      const estrellas = estrellasDiv.querySelectorAll('.estrella');
  
      estrellas.forEach((estrella, index) => {
        // ⭐ Clic para valorar
        estrella.addEventListener('click', function () {
          const valor = index + 1;
  
          // Marcar visualmente las estrellas
          estrellas.forEach((s, i) => {
            s.classList.toggle('seleccionada', i < valor);
          });
  
          // Enviar formulario
          if (input && form) {
            input.value = valor;
            setTimeout(() => {
              form.submit();
            }, 100);
          }
        });
  
        // ⭐ Hover para previsualización
        estrella.addEventListener('mouseenter', function () {
          estrellas.forEach((s, i) => {
            s.classList.toggle('seleccionada', i <= index);
          });
        });
  
        // ❌ Quitar visualización al salir del área
        estrellasDiv.addEventListener('mouseleave', function () {
          const valorGuardado = parseInt(input.value || "0");
          estrellas.forEach((s, i) => {
            s.classList.toggle('seleccionada', i < valorGuardado);
          });
        });
      });
    });
  });