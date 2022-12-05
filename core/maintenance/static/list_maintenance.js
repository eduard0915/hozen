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
            {'data': 'maintenance_number'},
            {'data': 'equipment'},
            {'data': 'date_maintenance'},
            {'data': 'maintenance_type'},
            {'data': 'made_by'},
            {'data': 'id'},
        ],
        columnDefs: [
            {
                targets: [0, 2, 3],
                class: 'td-actions text-center'
            },
            {
                targets: [1],
                class: 'td-actions text-center',
                orderable: false,
                render: function (data, type, row) {
                    return row['equipment__code'] + ' ' + row['equipment__description'] + ', serial: ' + row['equipment__serial']
                }
            },
            {
                targets: [4],
                class: 'td-actions text-center',
                orderable: false,
                render: function (data, type, row) {
                    return row['made_by__first_name'] + ' ' + row['made_by__last_name'] + ', ' + row['made_by__cargo']
                }
            },
            {
                targets: [5],
                class: 'td-actions text-center',
                orderable: false,
                render: function (data, type, row) {
                    let edition
                    edition = '<a href="/equipment/detail/' + row.id + '/" type="button" rel="tooltip" class="btn btn-warning btn-xs btn-just-icon btn-simple"><i class="material-icons">dvr</i</a>';
                    edition += '<a href="/equipment/update/' + row.id + '/" type="button" rel="tooltip" class="btn btn-info btn-xs btn-just-icon btn-simple"><i class="material-icons">edit</i</a>';
                    return edition;
                }
            },
        ],
        initComplete: function (settings, json) {
        }
    });
});