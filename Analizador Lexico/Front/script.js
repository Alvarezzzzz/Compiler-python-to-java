var pyqt;

        // Configurar el canal WebChannel cuando la página cargue
        new QWebChannel(qt.webChannelTransport, function(channel) {
            pyqt = channel.objects.pyqt;  // Obtener la instancia de pyqt
        });

        function sendDataToPython() {
            
            const data = document.getElementsByClassName('main__editor-textarea')[0].value; 
            // Enviar datos a Python usando el canal
            if (pyqt) {
                pyqt.sendData(data);
            }
        }

        function processResult(result) {
            // Reemplazar 'noseN' con 'N' espacios
            result = result.replace(/nose(\d+)/g, (match, p1) => ' '.repeat(Number(p1)));
        
            // Reemplazar 'noseSalto' con un salto de línea
            result = result.replace(/noseSalto/g, '\n');
        
            return result;
        }
        

        function handlePythonData(data) {
            // Recibir los datos procesados por Python y mostrarlo en la interfaz

            document.getElementsByClassName('main__result-container')[0].innerHTML = data.slice(1, -1);
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
        