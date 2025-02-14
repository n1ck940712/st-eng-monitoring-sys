$(document).ready(()=>{
    connect_websocket()
    
})

function connect_websocket(){
    var endpoint = 'ws://'
    + window.location.host
    + '/ws/socket/'
    chatSocket = new WebSocket(endpoint)
    websocket_sending_flag = false

    chatSocket.onmessage = function(e) {
        var data = JSON.parse(e.data).data
        // console.log(data)
        if ((data.message_type == 'request input before process start') && (window.location.pathname == '/monitoring-sys/')){
            load_data_input_modal(data.message)
        }
        else if (data.message_type == 'prompt'){
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
            handle_event(data.message)
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

function handle_event(message){
    if (message.event == ''){
        get_status()
    }

    else if (message.event == 'pre production started'){
        close_prompt()
        data = {
            'title': 'Pre Production',
            'text': 'Pre production started.',
            'process_name': '',
            'button_text': '',
            'wait_for_acknowledge': false,
        }
        load_prompt(data)
        get_status()
        setTimeout(() => {
            parameters_list = ['n2 flow rate', 'purging duration']
            ajax_request('default_values/', 'get', 'get default values specific', {'process_name': 'pre production', 'parameters': JSON.stringify(parameters_list)}).done((ajax_data)=>{
                data = {
                    'title': 'Pre Production',
                    'text': 'Waiting to start purging process.',
                    'process_name': 'pre production',
                    'button_text': 'Start',
                    'variables_list': ajax_data.variables_list,
                    'wait_for_acknowledge': true,
                }
                load_data_input_modal(data)
            })
        }, 3100);
    }

    else if (message.event == 'pre production purging duration reached'){
        close_prompt()
        data = {
            'title': 'Pre Production',
            'text': 'Purging duration reached. Waiting for deactivation of flow controller.',
            'process_name': 'pre production deactivate flow',
            'button_text': 'Deactivate',
            'wait_for_acknowledge': true,
        }
        load_prompt(data)
    }

    else if (message.event == 'pre production completed'){
        close_prompt()
        data = {
            'title': 'Pre Production',
            'text': 'Pre production completed. Report generated.',
            'process_name': 'end pre production',
            'button_text': 'Proceed',
            'wait_for_acknowledge': true,
        }
        load_prompt(data)
        get_status()
    }

    else if (message.event == 'production part 1 start'){
        close_prompt()
        data = {
            'title': 'Production Part 1',
            'text': 'Production part 1 started.',
            'process_name': '',
            'button_text': '',
            'wait_for_acknowledge': false,
        }
        load_prompt(data)
        get_status()
        setTimeout(() => {
            parameters_list = ['n2 flow rate', 'target temperature', 'logging interval', 'heater set point']
            ajax_request('default_values/', 'get', 'get default values specific', {'process_name': 'production part 1', 'parameters': JSON.stringify(parameters_list)}).done((ajax_data)=>{
                data = {
                    'title': 'Production Part 1',
                    'text': '',
                    'process_name': 'production part 1',
                    'button_text': 'Start',
                    'variables_list': ajax_data.variables_list,
                    'wait_for_acknowledge': true,
                }
                load_data_input_modal(data)
            })
        }, 3100);
    }

    else if (message.event == 'production part 1 end'){
        close_prompt()
        data = {
            'title': 'Production Part 1',
            'text': 'Production part 1 completed. Start production part 2?',
            'process_name': 'start production part 2',
            'button_text': 'Start',
            'wait_for_acknowledge': true,
        }
        load_prompt(data)
    }

    else if (message.event == 'production part 2 start'){
        close_prompt()
        data = {
            'title': 'Production Part 2',
            'text': 'Production part 2 started.',
            'process_name': '',
            'button_text': '',
            'wait_for_acknowledge': false,
        }
        load_prompt(data)
        get_status()
        setTimeout(() => {
            parameters_list = ['logging interval', 'process duration', 'heater set point']
            ajax_request('default_values/', 'get', 'get default values specific', {'process_name': 'production part 2', 'parameters': JSON.stringify(parameters_list)}).done((ajax_data)=>{
                data = {
                    'title': 'Production Part 2',
                    'text': '',
                    'process_name': 'production part 2',
                    'button_text': 'Start',
                    'variables_list': ajax_data.variables_list,
                    'wait_for_acknowledge': true,
                }
                load_data_input_modal(data)
            })
        }, 3100);
    }

    else if (message.event == 'production part 2 end'){
        close_prompt()
        data = {
            'title': 'Production Part 2',
            'text': 'Production part 2 completed. Start production part 3?',
            'process_name': 'start production part 3',
            'button_text': 'Start',
            'wait_for_acknowledge': true,
        }
        load_prompt(data)
    }

    else if (message.event == 'production part 3 start'){
        close_prompt()
        data = {
            'title': 'Production Part 3',
            'text': 'Production part 3 started.',
            'process_name': '',
            'button_text': '',
            'wait_for_acknowledge': false,
        }
        load_prompt(data)
        get_status()
        setTimeout(() => {
            parameters_list = ['n2 flow rate', 'logging interval', 'process duration', 'heater set point']
            ajax_request('default_values/', 'get', 'get default values specific', {'process_name': 'production part 3', 'parameters': JSON.stringify(parameters_list)}).done((ajax_data)=>{
                data = {
                    'title': 'Production Part 3',
                    'text': '',
                    'process_name': 'production part 3',
                    'button_text': 'Start',
                    'variables_list': ajax_data.variables_list,
                    'wait_for_acknowledge': true,
                }
                load_data_input_modal(data)
            })
        }, 3100);
    }

    else if (message.event == 'production part 3 end'){
        close_prompt()
        data = {
            'title': 'Production Part 3',
            'text': 'Production completed. Report generated.',
            'process_name': 'end production',
            'button_text': 'Acknowledge',
            'wait_for_acknowledge': true,
        }
        load_prompt(data)
        get_status()
    }

    else if (message.event == 'post production day 1 start'){
        close_prompt()
        data = {
            'title': 'Post Production Day 1',
            'text': 'Post Production Day 1 started.',
            'process_name': '',
            'button_text': '',
            'wait_for_acknowledge': false,
        }
        load_prompt(data)
        get_status()
        setTimeout(() => {
            parameters_list = ['process duration', 'logging interval']
            ajax_request('default_values/', 'get', 'get default values specific', {'process_name': 'post production day 1', 'parameters': JSON.stringify(parameters_list)}).done((ajax_data)=>{
                data = {
                    'title': 'Post Production Day 1',
                    'text': '',
                    'process_name': 'post production day 1',
                    'button_text': 'Start',
                    'variables_list': ajax_data.variables_list,
                    'wait_for_acknowledge': true,
                }
                load_data_input_modal(data)
            })
        }, 3100);
    }

    else if (message.event == 'post production day 1 end'){
        close_prompt()
        data = {
            'title': 'Post Production Day 1',
            'text': 'Post Production Day 1 completed.',
            'process_name': '',
            'button_text': 'Acknowledge',
            'wait_for_acknowledge': true,
        }
        load_prompt(data)
        get_status()
    }

    else if (message.event == 'post production day 2 start'){
        close_prompt()
        data = {
            'title': 'Post Production Day 2',
            'text': 'Post Production Day 2 started.',
            'process_name': '',
            'button_text': '',
            'wait_for_acknowledge': false,
        }
        load_prompt(data)
        get_status()
        setTimeout(() => {
            parameters_list = ['process duration', 'logging interval']
            ajax_request('default_values/', 'get', 'get default values specific', {'process_name': 'post production day 2', 'parameters': JSON.stringify(parameters_list)}).done((ajax_data)=>{
                data = {
                    'title': 'Post Production Day 2',
                    'text': '',
                    'process_name': 'post production day 2',
                    'button_text': 'Start',
                    'variables_list': ajax_data.variables_list,
                    'wait_for_acknowledge': true,
                }
                load_data_input_modal(data)
            })
        }, 3100);
    }
    
    else if (message.event == 'post production day 2 end'){
        close_prompt()
        data = {
            'title': 'Post Production Day 2',
            'text': 'Post Production Day 2 completed.',
            'process_name': '',
            'button_text': 'Acknowledge',
            'wait_for_acknowledge': true,
        }
        load_prompt(data)
        get_status()
    }

    else if (message.event == 'post production day 3 start'){
        close_prompt()
        data = {
            'title': 'Post Production Day 3',
            'text': 'Post Production Day 3 started.',
            'process_name': '',
            'button_text': '',
            'wait_for_acknowledge': false,
        }
        load_prompt(data)
        get_status()
        setTimeout(() => {
            parameters_list = ['process duration', 'logging interval']
            ajax_request('default_values/', 'get', 'get default values specific', {'process_name': 'post production day 3', 'parameters': JSON.stringify(parameters_list)}).done((ajax_data)=>{
                data = {
                    'title': 'Post Production Day 3',
                    'text': '',
                    'process_name': 'post production day 3',
                    'button_text': 'Start',
                    'variables_list': ajax_data.variables_list,
                    'wait_for_acknowledge': true,
                }
                load_data_input_modal(data)
            })
        }, 3100);
    }

    else if (message.event == 'post production day 3 end'){
        close_prompt()
        data = {
            'title': 'Post Production Day 3',
            'text': 'Post Production Day 3 completed. Report generated.',
            'process_name': 'end post production',
            'button_text': 'Acknowledge',
            'wait_for_acknowledge': true,
        }
        load_prompt(data)
        get_status()
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
    if (!websocket_sending_flag){
        websocket_sending_flag = true
        data.user_role = $('#user-role').val()
        data.recipient_ip = '127.0.0.1'
        chatSocket.send(JSON.stringify({
            'data': data,
            'sender': 'UI',
        }))
        setTimeout(() => {
            websocket_sending_flag = false
        }, 1000);
    }
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
                error_flag = true
            }
        }
    })
    if (!error_flag){
        var data = {
            'message': values,
            'message_type': 'prompt data input submit',
        }
        websocket_send(data)
    }
    else {
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
    $('#data-input-modal .modal-body-text').html(`<span>${message.text}</span>`)
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
    if ((typeof message.title !== 'undefined') && (message.title !== '')){
        $('#prompt-modal #prompt-title').html(message.title.toUpperCase())
    }
    else{
        $('#prompt-modal #prompt-title').html('System Dialog')
    }
    $('#prompt-modal .modal-body').html(`<span>${message.text}</span>`)
    $('#prompt-modal #process-name').val(message.process_name)
    $('#prompt-modal .button-proceed').html(message.button_text)
    if (message.wait_for_acknowledge){
        $('#prompt-modal .modal-footer').attr("hidden", false)
    }
    else{
        $('#prompt-modal .modal-footer').attr("hidden", true)
        setTimeout(() => {
            $('#prompt-modal').modal('hide')
        }, 3000)
    }
    $('#prompt-modal').modal('show')
}

function load_deviation_prompt(message){
    if (typeof message.title !== 'undefined'){
        $('#deviation-modal #deviation-title').html(message.title.toUpperCase())
    }
    else{
        $('#deviation-modal #deviation-title').html('Readings Deviated')
    }
    $('#deviation-modal .modal-body').html(`<span>${message.text}</span>`)
    $('#deviation-modal #process-name').val(message.process_name)
    $('#deviation-modal').modal('show')
}

function prompt_data_check(message){
    if (typeof message.title !== 'undefined'){
        $('#prompt-modal #prompt-title').html(message.title.toUpperCase())
    }
    else{
        $('#prompt-modal #prompt-title').html('System Dialog')
    }
    $('#prompt-modal .modal-body').html(`<span>${message.text}</span>`)
    $('#prompt-modal #process-name').val(message.process_name)
    $.each(message.parameters, (index, value)=>{
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
    $('#prompt-modal').modal('show')
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
    data = {
        'event_name': message.event_name
    }
    ajax_request('trigger_event/', 'get', 'trigger event', {'event_name': message.event_name}).done((data)=>{
        $('.grid-stack-item-content').html(data.html)
    })
}

async function get_status(){
    if (window.location.pathname == '/monitoring-sys/'){
        if ($('.grid-stack-item').length > 0){
            $('.grid-stack-item').hide(0, async ()=>{
                grid.removeAll()
                await ajax_request('trigger_event/', 'get', 'get status').done((data)=>{
                    if (data.process_running){
                        $("a.nav-link").addClass('link-disabled')
                    }
                    else{
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
                load_widget($.parseJSON(data.layout))
                $('.grid-stack-item-content').html(data.html)
                if (data.process_running){
                    $("a.nav-link").addClass('link-disabled')
                }
                else{
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
    $('#confirmation-modal .modal-body').html(`<span>${message.text}</span>`)
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