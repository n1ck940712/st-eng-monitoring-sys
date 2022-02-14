$(document).ready(()=>{
    connect_websocket()
})

function connect_websocket(){
    var endpoint = 'ws://'
    + window.location.host
    + '/ws/socket/'
    chatSocket = new WebSocket(endpoint)

    chatSocket.onmessage = function(e) {
        var data = JSON.parse(e.data).data
        console.log(data)
        if ((data.message_type == 'request input before process start') && (window.location.pathname == '/monitoring-sys/')){
            load_data_input_modal(data.message)
        }
        else if (data.message_type == 'prompt'){
            console.log(data.message)
            load_prompt(data.message)
        }
        else if (data.message_type == 'close prompt'){
            close_prompt(data.message)
        }
        else if ((data.message_type == 'prompt data check') && (window.location.pathname == '/monitoring-sys/')){
            prompt_data_check(data.message)
        }
        else if ((data.message_type == 'prompt data check update') && (window.location.pathname == '/monitoring-sys/')){
            prompt_data_check_update(data.message)
        }
        else if (data.message_type == 'trigger event'){
            get_status()
        }
        else if (data.message_type == 'confirm prompt'){
            load_confirm_prompt(data.message)
        }
        else if ((data.message_type == 'progress update') && (window.location.pathname == '/monitoring-sys/')){
            update_progress(data.message)
        }
        else if ((data.message_type == 'deviation prompt') && (window.location.pathname == '/monitoring-sys/')){
            load_deviation_prompt(data.message)
        }
        // else if ((data.message_type == 'force logout')){
        //     force_logout()
        // }
        else if ((data.message_type == 'sensor reading update')){
            update_sensor_reading(data.message)
        }
        else if ((data.message_type == 'report edit')){
            report_edit_result(data.message)
        }
        else if ((data.message_type == 'export response')){
            handle_export_response(data.message)
        }
        else if ((data.message_type == 'report delete response')){
            handle_delete_response(data.message)
        }
    }
}

function handle_delete_response(message){
    $('.loading-overlay').hide()
    $('.loading-overlay').removeClass('show')
    show_alert(message.success, message.message)
    if (message.success){
        $('#report-delete-modal').modal('hide')
        table.ajax.reload()
    }
}

function handle_export_response(message){
    $('.loading-overlay').hide()
    $('.loading-overlay').removeClass('show')
    show_alert(message.success, message.message)
}

function report_edit_result(message){
    $('.loading-overlay').hide()
    $('.loading-overlay').removeClass('show')
    if (message.success){
        $('#report-edit-modal').modal('hide')
        show_alert(true, 'Report updated successfully')
        load_report_pdf($('#report-preview-modal .modal-title').text())
        
    }
    else{
        show_alert(false, 'Report failed to update')
    }
}

function force_logout(){
    location.href = '/monitoring-sys/logout/'
}

function websocket_send(data){
    data.user_role = $('#user-role').val()
    data.recipient_ip = '127.0.0.1'
    console.log(data)
    chatSocket.send(JSON.stringify({
        'data': data,
        'sender': 'UI',
    }))
}



// =============================================================
// prompt
// =============================================================
// ================================================ monitoring sys ===================================================


// $(document).ready(()=>{
//     get_status()
// })


$('#select-process-form').submit((e)=>{
    // $('#select-process-modal').modal('hide')
    e.preventDefault()
    var data = {
        'message': $('#select-process-input').val().toLowerCase(),
        'message_type': 'process select',
    }
    websocket_send(data)
})

$('#data-input-form').submit((e)=>{
    var reg = new RegExp(/^(?:[1-9]\d*|0)?(?:\.\d+)?$/);
    // $('#data-input-modal').modal('hide')
    e.preventDefault()
    var $inputs = $('#data-input-form :input')
    var values = {}
    var error_flag = false
    $inputs.each(function() {
        var key = this.id.replace(/-/g,'_')
        values[key] = $(this).val()
        if (key != 'start_process_name'){
            if (!reg.test($(this).val())){
                console.log('regex test failed')
                error_flag = true
            }
        }
    })
    console.log(values)
    if (!error_flag){
        var data = {
            'message': values,
            'message_type': 'prompt data input submit',
        }
        websocket_send(data)
    }
    else {
        console.log('non valid input detected ')
        $('#data-input-modal .modal-body-error').html('Invalid input')
    }
})

