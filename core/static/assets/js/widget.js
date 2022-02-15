
// ================================================
// imports
// ================================================

// gridstack
$("head").append($("<script></script>").attr("src", "/static/assets/js/plugins/gridstack/dist/gridstack-h5.js"));

$("head").append($("<link></link>").attr({"href": "/static/assets/js/plugins/gridstack/dist/gridstack.min.css", "rel": 'stylesheet'}));
$("head").append($("<link></link>").attr({"href": "/static/assets/js/plugins/gridstack/dist/gridstack-64col.css", "rel": 'stylesheet'}));
    
// datatables
$("head").append($("<script></script>").attr("src", "/static/assets/js/plugins/DataTables/datatables.js"));

$("head").append($("<link></link>").attr({"href": "/static/assets/js/plugins/DataTables/datatables.css", "rel": 'stylesheet'}));

// jquery knob gauge
$("head").append($("<script></script>").attr("src", "/static/assets/js/plugins/jquery-knob/dist/jquery.knob.min.js"));

// ChartJS
$("head").append($("<script></script>").attr("src", "/static/assets/js/plugins/chart.js/dist/Chart_v3.5.1.min.js"));
// $("head").append($("<script></script>").attr("src", "/static/assets/js/plugins/chart.js/dist/Chart.extension.js"));
// chartjs time adapter
$("head").append($("<script></script>").attr("src", "/static/assets/js/plugins/chart.js/dist/Chart_adapter_date_fns_v2.0.0.js"));
// zoom enabled plugin
$("head").append($("<script></script>").attr("src", "/static/assets/js/plugins/hammer-js/hammer-v2.0.8.js"));
$("head").append($("<script></script>").attr("src", "/static/assets/js/plugins/chart.js/dist/chartjs-plugin-zoom.min.js"));

// Google Maps
// $("head").append($("<script></script>").attr("src", "https://maps.googleapis.com/maps/api/js?key=YOUR_KEY_HERE"));

// datepicker
$("head").append($("<script></script>").attr("src", "/static/assets/js/plugins/bootstrap-datepicker/dist/js/bootstrap-datepicker.min.js"));

// date range picker
$("head").append($("<script></script>").attr("src", "/static/assets/js/plugins/daterangepicker/moment.min.js"));
$("head").append($("<script></script>").attr("src", "/static/assets/js/plugins/daterangepicker/daterangepicker.js"));
$("head").append($("<link></link>").attr({"href": "/static/assets/js/plugins/daterangepicker/daterangepicker.css", "rel": 'stylesheet'}));



// ======================================================================================================
// event listener
// ======================================================================================================


// widget removed event
// grid.on('removed', (e, items)=>{
//     items.forEach((item)=>{
//         widget_delete(items.id)
//     })
// })
// gridstack new widget added event
// grid.on('added', function(e, items) {
//     let str = '';
//     items.forEach(function(item) { str += ' (x,y)=' + item.x + ',' + item.y; });
// })



// ======================================================================================================
// functions
// ======================================================================================================


// widget layout management --------------------------------------------------------------------------------

// gridstack init 
var grid = GridStack // global gridstack variable
function init_gridstack(){
    grid = GridStack.init({
        column: 64,
        cellHeight: 10,
        acceptWidgets: true,
        dragIn: '.newWidget',  // class that can be dragged from outside
        dragInOptions: { revert: 'invalid', scroll: false, appendTo: 'body', helper: 'clone' }, // clone or can be your function
        removable: '#trash', // drag-out delete class
        // alwaysShowResizeHandle: /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) // resize handle for mobile
    });
}


// save widget layout
function save_widget_layout(){
    var widgets = [];
    $('.grid-stack-item').each(function () {
        widgets.push({
            gs_x: $(this).attr('gs-x'),
            gs_y: $(this).attr('gs-y'),
            gs_w: $(this).attr('gs-w'),
            gs_h: $(this).attr('gs-h'),
            widget_id: $(this).attr('gs-id'),
            widget_type: $(this).attr('widget-type'),
            widget_name: $(this).find('.widget-name').text(),
        });
    });
    ajax_request('widget/', 'POST', 'save layout', {widgets: JSON.stringify(widgets)}, true)
}


