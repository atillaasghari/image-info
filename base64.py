import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QLineEdit
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from PIL import Image, ImageQt
import base64

class ImageInfoApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize UI components
        self.init_ui()

        # Create instance variable for ImageWidget
        self.img_widget = None

    def init_ui(self):
        # Set application font
        font = QFont("Helvetica", 12)
        self.setFont(font)

        # Create labels
        self.info_label = QLabel("<h2 style='color:#333333;'>Image Information</h2>")
        self.pixel_count_label = QLabel("<b>Pixel Count:</b>")
        self.turn_to_bin = QLabel("<h3>Turn Image to binary:</h3>")

        # Create entry to display pixel count
        self.pixel_count_entry = QLineEdit(self)
        self.pixel_count_entry.setReadOnly(True)

        # Create buttons
        self.browse_button = QPushButton("Browse Image", self)
        self.browse_button.clicked.connect(self.browse_image)

        self.save_button = QPushButton("Save Base64 Data", self)
        self.save_button.clicked.connect(self.save_base64_data)

        self.reconstruct_button = QPushButton("Reconstruct Image", self)
        self.reconstruct_button.clicked.connect(self.reconstruct_image)

        # Create entry to input Base64 data
        self.base64_entry_label = QLabel("<h3>Enter Base64 Data:</h3>")
        self.base64_entry = QLineEdit(self)

        # Create button to save reconstructed image
        self.save_image_button = QPushButton("Save Reconstructed Image", self)
        self.save_image_button.clicked.connect(self.save_reconstructed_image)

        # Create layouts
        vbox = QVBoxLayout()
        vbox.addWidget(self.info_label, 0, alignment=Qt.AlignmentFlag.AlignTop)
        vbox.addWidget(self.browse_button)
        vbox.addWidget(self.pixel_count_label)
        vbox.addWidget(self.pixel_count_entry)
        vbox.addWidget(self.turn_to_bin)
        vbox.addWidget(self.save_button)
        vbox.addWidget(self.base64_entry_label)
        vbox.addWidget(self.base64_entry)
        vbox.addWidget(self.reconstruct_button)
        vbox.addWidget(self.save_image_button)

        hbox = QHBoxLayout(self)
        hbox.addLayout(vbox)

        self.setLayout(hbox)

        # Set application properties
        self.setWindowTitle('Image Info App')
        self.setGeometry(100, 100, 400, 300)

        # Apply a custom color scheme
        self.setStyleSheet(
            "QWidget { background-color: #f8f8f8; color: #333333; }"
            "QLabel { font-size: 16pt; color: #3498db; }"
            "QPushButton { font-size: 12pt; background-color: #3498db; color: #ecf0f1; }"
            "QLineEdit { font-size: 12pt; background-color: #ecf0f1; color: #333333; }"
            "QLineEdit:read-only { background-color: #d0d3d4; }"
        )
    def save_reconstructed_image(self):
        if self.img_widget:
            file_path, _ = QFileDialog.getSaveFileName(self, 'Save Reconstructed Image', '', 'Image Files (*.png; *.jpg; *.jpeg)')
            if file_path:
                try:
                    self.img_widget.image.save(file_path)
                    print(f"Reconstructed image saved to {file_path}")
                except Exception as e:
                    print(f"Error saving reconstructed image: {e}")
            else:
                print("Save operation canceled.")

    def browse_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.png; *.jpg; *.jpeg)')
        if file_path:
            result = self.calculate_pixel_count(file_path)
            if result is not None:
                self.pixel_count_entry.setText(str(result))

    def calculate_pixel_count(self, image_path):
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                pixel_count = width * height
                return pixel_count
        except Exception as e:
            print(f"Error: {e}")
            return None

    def save_base64_data(self):
        if self.pixel_count_entry.text():
            file_path, _ = QFileDialog.getSaveFileName(self, 'Save Base64 Data', '', 'Text Files (*.txt)')
            if file_path:
                try:
                    with open(file_path, "wb") as file:
                        base64_data = self.get_base64_data()
                        file.write(base64_data.encode('utf-8'))
                    print(f"Base64 data saved to {file_path}")
                except Exception as e:
                    print(f"Error saving base64 data: {e}")

    def get_base64_data(self):
        image_path, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.png; *.jpg; *.jpeg)')
        if image_path:
            try:
                with Image.open(image_path) as img:
                    binary_data = img.tobytes()
                    base64_representation = base64.b64encode(binary_data).decode('utf-8')
                    return base64_representation
            except Exception as e:
                print(f"Error: {e}")
                return ""

    def reconstruct_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Base64 File', '', 'Text Files (*.txt)')
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    base64_data = file.read()
                    binary_data = base64.b64decode(base64_data)
                    image = Image.frombytes('RGB', (400, 297), binary_data)  # Replace (300, 300) with actual image dimensions

                    # Check if the img_widget already exists, close it before creating a new one
                    if self.img_widget:
                        self.img_widget.close()

                    # Create and display the image in a new window
                    self.img_widget = ImageWidget(image)
                    self.img_widget.show()
                    print("Image reconstructed successfully!")
            except Exception as e:
                print(f"Error reconstructing image: {e}")


class ImageWidget(QWidget):
    def __init__(self, image):
        super().__init__()

        self.image = ImageQt.ImageQt(image)
        pixmap = QPixmap.fromImage(self.image)

        self.label = QLabel(self)
        self.label.setPixmap(pixmap)

        self.setGeometry(510, 100, pixmap.width(), pixmap.height())
        self.setWindowTitle('Reconstructed Image')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageInfoApp()
    ex.show()
    sys.exit(app.exec_())
