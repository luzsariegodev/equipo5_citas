function validar_formulario(){
    var username = document.formRegistro.username;
    var email = document.formRegistro.correo;
    var password = document.formRegistro.password;
    var username_len = username.value.length;
    if (username_len == 0 || username_len < 8) {
        alert("Debes ingresar un username con min. 8 caracteres");
        username.focus();
        return false; //Para la parte dos, que los datos se conserven
    }
    /* Formato email es una variable de tipo REGEXP lo cual nos sirve para almacenar
    patrones de expresiones regulares */
    var formato_email = /^\w+([\.-]?\w+)@\w+([\.-]?\w+)(\.\w{2,3})+$/;
        if (!email.value.match(formato_email)) {
        alert("Debes ingresar un email electronico valido!");
        email.focus();
        return false; //Para la parte dos, que los datos se conserven
    }
    var passid_len = password.value.length;
        if (passid_len == 0 || passid_len < 8) {
        alert("Debes ingresar una password con mas de 8 caracteres");
        password.focus();
    }
}

function mostrarPassword(){
    document.formRegistro.contraseña.type = "text";
}

function ocultarPassword(){
    document.formRegistro.contraseña.type = "password";
}