$('#waiting-prompt-form').submit((e)=>{
    e.preventDefault()
    // $('#prompt-modal').modal('hide')
    var $inputs = $('#waiting-prompt-form :input')
    var values = {}
    $inputs.each(function() {
        values[this.id.replace(/-/g,'_')] = $(this).val()
    })
    var data = {
        'message': values,
        'message_type': 'waiting prompt acknowledged',
    }
    websocket_send(data)
})

$('#deviation-form').submit((e)=>{
    e.preventDefault()
    // $('#deviation-modal').modal('hide')
    var data = {
        'message': 'message',
        'message_type': 'deviation',
    }
    websocket_send(data)
})

$('#confirmation-form').submit((e)=>{
    // $('#prompt-modal').modal('hide')
    e.preventDefault()
    process_name = $('#confirmation-process-name').val()
    var data = {
        'message': {
            'process_name': process_name
        },
        'message_type': 'confirm',
    }
    websocket_send(data)
})

function load_data_input_modal(message){
    $('#data-input-modal .modal-body-error').html('')
    $('#data-input-modal #data-input-modal-title').html('').append(message.title.toUpperCase())
    $('#data-input-modal .modal-body-text').html('').append(message.text)
    $('#data-input-modal .button-proceed').html(message.button_text)
    $input = `<input hidden type="text" id="start-process-name" value="${message.process_name}" required>`
    $('#data-input-form').html('').append($input)
    $.each(message.variables_list, (index, value)=>{
        $input = $(`
        <div class="input-group mb-3">
            <div class="input-group-prepend">
            <label class="input-group-text text-dark">${value.name}</label>
            </div>
            <input type=number inputmode="numeric" step=0.01 class="form-control" id="${value.name.replace(/ /g,"-")}" value=${value.value} required>
            <div class="input-group-append">
                <span class="input-group-text">${value.unit}</span>
            </div>
        </div>`)
        $('#data-input-form').append($input)
        $('#data-input-modal').modal('show')
    })
}

function load_prompt(message){
    $('#prompt-modal #prompt-title').html('').append(message.title.toUpperCase())
    $('#prompt-modal .modal-body').html('').append(message.text)
    $('#prompt-modal #process-name').val(message.process_name)
    $('#prompt-modal .button-proceed').html(message.button_text)
    $('#prompt-modal').modal('show')
    if (message.wait_for_acknowledge){
        $('#prompt-modal .modal-footer').attr("hidden", false)
    }
    else{
        $('#prompt-modal .modal-footer').attr("hidden", true)
        setTimeout(() => {
            $('#prompt-modal').modal('hide')
        }, 3000)
    }
}

function load_deviation_prompt(message){
    $('#deviation-modal #deviation-title').html('').append(message.title.toUpperCase())
    $('#deviation-modal .modal-body').html('').append(message.text)
    $('#deviation-modal #process-name').val(message.process_name)
    $('#deviation-modal').modal('show')
}

function prompt_data_check(message){
    console.log('prompt_data_check')
    $('#prompt-modal').modal('show')
    $('#prompt-modal .modal-body').html('').append(message.text)
    $('#prompt-modal #process-name').val(message.process_name)
    console.log($('#prompt-modal #process-name').val())
    $.each(message.parameters, (index, value)=>{
        console.log(index, value)
        $row = $(`
        <div class="input-group mb-3">
            <div class="input-group-prepend">
            <label class="input-group-text text-dark">Current ${value.name}</label>
            </div>
            <input type="text" class="form-control" id="${value.name.replace(/ /g,"-")}" value='' readonly>
            <div class="input-group-append">
                <span class="input-group-text">${value.unit}</span>
            </div>
        </div>`)
        $('#prompt-modal .modal-body').append($row)
    })
    $.each(message.set_parameters, (index, value)=>{
        console.log(index, value)
        $row = $(`
        <div class="input-group mb-3">
            <div class="input-group-prepend">
            <label class="input-group-text text-dark">Set ${value.name}</label>
            </div>
            <input type="text" class="form-control" id="set-${value.name.replace(/ /g,"-")}" value='${value.value}' readonly>
            <div class="input-group-append">
                <span class="input-group-text">${value.unit}</span>
            </div>
        </div>`)
        $('#prompt-modal .modal-body').append($row)
    })
    $('#prompt-modal .modal-footer').attr("hidden", false)
    $('#prompt-modal .button-proceed').html(message.button_text)
}

