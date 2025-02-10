import sys
from PyQt6.QtCore import QUrl, pyqtSlot, QObject
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel
import lexer
import json

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Web Communication Example")
        self.setGeometry(100, 100, 800, 600)

        # Configuramos el QWebEngineView
        self.browser = QWebEngineView(self)
        self.browser.setGeometry(0, 0, self.width(), self.height())  # Ajustar automáticamente

        # Cargamos el archivo HTML con la ruta correcta
        # Cargamos el archivo HTML con la ruta correcta
        #self.browser.setUrl(QUrl("file:///D:/Repo%20Compilador/Trasnspiler-python-to-java/Analizador%20Lexico/Front/index.html"))
        self.browser.setUrl(QUrl.fromLocalFile("c:/Users/yourb/OneDrive/Desktop/traductores/Trasnspiler-python-to-java/Analizador Lexico/Front/index.html"))

        
        # Configurar QWebChannel
        self.channel = QWebChannel()
        self.browser.page().setWebChannel(self.channel)

        # Registrar la función de Python en el canal
        self.pyqt = PyQtBridge(self)
        self.channel.registerObject("pyqt", self.pyqt)
        
        self.show()

    @pyqtSlot(str)
    def on_receive_data(self, data):
        print(f"Data received from JS: \n{data}")
        # Realizamos alguna operación en Python (por ejemplo, procesar la cadena recibida)
        result = lexer.test_lexer(data)
        return result

    def resizeEvent(self, event):
        # Hacer que el contenido HTML se ajuste correctamente al tamaño de la ventana
        self.browser.setGeometry(0, 0, self.width(), self.height())  # Ajustar dinámicamente
        super().resizeEvent(event)

class PyQtBridge(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot(str)
    def sendData(self, data):
        result = self.parent().on_receive_data(data)
        print(result)

        safe_result = json.dumps(result)  # Escapa la cadena para evitar problemas con caracteres especiales
        print(safe_result)

        # Enviar datos procesados de vuelta a JS
        self.parent().browser.page().runJavaScript(f"handlePythonData('{safe_result}')")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec())
