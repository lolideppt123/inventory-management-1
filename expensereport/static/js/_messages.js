setTimeout(() => {
    var alertId = document.getElementById('myAlert');
    alertId.classList.add('fade-out')
}, 500);

setTimeout(() => {
    var alertId = document.getElementById('myAlert');
    alertId.style.display = 'none';
}, 4000)