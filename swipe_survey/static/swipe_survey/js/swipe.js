$(document).ready(function() {
    $(".survey-card").each(function(index, card) {
        let startX, startY;
        let direction_swipe = '';
        let abort_swipe = false;
        let isDragging = false;
        const nbCards = $(".survey-card").length;

        card.addEventListener('touchstart', touchStart);
        card.addEventListener('touchmove', touchMove);
        card.addEventListener('touchend', touchEnd);
        card.addEventListener('mousedown', mouseDown);
        card.addEventListener('mousemove', mouseMove);
        card.addEventListener('mouseup', mouseUp);
        card.addEventListener('mouseleave', mouseLeave);

        function touchStart(e) {
            if (card.classList.contains("current") === false) {
                return;
            }
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
            direction_swipe = '';
            abort_swipe = false;
            isDragging = false;
            card.classList.remove('drag-right');
            card.classList.remove('drag-left');
            card.classList.remove('drag-up');
            card.classList.remove('drag-down');
        }

        function touchMove(e) {
            if (abort_swipe || isDragging) {
                return;
            }
            const xDiff = e.touches[0].clientX - startX;
            const yDiff = e.touches[0].clientY - startY;
            detectSwipe(xDiff, yDiff);
        }

        function touchEnd(e) {
            handleSwipe();
        }

        function mouseDown(e) {
            if (card.classList.contains("current") === false) {
                return;
            }
            startX = e.clientX;
            startY = e.clientY;
            isDragging = true;
            abort_swipe = false;
        }

        function mouseMove(e) {
            if (!isDragging || abort_swipe) {
                return;
            }
            const xDiff = e.clientX - startX;
            const yDiff = e.clientY - startY;
            detectSwipe(xDiff, yDiff);
        }

        function mouseUp(e) {
            if (!isDragging) {
                return;
            }
            handleSwipe();
            isDragging = false;
        }

        function mouseLeave(e) {
            if (!isDragging) {
                return;
            }
            handleSwipe();
            isDragging = false;
        }

        function detectSwipe(xDiff, yDiff) {
            if (direction_swipe === '') {
                if (Math.abs(xDiff) > Math.abs(yDiff)) {
                    if (xDiff > 0) {
                        direction_swipe = 'right';
                        card.classList.add('drag-right');
                    } else {
                        direction_swipe = 'left';
                        card.classList.add('drag-left');
                    }
                } else {
                    if (yDiff > 0) {
                        direction_swipe = 'down';
                        card.classList.add('drag-down');
                    } else {
                        direction_swipe = 'up';
                        card.classList.add('drag-up');
                    }
                }
            }
            // Détection de l'annulation du swipe
            if (direction_swipe === 'right' && xDiff < 0) {
                direction_swipe = '';
                card.classList.remove('drag-right');
                abort_swipe = true;
            } else if (direction_swipe === 'left' && xDiff > 0) {
                direction_swipe = '';
                card.classList.remove('drag-left');
                abort_swipe = true;
            } else if (direction_swipe === 'down' && yDiff < 0) {
                direction_swipe = '';
                card.classList.remove('drag-down');
                abort_swipe = true;
            } else if (direction_swipe === 'up' && yDiff > 0) {
                direction_swipe = '';
                card.classList.remove('drag-up');
                abort_swipe = true;
            }
        }

        function handleSwipe() {
            if (abort_swipe) {
                card.classList.remove('drag-right');
                card.classList.remove('drag-left');
                card.classList.remove('drag-up');
                card.classList.remove('drag-down');
                return;
            }
            if (["left", "right", "up", "down"].includes(direction_swipe)) {
                animateSwipe(card, direction_swipe);
            }
        }

        function animateSwipe(card, direction) {
            card.style.transition = "0.6s ease-out";
            card.classList.remove('current');
            classes = card.classList;
            order = Array.from(classes).filter(className => className.startsWith('order-'))[0];
            order = parseInt(order.split('-')[1]);
            switch (direction) {
                case 'right':
                    card.classList.add('swipe-right');
                    card.classList.remove('drag-right');
                    break;
                case 'left':
                    card.classList.add('swipe-left');
                    card.classList.remove('drag-left');
                    break;
                case 'up':
                    card.classList.add('swipe-up');
                    card.classList.remove('drag-up');
                    break;
                case 'down':
                    card.classList.add('swipe-down');
                    card.classList.remove('drag-down');
                    break;
            }
            // Remove card from DOM after animation
            setTimeout(() => {
                if (order < nbCards - 1) {
                    let nextCard = $(".survey-card.order-" + (order + 1));
                    nextCard.addClass('current');
                }
            }, 100);
            setTimeout(() => {
                card.remove();
            }, 600);
        }
    });
});
