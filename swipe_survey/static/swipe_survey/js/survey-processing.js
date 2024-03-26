// Une fois tout les éléments chargés
document.addEventListener('DOMContentLoaded', function () {
    survey = $(".survey-container");
    nbCards = survey.find(".survey-card").length;
    for (let i = 0; i < nbCards; i++) {
        let card = $(".survey-card.order-" + i);
        card.css("z-index", nbCards - i);
    }
});