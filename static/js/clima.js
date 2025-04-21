document.addEventListener("DOMContentLoaded", function () {
    const ciudadSpan = document.getElementById('clima-ciudad');
    const climaSpan = document.getElementById('clima');
  
    if (!ciudadSpan || !climaSpan) return;
  
    function mostrarClima(ciudad, lat, lon) {
      fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true`)
        .then(res => res.json())
        .then(data => {
          const temp = data.current_weather.temperature;
          ciudadSpan.textContent = `🌡️ ${ciudad}`;
          climaSpan.textContent = `${temp}°C`;
        })
        .catch(error => {
          ciudadSpan.textContent = '🌤️';
          climaSpan.textContent = 'No disp.';
          console.error('Error al obtener clima:', error);
        });
    }
  
    fetch("https://ipinfo.io/json?token=bdc0e1a20f8c63")
      .then(res => res.json())
      .then(loc => {
        if (loc && loc.loc && loc.city) {
          const [lat, lon] = loc.loc.split(',');
          const ciudad = loc.city;
          mostrarClima(ciudad, lat, lon);
        } else {
          console.warn("🌐 IP info no disponible, usando fallback.");
          mostrarClima("Santiago", -33.4489, -70.6693);
        }
      })
      .catch(error => {
        console.error('Error al obtener ubicación IP:', error);
        mostrarClima("Santiago", -33.4489, -70.6693);
      });
  });