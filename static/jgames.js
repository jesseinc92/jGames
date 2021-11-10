document.addEventListener('DOMContentLoaded', () => {
    
    // GAME DETAILS HTML WORKAROUND

    const description = document.querySelector('#game-desc');

    if (description) {
        description.innerHTML = description.innerText;
    }

});