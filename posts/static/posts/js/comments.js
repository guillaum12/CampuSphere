// Comment without reloading page
function submitCommentAsync(commentForm, e){
  e.preventDefault()

  const post_id = $(commentForm).attr('id')
  const url = $(commentForm).attr('action')
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
        let comment_html = response['comment_html'];
        textarea.value = "";
        $('#custom-comment-' + post_id).find('.comment-replies:first').prepend(comment_html);
        // On ajoute la méthode AJAX pour les nouveaux commentaires
        $('#custom-comment-' + post_id).find('.comment-replies:first').find('.comment-form:first').submit(function(e){
            submitCommentAsync(this, e);
        })
    },
      error: function(response) {
          console.log('error', response)
      }
  })
}

// Envoyer les commentaires sans recharger la page
$('.comment-form').submit(function(e){
    submitCommentAsync(this, e);
})

// Envoyer le commentaire si les touches "Enter" et "Ctrl" sont pressées
$(document).ready(function () {
    $('.comment-form').on('keydown', 'textarea', function (e) {
        if (e.key === 'Enter' && !e.ctrlKey) {
            e.preventDefault();
            $(this).closest('form').submit();
        }
    });
});