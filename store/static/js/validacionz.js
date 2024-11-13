


document.getElementById('form').addEventListener('submit', function(e){
    let nombre = document.getElementById('nombre').value;
    let correo = document.getElementById('correo').value;
    let mensaje = document.getElementById('mensaje').value;
    if(nombre === '' || correo === '' || mensaje === ''){
        alert('rellene los campos vacios porfavor');
        e.preventDefault();
    }

    
});