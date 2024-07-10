
$(function() {

    $.ajax({
        url:'/prestamo/data',
        type: 'GET',
        success: function(response){
            console.log(response);
            const table = new DataTable('#dataPrestamo', {
                "data":response['datos'],
                "columns": [
                    {"data":response[0]},
                    {"data":response[1]},
                    {"data":response[2]},
                    {"data":response[3]},
                    {"data":response[4]},
                    {"data":response[5]},

                ],
                // processing: true,
                language:{
                    url:  'https://cdn.datatables.net/plug-ins/2.0.3/i18n/es-MX.json'
                },
                info: true,
                ordering: true,
                paging: true,
                select: true,
                responsive: true,
                layout: {
                    top1Start: {
                        buttons: [
                            {
                                extend: 'collection',
                                buttons: ['copy', 'excel', 'csv', 'pdf','print']
                            },
                        ]
                    },
                },

            });
            //*SELECT
            $('#dataPrestamo tbody').on('click','tr', function() {
                var rowIndex = table.row(this).index();
                var idRow = $('#dataPrestamo').DataTable().cell(rowIndex,0).data();
                var detalleBtn = document.getElementById('detalleBtn');
                detalleBtn.className = idRow;

                console.log("EL id seleccionado es: "+idRow);
            });

        }
    });
})


//*CREATE

var modal = document.getElementById('create');
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}


$("#formulario").submit(function(event) {
    event.preventDefault();

    var nombre = $("#afiliado").val();
    var numeroSerie = $("#numeroSerie").val();
    var estado = $("#estado").val();
    var fechaEntrega = $("#fechaEntrega").val();


    $.ajax({
      url: "/prestamo/nuevoprestamo",
      type: "post",
      data: {
        nombre: nombre,
        numeroSerie: numeroSerie,
        estado: estado,
        fechaEntrega: fechaEntrega,

      },
      success: function(response) {
        alert(response);
      }
    });
});

//*Detalle prestamo
var detalleBtn = document.getElementById('detalleBtn');
detalleBtn.addEventListener("click", function() {
    console.log('detalleBtn');

    const modal = document.getElementById('detalle');
    const id = detalleBtn.className;
    if(!id){
        alert('Selecciona una fila')
        modal.style.display = 'nona'
        return;
    }else {
        modal.style.display = 'block'
        select = document.getElementById('tpDatos');
        select.innerHTML = ''
        console.log(id);
        $.ajax({
            url:'/prestamo/detalle/'+id,
            type: 'POST',
            success: function(response){
                dato = response['datos'];
                console.log(dato[0].length);

                select.style.display = "flex";
                select.style="--bs-columns: 2;";

                for (var i = 0; i < dato.length; i++) {
                    var divCard = document.createElement('div');
                    divCard.className = 'card';

                    if (dato[i] !== undefined) {
                        var divBody = document.createElement('div');
                        divBody.className = 'card-body'

                        for (var j = 0; j < dato[i].length; j++) {
                            var parrafo = document.createElement('p');
                            parrafo.className = 'card-text'

                            parrafo.textContent = dato[i][j];
                            console.log(dato[i][j]);
                            divBody.appendChild(parrafo);
                        }
                    }
                    divCard.appendChild(divBody)
                    select.appendChild(divCard)

                }

            },
            error: function(error){
                console.log('Error: '+error);
            }
        })
    }
});



//*nuevo libro prestamo
var count = 1; // Contador para el número de libro a sacar

var addPrestamoBtn = document.getElementById('addPrestamoBtn');
addPrestamoBtn.addEventListener("click", function() {
    count++; // Incrementar el contador

    //var divLibro = document.createElement('div');
    var divCont = document.getElementById('container');

    var labelLibro = document.createElement('label');
    labelLibro.innerHTML = 'Numero del Libro'
    var nombreLibro = document.createElement('input');
    nombreLibro.type = 'text';
    nombreLibro.name = 'numeroSerie'+count;
    nombreLibro.placeholder = 'Numero de Serie'
    nombreLibro.required

    divCont.appendChild(labelLibro);
    divCont.appendChild(nombreLibro);

    var labelEstado = document.createElement('label');
    labelEstado.innerHTML = 'Estado del libro'
    var estadoLibro = document.createElement('select');
    estadoLibro.id = 'estado'+count;
    estadoLibro.name = 'estadoLibro'+count;
    estadoLibro.required;

    divCont.appendChild(labelEstado);
    divCont.appendChild(estadoLibro);

    $('#estado'+count).append('<option value="1">Perfecto estado</option>');
    $('#estado'+count).append(' <option value="2">Buen estado</option>');
    $('#estado'+count).append('<option value="3">Estado regular</option>');
    $('#estado'+count).append('<option value="4">Ligeramente dañado</option>');
    $('#estado'+count).append('<option value="5">Muy dañado</option>');

    //divCont.appendChild(divLibro);

        //$('#imagen-producto').append('<input accept="image/png" type="file" name="imgProd[]" id="imgProd' + imgCount + '">'); // Añadir el nuevo input de imagen al formulario
    // $.ajax({
    //     url: '/prestamo/add',
    //     type: 'POST',
    //     success: function(response) {

    //     },
    //     error: function(error) {
    //         console.log("Error: "+error);
    //     }
    // })
});


//********************************************* ESTATUS ENTREGADO

var EntregadoBtn = document.getElementById('EntregadoBtn');
EntregadoBtn.addEventListener("click", function() {

    const id = detalleBtn.className;
    $.ajax({
        url:'/prestamo/entregado/'+id,
        type: 'POST'
    });
});