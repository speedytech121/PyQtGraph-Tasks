# Import necessary modules
import sys, os  # System-specific parameters
import numpy as np  # Numerical operations
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QComboBox, QFileDialog, QSlider, \
    QAction  # PyQt5 widgets
from PyQt5.QtCore import Qt, QTimer  # Core functionalities
import pandas as pd  # Data manipulation
import pyqtgraph as pg  # Plotting library
from PyQt5.QtGui import QIcon  # Icon for the window

# Define the main application class
class RealTimeWaveformPlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.num = 0.01  # Initialize a variable

        # Initialize the user interface
        self.init_ui()

        # Set up a timer for updating the plot
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)  # Update every 100 milliseconds (0.1 seconds)

    def init_ui(self):
        # Set the window title
        self.setWindowTitle("Chara Task 2")

        # Create menubar
        menubar = self.menuBar()
        
        # Add a 'File' menu to the menubar
        fileMenu = menubar.addMenu('File')
        # Add a 'Select WaveForm' menu to the menubar
        waveform_menu = menubar.addMenu('Select WaveForm')

        # Load Csv Action
        loadCsvAction = QAction(QIcon(self.resource_path('../../static/csv-file.png')), 'Select File', self)
        loadCsvAction.triggered.connect(self.loadCsv)  # Connect action to loadCsv method
        fileMenu.addAction(loadCsvAction)

        # Add actions for different waveforms to the 'Select WaveForm' menu
        sine_action = QAction(QIcon(self.resource_path('../../static/sine.png')),'Sine', self)
        sine_action.triggered.connect(lambda: self.set_waveform("Sine"))
        waveform_menu.addAction(sine_action)

        cosine_action = QAction(QIcon(self.resource_path('../../static/cosine.png')),'Cosine', self)
        cosine_action.triggered.connect(lambda: self.set_waveform("Cosine"))
        waveform_menu.addAction(cosine_action)

        triangular_action = QAction(QIcon(self.resource_path('../../static/triangular.png')),'Triangular', self)
        triangular_action.triggered.connect(lambda: self.set_waveform("Triangular"))
        waveform_menu.addAction(triangular_action)

        # Set up the main layout
        central_widget = QWidget()
        self.layout = QVBoxLayout()

        # Create a plot widget
        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)

        # Create a dropdown for selecting waveforms
        self.waveform_combo = QComboBox()
        self.waveform_combo.addItems(["Sine", "Cosine", "Triangular"])

        # Create sliders for adjusting frequency and amplitude
        self.frequency_label = QLabel("Frequency *:")
        self.frequency_label.setToolTip('Choose Frequency...')
        self.frequency_slider = QSlider(Qt.Horizontal)
        self.frequency_slider.setMinimum(1)
        self.frequency_slider.setMaximum(10)
        self.layout.addWidget(self.frequency_label)
        self.layout.addWidget(self.frequency_slider)

        self.amplitude_label = QLabel("Amplitude *:")
        self.amplitude_label.setToolTip('Choose Amplitude...')
        self.amplitude_slider = QSlider(Qt.Horizontal)
        self.amplitude_slider.setMinimum(1)
        self.amplitude_slider.setMaximum(100)
        self.layout.addWidget(self.amplitude_label)
        self.layout.addWidget(self.amplitude_slider)

        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        # Set initial color
        self.plot = self.plot_widget.plot(pen='g')  # Green line

        # Connect signals to update methods
        self.waveform_combo.currentIndexChanged.connect(self.update_waveform)
        self.frequency_slider.valueChanged.connect(self.update_frequency)
        self.amplitude_slider.valueChanged.connect(self.update_amplitude)

        # Set initial waveform, frequency, amplitude, and plot data
        self.current_waveform = "Sine"
        self.current_frequency = 1
        self.current_amplitude = 100
        self.t = np.linspace(0, 2 * np.pi, 1000)
        self.setGeometry(0, 0, 1200, 800)
        self.setStyle()
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
            
            self.layout.addWidget(win)

    # Method to set the selected waveform
    def set_waveform(self, waveform):
        self.num = 0.01
        self.current_waveform = waveform
        self.waveform_combo.setCurrentText(waveform)
        self.update_plot()

    # Method to update the real-time plot based on selected waveform
    def update_plot(self):
        if self.current_waveform == "Sine":
            data = self.current_amplitude * np.sin(self.t + (self.num * self.current_frequency))
            self.num += 0.5
            color = 'g'  # Green for sine
        elif self.current_waveform == "Cosine":
            data = self.current_amplitude * np.cos(self.t + (self.num * self.current_frequency))
            self.num += 0.5
            color = 'r'  # Red for cosine
        elif self.current_waveform == "Triangular":
            data = self.current_amplitude * (2 * np.abs((self.t * self.current_frequency) % 1) - 1)
            color = 'b'  # Blue for triangular

        # Introduce less random noise
        noise = np.random.normal(0, 0.2, len(self.t))
        data += noise

        # Update color and data
        self.plot.setData(self.t, data, pen=color)

    def update_waveform(self):
        self.num = 0.01
        self.current_waveform = self.waveform_combo.currentText()
        self.update_plot()

    def update_frequency(self):
        self.num = 0.01
        self.current_frequency = self.frequency_slider.value()
        self.update_plot()

    def update_amplitude(self):
        self.num = 0.01
        self.current_amplitude = self.amplitude_slider.value()
        self.update_plot()
    
    
    
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    
    
    
    def setStyle(self):
        self.setStyleSheet("""
            QMenuBar {
                background-color: #7FB3D5 ;
                color: black;
            }

            QMenuBar::item {
                background: transparent;
            }

            QMenuBar::item:selected {
                background-color: #F2F4F4 ;
            }

            QAction {
                background-color: transparent;
                color: white;
                padding: 5px 15px;
            }

            QAction:selected {
                background-color: #555;
            }
        """)

if __name__ == '__main__':
    # This block of code is executed only when the script is run directly, not when it's imported as a module.    
    # Create a QApplication instance to manage the GUI application
    app = QApplication(sys.argv)
    
    # Create an instance of the RealTimeWaveformPlotter class, which represents the main window of the application
    ex = RealTimeWaveformPlotter()
    
    # Start the application event loop
    sys.exit(app.exec_())