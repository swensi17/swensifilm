// Добавляем обработчик для постеров в результатах поиска
document.addEventListener('DOMContentLoaded', function() {
    const movieCards = document.querySelectorAll('.movie-card');
    
    movieCards.forEach(card => {
        card.addEventListener('click', function() {
            const movieId = this.dataset.movieId;
            if (movieId) {
                window.location.href = `/movie/${movieId}`;
            }
        });
    });
}); 