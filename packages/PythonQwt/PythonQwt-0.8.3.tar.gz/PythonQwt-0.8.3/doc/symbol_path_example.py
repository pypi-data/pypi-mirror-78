from qtpy import QtWidgets as QW
from qtpy import QtGui as QG
from qtpy import QtCore as QC
import qwt
import numpy as np
import os.path as osp

app = QW.QApplication([])

# --- Construct custom symbol ---

path = QG.QPainterPath()
path.moveTo(0, 8)
path.lineTo(0, 5)
path.lineTo(-3, 5)
path.lineTo(0, 0)
path.lineTo(3, 5)
path.lineTo(0, 5)

transform = QG.QTransform()
transform.rotate(-30.0)
path = transform.map(path)

pen = QG.QPen(QC.Qt.black, 2)
pen.setJoinStyle(QC.Qt.MiterJoin)

symbol = qwt.QwtSymbol()
symbol.setPen(pen)
symbol.setBrush(QC.Qt.red)
symbol.setPath(path)
symbol.setPinPoint(QC.QPointF(0.0, 0.0))
symbol.setSize(10, 14)

# --- Test it within a simple plot ---

curve = qwt.QwtPlotCurve()
curve_pen = QG.QPen(QC.Qt.blue)
curve_pen.setStyle(QC.Qt.DotLine)
curve.setPen(curve_pen)
curve.setSymbol(symbol)
x = np.linspace(0, 10, 10)
curve.setData(x, np.sin(x))

plot = qwt.QwtPlot()
curve.attach(plot)
plot.resize(600, 300)
plot.replot()
plot.show()

plot.grab().save(
    osp.join(osp.abspath(osp.dirname(__file__)), "images", "symbol_path_example.png")
)

app.exec_()
