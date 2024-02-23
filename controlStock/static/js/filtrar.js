// filtrar.js

document.addEventListener('DOMContentLoaded', function() {
    // Asociar la función de confirmar borrado al botón correspondiente
    document.getElementById('confirmarBorrado').addEventListener('click', function() {
        // Redirigir a la vista que borra todos los productos
        window.location.href = "{% url 'borrar_todos_productos' %}";
    });

    // Obtener referencia al cuadro de búsqueda y la tabla
    var cuadroBusqueda = document.getElementById('cuadro-busqueda');
    var tablaRegistros = document.getElementById('tabla-registros');

    // Escuchar el evento de entrada en el cuadro de búsqueda
    cuadroBusqueda.addEventListener('input', function() {
        var filtro = cuadroBusqueda.value.toLowerCase();
        var filas = tablaRegistros.getElementsByTagName('tr');

        // Iterar sobre las filas y mostrar/ocultar según el filtro
        for (var i = 1; i < filas.length; i++) {
            var textoFila = filas[i].textContent || filas[i].innerText;
            var coincide = textoFila.toLowerCase().indexOf(filtro) > -1;
            filas[i].style.display = coincide ? '' : 'none';
        }
    });
});
