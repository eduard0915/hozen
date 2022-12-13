$(function () {
    $('#datatable').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        order: [[ 4, "desc" ]],
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
            {'data': 'description_equipment__description'},
            {'data': 'serial'},
            {'data': 'fix_active'},
            {'data': 'status'},
            {'data': 'id'},
        ],
        columnDefs: [
            {
                targets: [0],
                className: 'td-actions text-center',
                render: function (data, type, row) {
                    return row['description_equipment__description'] + ' ' + row['description_equipment__mark'] + '/' + row['description_equipment__model'];
                }
            },
            {
                targets: [1, 2],
                class: 'td-actions text-center'
            },
            {
                targets: [3],
                className: 'td-actions text-center',
                render: function (data, type, row) {
                    let estado = null
                    switch (row['status']) {
                        case true:
                            estado = 'En Servicio'
                            break;
                        case false:
                            estado = '<span class="badge" style="background-color: #e52d27">Fuera de Servicio</span>'
                            break;
                    }
                    return estado;
                }
            },
            {
                targets: [4],
                class: 'td-actions text-center',
                orderable: false,
                render: function (data, type, row) {
                    let edition
                    edition = '<a title="Hoja de Vida" href="/equipment/detail/' + row.id + '/" type="button" rel="tooltip" class="btn btn-warning btn-xs btn-just-icon btn-simple"><i class="material-icons">dvr</i></a>';
                    edition += '<a title="Editar" href="/equipment/update/' + row.id + '/" type="button" rel="tooltip" class="btn btn-info btn-xs btn-just-icon btn-simple"><i class="material-icons">edit</i></a>';
                    if (row['status'] === true){
                        edition += '<a title="Fuera de Servicio" onclick=open_modal("/equipment/inactive/' + row.id + '/") type="button" rel="tooltip" class="btn btn-danger btn-xs btn-just-icon btn-simple"><i class="material-icons">power_settings_new</i></a>';
                    } else {
                        edition += '<a title="En Servicio" onclick=open_modal("/equipment/active/' + row.id + '/") type="button" rel="tooltip" class="btn btn-success btn-xs btn-just-icon btn-simple"><i class="material-icons">power_settings_new</i></a>';
                    }
                    return edition;
                }
            },
        ],
        initComplete: function (settings, json) {
        }
    });
});