function disable_widget_edit(){
    grid.movable('.grid-stack-item', false)
    grid.resizable('.grid-stack-item', false)
}


function enable_widget_edit(){
    grid.movable('.grid-stack-item', true)
    grid.resizable('.grid-stack-item', true)
}


// count number of the type of widget selected
function get_widget_id_num(){
    widget_count = $('.grid-stack-item').length + 1
    var arr = $('.grid-stack-item').attrs('gs-id')
    var missing_widget_id = new Array();
    for (var i = 1; i <= widget_count; i++) {
        if (arr.indexOf(String(i)) == -1) {
            missing_widget_id.push(String(i));
        }
    }
    return missing_widget_id[0]
}


// get widget layout safe state from database
async function get_widget_save(){
    await ajax_request('widget/', 'GET', 'get layout', {}, false, true).done((data)=>{
        if (data.success){ 
            load_widget($.parseJSON(data.all_widgets))
        }
    })
    await insert_all_widget_html()
    init_new_widget()
}


// load widget
async function load_widget(layout){
    $.each(layout,async function(index, widget){ 
        var gs_x = widget['gs_x']
        var gs_y = widget['gs_y']
        var gs_w = widget['gs_w']
        var gs_h = widget['gs_h']
        var widget_id = widget['widget_id']
        var widget_type = widget['widget_type']
        var widget_name = widget['widget_name']
        await insert_new_widget(gs_x, gs_y, gs_w, gs_h, widget_type, widget_id, widget_name)
    });
}


// insert selected widget
async function insert_new_widget(gs_x, gs_y, gs_w, gs_h, widget_type, widget_id, widget_name){
    if (!widget_id) {
        var widget_id = get_widget_id_num()
    }
    grid.addWidget({x:gs_x, y:gs_y, w: gs_w, h: gs_h, id: widget_id});
    var header = '<div class="widget-name"><h6>'+widget_name+'</h6></div>'
    $('[gs-id="'+widget_id+'"]').attr('widget-type', widget_type).find('.grid-stack-item-content').html(header)
}


// insert widget html to div
async function insert_all_widget_html(){
    var widgets_type = $('.grid-stack-item').attrs('widget-type')
    await ajax_request('widget/', 'GET', 'get widget html all', {widgets_type: JSON.stringify(widgets_type)}).done((data)=>{
        if (data.success) { 
            $.each(data.widgets_html, (index, value)=>{
                $('[gs-id="'+value.widget_id+'"]').find('.grid-stack-item-content').append(value.widget_html)
                if (value.device_id != null){
                    $('[gs-id="'+value.widget_id+'"]').attr({'device-id':value.device_id, 'device-unit':value.device_unit})
                }
            }) 
        }
    })
}

// insert widget html to div
async function insert_widget_html(widget_id, widget_type, widget_name){
    await ajax_request('widget/', 'GET', 'get widget html', {widget_type: widget_type}, false).done((data)=>{
        if (data.success) { 
            var header = '<div class="widget-name"><h6>'+widget_name+'</h6></div>'
            $('[gs-id="'+widget_id+'"]').attr('widget-type', widget_type).find('.grid-stack-item-content').html(header+data.html)
        }
    })
}


// get widget default size
function get_widget_default_size(widget_type){
    if (widget_type == 'button'){
        return {gs_w: 12, gs_h: 15};
    }
    else {
        return {gs_w: 14, gs_h: 14};
    }
}


// get list of available widget type according to .html file in core/static/widget directory
function get_available_widget(){
    ajax_request('widget/', 'GET', 'get available').done((data)=>{
        if (data.success){
            load_available_widget(data.widget)
        }
    })
}


// ====================================================================================================================================
// widget inits
// ====================================================================================================================================

