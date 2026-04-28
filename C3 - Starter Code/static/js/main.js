let clearForm = () => {
    let form = document.getElementById('book-form');
    document.getElementById('form-errors').replaceChildren();
    form.querySelectorAll("input:not([name='csrfmiddlewaretoken'])").forEach(
        input => input.value = ''
    );

    form.querySelectorAll('select').forEach(select => select.selectedIndex = 0);

    document.querySelectorAll('.form-field-errors').forEach(errorField =>{
        errorField.replaceChildren();
    });

    removeEmptyBooksMessage();
}
// 
let removeEmptyBooksMessage = () => {
    let emptyRow = document.querySelector('.empty-message')
    if (emptyRow) {
        emptyRow.remove()
    }
}

let addEmptyBooksMessage = () => {
    let tbody = document.querySelector('#book-table > tbody');
    let rows = tbody.querySelectorAll('tr:not(.empty-message)');
    if (rows.length === 0) {
        let tr = document.createElement('tr');
        tr.classList.add('empty-message');
        tr.innerHTML = '<td>You have no books in your library</td>';
        tbody.appendChild(tr);
    }
}

let fadeOutAndRemove = (row) => {
    row.style.transition = 'opacity 0.5s';
    row.style.opacity = '0';
    setTimeout(() => {
        row.remove();
        addEmptyBooksMessage(); // siempre va aquí
    }, 500);
}