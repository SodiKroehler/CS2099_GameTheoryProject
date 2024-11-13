from solver import minimize_sum_with_constraints
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt

class OptimizationApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Optimization Result Viewer")
        self.setGeometry(100, 100, 400, 400)

        # Input label and entry for m
        self.label_m = QLabel("Enter the value of m:", self)
        self.entry_m = QLineEdit(self)

        # Calculate button
        self.calc_button = QPushButton("Calculate", self)
        self.calc_button.clicked.connect(self.on_calculate)

        # Result label for displaying results
        self.output_label = QLabel("", self)
        self.output_label.setAlignment(Qt.AlignLeft)
        
        # Layout for input and button
        vbox = QVBoxLayout()
        vbox.addWidget(self.label_m)
        vbox.addWidget(self.entry_m)
        vbox.addWidget(self.calc_button)
        vbox.addWidget(self.output_label)
        
        # Set layout
        self.setLayout(vbox)

    def on_calculate(self):
        try:
            m = float(self.entry_m.text())
            if m < 3:
                QMessageBox.warning(self, "Warning", "m must be at least 3 for a feasible solution.")
                return

            # Run the optimization function with the entered m value
            result = minimize_sum_with_constraints(m)

            if result:
                # Display the result in the output label
                result_text = (
                    f"Optimal x1: {result['x1']:.2f}\n"
                    f"Optimal x2: {result['x2']:.2f}\n"
                    f"Optimal x3: {result['x3']:.2f}\n"
                    f"Sum of x1, x2, x3: {result['sum']:.2f}"
                )
                self.output_label.setText(result_text)

                # Update the node values
                self.x1_value = result['x1']
                self.x2_value = result['x2']
                self.x3_value = result['x3']
                self.update()
            else:
                self.output_label.setText("No feasible solution found.")
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Please enter a valid number for m.")
    
    def paintEvent(self, event):
        # Draw nodes as circles on the window
        qp = QPainter()
        qp.begin(self)
        self.draw_nodes(qp)
        qp.end()
        
    def draw_nodes(self, qp):
        qp.setFont(QFont('Arial', 10))
        
        # Draw node for x1
        qp.setBrush(QColor(173, 216, 230))  # lightblue
        qp.drawEllipse(50, 200, 50, 50)
        qp.drawText(60, 265, f"x1: {getattr(self, 'x1_value', ''):.2f}" if hasattr(self, 'x1_value') else "x1: ")

        # Draw node for x2
        qp.setBrush(QColor(144, 238, 144))  # lightgreen
        qp.drawEllipse(150, 200, 50, 50)
        qp.drawText(160, 265, f"x2: {getattr(self, 'x2_value', ''):.2f}" if hasattr(self, 'x2_value') else "x2: ")

        # Draw node for x3
        qp.setBrush(QColor(240, 128, 128))  # lightcoral
        qp.drawEllipse(250, 200, 50, 50)
        qp.drawText(260, 265, f"x3: {getattr(self, 'x3_value', ''):.2f}" if hasattr(self, 'x3_value') else "x3: ")

# Main loop


if __name__ == '__main__':
    app = QApplication(sys.argv)
    opt_app = OptimizationApp()
    opt_app.show()
    sys.exit(app.exec_())