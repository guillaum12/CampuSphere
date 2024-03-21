// Like post without reloading page
$(document).on('submit', '.like-form, .like-header-form', function(e){
  e.preventDefault()

  const post_id = $(this).attr('id')
  const url = $(this).attr('action')
  const form = $(this)

  $.ajax({
      type: 'POST',
      url: url,
      data: {
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
          'post_id':post_id,
      },
      success: function(response) {
        const icon_str_id = '#like_icon_' + post_id
        if(response['like_added']) {
            if(form.hasClass('like-form')) {
                $(icon_str_id).removeClass('black')
                $(icon_str_id).addClass('yellow')
                $(icon_str_id).next("small").html("Favori")
            } else {
                $(icon_str_id).removeClass('white')
                $(icon_str_id).addClass('yellow')
            }
        } else {
            if(form.hasClass('like-form')) {
                $(icon_str_id).removeClass('yellow')
                $(icon_str_id).addClass('black')
                $(icon_str_id).next("small").html("Ajouter aux favoris")
            } else {
                $(icon_str_id).removeClass('yellow')
                $(icon_str_id).addClass('white')
            }
        }
      },
      error: function(response) {
          console.log('error', response)
      }
  })
})
