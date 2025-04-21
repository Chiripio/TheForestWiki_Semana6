document.addEventListener('DOMContentLoaded', function () {
    const carrusel = document.querySelector('.carousel');
    if (!carrusel) return;
  
    let isDragging = false;
    let startX = 0;
  
    const glider = new Glider(carrusel, {
      slidesToShow: 8,
      slidesToScroll: 1,
      draggable: true,
      dots: '.indicadores',
      arrows: {
        prev: '#flecha-izquierda',
        next: '#flecha-derecha'
      },
      responsive: [
        { breakpoint: 1024, settings: { slidesToShow: 8, slidesToScroll: 1 }},
        { breakpoint: 768,  settings: { slidesToShow: 3, slidesToScroll: 1 }},
        { breakpoint: 480,  settings: { slidesToShow: 2, slidesToScroll: 1 }}
      ]
    });
  
    // Evento de inicio (mouse/touch)
    carrusel.addEventListener('mousedown', e => {
      isDragging = false;
      startX = e.clientX;
    });
  
    carrusel.addEventListener('mousemove', e => {
      if (Math.abs(e.clientX - startX) > 5) isDragging = true;
    });
  
    carrusel.addEventListener('mouseup', () => {
      setTimeout(() => isDragging = false, 50);
    });
  
    carrusel.addEventListener('touchstart', e => {
      isDragging = false;
      startX = e.touches[0].clientX;
    });
  
    carrusel.addEventListener('touchmove', e => {
      if (Math.abs(e.touches[0].clientX - startX) > 5) isDragging = true;
    });
  
    carrusel.addEventListener('touchend', () => {
      setTimeout(() => isDragging = false, 50);
    });
  
    // Corrección final: forzar navegación solo si NO hubo arrastre
    document.querySelectorAll('.pelicula a').forEach(link => {
      link.addEventListener('click', function (e) {
        e.preventDefault(); // Evitamos comportamiento automático SIEMPRE
        if (!isDragging) {
          const destino = this.getAttribute('href');
          console.log("✅ Redirigiendo a:", destino);
          window.location.href = destino; // Forzamos navegación
        } else {
          console.log("🚫 Clic bloqueado por arrastre");
        }
      });
    });
  
    console.log("✅ Glider cargado y eventos listos");
  });