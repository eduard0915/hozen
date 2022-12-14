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
            {'data': 'description'},
            {'data': 'mark'},
            {'data': 'model'},
            {'data': 'maker'},
            {'data': 'id'},
        ],
        columnDefs: [
            {
                targets: [0, 1, 2, 3],
                class: 'td-actions text-center'
            },
            {
                targets: [4],
                class: 'td-actions text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<a title="Editar" onclick=open_modal_two("/equipment/mark_model/update/' + row.id + '/") type="button" rel="tooltip" class="btn btn-info btn-xs btn-just-icon btn-simple"><i class="material-icons">edit</i></a>';
                }
            },
        ],
        initComplete: function (settings, json) {
        }
    });
});