// Like post without reloading page
$('.like-form').submit(function(e){
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
        const icon_str_id = '#like_icon_' + post_id
        console.log('like_added', response['like_added'])
        if(response['like_added']) {
            $(icon_str_id).removeClass('black')
            $(icon_str_id).addClass('yellow')
        } else {
            $(icon_str_id).removeClass('yellow')
            $(icon_str_id).addClass('black')
        }
      },
      error: function(response) {
          console.log('error', response)
      }
  })
})
