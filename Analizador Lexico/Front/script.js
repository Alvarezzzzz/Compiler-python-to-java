var pyqt;

// Configurar el canal WebChannel cuando la página cargue
new QWebChannel(qt.webChannelTransport, function(channel) {
    pyqt = channel.objects.pyqt;  // Obtener la instancia de pyqt
});

function handleFileUpload(event) {
    const file = event.target.files[0]; // Obtiene el primer archivo seleccionado
    if (file) {
        const reader = new FileReader(); // Crea un lector de archivos
        reader.onload = function(e) {
            const content = e.target.result; // Obtiene el contenido del archivo
            document.querySelector('.main__editor-textarea').value = content; // Lo coloca en el textarea
            event.target.value = ""; // Reinicia la lista de archivos
        };
        reader.readAsText(file); // Lee el archivo como texto
    }
}




function sendDataToPython() {
    const opcion = document.getElementById('opcion').value; //Se obtiene la opcion del usuario

    const content = document.querySelector('.main__editor-textarea').value;
    if (window.pyqt && opcion == 'analisis_lexico') {
        window.pyqt.sendData(content);
    } else if (window.pyqt && opcion == 'analisis_sintactico') {
        window.pyqt.sendDataSintactico(content);
    } else if (window.pyqt && opcion == 'compilador') {
        window.pyqt.sendDataTranslator(content);
    }
    else {
        console.error("PyQt bridge is not available.");
    }
}

function clearEditor() {
    document.querySelector('.main__editor-textarea').value = '';
    document.querySelector('.main__result-container').innerHTML = '';
}



function handlePythonData(data) {
    // Recibir los datos procesados por Python y mostrarlo en la interfaz
    document.getElementsByClassName('main__result-container')[0].innerHTML = data.slice(1, -1);
}

/* Funcion que convierte los < y > en &lt; y &gt; */
function convertToHTML(data) {
    return data.replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function handlePythonDataSintactico(data) {
    // Recibir los datos procesados por Python y mostrarlo en la interfaz
    document.getElementsByClassName('main__result-container')[0].innerHTML = convertToHTML(data).slice(1, -1);
}

function handlePythonDataTranslator(data) {
    document.getElementsByClassName('main__result-container')[0].innerHTML = convertToHTML(data).slice(1, -1);
}

document.addEventListener("DOMContentLoaded", function () {
    const resizable = document.getElementById("resizable"); // Asegúrate de que este ID sea correcto
    let isResizing = false;
    let startX, startWidth;

    function startResize(e) {
        isResizing = true;
        startX = e.clientX;
        startWidth = resizable.getBoundingClientRect().width; // Usa getBoundingClientRect() para precisión

        document.addEventListener("mousemove", resize);
        document.addEventListener("mouseup", stopResize);
    }

    function resize(e) {
        if (!isResizing) return;
        const deltaX = startX - e.clientX; // Calculamos la diferencia con el sentido invertido
        let newWidth = startWidth + deltaX; // Restamos deltaX si el mouse se mueve a la izquierda y sumamos si va a la derecha

        resizable.style.width = `${newWidth}px`; // Aplica el nuevo ancho directamente
    }

    function stopResize() {
        isResizing = false;
        document.removeEventListener("mousemove", resize);
        document.removeEventListener("mouseup", stopResize);
    }

    document.querySelector(".resize-handle").addEventListener("mousedown", startResize);
});
