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
            {'data': 'date_calibration'},
            {'data': 'equipment'},
            {'data': 'calibration_made_by'},
            {'data': 'date_calibration_next'},
            {'data': 'calibration_certificate'},
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
                className: 'td-actions text-center',
                orderable: false,
                render: function (data, type, row) {
                    let type_doc = '';
                    let anexos = row['calibration_certificate'];
                        if (anexos !== '') {
                            let ext = anexos.split(".")[1];
                            switch (ext) {
                                case "docx":
                                    type_doc = '><i class="material-icons btn-xs" style="color:#425CF0">description</i>';
                                    break;
                                case "doc":
                                    type_doc = '><i class="material-icons" style="color:#425CF0">description</i>';
                                    break;
                                case "xlsx":
                                    type_doc = '><i class="material-icons" style="color:#008000">description</i>';
                                    break;
                                case "xls":
                                    type_doc = '><i class="material-icons" style="color:#008000">description</i>';
                                    break;
                                case "pdf":
                                    type_doc = '><i class="material-icons" style="color:#e9322d">picture_as_pdf</i>';
                                    break;
                                case "ppt":
                                    type_doc = '><i class="material-icons" style="color:#E74C3C">description</i>';
                                    break;
                                case "pptx":
                                    type_doc = '><i class="material-icons" style="color:#E74C3C">description</i>';
                                    break;
                                case "zip":
                                    type_doc = '><i class="material-icons" style="color:#F1C40F">folder_zip</i>';
                                    break;
                                case "rar":
                                    type_doc = '><i class="material-icons" style="color:#F1C40F">folder_zip</i>';
                                    break;
                                case "jpg":
                                    type_doc = '><i class="material-icons">image</i>';
                                    break;
                                case "png":
                                    type_doc = '><i class="material-icons">image</i>';
                                    break;
                                case "svg":
                                    type_doc = '><i class="material-icons">image</i>';
                                    break;
                            }
                        }
                    if (type_doc !== '') {
                        return '<a title="Descargar Certificado" type="button" target="_blank" href="/calibration/certificate?id=' + row.id + '&type=calibration_certificate" ' + type_doc;
                    }
                }
            },
            {
                targets: [5],
                class: 'td-actions text-center',
                orderable: false,
                render: function (data, type, row) {
                    let edition
                    edition = '<a title="Observaciones Calibración" onclick=open_modal_two("/calibration/detail/' + row.id + '/") type="button" rel="tooltip" class="btn btn-warning btn-xs btn-just-icon btn-simple"><i class="material-icons btn-xs">dvr</i</a>';
                    edition += '<a title="Editar Registro" href="/calibration/update/' + row.id + '/" type="button" rel="tooltip" class="btn btn-info btn-xs btn-just-icon btn-simple"><i class="material-icons">edit</i</a>';
                    return edition;
                }
            },
        ],
        initComplete: function (settings, json) {
        }
    });
});