function init_new_widget(){
    var widget_id_arr = $('.grid-stack-item').attrs('gs-id')
    var widget_type_arr = $('.grid-stack-item').attrs('widget-type')
    $.each(widget_id_arr, (index, value)=>{
        var $widget = $('[gs-id="'+value+'"]')
        var widget_type = widget_type_arr[index]
        if (widget_type =='idle'){
            $('.select-process-button').click((e)=>{
                var process_name = e.target.attributes['data-process'].value
                process_name = process_name.toLowerCase().replace(/\b[a-z]/g, function(letter) {
                    return letter.toUpperCase();
                })
                $('#select-process-modal').modal('show')
                $('#select-process-modal').find('.process-name').html(process_name)
                $('#select-process-modal').find('#select-process-input').attr('value',process_name)
            })
        }
        else if(jQuery.inArray(widget_type, ['pre production', 'production_part_1', 'production_part_2', 'production_part_3', 'post_production_day_1', 'post_production_day_2', 'post_production_day_3']) != -1) {
            get_progress()
            $widget.find('.cancel-operation').click(()=>{
                var data = {
                    'message': '',
                    'message_type': 'cancel operation',
                }
                websocket_send(data)
            })
        }
        else if (widget_type =='post_production_wait_day_2'){
            $('.select-process-button').click((e)=>{
                var process_name = e.target.attributes['data-process'].value
                process_name = process_name.toLowerCase().replace(/\b[a-z]/g, function(letter) {
                    return letter.toUpperCase();
                })
                $('#select-process-modal').modal('show')
                $('#select-process-modal').find('.process-name').html(process_name)
                $('#select-process-modal').find('#select-process-input').attr('value',process_name)
            })
            $('.cancel-operation').click(()=>{
                var data = {
                    'message': '',
                    'message_type': 'cancel operation',
                }
                websocket_send(data)
            })
        }
        else if (widget_type =='post_production_wait_day_3'){
            $('.select-process-button').click((e)=>{
                var process_name = e.target.attributes['data-process'].value
                process_name = process_name.toLowerCase().replace(/\b[a-z]/g, function(letter) {
                    return letter.toUpperCase();
                })
                $('#select-process-modal').modal('show')
                $('#select-process-modal').find('.process-name').html(process_name)
                $('#select-process-modal').find('#select-process-input').attr('value',process_name)
            })
            $('.cancel-operation').click(()=>{
                var data = {
                    'message': '',
                    'message_type': 'cancel operation',
                }
                websocket_send(data)
            })
        }
        // else if (widget_type == 'linechart'){
        //     var $chart = $($widget).find('.chart-canvas')
        //     datarangepicker_init($widget)
        //     line_chart_init($chart, widget_type)
        // }
        // else if (widget_type == 'barchart'){
        //     var $chart = $($widget).find('.chart-canvas')
        //     bar_chart_init($chart, widget_type)
        // }
        // else if (widget_type == 'tagstatus'){
        //     var $chart = $($widget).find('.chart-canvas')
        //     pie_chart_init($chart, widget_type)
        // }
        // else if (widget_type == 'button'){
        //     $widget.find('.btn-floskid').on('click', function(){
        //     $(this).toggleClass('active')
        //     })
        // }
        // else if (widget_type == 'status'){
        // }
        // else if (widget_type == 'gauge'){
        //     var gauge = $($widget).find('.gauge-container')
        //     gauge_init(gauge)
        // }
        // else if (widget_type == 'tagtable'){
        //     tag_table_init($widget)
        // }
        // else if (widget_type == 'readertable'){
        //     reader_table_init($widget)
        // }
        // else if (widget_type == 'alarmlogtable'){
        //     alarm_log_table_init($widget)
        // }
        // else if (widget_type == 'alarmtable'){
        //     alarm_table_init($widget)
        // }
    })
}

function get_progress(){
    ajax_request('get_progress/', 'GET', 'get progress').done((data)=>{
        $.each(data.description, (index, value)=>{
            $row = value.timestamp + ' - ' + value.description + '\n'
            $('#progress-description').val($('#progress-description').val()+$row)
        })
        var progress_description = $('#progress-description');
        if(progress_description.length)
            progress_description.scrollTop(progress_description[0].scrollHeight - progress_description.height());
        $('#progress-bar').css({'width': data.percentage+'%'})
    })
}


