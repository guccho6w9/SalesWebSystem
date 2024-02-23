// Mostrar fecha actual
function setearFechaActual() {
    var fecha = new Date();
    var diasSemana = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
    var nombreDia = diasSemana[fecha.getDay()];
    var dia = fecha.getDate();
    var mes = fecha.toLocaleString('default', { month: 'long' });
    var anio = fecha.getFullYear();
    var fechaFormateada = nombreDia + ', ' + dia + ' de ' + mes + ' del ' + anio;
  
    // Busca todos los elementos con ID "fecha-actual" y establece el valor
    var elementosFechaActual = document.querySelectorAll('[id^="fecha-actual"]');
    elementosFechaActual.forEach(function(elemento) {
        if (elemento.tagName === 'INPUT' || elemento.tagName === 'TEXTAREA') {
            elemento.value = fechaFormateada;
        } else {
            elemento.textContent = fechaFormateada;
        }
    });
  }
  
  // Llama a la función cuando se carga la página
  document.addEventListener('DOMContentLoaded', setearFechaActual);
  
  
  // ----------------------------------------------------
  // Esto permite visualizar los tooltips de Bootstrap
  document.addEventListener('DOMContentLoaded', function () {
    // Inicializa los tooltips de Bootstrap
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
      new bootstrap.Tooltip(tooltipTriggerEl);
    });
  });
  
  /*const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  
  if (tooltipTriggerList.length > 0) {
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
  }*/
  
  
  // ----------------------------------------------------
  // Esto permite visualizar los Modals de Bootstrap
  const myModal = document.getElementById('myModal');
  const myInput = document.getElementById('myInput');
  
  if (myModal && myInput) {
    myModal.addEventListener('shown.bs.modal', () => {
      myInput.focus();
    });
  }
  
  
  // ----------------------------------------------------
  // Deshabilita el uso de las flechas del teclado en los inputs de tipo number y no permite los valores negativos.
  function validarInputsNumber() {
    // Obtén todos los elementos input de tipo number
    var inputsNumber = document.querySelectorAll('input[type="number"]');
  
    // Itera sobre los inputs de tipo number
    inputsNumber.forEach(function(input) {
      // Agrega un listener para el evento input
      input.addEventListener('input', function() {
        // Valida si el valor es negativo
        if (input.value < 0) {
          // Si es negativo, establece el valor a 0
          input.value = 0;
        }
      });
  
      // Agrega un listener para el evento keydown para prevenir el uso de flechas
      input.addEventListener('keydown', function(e) {
        // Valida si se presionaron las flechas arriba o abajo
        if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
          // Previene el comportamiento predeterminado
          e.preventDefault();
        }
      });
    });
  }
  
  // Llama a la función al cargar la página
  validarInputsNumber();