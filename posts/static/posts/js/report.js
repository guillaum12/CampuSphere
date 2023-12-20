// Like post without reloading page
$('.report-form').submit(function(e){
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
          const icon_str_id = '#report_icon_' + post_id
          if(response['report_added']) {
              $(icon_str_id).removeClass('grey')
              $(icon_str_id).addClass('red')
          } else {
              $(icon_str_id).removeClass('red')
              $(icon_str_id).addClass('grey')
          }
        },
        error: function(response) {
            console.log('error', response)
        }
    })
  })
  