// others --------------------------------------------------------------------------------

function datarangepicker_init($widget){
    $($widget).find('.date-range-picker').daterangepicker({
        opens: 'right',
    })
}



// init widget according to widget type -----------------------------------------------------------------

// alarm datatable
function alarm_table_init($widget){
    var table = $($widget).find('.table').DataTable({
        bInfo : false,
        bLengthChange: false,
        bPaginate: false,
        responsive: true,
        ajax:  {
            'url': "alarm/",
            "type": "GET",
            'dataSrc': "", 
            'data': {
                'mode' : 'get active',
            }
        },
        columns: [
            { 'data': "rtu__rtu_name" },
            { 'data': "rtu__rtu_location" },
            { 'data': "alarm" },
            { 'data': "time_alarm" },
            { 'data': "status" },
        ],
        language: {
            "emptyTable": "No Active Alarm Found"
        }
    });
    setInterval(function() {
        table.ajax.reload()
    }, 1000)
}


// alarm logs datatable
function alarm_log_table_init($widget){
    var table = $($widget).find('.table').DataTable({
        bInfo : false,
        bLengthChange: false,
        bPaginate: false,
        ajax:  {
            'url': "alarm/",
            "type": "GET",
            'dataSrc': "", 
            'data': {
                'mode' : 'get logs',
            }
        },
        columns: [
            { 'data': "rtu__rtu_name" },
            { 'data': "rtu__rtu_location" },
            { 'data': "alarm" },
            { 'data': "time_alarm" },
            { 'data': "time_deactivate"},
        ],
        language: {
            "emptyTable": "No Alarm Logs Found"
        }
    });
    setInterval(function() {
        table.ajax.reload()
    }, 1000)
}


// tag table datatable
function tag_table_init($widget){
    var table = $($widget).find('.table').DataTable({
        bInfo : false,
        bLengthChange: false,
        bPaginate: false,
        ajax:  {
            'url': "tag_manager/",
            "type": "GET",
            'dataSrc': "", 
            'data': {
                'mode' : 'tagtable_datatable',
                'rtu_id' : function() {
                    return $($widget).find('.rtu_select').val();
                },
                'reader_location' : function() {
                    return $($widget).find('.location_select').val();
                },
            }
        },
        columns: [
            { 'data': "tag_name" },
            { 'data': "tag_id" },
            { 'data': "latest_reading" },
            { 'data': "latest_timestamp" },
            { 'data': "enabled" },
        ],
        language: {
            "emptyTable": "No RFID Tags found for selected RTU"
        }
    });
    setInterval(function() {
        table.ajax.reload()
    }, 1000)
}

// reader table datatable
function reader_table_init($widget){
    var table = $($widget).find('.table').DataTable({
        bInfo : false,
        bLengthChange: false,
        searching: false,
        bPaginate: false,
        ajax:  {
            'url': "rtu_manager/",
            "type": "GET",
            'dataSrc': "", 
            'data': {
                'mode' : 'readertable_datatable',
                // 'reader_id' : function() {
                //     return $($widget).find('.reader_select').val();
                // },
                // 'reader_location' : function() {
                //     return $($widget).find('.location_select').val();
                // },
            }
        },
        columns: [
            { 'data': "rtu_name" },
            { 'data': "rtu_location" },
            { 'data': "status" },
            { 'data': "last_connected" },
        ],
    });
    setInterval(function() {
        table.ajax.reload()
    }, 1000)
}


