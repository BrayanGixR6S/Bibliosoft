
$(function() {

    $.ajax({
        url:'/usuarios/data',
        type: 'GET',
        success: function(response){
            console.log(response);
            const table = new DataTable('#dataUser', {
                "data":response['datos'],
                "columns": [
                    {"data":response[0]},
                    {"data":response[1]},
                    {"data":response[2]},
                    {"data":response[3]},
                    {"data":response[4]},
                    // {"data":response[5]},//password
                    {"data":response[5]},
                    {"data":response[6]},
                    {"data":response[7]},
                    {"data":response[8]},
                    {"data":response[9]}

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
            $('#dataUser tbody').on('click','tr', function() {
                var rowIndex = table.row(this).index();
                var idRow = $('#dataUser').DataTable().cell(rowIndex,0).data();
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
        url: '/usuarios/delete/'+id,
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
    var username = $("#username").val();
    var fechanaci = $("#fechanaci").val();
    var curp = $("#curp").val();
    var psw = $("#psw").val();
    var telefono = $("#telefono").val();
    var correo = $("#correo").val();
    var genero = $("#genero").val();
    var perfil = $("#perfil").val();

    $.ajax({
      url: "/usuarios",
      type: "post",
      data: {
        nombre: nombre,
        username: username,
        fechanaci: fechanaci,
        curp: curp,
        psw: psw,
        telefono: telefono,
        correo: correo,
        genero: genero,
        perfil: perfil,


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
            url:'/usuarios/update/'+id,
            type: 'POST',
            success: function(response){
                dato = response['datos'][0];
                // console.log(dato);
                document.getElementById("nombreUp").value = dato[1]
                document.getElementById("userNameUp").value = dato[2]
                document.getElementById("fechanaciUp").value = dato[3]
                document.getElementById("curpUp").value = dato[4]
                //document.getElementById("pswUp").value = dato[5]
                document.getElementById("telefonoUp").value = dato[6]
                document.getElementById("correoUp").value = dato[7]
                document.getElementById("generoUp").value = dato[8]
                document.getElementById("perfilUp").value = dato[9]
                // var genero = dato[11]

                // select = document.getElementById('genero');
                // const dataGen = ['Masculino','Femenino','Otro']
                // for(var i =0; i<=2; i++){
                //     var opt = document.createElement('option')
                //     opt.value = i
                //     opt.innerHTML = dataGen[i]
                //     if(genero == (i+1)){
                //         select.selectedIndex = i
                //     }
                //     select.appendChild(opt);
                // }
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
    var username = $("#userNameUp").val();
    var fechanaci = $("#fechanaciUp").val();
    var curp = $("#curpUp").val();
    var telefono = $("#telefonoUp").val();
    var correo = $("#correoUp").val();
    var genero = $("#generoUp").val();
    var perfil = $("#perfilUp").val();


    $.ajax({
        url: "/usuarios/update/"+idRow+"/",
        type: "post",
        data: {
            nombre: nombre,
            username: username,
            fechanaci: fechanaci,
            curp: curp,
            telefono: telefono,
            correo: correo,
            genero: genero,
            perfil: perfil,
        },
        success: function(response) {
            // console.log(response);
            location.reload();


        }
      });
});