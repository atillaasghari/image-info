import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QLineEdit, QFormLayout
from PyQt5.QtGui import QPixmap, QFont, QImage
from PyQt5.QtCore import Qt
from PIL import Image

class ImageInfoApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize UI components
        self.init_ui()

        # Create instance variable for ImageWidget
        self.img_widget = None

        # Store width and height for reconstruction
        self.reconstruction_width = None
        self.reconstruction_height = None

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

        self.save_button = QPushButton("Save Binary Data", self)
        self.save_button.clicked.connect(self.save_binary_data)

        self.reconstruct_button = QPushButton("Reconstruct Image", self)
        self.reconstruct_button.clicked.connect(self.reconstruct_image)

        # Create entry to input binary data
        self.binary_entry_label = QLabel("<h3>Enter Binary Data:</h3>")
        self.binary_entry = QLineEdit(self)

        # Create button to save reconstructed image
        self.save_image_button = QPushButton("Save Reconstructed Image", self)
        self.save_image_button.clicked.connect(self.save_reconstructed_image)

        # Create form layout for image dimensions
        self.image_dimensions_layout = QFormLayout()
        self.width_entry = QLineEdit(self)
        self.height_entry = QLineEdit(self)
        self.image_dimensions_layout.addRow("Width:", self.width_entry)
        self.image_dimensions_layout.addRow("Height:", self.height_entry)

        # Create button to submit height and width
        self.submit_dimensions_button = QPushButton("Submit Dimensions", self)
        self.submit_dimensions_button.clicked.connect(self.submit_dimensions)

        # Create layouts
        vbox = QVBoxLayout()
        vbox.addWidget(self.info_label, 0, alignment=Qt.AlignmentFlag.AlignTop)
        vbox.addWidget(self.browse_button)
        vbox.addWidget(self.pixel_count_label)
        vbox.addWidget(self.pixel_count_entry)
        vbox.addWidget(self.turn_to_bin)
        vbox.addWidget(self.save_button)
        vbox.addLayout(self.image_dimensions_layout)
        vbox.addWidget(self.submit_dimensions_button)  # Add the submit dimensions button
        vbox.addWidget(self.binary_entry_label)
        vbox.addWidget(self.binary_entry)
        vbox.addWidget(self.reconstruct_button)
        vbox.addWidget(self.save_image_button)

        hbox = QHBoxLayout(self)
        hbox.addLayout(vbox)

        self.setLayout(hbox)

        # Set application properties
        self.setWindowTitle('Image Info App')
        self.setGeometry(100, 100, 400, 400)

        # Apply a custom color scheme
        self.setStyleSheet(
            "QWidget { background-color: #f8f8f8; color: #333333; }"
            "QLabel { font-size: 16pt; color: #3498db; }"
            "QPushButton { font-size: 12pt; background-color: #3498db; color: #ecf0f1; }"
            "QLineEdit { font-size: 12pt; background-color: #ecf0f1; color: #333333; }"
            "QLineEdit:read-only { background-color: #d0d3d4; }"
        )

    def submit_dimensions(self):
        # Get width and height values
        width_text = self.width_entry.text()
        height_text = self.height_entry.text()

        if not width_text or not height_text:
            print("Please enter values for both width and height.")
            return

        try:
            width = int(width_text)
            height = int(height_text)
        except ValueError as ve:
            print(f"Invalid values for width and/or height: {ve}")
            return

        # Store the width and height in instance variables for later use
        self.reconstruction_width = width
        self.reconstruction_height = height


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

    def save_binary_data(self):
        if self.pixel_count_entry.text():
            file_path, _ = QFileDialog.getSaveFileName(self, 'Save Binary Data', '', 'Binary Files (*.bin)')
            if file_path:
                try:
                    with open(file_path, "wb") as file:
                        binary_data = self.get_binary_data()
                        file.write(binary_data)
                    print(f"Binary data saved to {file_path}")
                except Exception as e:
                    print(f"Error saving binary data: {e}")

    def get_binary_data(self):
        image_path, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.png; *.jpg; *.jpeg)')
        if image_path:
            try:
                with Image.open(image_path) as img:
                    binary_data = img.tobytes()
                    return binary_data
            except Exception as e:
                print(f"Error: {e}")
                return b''

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

    def reconstruct_image(self):
        # Get width and height values
        width_text = self.width_entry.text()
        height_text = self.height_entry.text()

        if not width_text or not height_text:
            print("Please enter values for both width and height.")
            return

        try:
            width = int(width_text)
            height = int(height_text)
        except ValueError as ve:
            print(f"Invalid values for width and/or height: {ve}")
            return

        # Proceed with reconstructing the image
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Binary File', '', 'Binary Files (*.bin)')
        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    binary_data = file.read()

                    # Check if there is enough image data for the specified dimensions
                    expected_size = width * height * 3  # Assuming RGB image
                    if len(binary_data) != expected_size:
                        print(f"Not enough image data for the specified dimensions or you entered the wrong dimensions. Expected {expected_size} bytes, but got {len(binary_data)} bytes.")
                        return

                    image = Image.frombytes('RGB', (width, height), binary_data)

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

        q_image = QImage(image.tobytes(), image.width, image.height, image.width * 3, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)

        self.label = QLabel(self)
        self.label.setPixmap(pixmap)

        self.setGeometry(510, 100, pixmap.width(), pixmap.height())
        self.setWindowTitle('Reconstructed Image')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageInfoApp()
    ex.show()
    sys.exit(app.exec_())
