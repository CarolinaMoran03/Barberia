
function onSelectChange() {
    const select = document.getElementById('opciones')
    // Extrae el valor del elemento select
    const valorBarberia = select.value;

    // Haz algo con el valor
    // Por ejemplo, puedes mostrarlo en la consola
    console.log(valorBarberia);
}

// Asocia la función al evento "change" del elemento select
select.addEventListener("change", onSelectBarberiaChange);