$(function () {
    $('#datatable').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
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
            {'data': 'code'},
            {'data': 'description'},
            {'data': 'serial'},
            {'data': 'fix_active'},
            {'data': 'status'},
            {'data': 'id'},
        ],
        columnDefs: [
            {
                targets: [0, 1, 2, 3],
                class: 'td-actions text-center'
            },
            {
                targets: [4],
                className: 'td-actions text-center',
                render: function (data, type, row) {
                    let estado = null
                    switch (row['status']) {
                        case true:
                            estado = 'Activo'
                            break;
                        case false:
                            estado = 'Inactivo'
                            break;
                    }
                    return estado;
                }
            },
            {
                targets: [5],
                class: 'td-actions text-center',
                orderable: false,
                render: function (data, type, row) {
                    let edition
                    edition = '<a href="/traceability/detail/' + row.id + '/" type="button" rel="tooltip" class="btn btn-warning btn-xs btn-just-icon btn-simple"><i class="material-icons">dvr</i</a>';
                    edition += '<a href="/equipment/update/' + row.id + '/" type="button" rel="tooltip" class="btn btn-info btn-xs btn-just-icon btn-simple"><i class="material-icons">edit</i</a>';
                    return edition;
                }
            },
        ],
        initComplete: function (settings, json) {
        }
    });
});