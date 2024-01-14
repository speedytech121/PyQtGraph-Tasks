# Import necessary modules
import sys  # System-specific parameters
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QFrame, QMenuBar, QMenu, QAction, QFileDialog, QWidget, QSizePolicy  # PyQt5 widgets
from PyQt5.QtGui import QIcon  # Icon for the window
import pandas as pd  # Data manipulation
import pyqtgraph as pg  # Plotting library

# Define the main application class
class MyApplication(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the user interface
        self.initUI()

    def initUI(self):
        self.csv_path = None
        self.mainLayout = QVBoxLayout()

        # First frame with QMenuBar
        frame1 = QFrame(self)
        frame1.setFixedHeight(30)
        frame1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        frame1Layout = QHBoxLayout(frame1)
        frame1Layout.setContentsMargins(0, 0, 0, 0)

        # Create a QMenuBar
        menuBar = self.menuBar()
        menuBar.setStyleSheet("background-color: white; border-radius:3px")
        fileMenu = QMenu("_File", self)
        menuBar.addMenu(fileMenu)

        # Add 'Select File' action to the menu
        loadCsvAction = QAction(QIcon('../../static/csv-file.png'), 'Select File', self)
        loadCsvAction.triggered.connect(self.loadCsv)  # Connect action to loadCsv method
        fileMenu.addAction(loadCsvAction)

        frame1Layout.addWidget(menuBar)

        # Second frame with grey background
        self.frame2 = QFrame(self)
        self.frame2.setStyleSheet("background-color: grey;")
        self.frame2Layout = QHBoxLayout(self.frame2)
        self.frame2Layout.setContentsMargins(0, 0, 0, 0)

        self.mainLayout.addWidget(frame1)
        self.mainLayout.addWidget(self.frame2)

        centralWidget = QWidget()
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)

        self.setGeometry(0, 0, 2000, 1700)
        self.setWindowTitle('Chara Task 1')
        self.show()

    # Method to load CSV file
    def loadCsv(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filePath, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)

        if filePath:
            print(f"CSV file loaded: {filePath}")
            self.csv_path = filePath
            self.updateGraph()  # Call method to update the graph with CSV data

    # Method to update the graph with CSV data
    def updateGraph(self):
        if self.csv_path is not None:
            df = pd.read_csv(self.csv_path)
            symbols = ['s', '+', 't','+','s']
            flag = 0
            win = pg.GraphicsLayoutWidget(show=True, title='csv data plots')
            for i, (col, symbol) in enumerate(zip(df.columns, symbols)):
                if flag == 0:
                    plot = win.addPlot(title='dummy graph')
                    flag += 1
                curve = plot.plot(df.index, df[col], pen=pg.mkPen(color=(i, len(df.columns) * 1.3), width=1))
                scatter = pg.ScatterPlotItem(df.index, df[col], symbol=symbol,
                                            brush=pg.mkBrush(color=(i, len(df.columns) * 2.3), width=2),
                                            name=f'Points {col}')
                plot.addLegend()
                plot.addItem(scatter)
                curve.setSymbol(pg.QtGui.QPainterPath())
                plot.setLabel('bottom', 'Row')
                plot.setLabel('left', 'Column')

            self.frame2Layout.addWidget(win)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApplication()
    sys.exit(app.exec_())
