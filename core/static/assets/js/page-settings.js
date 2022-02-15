
// ======================================================================================================
// dependencies
// ======================================================================================================

// datatables
$("head").append($("<script></script>").attr("src", "/static/assets/js/plugins/DataTables/datatables.js"));


// ======================================================================================================
// event listener
// ======================================================================================================


// inits ------------------------------------------------------------------------
$(document).ready(()=>{
    get_default_value_setting()
})


// update indicator when range-slider is changed
$('#settings-moist-threshold').change(function () {
    $('#settings-moist-threshold-indicator').val($(this).val())
});
$('#settings-wet-threshold').change(function () {
    $('#settings-wet-threshold-indicator').val($(this).val())
});

// post forms ------------------------------------------------------------------------

// post settings changes to server
$('#edit-default-values-form').submit((e)=>{
    e.preventDefault()
    post_default_value_changes()
})



// ======================================================================================================
// functions
// ======================================================================================================




function post_rtu_setting_changes(){
    var data = {
        rtu_id: $('#settings-rtu-select').val(),
        rtu_location: $('#settings-rtu-location').val(),
        moist_threshold: $('#settings-moist-threshold').val(),
        wet_threshold: $('#settings-wet-threshold').val(),
        min_tag_reading: $('#settings-min-tag-reading').val(),
        reading_average: $('#settings-reading-average').val(),
        reading_time: $('#settings-reading-time').val(),
    }
    ajax_request('rtu_manager/', 'POST', 'save settings', data, true).done((data)=>{
        set_rtu_settings(data.rtu_settings)
    })
}


function get_rtu_settings(){
    ajax_request('rtu_manager/', 'GET', 'get settings', {rtu_id:$('#settings-rtu-select').val()}, false).done((data)=>{
        set_rtu_settings(data.rtu_settings)
    })
}

function set_rtu_settings(rtu_settings){
    $.each(rtu_settings, function(index, value){
        $('#settings-rtu-location').val(value.rtu_location)
        $('#settings-moist-threshold').val(value.moist_threshold)
        $('#settings-moist-threshold-indicator').val(value.moist_threshold)
        $('#settings-wet-threshold').val(value.wet_threshold)
        $('#settings-wet-threshold-indicator').val(value.wet_threshold)
        $('#settings-min-tag-reading').val(value.min_tag_read)
        $('#settings-reading-average').val(value.average)
        $('#settings-reading-time').val(value.data_sampling_interval)
    })
}

function get_default_value_setting(){
    ajax_request('default_values/', 'GET', 'get default values').done((data)=>{
        if (data.success){
            set_default_value_setting(data.default_value_list)
        }
    })
}

function set_default_value_setting(default_values){
    var process_type = ''
    var first_run = true
    $.each(default_values, function(index, value){
        var setting_name = value.name
        var setting_value = value.value
        var setting_process = value.process
        var setting_unit = value.unit
        if (process_type != setting_process){
            if (first_run){
                $row = $(`
                <h6 class="heading-small text-muted mb-4">${setting_process}</h6>
                `)
                $('#edit-default-values-form .input-container').append($row)
                
            }
            else{
                $row = $(`
                <hr class="my-4" />
                <h6 class="heading-small text-muted mb-4">${setting_process}</h6>
                `)
                $('#edit-default-values-form .input-container').append($row)
            }
            process_type = setting_process
        }
        $row = $(`
        <div class="row">
            <div class="col">
                <div class="input-group mb-3">
                    <div class="input-group-prepend">
                        <span class="input-group-text">${setting_name}</span>
                    </div>
                    <input type=number step=0.01 class="form-control" id="settings-${setting_name.replace(' ', '-')}_${setting_process.replace(' ', '-')}" value="${setting_value}">
                    <div class="input-group-append">
                        <span class="input-group-text">${setting_unit}</span>
                    </div>
                </div>
            </div>
        </div>
        `)
        $('#edit-default-values-form .input-container').append($row)
        first_run = false
    })
}


function post_default_value_changes(){
    var $inputs = $('#edit-default-values-form :input').not(':input[type=submit]')
    var values = []
    $inputs.each(function() {
        var name = this.id.split('_')[0].replace(/-/g, ' ')
        var process = this.id.split('_')[1].replace(/-/g, ' ')
        values.push({'name': name, 'process': process, 'value': $(this).val()})
        // values[this.id.replace(/-/g,' ')] = $(this).val()
    })
    ajax_request('default_values/', 'POST', 'save default values', {value_list: JSON.stringify(values)}, true)
}