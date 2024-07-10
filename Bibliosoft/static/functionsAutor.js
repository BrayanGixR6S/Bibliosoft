
$(function() {

    $.ajax({
        url:'/libro/autor/data',
        type: 'GET',
        success: function(response){
            console.log(response);
            const table = new DataTable('#dataAutor', {
                "data":response['datos'],
                "columns": [
                    {"data":response[0]},
                    {"data":response[1]},
                    {"data":response[2]},

                ],
                // processing: true,
                language:{
                    url:  'https://cdn.datatables.net/plug-ins/2.0.3/i18n/es-MX.json'
                },
                scrollX: 1050,
                scrollY: 300,
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
            $('#dataAutor tbody').on('click','tr', function() {
                var rowIndex = table.row(this).index();
                var idRow = $('#dataAutor').DataTable().cell(rowIndex,0).data();
                var btnDelete = document.getElementById('delete');
                var btnUpdate = document.getElementById('updateBtn');

                btnDelete.className = idRow;
                btnUpdate.className = idRow;

                console.log("EL id seleccionado es: "+idRow);
            });

        }
    });
})

//*DELETE
var button = document.getElementById('delete');
button.addEventListener("click", function() {
    console.log( this.className);
    var id = this.className;
    if(!id){
        alert('Selecciona una fila')
        return;
    }
    $.ajax({
        url: '/libro/autor/delete/'+id,
        type: 'POST',
        success: function(response){
            console.log(response);
            location.reload();

        },
        error: function(error){
            console.log(error);
        }
    });
});

//*CREATE

var modal = document.getElementById('create');
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}


$("#formulario").submit(function(event) {
    event.preventDefault();

    var nombre = $("#nombre").val();

    $.ajax({
      url: "/libro/autor/create",
      type: "post",
      data: {
        nombre: nombre,
      },
      success: function(response) {
        alert(response);
      }
    });
});

//*Update
var updateBtn = document.getElementById('updateBtn');
updateBtn.addEventListener("click", function() {
    console.log('updateBtn');

    const modal = document.getElementById('update');
    const id = updateBtn.className;
    if(!id){
        alert('Selecciona una fila')
        modal.style.display = 'nona'
        return;
    }else {
        modal.style.display = 'block'
        $.ajax({
            url:'/libro/autor/update/'+id,
            type: 'POST',
            success: function(response){
                dato = response['datos'][0];
                // console.log(dato);
                document.getElementById("nombreUp").value = dato[1]
                document.getElementById("estatusUp").value = dato[2]
            },
            error: function(error){
                console.log('Error: '+error);
            }
        })
    }
});


$("#updateForm").submit(function(event) {
    event.preventDefault();

    var btnUpdate = document.getElementById('updateForm');//updatebtn
    var btnUpdate = document.getElementById('updateBtn');
    var idRow = btnUpdate.className;


    console.log( btnUpdate);


    var nombre = $("#nombreUp").val();
    var estatus = $("#estatusUp").val();


    $.ajax({
        url: "/libro/autor/update/"+idRow+"/",
        type: "post",
        data: {
            nombre: nombre,
            estatus: estatus,
        },
        success: function(response) {
            location.reload();

        }
      });
});