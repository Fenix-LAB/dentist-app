from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo   # Modulo Serial de PyQt5
from PyQt5.QtCore import *                                    # Modulo PyQt5 para intarfaces graficas
from gui_design import *
from PyQt5.QtGui import *
import pyqtgraph as pg
import numpy as np

#Clase de la ventana heredada de la interfaz "gui_design.py"
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    # Se define le contructor con todos los atributos necesarios y asociacion de metodos
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        # Usamos la funcion QPoint() para guardar la posicion del mouse
        self.click_position = QPoint()
        self.btn_menu.clicked.connect(self.mover_menu)

        # Se configura la ventana asociando los eventos con metodos
        self.btn_normal.hide()
        self.btn_min.clicked.connect(lambda: self.showMinimized())
        self.btn_cerrar.clicked.connect(self.control_btn_cerrar)
        self.btn_normal.clicked.connect(self.control_btn_normal)
        self.btn_max.clicked.connect(self.control_btn_maximizar)
        self.btn_45_grd.clicked.connect(self.set_45_degrees)
        self.btn_55_grd.clicked.connect(self.set_55_degrees)
        self.btn_boca_cerrada.clicked.connect(self.set_0_degrees)


        # Se elimina la barra de titulo por default
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Size grip
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)

        # Movimiento de la ventana
        self.frame_superior.mouseMoveEvent = self.mover_ventana

        # Control connect
        self.serial = QSerialPort()
        self.btn_actualizar.clicked.connect(self.read_ports)
        self.btn_conectar.clicked.connect(self.serial_conect)
        self.btn_desconectar.clicked.connect(lambda: self.serial.close())

        # Asociacion de metodos
        self.serial.readyRead.connect(self.read_data)

        # Graficas
        self.x = list(np.linspace(0, 100, 100))
        self.y = list(np.linspace(0, 0, 100))

        # Creacion de la grafica 1
        # pg.setConfigOption('background', '#ebfeff')
        # pg.setConfigOption('foreground', '#000000')
        # self.plt = pg.PlotWidget(title='Apertura')
        # self.graph_apertura.addWidget(self.plt)
        pg.setConfigOption('background', '#ebfeff')
        pg.setConfigOption('foreground', '#000000')
        self.plt = pg.PlotWidget(title='Apertura')
        self.plt.getAxis('left').setTicks([])  # Oculta los ticks del eje Y
        self.plt.getAxis('bottom').setTicks([])  # Oculta los ticks del eje X
        self.graph_apertura.addWidget(self.plt)

        # Se inician los siguientes metodos y atributos adicionles
        self.read_ports()

    def set_55_degrees(self):
        print("55")
        self.plt.clear()
        # first point
        x = np.linspace(0, 0, 100)
        y = np.linspace(0, 0, 100)
        # second point
        x = np.linspace(0, 70, 100)
        y = np.linspace(0, 100, 100)
        self.plt.plot(x, y, pen=pg.mkPen('#1300FF', width=2))
        print("done")

    def set_0_degrees(self):
        print("0")
        self.plt.clear()
        # first point
        x = np.linspace(0, 0, 100)
        y = np.linspace(0, 0, 100)
        # second point
        x = np.linspace(0, 100, 100)
        y = np.linspace(0, 0, 100)
        self.plt.plot(x, y, pen=pg.mkPen('#1300FF', width=2))
        print("done")

    def set_45_degrees(self):
        print("45")
        self.plt.clear()
        # first point
        x = np.linspace(0, 0, 100)
        y = np.linspace(0, 0, 100)
        # second point
        x = np.linspace(0, 100, 100)
        y = np.linspace(0, 100, 100)
        self.plt.plot(x, y, pen=pg.mkPen('#1300FF', width=2))
        print("done")

    # Metodo del boton de menu
    def mover_menu(self):
        if True:
            width = self.frame_menu.width()
            normal = 0
            if width == 0:
                extender = 250
            else:
                extender = normal
            self.animacion = QPropertyAnimation(self.frame_menu, b'minimumWidth')
            self.animacion.setDuration(300)
            self.animacion.setStartValue(width)
            self.animacion.setEndValue(extender)
            self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animacion.start()

    # Metodo del boton cerrar
    def control_btn_cerrar(self):
        self.close()
        # cap.release()
        self.label.clear()

    # Metodo del boton de ventana normal
    def control_btn_normal(self):
        self.showNormal()
        self.btn_normal.hide()
        self.btn_max.show()

    # Metodo del boton de minimizar
    def control_btn_maximizar(self):
        self.showMaximized()
        self.btn_max.hide()
        self.btn_normal.show()

    # Metodo para redimensionar la ventana
    def resizeEvent(self, event):
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)

    def mousePressEvent(self, event):
        self.click_posicion = event.globalPos()

    # Metodo para mover la ventana por la barra de titulo
    def mover_ventana(self, event):
        if self.isMaximized() == False:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.click_posicion)
                self.click_posicion = event.globalPos()
                event.accept()
        if event.globalPos().y() <= 5 or event.globalPos().x() <= 5:
            self.showMaximized()
            self.btn_max.hide()
            self.btn_normal.show()
        else:
            self.showNormal()
            self.btn_normal.hide()
            self.btn_max.show()

    # Metodo para leer los puertos y seleccionar la velocidad de los datos
    def read_ports(self):
        self.baudrates = ['1200', '2400', '4800', '9600', '19200', '34800', '115200']
        portList = []
        ports = QSerialPortInfo().availablePorts()
        for i in ports:
            portList.append(i.portName())

        self.comboBox_puerto.clear()
        self.comboBox_velocidad.clear()
        self.comboBox_puerto.addItems(portList)
        self.comboBox_velocidad.addItems(self.baudrates)
        self.comboBox_velocidad.setCurrentText("115200")      # Se coloca por default una velocidad de  9600 baudios

    # Conexion con las caracteristicas especificadas de velocidad y puerto
    def serial_conect(self):
        self.serial.waitForReadyRead(100)
        self.port = self.comboBox_puerto.currentText()
        self.baud = self.comboBox_velocidad.currentText()
        self.serial.setBaudRate(int(self.baud))
        self.serial.setPortName(self.port)
        self.serial.open(QIODevice.ReadWrite)

    # Metodo para leer datos seriales (No se uso en esta aplicacion)
    def read_data(self):
        if not self.serial.canReadLine(): return
        rx = self.serial.readLine()
        datos = str(rx, 'utf-8').strip()
        listaDatos = datos.split(",")
        self.dato1 = listaDatos[0]
        self.dato2 = listaDatos[1]
        self.dato3 = listaDatos[2]
        print(self.dato1)
        print(self.dato2)
        print(self.dato3)

        x1 = float(self.dato3)

        self.y = self.y[1:]
        self.y.append(x1)

        self.plt.clear()
        self.plt.plot(self.x, self.y, pen=pg.mkPen('#1300FF', width=2))

        self.showInfo()

    def showInfo(self):
        self.val_RC.setText(str(self.dato1))
        self.val_porcentaje.setText(str(self.dato2))
        self.indicator_oxigeno(int(self.dato3))

    # Metodo para enviar datos por comunicacion Serial
    def send_data(self, data):
        data = data + "\n"
        #data = data
        #print(data)
        if self.serial.isOpen():
            self.serial.write(data.encode())
            #print("enviado")

    def indicator_oxigeno(self, val):
        # Indicador de temperatura
        estilo_temp = """QFrame{
        border-radius: 100px;
        background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{stop1} rgba(255, 72, 72, 255), stop:{stop2} rgba(255, 188, 188, 80));
        }"""
        # Indicadores de 0 a 1
        # Stop2 es el valor al que se coloca el indicador
        if val > 100 or val < 0:
            self.val_acotado = 100

        self.val_porcentaje.setText(str(self.val_acotado))

        self.val_map = val/100
        stop2 = val
        stop1 = stop2 - 0.001
        Sstop1 = str(stop1)
        Sstop2 = str(stop2)
        nuevo_estilo = estilo_temp.replace('{stop1}', Sstop1).replace('{stop2}', Sstop2)
        self.Indicador_OS.setStyleSheet(nuevo_estilo)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MyApp()
    window.show()
    app.exec_()