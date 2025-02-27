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

function toggleBio() {
    const bioText = document.querySelector('.bio-text');
    const readMoreBtn = document.querySelector('.btn-read-more');
    
    if (bioText.classList.contains('collapsed')) {
        bioText.classList.remove('collapsed');
        bioText.classList.add('expanded');
        readMoreBtn.innerHTML = '<span>Свернуть</span><i class="fas fa-chevron-up"></i>';
    } else {
        bioText.classList.remove('expanded');
        bioText.classList.add('collapsed');
        readMoreBtn.innerHTML = '<span>Читать далее</span><i class="fas fa-chevron-down"></i>';
    }
}

// Обновим функцию открытия модального окна актера
async function openActorModal(actorId) {
    const modal = new bootstrap.Modal(document.getElementById('actorModal'));
    
    try {
        const response = await fetch(`/api/actor/${actorId}`);
        const actor = await response.json();
        
        // Заполняем модальное окно данными
        document.getElementById('actorModalPhoto').src = actor.profile_path ? 
            `https://image.tmdb.org/t/p/w500${actor.profile_path}` : '';
        document.getElementById('actorModalName').textContent = actor.name;
        
        // Обновляем биографию с новой структурой
        const bioElement = document.getElementById('actorBio');
        bioElement.textContent = actor.biography || 'Биография отсутствует';
        bioElement.classList.add('collapsed');
        bioElement.classList.remove('expanded');
        
        // Сбрасываем кнопку "Читать далее"
        const readMoreBtn = bioElement.nextElementSibling.nextElementSibling;
        readMoreBtn.innerHTML = '<span>Читать далее</span><i class="fas fa-chevron-down"></i>';
        readMoreBtn.classList.remove('expanded');
        
        document.getElementById('actorModalBirthday').textContent = actor.birthday || 'Неизвестно';
        document.getElementById('actorModalBirthplace').textContent = actor.place_of_birth || 'Неизвестно';
        
        // Заполняем фильмографию
        const filmography = document.getElementById('actorFilmography');
        filmography.innerHTML = actor.credits.cast.map(movie => `
            <div class="film-card" onclick="window.location.href='/movie/${movie.id}'">
                <img src="https://image.tmdb.org/t/p/w342${movie.poster_path}" 
                     alt="${movie.title}" 
                     class="film-poster">
                <div class="film-info">
                    <div class="film-title">${movie.title}</div>
                    <div class="film-year">${movie.release_date.split('-')[0]}</div>
                </div>
            </div>
        `).join('');
        
        modal.show();
    } catch (error) {
        console.error('Error fetching actor data:', error);
    }
} 