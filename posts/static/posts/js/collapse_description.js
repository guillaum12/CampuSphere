// Au chargement du document on affiche toutes les descriptions .description-preview-post-short
$(document).ready(function() {
    descriptions_to_display = $('.description-preview-post-short');
    descriptions_to_display.each(function() {
        myCollapse = new bootstrap.Collapse($(this));
        myCollapse.show();
    })
})

$(document).on("click", ".display-full-description-preview-post", function() {
    if ($(this).children("small").text() === "Afficher plus") {
        $(this).children("small").text("Masquer le détail")
        $(this).children("i.icon").addClass("up")
        $(this).children("i.icon").removeClass("down")
    }
    else {
        $(this).children("small").text("Afficher plus")
        $(this).children("i.icon").addClass("down")
        $(this).children("i.icon").removeClass("up")
    }
} )