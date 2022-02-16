
// ================================================
// dependencies
// ================================================

// widget.js
$("head").append($("<script></script>").attr("src", "/static/assets/js/websocket.js"))
$("head").append($("<script></script>").attr("src", "/static/assets/js/widget.js"))
// date range picker
// $("head").append($("<script></script>").attr("src", "/static/assets/js/plugins/daterangepicker/moment.min.js")); // moment.js imported in page-report.html
$("head").append($("<script></script>").attr("src", "/static/assets/js/plugins/daterangepicker/daterangepicker.js"));
$("head").append($("<link></link>").attr({"href": "/static/assets/js/plugins/daterangepicker/daterangepicker.css", "rel": 'stylesheet'}));
// PDFObject
$("head").append($("<script></script>").attr("src", "/static/assets/js/plugins/PDFObject/pdfobject.js"));



$(document).ready(()=>{
    set_monday_start_of_week()
    date_range_init_report()
    report_table_init()
})

const baseUrl = `${window.location.protocol}//${window.location.host}/static/assets/package/dist/`;


// ======================================================================================================
// event listeners
// ======================================================================================================

// export report
$('#report-table-export').click(()=>{
    var data = table.rows({selected: true}).data()
    var report_list=[]
    for (var i=0; i < data.length ;i++){
        report_list.push(data[i]['file_name'])
     }
    if (report_list[0]){
        var data = {
            'message': report_list,
            'message_type': 'request export',
        }
        websocket_send(data)
        $('.loading-overlay').show()
        $('.loading-overlay').addClass('show')
    }
    else{
        message = {
            title: '',
            text: 'Select a report to export.',
            button_text: 'report export',
            process_name: 'report export',
            wait_for_acknowledge: false,
        }
        load_prompt(message)
    }
})


// preview report
$('#report-table-preview').click(()=>{
    var data = table.rows({selected: true}).data()
    var report_list=[]
    for (var i=0; i < data.length ;i++){
        report_list.push(data[i]['file_name'])
    }
    if (report_list[0]){
        load_report_pdf(report_list[0])
        $('#report-preview-modal .modal-title').text(report_list[0])
        $('#report-preview-modal').modal('show')
    }
    else {
        $('#pdf-preview-container').html($('<p style="    margin-top: 20vh;">Select a report for preview.</p>'))
        message = {
            title: '',
            text: 'Select a report for preview.',
            button_text: 'report preview',
            process_name: 'report preview',
            wait_for_acknowledge: false,
        }
        load_prompt(message)
    }
})


// delete report
$('#report-table-delete').click(()=>{
    var data = table.rows({selected: true}).data()
    var report_list=[]
    for (var i=0; i < data.length ;i++){
        report_list.push(data[i]['file_name'])
    }
    if (report_list[0]){
        $('#report-delete-form #report-delete-file-name').val(report_list[0])
        $('#report-delete-file-name-confirm').html(report_list[0])

        $('#report-delete-modal').modal('show')
    }
    else {
        message = {
            title: '',
            text: 'Select a report to delete.',
            button_text: 'report delete',
            process_name: 'report delete',
            wait_for_acknowledge: false,
        }
        load_prompt(message)
    }
})

$('#report-delete-form').submit((e)=>{
    e.preventDefault()
    $('.loading-overlay').show()
    $('.loading-overlay').addClass('show')
    var data = {
        'message':{
            'file_name': $('#report-delete-file-name').val(),
        },
        'message_type': 'delete report',
    }
    websocket_send(data)
})


// edit report
$('#report-edit-button').click(()=>{
    report_type = $('#report-preview-modal .modal-title').text().split('_')
    report_type.splice(-1,1)
    report_type = report_type.join(' ')
    load_report_edit_fields(report_type, $('#report-preview-modal .modal-title').text())
    $('#report-edit-modal').modal('show')
    
})

$('#report-edit-form').submit((e)=>{
    e.preventDefault()
    $('.loading-overlay').show()
    $('.loading-overlay').addClass('show')
    var $inputs = $('#report-edit-form :input').not(':input[type=submit]')
    var values = []
    $inputs.each(function() {
        var variable = this.id.split('_')[0].replace(/-/g, ' ')
        values.push({'variable': variable, 'value': $(this).val()})
    })
    var data = {
        'message':{
            'variable_list': values,
        },
        'message_type': 'edit report',
    }
    websocket_send(data)
})


