
$(function() {

    $.ajax({
        url:'/catalogo/data',
        type: 'GET',
        success: function(response){
            console.log(response);
            const table = new DataTable('#dataUser', {
                "data":response['datos'],
                "columns": [
                    {"data":response[0]},
                    {"data":response[1]},
                    {
                        "data": response[2],
                        render: function (file_id) {
                            return file_id
                            ? `<img src="../static/imgl/${file_id}"/>`
                            : null;
                        },
                        defaultContent: 'No image',
                    },
                    {"data":response[3]},
                    {"data":response[4]},
                    {"data":response[5]},
                    {"data":response[6]},
                    {"data":response[7]},
                    {"data":response[8]},
                    {"data":response[9]},
                ],
                // processing: true,
                language:{
                    url:  'https://cdn.datatables.net/plug-ins/2.0.3/i18n/es-MX.json'
                },
                scrollX: 1050,
                scrollY: 400,
                info: true,
                ordering: true,
                paging: true,
                select: true,
                responsive: true,
            });


        }
    });
})
