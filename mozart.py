import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QPushButton, 
                           QVBoxLayout, QHBoxLayout,QFileDialog, QSlider, QLineEdit)
from PyQt5.QtGui import QImage, QPixmap, QColor, QPalette, QBrush
from PyQt5.QtCore import Qt, QSize
from PIL import Image, ImageEnhance, ImageFilter
import io

class Mozart(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mozart Photo Editor")
        background = QImage("mozart.png")
        scaled_background = background.scaled(QSize(1200, 800), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(scaled_background))
        self.setPalette(palette)
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #000000;  
            }
            QPushButton {
                background-color: #FF69B4;  
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QLabel {
                color: white;  /* Lemon Green */
            }
            QLineEdit, QSlider {
                background-color: white;
                padding: 5px;
            }
        """)
        
        self.init_ui()
        
    def init_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        
        # Left panel for controls
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Buttons
        self.load_btn = QPushButton("Load Image")
        self.save_btn = QPushButton("Save Image")
        self.blur_btn = QPushButton("Apply Blur")
        self.invert_btn = QPushButton("Invert Colors")
        self.reset_btn = QPushButton("Reset Image")
        
        # Sliders
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setMinimum(0)
        self.brightness_slider.setMaximum(200)
        self.brightness_slider.setValue(100)
        
        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setMinimum(0)
        self.contrast_slider.setMaximum(200)
        self.contrast_slider.setValue(100)
        
        # Text input for watermark
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Enter watermark text")
        self.add_text_btn = QPushButton("Add Text")
        
        # Additional filter buttons
        self.sharpen_btn = QPushButton("Sharpen")
        self.edge_enhance_btn = QPushButton("Edge Enhance")
        self.emboss_btn = QPushButton("Emboss")
        self.sepia_btn = QPushButton("Sepia")
        self.crop_btn = QPushButton("Crop")
        self.rotate_btn = QPushButton("Rotate 90°")
        self.flip_h_btn = QPushButton("Flip Horizontal")
        self.flip_v_btn = QPushButton("Flip Vertical")
        
        # Additional sliders
        self.saturation_slider = QSlider(Qt.Horizontal)
        self.saturation_slider.setMinimum(0)
        self.saturation_slider.setMaximum(200)
        self.saturation_slider.setValue(100)
        
        # Add widgets to left panel
        left_layout.addWidget(self.load_btn)
        left_layout.addWidget(self.save_btn)
        left_layout.addWidget(QLabel("Brightness:"))
        left_layout.addWidget(self.brightness_slider)
        left_layout.addWidget(QLabel("Contrast:"))
        left_layout.addWidget(self.contrast_slider)
        left_layout.addWidget(self.blur_btn)
        left_layout.addWidget(self.invert_btn)
        left_layout.addWidget(self.text_input)
        left_layout.addWidget(self.add_text_btn)
        left_layout.addWidget(self.reset_btn)
        left_layout.addWidget(QLabel("Saturation:"))
        left_layout.addWidget(self.saturation_slider)
        left_layout.addWidget(self.sharpen_btn)
        left_layout.addWidget(self.edge_enhance_btn)
        left_layout.addWidget(self.emboss_btn)
        left_layout.addWidget(self.sepia_btn)
        left_layout.addWidget(self.crop_btn)
        left_layout.addWidget(self.rotate_btn)
        left_layout.addWidget(self.flip_h_btn)
        left_layout.addWidget(self.flip_v_btn)
        left_layout.addStretch()
        
        # Image display
        self.image_label = QLabel()
        self.image_label.setStyleSheet("background-color: white;")
        
        # Add panels to main layout
        layout.addWidget(left_panel, 1)
        layout.addWidget(self.image_label, 4)
        
        # Connect buttons to functions
        self.load_btn.clicked.connect(self.load_image)
        self.save_btn.clicked.connect(self.save_image)
        self.blur_btn.clicked.connect(self.apply_blur)
        self.invert_btn.clicked.connect(self.invert_colors)
        self.add_text_btn.clicked.connect(self.add_watermark)
        self.reset_btn.clicked.connect(self.reset_image)
        self.brightness_slider.valueChanged.connect(self.adjust_brightness)
        self.contrast_slider.valueChanged.connect(self.adjust_contrast)
        self.sharpen_btn.clicked.connect(self.apply_sharpen)
        self.edge_enhance_btn.clicked.connect(self.apply_edge_enhance)
        self.emboss_btn.clicked.connect(self.apply_emboss)
        self.sepia_btn.clicked.connect(self.apply_sepia)
        self.crop_btn.clicked.connect(self.crop_image)
        self.rotate_btn.clicked.connect(self.rotate_image)
        self.flip_h_btn.clicked.connect(self.flip_horizontal)
        self.flip_v_btn.clicked.connect(self.flip_vertical)
        self.saturation_slider.valueChanged.connect(self.adjust_saturation)
        
        # Initialize image variables
        self.original_image = None
        self.current_image = None
        
        self.setGeometry(100, 100, 1000, 600)
        
    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", 
                                                 "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            self.original_image = Image.open(file_name)
            self.current_image = self.original_image.copy()
            self.update_display()
            
    def update_display(self):
        if self.current_image:
            # Convert PIL image to QPixmap
            buffer = io.BytesIO()
            self.current_image.save(buffer, format='PNG')
            qt_img = QImage.fromData(buffer.getvalue())
            pixmap = QPixmap.fromImage(qt_img)
            
            # Scale pixmap to fit label while maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(self.image_label.size(), 
                                        Qt.KeepAspectRatio, 
                                        Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
            
    def save_image(self):
        if self.current_image:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", 
                                                     "PNG (*.png);;JPEG (*.jpg *.jpeg);;BMP (*.bmp)")
            if file_name:
                self.current_image.save(file_name)
                
    def apply_blur(self):
        if self.current_image:
            self.current_image = self.current_image.filter(ImageFilter.BLUR)
            self.update_display()
            
    def invert_colors(self):
        if self.current_image:
            self.current_image = Image.eval(self.current_image, lambda x: 255 - x)
            self.update_display()
            
    def adjust_brightness(self):
        if self.current_image:
            factor = self.brightness_slider.value() / 100
            enhancer = ImageEnhance.Brightness(self.current_image)
            self.current_image = enhancer.enhance(factor)
            self.update_display()
            
    def adjust_contrast(self):
        if self.current_image:
            factor = self.contrast_slider.value() / 100
            enhancer = ImageEnhance.Contrast(self.current_image)
            self.current_image = enhancer.enhance(factor)
            self.update_display()
            
    def add_watermark(self):
        if self.current_image and self.text_input.text():
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(self.current_image)
            text = self.text_input.text()
            # You might want to adjust font size and position
            draw.text((10, 10), text, fill="white")
            self.update_display()
            
    def reset_image(self):
        if self.original_image:
            self.current_image = self.original_image.copy()
            self.brightness_slider.setValue(100)
            self.contrast_slider.setValue(100)
            self.update_display()

    def apply_sharpen(self):
        if self.current_image:
            self.current_image = self.current_image.filter(ImageFilter.SHARPEN)
            self.update_display()
    
    def apply_edge_enhance(self):
        if self.current_image:
            self.current_image = self.current_image.filter(ImageFilter.EDGE_ENHANCE)
            self.update_display()
    
    def apply_emboss(self):
        if self.current_image:
            self.current_image = self.current_image.filter(ImageFilter.EMBOSS)
            self.update_display()
    
    def apply_sepia(self):
        if self.current_image:
            width, height = self.current_image.size
            pixels = self.current_image.load()
            for x in range(width):
                for y in range(height):
                    r, g, b = self.current_image.getpixel((x, y))[:3]
                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                    self.current_image.putpixel((x, y), (min(tr, 255), min(tg, 255), min(tb, 255)))
            self.update_display()
    
    def crop_image(self):
        if self.current_image:
            # For simplicity, this crops the image to 80% of its original size
            width, height = self.current_image.size
            left = width * 0.1
            top = height * 0.1
            right = width * 0.9
            bottom = height * 0.9
            self.current_image = self.current_image.crop((left, top, right, bottom))
            self.update_display()
    
    def rotate_image(self):
        if self.current_image:
            self.current_image = self.current_image.rotate(90, expand=True)
            self.update_display()
    
    def flip_horizontal(self):
        if self.current_image:
            self.current_image = self.current_image.transpose(Image.FLIP_LEFT_RIGHT)
            self.update_display()
    
    def flip_vertical(self):
        if self.current_image:
            self.current_image = self.current_image.transpose(Image.FLIP_TOP_BOTTOM)
            self.update_display()
    
    def adjust_saturation(self):
        if self.current_image:
            factor = self.saturation_slider.value() / 100
            enhancer = ImageEnhance.Color(self.current_image)
            self.current_image = enhancer.enhance(factor)
            self.update_display()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mozart = Mozart()
    mozart.show()
    sys.exit(app.exec_())