// date range selector
$('.date-range-picker').on('apply.daterangepicker', function(ev, picker){
    $('.date-range-picker-start-date').val(picker.startDate.format('YYYY/MM/DD'))
    $('.date-range-picker-end-date').val(picker.endDate.format('YYYY/MM/DD'))
    table.ajax.reload()
})


// // select all check box
// $('.report-table-select-col').click(()=>{
//     checkbox = $('#report-table-select-all-checkbox')
//     checkbox.prop("checked", !checkbox.prop("checked"))
//     if (checkbox.prop('checked') == true) {
//         table.rows().select()
//     }
//     else {
//         table.rows().deselect()
//     }
// })

// ======================================================================================================
// functions
// ======================================================================================================
function load_report_edit_fields(report_type, file_name){
    if (report_type== 'pre production'){
        field = [
            'lot or drum number', 
            'pre operation n2 pallet pressure', 
            'pre operation 2nd n2 pallet pressure', 
            'after operation n2 pallet pressure', 
            'after operation 2nd n2 pallet pressure',
            'vacuum pump',
            'weighing balance serial no',
            'empty 220L drum',
            'filled 220L drum with HTPB, Treated',
            'amount of HTPB, Treated collected',
        ]
    }
    else if (report_type == 'production'){
        field = [
            'lot or drum number', 
            'vacuum pressure serial no', 
            'vessel temp serial no', 
            'heater set serial no', 
            'nitrogen flow serial no', 
        ]
    }
    else if (report_type == 'post production'){
        field = [
            'day 1 cleaning temp set point',
            'day 2 cleaning temp set point',
            'day 3 drying temp set point',
        ]
    }
    $('#report-edit-modal .modal-body-error').html('')
    $('#report-edit-modal #report-edit-modal-title').html('').append(report_type.toUpperCase())
    $input = $(`<input id="edit-report-name" value="${file_name}" hidden>`)
    $('#report-edit-form').html('').append($input)
    $.each(field, (index, value)=>{
        $input = $(`
        <div class="input-group mb-3">
            <div class="input-group-prepend">
            <label class="input-group-text text-dark">${value}</label>
            </div>
            <input type='text' pattern="[a-zA-Z0-9\s]+" title="Alphanumeric characters only." class="form-control" id="${value.replace(/ /g,"-")}" value>
        </div>`)
        $('#report-edit-form').append($input)
    })
}


function load_report_pdf(file_name){
    var options = {
        height: "100%",
        page: '1',
        pdfOpenParams: {
            view: 'FitV',
            pagemode: 'thumbs',
        }
    }
    PDFObject.embed("/static/assets/reports/"+file_name+".pdf#toolbar=0", "#pdf-preview-container")
}

function set_monday_start_of_week(){
    moment.updateLocale('en', {
        week: {
        dow : 1, // Monday is the first day of the week.
        }
    })
}

function date_range_init_report(){
    $('.date-range-picker').daterangepicker({
        opens: 'right',
        // singleDatePicker: true,
        showDropdowns: true,
        startDate: moment().startOf('week'),
        endDate: moment().endOf('week'),
        locale: { 
            format: 'DD MMM YYYY'
        }
    })
    $('.date-range-picker-start-date').val($('.date-range-picker').data('daterangepicker').startDate.format('YYYY/MM/DD'))
    $('.date-range-picker-end-date').val($('.date-range-picker').data('daterangepicker').endDate.format('YYYY/MM/DD'))
}


function report_table_init(){
    
    $.fn.dataTable.moment('DD MMM YYYY - hh:mm A');
    
    table = $('.table').DataTable({
        bInfo : false,
        bLengthChange: false,
        bPaginate: false,
        responsive: true,
        autoWidth: false,
        scrollY: "500px",
        order: [[ 1, 'desc' ]],
        select: {
            style:    'single',
            selector: 'td'
        },
        ajax:  {
            'url': "report/",
            "type": "GET",
            'dataSrc': "", 
            'data': {
                'mode' : 'get reports',
                'start_date' : ()=> {return $('.date-range-picker-start-date').val()},
                'end_date' : ()=> {return $('.date-range-picker-end-date').val()}
            }
        },
        columns: [
            { 'data': "file_name" },
            { 'data': "time_completed" },
        ],
        language: {
            "emptyTable": "No report found"
        }
    });
    table.columns.adjust()
}

