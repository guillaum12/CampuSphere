// Like post without reloading page
$(document).on('click', '.like-comment-form label', function (e) {
  e.preventDefault()
  const form = $(this).closest('.like-comment-form')
  const comment_id = form.find('input[name=comment-id]').val()
  const url = form.attr('action')
  const like_status = $(this).find("input[name='like-button']").val()
  console

  $.ajax({
      type: 'POST',
      url: url,
      data: {
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
          'post_id':comment_id,
          'like_status':like_status,
      },
      success: function(response) {
        const icon_str_id = '#like_icon_' + comment_id
        if(response['like_added']) {
            if (like_status == 0) {
                // On incrémente le nombre de dislikes
                form.find("span.dislikes-count").text(parseInt(form.find("span.dislikes-count").text()) + 1)
                // On décrémente le nombre de likes si l'utilisateur a déjà liké le commentaire
                if (!form.find("i.icon.thumbs.up").hasClass("outline")) {
                    form.find("span.likes-count").text(parseInt(form.find("span.likes-count").text()) - 1)
                }
                form.find("i.icon.thumbs.up").addClass("outline")
                form.find("i.icon.thumbs.down").removeClass("outline")
            }
            else if (like_status == 1) {
                // On incrémente le nombre de likes
                form.find("span.likes-count").text(parseInt(form.find("span.likes-count").text()) + 1)
                // On décrémente le nombre de dislikes si l'utilisateur a déjà disliké le commentaire
                if (!form.find("i.icon.thumbs.down").hasClass("outline")) {
                    form.find("span.dislikes-count").text(parseInt(form.find("span.dislikes-count").text()) - 1)
                }
                form.find("i.icon.thumbs.up").removeClass("outline")
                form.find("i.icon.thumbs.down").addClass("outline")
            }
        } else {
            // On décrémente le nombre de likes ou de dislikes au besoin
            if (!form.find("i.icon.thumbs.up").hasClass("outline")) {
                form.find("span.likes-count").text(parseInt(form.find("span.likes-count").text()) - 1)
            }
            if (!form.find("i.icon.thumbs.down").hasClass("outline")) {
                form.find("span.dislikes-count").text(parseInt(form.find("span.dislikes-count").text()) - 1)
            }
            form.find("i.icon.thumbs").addClass("outline")
        }
      },
      error: function(response) {
          console.log('error', response)
      }
  })
})
