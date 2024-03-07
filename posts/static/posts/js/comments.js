// Comment without reloading page
$(document).on('submit', '.comment-form', function(e){
  e.preventDefault()

  const post_id = $(this).attr('id')
  const url = $(this).attr('action')
  var textarea = document.querySelector('textarea[id="textComment' + post_id + '"]');
  const commentText = textarea.value; 

  if (commentText.trim() === '') {
    // If it's blank, you can choose to alert the user or handle it in another way
    alert('Veuillez remplir un commentaire avant de l\'envoyer.');
    return; // Stop the code execution
  }

  $.ajax({
      type: 'POST',
      url: url,
      data: {
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
          'post_id':post_id,
          'content': commentText
      },
    success: function(response) {
        if ("comment_html" in response){
            let comment_html = response['comment_html'];
            textarea.value = "";
            $('#custom-comment-' + post_id).find('.comment-replies:first').prepend(comment_html);
        }
        // Ajout du toast
        let toast = response['toast_html'];
        $('#toasts-container').append(toast);
        // On ferme le collapse de réponse si c'est une réponse à un commentaire
        if ($('#collapseReply'+post_id).length){
            collapseCommentForm = new bootstrap.Collapse($("#collapseReply"+post_id))
            collapseCommentForm.hide()
        }
    },
      error: function(response) {
          console.log('error', response)
      }
  })
})

// Envoyer le commentaire si les touches "Enter" et "Ctrl" sont pressées
$(document).on('keydown', '.comment-form textarea', function (e) {
    if (e.key === 'Enter' && e.ctrlKey) {
        e.preventDefault();
        $(this).closest('form').submit();
    }
});