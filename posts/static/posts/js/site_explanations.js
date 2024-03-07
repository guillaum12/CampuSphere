// Report post without reloading page
$(document).on('submit', '.form-hide-site-explanations', function(e){
    e.preventDefault()
    
    const profile_id = $('.form-hide-site-explanations input[name=profile_id]').val();
    const url = $(this).attr('action')
    console.log(url)
  
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'csrfmiddlewaretoken': $('.form-hide-site-explanations  input[name=csrfmiddlewaretoken]').val(),
            'profile_id': profile_id,
        },
        success: function(response) {
            // Ajout du toast
            let toast = response['toast_html'];
            $('#toasts-container').append(toast);
            // Hide the explanations
            welcomeModal.hide();
        },
        error: function(response) {
            console.log('error', response)
        }
    })
  })

