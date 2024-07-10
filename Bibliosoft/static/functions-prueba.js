
$(function() {

    $.ajax({
        url:'/categoria/data',
        type: 'GET',
        success: function(response){
            console.log(response);
            new DataTable('#dataUser', {
                "data":response['datos'],
                "columns": [
                    {"data":response[0]},
                    {"data":response[1]},
                    {"data":response[2]},
                    {"data":response[3]},
                    {"data":response[4]},
                    {"data":response[5]},
                    {"data":response[6]},
                    {"data":response[7]},
                    {"data":response[8]},
                    {"data":response[9]},
                    {"data":response[10]},
                    {"data":response[11]},
                    {"data":response[12]},
                    {"data":response[13]},

                ],
                // processing: true,
                // serverSide: true,
                language:{
                    url:  '//cdn.datatables.net/plug-ins/2.0.2/i18n/es-MX.json'
                },
                info: true,
                ordering: true,
                paging: true,
                responsive: true,
                // select: true,
                // serverSide: true,
                // buttons: [
                //     'copy', 'excel', 'pdf'
                // ],
                layout: {
                    top1Start: {
                        buttons: [
  
                            {
                                extend: 'collection',
                                buttons: ['copy', 'excel', 'csv', 'pdf','print']
                            },
                            // { extend: 'create', editor: editor },
                            // { extend: 'edit', editor: editor },
                            // { extend: 'remove', editor: editor }
                        ]
                    },
                    // top: 'searchBuilder',
                    // topStart: {
                    //     buttons: [
                    //         { extend: 'create', editor: editor },
                    //         { extend: 'edit', editor: editor },
                    //         { extend: 'remove', editor: editor }
                    //     ]
                    // }
                },

            });



        }
    });
})
