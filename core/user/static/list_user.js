$(function () {
    $('#datatable').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        order: [[ 5, "desc" ]],
        language: {
            url: "//cdn.datatables.net/plug-ins/1.10.21/i18n/Spanish.json"
        },
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {'data': 'first_name'},
            {'data': 'username'},
            {'data': 'cargo'},
            {'data': 'groups__name'},
            {'data': 'email'},
            {'data': 'is_active'},
            {'data': 'id'},
        ],
        columnDefs: [
            {
                targets: [1, 2, 3, 4],
                class: 'td-actions text-center'
            },
            {
                targets: [0],
                class: 'td-actions text-center',
                orderable: false,
                render: function (data, type, row) {
                    return row['first_name'] + ' ' + row['last_name']
                }
            },
            {
                targets: [5],
                className: 'td-actions text-center',
                render: function (data, type, row) {
                    let estado = null
                    switch (row['is_active']) {
                        case true:
                            estado = '<span style="font-weight: bold; color: #1b5e20">Activo</span>'
                            break;
                        case false:
                            estado = '<span style="font-weight: bold; color:#e52d27">Inactivo</span>'
                            break;
                    }
                    return estado;
                }
            },
            {
                targets: [6],
                class: 'td-actions text-center',
                orderable: false,
                render: function (data, type, row) {
                    let edition
                    edition = '<a title="Perfil de Usuario" href="/user/detail/' + row.id + '/" type="button" rel="tooltip" class="btn btn-warning btn-xs btn-just-icon btn-simple"><i class="material-icons">dvr</i</a>';
                    edition += '<a title="Editar Usuario" href="/user/update/' + row.id + '/" type="button" rel="tooltip" class="btn btn-info btn-xs btn-just-icon btn-simple"><i class="material-icons">edit</i</a>';
                    edition += '<a title="Inactivar" href="/user/update/' + row.id + '/" type="button" rel="tooltip" class="btn btn-danger btn-xs btn-just-icon btn-simple"><i class="material-icons">person_off</i</a>';
                    edition += '<a title="Resetear Contraseña" href="/user/update/' + row.id + '/" type="button" rel="tooltip" class="btn btn-warning btn-xs btn-just-icon btn-simple"><i class="material-icons">password</i</a>';
                    return edition;
                }
            },
        ],
        initComplete: function (settings, json) {
        }
    });
});