// ======================================================================================================
// dependencies
// ======================================================================================================

// ======================================================================================================
// event listener
// ======================================================================================================

// get user profile and user info form
$('#edit-self-user-form').ready(async function(){
    await get_self_user_profile()
    if ($('.table-user-management').length > 0){
        get_user_list()
    }
})

// $('.table-user-management').ready(function(){
//     if ($('.table-user-management').length > 0){
//         get_user_list()
//     }
// })

$('.btn-add-user').click(function(){
    $('#add-user-modal-container').modal('show')
    $('#add-user-form').find('input').val('')
    $('#add-user-form').find('select').val('')
})

// post forms ------------------------------------------------------------------------

// user manager post changes
$('#edit-user-form').submit((e)=>{
    e.preventDefault();
    post_edit_user_form()
})

// update self profile changes
$('#edit-self-user-form').submit((e)=>{
    e.preventDefault();
    post_edit_self_user()
})

// add new user
$('#add-user-form').submit((e)=>{
    e.preventDefault()
    post_add_user_form()
})

// change password
$('#change-password-form').submit((e)=>{
    e.preventDefault()
    post_change_password_form()
})


// post forms ------------------------------------------------------------------------

$(document).on('click', '.btn-edit-user', function(e){
    get_user_profile($(this).attr('name'))
    $('#edit-user-modal-container').modal('toggle')
})


// ======================================================================================================
// functions
// ======================================================================================================

async function get_self_user_profile(){
    await ajax_request('user_profile/', 'GET', 'get one', {username: 'self'}, false, true).done((data)=>{
        if (data.success){
            var $form = $('#edit-self-user-form')
            $form.find('#input-username').val(data.username)
            $form.find('#input-email').val(data.email)
            $form.find('#input-first-name').val(data.first_name)
            $form.find('#input-last-name').val(data.last_name)
            $form.find('#input-phone-number').val(data.phone_number)
            $form.find('#input-role').val(data.user_role)
            if (data.user_role != 'Super Admin'){
                $form.find('#input-role option').attr('disabled', true)
                $form.find('#input-role option[value="'+data.user_role+'"]').attr('disabled', false)
            }
        }
    })
}


function post_edit_self_user(){
    var $form = $('#edit-self-user-form')
    var data = {
        'username':  $form.find('#input-username').val(), 
        'email':  $form.find('#input-email').val(), 
        'first_name':  $form.find('#input-first-name').val(), 
        'last_name':  $form.find('#input-last-name').val(), 
        'phone_number':  $form.find('#input-phone-number').val(), 
        'role':  $form.find('#input-role').val()
    }
    ajax_request('user_profile/', 'POST', 'update', data, true).done((data)=>{
        get_self_user_profile()
    })
}


function get_user_list(){
    ajax_request('user_profile/', 'GET', 'get all', {}, false).done((data)=>{
        if (data.success){
            $('.table-user-management').find('tbody').html('')
            $.each(data.user_list, (i, user)=>{
                populate_user_management_table(user)
            }) 
        }
    })
}


function get_user_profile(username){
    ajax_request('user_profile/', 'GET', 'get one', {username: username}, false).done((data)=>{
        var $form = $('#edit-user-form')
        if (data.success){
            $form.find('#input-username').val(data.username)
            $form.find('#input-email').val(data.email)
            $form.find('#input-first-name').val(data.first_name)
            $form.find('#input-last-name').val(data.last_name)
            $form.find('#input-phone-number').val(data.phone_number)
            $form.find('#input-role').val(data.user_role)
        }
    })
}


function populate_user_management_table(user){
    username = user['username']
    email = user['email']
    first_name = user['first_name']
    last_name = user['last_name']
    phone_number = user['phone_number']
    role = user['role']
    if (username != 'guest'){
        row_html = 
        `
        <tr>
            <th scope="row"><button class="btn btn-sm btn-success btn-edit-user" name="`+username+`">Edit</button></th>
            <th scope="row">`+username+`</th>
            <td>`+role+`</td>
        </tr>
        `
        $('.table-user-management').find('tbody').append(row_html)
    }
}


function post_edit_user_form(){
    var $form = $('#edit-user-form')
    var data = {
        'username': $form.find('#input-username').val(), 
        'email': $form.find('#input-email').val(), 
        'first_name': $form.find('#input-first-name').val(), 
        'last_name': $form.find('#input-last-name').val(), 
        'phone_number': $form.find('#input-phone-number').val(), 
        'role': $form.find('#input-role').val()
    }
    ajax_request('user_profile/', 'POST', 'update', data, true).done((data)=>{
        if (data.success){
            $('#edit-user-modal-container').modal('toggle')
            get_user_list()
            get_self_user_profile()
        }
    })
}



function post_add_user_form(){
    var $form = $('#add-user-form')
    var data = {
        'username':$form.find('#input-username').val(), 
        'email':$form.find('#input-email').val(), 
        'first_name':$form.find('#input-first-name').val(), 
        'last_name':$form.find('#input-last-name').val(), 
        'phone_number':$form.find('#input-phone-number').val(), 
        'role':$form.find('#input-role').val(),
        'password1':$form.find('#input-password1').val(),
        'password2':$form.find('#input-password2').val(),
    }
    ajax_request('user_profile/', 'POST', 'create', data, true).done((data)=>{
        if (data.success){
            $('#add-user-modal-container').modal('toggle')
            get_user_list()
        }
    })
}


function post_change_password_form(){
    var $form = $('#change-password-form')
    var data = {
        'password1': $form.find('#input-password1').val(),
        'password2': $form.find('#input-password2').val(),
        'password_old': $form.find('#input-password-old').val(),
    }
    ajax_request('user_profile/', 'POST', 'update_password', data, true).done((data)=>{
        if (data.success){
            $('#change-password-modal-container').modal('hide')
        }

    })
}


