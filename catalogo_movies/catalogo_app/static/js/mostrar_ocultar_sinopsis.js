// selecciona todos los elementos con la clase 'leer-sinopsis' y agrega un evento de clic a cada uno
document.querySelectorAll('.leer-sinopsis').forEach(function(btn) {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        // encuentra el elemento hermano anterior (suponiendo que sea el elemento de la sinopsis)
        var sinopsis = btn.previousElementSibling;
        // si la sinopsis esta oculta o no tiene un estilo de visualizacion, muestra y cambia el texto del boton por 'Ocultar Sinopsis'
        if (sinopsis.style.display === 'none' || sinopsis.style.display === '') {
            sinopsis.style.display = 'block';
            btn.textContent = 'Ocultar Sinopsis';
        } else {
            // si la sinopsis es visible, oculta y cambia el texto del boton por 'Leer Sinopsis'
            sinopsis.style.display = 'none';
            btn.textContent = 'Leer Sinopsis';
        }
    });
});
