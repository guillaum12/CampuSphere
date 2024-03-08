$(document).on('click', '.feedback input[type="radio"]', function (e) {
    var radio_button = $(this);
    var post_power = $(this).val();
    var form = $(this).closest('form');
    var post_id = form.find("input[name='post_id']").val()
    var csrf_token = form.find('input[name="csrfmiddlewaretoken"]').val();
    var url = form.attr('action');
    
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'csrfmiddlewaretoken': csrf_token,
            'post_id':post_id,
            'power_amount':post_power,
        },
        success: function(response) {
            if (response['power_added']) {
                $('#progress_zone_' + post_id).css("display", "block");
                
                // update progress number
                var progress_number = $('#post_progress_' + post_id);
                progress_number.text(response['post_progress']);

                // Update voter number
                var voter_number = $('#voter_number_' + post_id);
                voter_number.text(response['voter_number']);

                // Update progress bar style
                var progressBar = $('#progress_bar_' + post_id);
                progressBar.css("width",response['post_progress'] + '%');
                progressBar.css("background", response['post_color']);

                // On ajoute la classe power-saved au bouton pour développer la possibilité de voter
                $('#developVoteButton'+post_id).addClass('power-saved')
            }
            else{
                $('#progress_zone_' + post_id).css("display", "none");
                // On enleve le vote
                radio_button.prop('checked', false);
                
                // On retire la classe power-saved au bouton pour développer la possibilité de voter
                $('#developVoteButton'+post_id).removeClass('power-saved')
            }
            // On ferme le collapse pour le vote
            var powerCollapse = new bootstrap.Collapse($("#powerCollapse" + post_id))
            console.log(powerCollapse)
            powerCollapse.hide()
        },
        error: function(response) {
            console.log('error', response)
        }
    });
});