// line and bar chart
function line_chart_init($chart, widget_type) {

    // demo data
    // var data = {
    //   labels: ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00'],
    //   datasets: [{
    //     label: 'Flow Rate',
    //     data: [0, 20, 10, 30, 15, 40, 20, 60, 60]
    //   }]
    // }

    var mxwitdh;
    if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|ipad|iris|kindle|Android|Silk|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(navigator.userAgent) 
        || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(navigator.userAgent.substr(0,4))) { 
        ztype = "x";
        fsize = 10;
        fsize2 = 10;
        mxwitdh = 50;
    } else { ztype = "xy"; fsize = 12; fsize2 = 16; mxwitdh=80; }	
    
    var data = {
      labels: [],
      datasets: [{
        label: 'Tag Reading',
        borderColor: '#4695c5',
        backgroundColor: '#4695c5',
        pointRadius: 0,
        borderWidth: 1,
        pointHitRadius: 20,
        data: []
      }]
    }
    
    // var no_data_plugin = {
    //     afterDraw: function(chart) {
    //         if (chart.data.datasets[0].data.every(item => item === 0)) {
    //             let ctx = chart.chart.ctx;
    //             let width = chart.chart.width;
    //             let height = chart.chart.height;

    //             chart.clear();
    //             ctx.save();
    //             ctx.textAlign = 'center';
    //             ctx.textBaseline = 'middle';
    //             ctx.fillText('No data to display', width / 2, height / 2);
    //             ctx.restore();
    //         }
    //     }
    // }
    
    // line chart config
    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            spanGaps: true,
            interaction: {
                mode: 'nearest'
            },
            plugins: {
                title: {
                    display: true,
                    text: 'RFID Tag 1',
                },
                legend: {
                    display: false,
                },
                zoom: {
                    zoom: {
                        drag: {
                            enabled: false,
                        },
                        mode: 'xy',                   
                        // pinch: {
                        //     enabled: true
                        // },
                    },
                    pan: {
                        enabled: true,
                        mode: 'xy',
                        speed: 1,
                    },
                },
            },
            scales: {
                x: {
                    // adapters: {
                    //     date: {
                    //         locale: de
                    //     }
                    // },
                    type: 'time',
                    display: true,
                    position: 'bottom',
                    // min: new Date('2021-07-01').valueOf(),
                    // max: new Date('2021-07-04').valueOf(),
                    time: {
                        source: 'auto',
                        displayFormats: {
                            hour: 'HH:mm dd-MMM-yy', 
                            day: 'HH:mm dd MMM yy', 
                        },
                        unit: 'hour',
                        stepSize: 6
                    }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    beginAtZero: true,
                    min: 0,
                    max: 35,
                    ticks: {
                        // color: '#0ac238',
                        major: true,
                    }
                },
            },
        },
        // plugins: [no_data_plugin]
    }

    
    var chart = new Chart($chart, config);

    // Save to jQuery object
    $chart.data('chart', chart);
};


// bar chart
function bar_chart_init($chart, widget_type){
    var data = {
        labels: [],
        datasets: [{
          label: 'Tag Reading',
          borderColor: '#4695c5',
          backgroundColor: '#4695c5',
          pointRadius: 0,
          borderWidth: 1,
          pointHitRadius: 20,
          data: []
        }]
      }
    // bar chart config
    const config = {
        type: 'bar',
        data: data,
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text: 'Chart.js Bar Chart'
            }
          }
        },
      }
    var chart = new Chart($chart, config);
    $chart.data('chart', chart);
}

// pie chart 
function pie_chart_init($chart, widget_type){
    const data = {
        labels: [
          'Dry',
          'Moist',
          'Wet'
        ],
        datasets: [{
          label: 'My First Dataset',
        //   data: [300, 50, 100],
          data: [],
          backgroundColor: [
            'rgb(87, 163, 0)', // dry
            'rgb(255, 201, 64)', // moist
            'rgb(191, 0, 0)' // wet
          ],
          hoverOffset: 4
        }]
      };
    // bar chart config
    const config = {
        type: 'doughnut',
        data: data,
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
            },
            title: {
              display: false,
              text: 'doughnut chart'
            }
          }
        },
      }
    var chart = new Chart($chart, config);
    $chart.data('chart', chart);
}



// gauge meter
function gauge_init(gauge){
    $(gauge).knob({
      'min': 0,
      'max': 50,
      'angleOffset': 220,
      'angleArc': 280,
      'readOnly': true,
      "skin":"tron",
      "inputColor":"white",
      "fgColor":"#2dce89",
      "displayInput":true,
      "bgColor":'white',
      // "format":'m3/h',
    })
    $(gauge).val(27).trigger('change');
}