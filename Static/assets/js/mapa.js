// Función para cargar mediciones desde la base de datos
function cargarMedicionesDesdeDB() {
    $.ajax({
      url: '/obtener_mediciones', // Ruta local en tu aplicación Flask
      method: 'GET',
      dataType: 'json',
      success: function(data) {
        data.forEach(function(medicion) {
          var latitud = parseFloat(medicion.puntodemed);
          var longitud = parseFloat(medicion.medicion);
          var informacion = `Fecha Tomada: ${medicion.fecha_tomada}<br>Usuario ID: ${medicion.usuario_id}<br>ID Lugar: ${medicion.id_lugar}`;
  
          var medicionMarker = L.marker([latitud, longitud]).addTo(map);
          medicionMarker.bindPopup(informacion);
        });
      },
      error: function(error) {
        console.log('Error al cargar mediciones desde la base de datos: ' + error);
      }
    });
  }
  
  cargarMedicionesDesdeDB();
  