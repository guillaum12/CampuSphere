// Comment without reloading page
$('.comment-form').submit(function(e){
  e.preventDefault()

  const post_id = $(this).attr('id')
  const url = $(this).attr('action')
  var textarea = document.querySelector('textarea[id="textComment' + post_id + '"]');
  const commentText = textarea.value; 

  if (commentText.trim() === '') {
    // If it's blank, you can choose to alert the user or handle it in another way
    alert('Comment cannot be empty!');
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
        $('#comment-box-' + post_id).prepend(comment_html);
    },
      error: function(response) {
          console.log('error', response)
      }
  })
})

$(document).ready(function () {
    $('.comment-form').on('keydown', 'textarea', function (e) {
        if (e.key === 'Enter' && !e.ctrlKey) {
            e.preventDefault();
            $(this).closest('form').submit();
        }
    });
});
