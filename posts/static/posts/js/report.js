// Report post without reloading page
$(document).on('submit', '.report-form', function(e){
    e.preventDefault()
  
    const post_id = $(this).attr('id')
    const url = $(this).attr('action')
  
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            'post_id':post_id,
        },
        success: function(response) {
            const button_str_id = '#report_button_' + post_id
            if(response['report_added']) {
                $(button_str_id).addClass('red')
            } else {
                $(button_str_id).removeClass('red')
            }
            // Ajout du toast
            let toast = response['toast_html'];
            $('#toasts-container').append(toast);
        },
        error: function(response) {
            console.log('error', response)
        }
    })
  })

