const searchInput = document.getElementById('searchInput');
    const cards = document.querySelectorAll('.card'); // seelecciona todas las tarjetas

    searchInput.addEventListener('input', function () {
        const searchText = searchInput.value.toLowerCase();

        cards.forEach(card => {
            const titleElement = card.querySelector('.card-title'); // encuentra el elemento del titulo en la tarjeta
            if (!titleElement) return; // saltar si no se encuentra el elemento de título

            const titleText = titleElement.textContent.toLowerCase();
            if (titleText.includes(searchText)) {
                card.style.display = ''; // muestra la tarjeta si coincide el titulo
            } else {
                card.style.display = 'none'; // oculta la tarjeta si no coincide el titulo
            }
        });
    });