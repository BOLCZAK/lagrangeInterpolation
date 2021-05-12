from PyQt5 import QtCore, QtGui, QtWidgets
import application
import numpy as np
import matplotlib.pyplot as plt

class MyQtApp(application.Ui_MainWindow, QtWidgets.QMainWindow):

    choosedFunction = None
    start = None
    stop = None
    node_amount = None
    interpolation_nodes = None

    def __init__(self):
        super(MyQtApp, self).__init__()
        self.setupUi(self)
        self.radioButton_liniowa.clicked.connect(self.liniowa_choosed)
        self.radioButton_wielomianowa.clicked.connect(self.wielomianowa_choosed)
        self.radioButton_trygonometryczna.clicked.connect(self.trygonometryczna_choosed)
        self.radioButton_modul.clicked.connect(self.modul_choosed)
        self.radioButton_zlozenie.clicked.connect(self.zlozona_choosed)
        self.pushButton_interpolacja.clicked.connect(self.interpolacja_button)

    def liniowa_choosed(self):
        self.label_wybranaFunkcja.setText('3*x+2')
        MyQtApp.choosedFunction = MyQtApp.liniowa

    def wielomianowa_choosed(self):
        self.label_wybranaFunkcja.setText('x**3+5*x**2-4*x-20')
        MyQtApp.choosedFunction = MyQtApp.wielomianowa

    def trygonometryczna_choosed(self):
        self.label_wybranaFunkcja.setText('3*sin(x)-cos(x)')
        MyQtApp.choosedFunction = MyQtApp.trygonometryczna

    def modul_choosed(self):
        self.label_wybranaFunkcja.setText('|x|')
        MyQtApp.choosedFunction = MyQtApp.modul

    def zlozona_choosed(self):
        self.label_wybranaFunkcja.setText('|(3*x+2)*(x**3+5*x**2-4*x-20)/(3*np.sin(x)-np.cos(x))|')
        MyQtApp.choosedFunction = MyQtApp.zlozona

    def interpolacja_button(self):
        if MyQtApp.choosedFunction is not None and self.lineEdit_zakresStart.text() != '' and self.lineEdit_zakresStop.text() != '' and self.spinBox_wezly.value() != 0:
            self.label_info.setStyleSheet("color: green;")
            self.label_info.setText("WSZYSTKIE POLA WYPEŁNIONE :)")
            MyQtApp.start = float(self.lineEdit_zakresStart.text())
            MyQtApp.stop = float(self.lineEdit_zakresStop.text())
            MyQtApp.node_amount = self.spinBox_wezly.value()
            MyQtApp.interpolation_nodes = np.sort(np.random.uniform(low=MyQtApp.start, high=MyQtApp.stop, size=MyQtApp.node_amount))
            print(MyQtApp.interpolation_nodes)
            self.label_punktyInterpolacji.setText(str(MyQtApp.interpolation_nodes))
            if MyQtApp.choosedFunction == MyQtApp.wielomianowa:
                print("TO JEST WIELOMIANOWA")
                self.label_info.setText("WSZYSTKIE POLA WYPEŁNIONE :) | KORZYSTANIE ZE SCHEMATU HORNERA")
                y1 = list(map(MyQtApp.choosedFunction, MyQtApp.interpolation_nodes))
                y_horner = []
                for x in MyQtApp.interpolation_nodes:
                    y_horner.append(self.horner([1, 5, -4, -20], 4, x))
                print(y_horner, '\n', y1)
                # wyznaczamy współczynniki
                F = self.lagrange(MyQtApp.interpolation_nodes, y_horner)
                print(F)
                # wyliczamy wartość funkcji F(x) dla "gęściej" rozmieszczonych punktów
                x2 = np.linspace(MyQtApp.start, MyQtApp.stop, 100)
                y2 = F(x2)

                plt.figure(figsize=(10, 8))
                # rysujemy nasze "punkty"
                plt.plot(MyQtApp.interpolation_nodes, y_horner, 'b.')

                # rysujemy wynik interpolacji
                plt.plot(x2, y2, 'r')

                # a powinno to wyglądać tak
                plt.plot(x2, list(map(MyQtApp.choosedFunction, x2)), 'g')
                plt.grid()
                plt.show()
            else:
                print("TO JEST INNA NIŻ WIELOMIANOWA")
                self.label_info.setText("WSZYSTKIE POLA WYPEŁNIONE :)")
                y1 = list(map(MyQtApp.choosedFunction, MyQtApp.interpolation_nodes))
                print('\n', y1)
                # wyznaczamy współczynniki
                F = self.lagrange(MyQtApp.interpolation_nodes, y1)
                print(F)
                # wyliczamy wartość funkcji F(x) dla "gęściej" rozmieszczonych punktów
                x2 = np.linspace(MyQtApp.start, MyQtApp.stop, 100)
                y2 = F(x2)

                plt.figure(figsize=(10, 8))
                # rysujemy nasze "punkty"
                plt.plot(MyQtApp.interpolation_nodes, y1, 'b.', label='Węzły')

                # rysujemy wynik interpolacji
                plt.plot(x2, y2, 'r', label='Interpolacja')

                # a powinno to wyglądać tak
                plt.plot(x2, list(map(MyQtApp.choosedFunction, x2)), 'g', label='Funkcja')
                plt.grid()
                plt.legend()
                plt.show()
        else:
            self.label_info.setStyleSheet("color: red;")
            self.label_info.setText("WYPEŁNIJ WSZYSTKIE POLA!!!")

    def horner(self, poly, n, x):

        # Zainicjowanie wyniku
        result = poly[0]

        # Oszacowanie wartości wielomianu
        # używając metody hornera
        for i in range(1, n):
            result = result * x + poly[i]

        return result

    def lagrange(self, x, w):
        M = len(x)
        p = np.poly1d(0.0)
        for j in range(M):
            pt = np.poly1d(w[j])
            for k in range(M):
                if k == j:
                    continue
                fac = x[j] - x[k]
                pt *= np.poly1d([1.0, -x[k]]) / fac
            p += pt
        return p

    liniowa = lambda x: 3*x+2
    wielomianowa = lambda x: x**3+5*x**2-4*x-20
    trygonometryczna = lambda x: 3*np.sin(x)-np.cos(x)
    # modul = lambda x: x/(x*x+0.1)**0.5
    modul = lambda x: abs(x)
    zlozona = lambda x: abs((3*x+2)*(x**3+5*x**2-4*x-20)/(3*np.sin(x)-np.cos(x)))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    ui = MyQtApp()
    # ui.setupUi(MainWindow)
    ui.show()
    sys.exit(app.exec_())
