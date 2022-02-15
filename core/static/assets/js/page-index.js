
// ================================================
// dependencies
// ================================================

// widget.js
$("head").append($("<script></script>").attr("src", "/static/assets/js/widget.js"))
$("head").append($("<script></script>").attr("src", "/static/assets/js/websocket.js"))


// ======================================================================================================
// event listeners 
// ======================================================================================================

// inits ------------------------------------------------------------------------

// get widget layout save state
$('.grid-stack').ready(async ()=>{
    init_gridstack()
    // await get_widget_save()
    disable_widget_edit()
    get_status()
})


// edit widget button 
$('.edit-widget').click(function(){
    enter_widget_edit()
})


// confirm edit button
$('.confirm-edit-widget').click(function(){
    save_widget_layout()
    exit_widget_edit()
})

$('#add-widget-type').change(()=>{
    add_device_section_show_hide($('#add-widget-type').val())
})


// modal  ------------------------------------------------------------------------

// 'add widget' form submit
$('#add-widget-form').submit(async (e)=>{
    e.preventDefault()
    $('#add_widget_modal').modal('toggle')
    
    var $form = $('#add-widget-form')
    var widget_name = $form.find('#add_widget_name').val()
    var widget_type=  $form.find('#add-widget-type').val()
    var widget_size = get_widget_default_size(widget_type)
    var widget_id = get_widget_id_num()
    
    insert_new_widget(0, 0, widget_size.gs_w, widget_size.gs_h, widget_type, widget_id, widget_name)
    await insert_widget_html(widget_id, widget_type, widget_name)
    // init_new_widget('single', widget_id, widget_type)
    
})

// clear 'add widget' form when modal is reopened
$('.add_widget_open_modal').click(function(){
    $('#add-device-section').hide()
    $('.custom-select').find('.widget_option').remove()
    $('#add_widget_name').val('')
    $('#add-widget-type').val('')
    $('.add_widget_form_sub').html('')
    get_available_widget()
})


// ============================================================================================================================================================================================================
// functions
// ============================================================================================================================================================================================================


// insert widget option into 'add widget' form select
function load_available_widget(widget) {
    $.each(widget, function(index, widget){
        $('#add-widget-type').prepend($('<option value="'+widget+'" class="widget_option">'+widget+'</option>'))
    })
}


//gridstack enter widget edit
function enter_widget_edit(){
    $('.add_widget_open_modal').fadeIn()
    $('.edit-widget').fadeOut()
    $('.confirm-edit-widget').fadeIn()
    $('.remove-widget').fadeIn()
    enable_widget_edit()
    $('.grid-stack').toggleClass('grid-stack-edit-enable')
}


//gridstack exit widget edit
function exit_widget_edit(){
    $('.add_widget_open_modal').fadeOut()
    $('.edit-widget').fadeIn()
    $('.confirm-edit-widget').fadeOut()
    $('.remove-widget').fadeOut()
    disable_widget_edit()
    if ($('.grid-stack').hasClass('grid-stack-edit-enable')){
        $('.grid-stack').toggleClass('grid-stack-edit-enable')
    }
}