function prompt_data_check_update(message){
    $.each(message, (index, value)=>{
        $(`#prompt-modal #${index.replace(/ /g,"-")}`).val(value)
    })
}

function close_prompt(prompt=null){
    if (prompt == null){ // close all prompt 
        prompt = ['notification prompt', 'data input prompt', 'confirmation prompt', 'select process prompt', 'deviation prompt', 'select process modal']
    }
    $.each(prompt, (index, value)=>{
        if (value == 'notification prompt'){
            $('#prompt-modal').modal('hide')
            $('#prompt-modal .modal-footer').attr("hidden", true)
            $('#prompt-modal .modal-body').html('')
        }
        if (value == 'data input prompt'){
            $('#data-input-modal').modal('hide')
            $('#data-input-modal .data-input-form').html('')
        }
        if (value == 'confirmation prompt'){
            $('#confirmation-modal').modal('hide')
            $('#confirmation-modal .modal-body').html('')
        }
        if (value == 'deviation prompt'){
            $('#deviation-modal').modal('hide')
            $('#deviation-modal .modal-body').html('')
        }
        if (value == 'select process prompt'){
            $('#select-process-modal').modal('hide')
        }
    })
}

function trigger_event(message){
    console.log(message.event_name)
    data = {
        'event_name': message.event_name
    }
    ajax_request('trigger_event/', 'get', 'trigger event', {'event_name': message.event_name}).done((data)=>{
        console.log(data)
        $('.grid-stack-item-content').html(data.html)
    })
}

async function get_status(){
    if (window.location.pathname == '/monitoring-sys/'){
        if ($('.grid-stack-item').length > 0){
            $('.grid-stack-item').hide(0, async ()=>{
                grid.removeAll()
                await ajax_request('trigger_event/', 'get', 'get status').done((data)=>{
                    console.log(data)
                    if (data.process_running){
                        console.log('disable other pages')
                        $("a.nav-link").addClass('link-disabled')
                    }
                    else{
                        console.log('enable other pages')
                        $("a.nav-link").removeClass('link-disabled')
                    }
                    load_widget($.parseJSON(data.layout))
                    $('.grid-stack-item-content').html(data.html)
                })
                await insert_all_widget_html()
                $('.grid-stack-item').show()
                init_new_widget()
                disable_widget_edit()
            })
        }
        else {
            await ajax_request('trigger_event/', 'get', 'get status').done((data)=>{
                console.log(data)
                load_widget($.parseJSON(data.layout))
                $('.grid-stack-item-content').html(data.html)
                if (data.process_running){
                    console.log('disable other pages')
                    $("a.nav-link").addClass('link-disabled')
                }
                else{
                    console.log('enable other pages')
                    $("a.nav-link").removeClass('link-disabled')
                }
            })
            await insert_all_widget_html()
            $('.grid-stack-item').show()
            init_new_widget()
            disable_widget_edit()
        }
    
    }
    else{
        await ajax_request('trigger_event/', 'get', 'get status').done((data)=>{
            if (data.process_running){
                window.location.replace('/monitoring-sys/')
            }
        })
    }
}


$('.cancel-operation').click(()=>{
    var data = {
        'message': '',
        'message_type': 'cancel operation',
    }
    websocket_send(data)
})

function load_confirm_prompt(message){
    $('#confirmation-modal .modal-body').html('').append(message.text)
    $('#confirmation-modal').modal('show')
    $('#confirmation-modal #confirmation-process-name').val(message.process_name)
}

function update_progress(message){
    if (message.description != ''){
        $row = message.timestamp + ' - ' + message.description + '\n'
        $('#progress-description').val($('#progress-description').val() + $row)
    }
    if (message.percentage != ''){
        $('#progress-bar').css({'width':message.percentage+'%',})
    }
}

function update_sensor_reading(message){
    $('#current_pressure').val(message.pressure + ' kPa')
    $('#current_temp').val(message.temperature + ' °C')
    $('#current_flow').val(message.n2_flow_rate + ' L/min')
}