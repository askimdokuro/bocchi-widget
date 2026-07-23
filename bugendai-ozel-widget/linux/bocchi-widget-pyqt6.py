#!/usr/bin/env python3
import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import QTimer, Qt, QRect
from PyQt6.QtGui import QPixmap, QPainter, QFont, QFontDatabase, QColor, QGuiApplication, QKeyEvent
from datetime import datetime

# Script'in olduğu klasörü otomatik bul
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class BocchiWidget(QWidget):
    def __init__(self, target_width, pos_x, pos_y, font_filename, font_size, font_hex_color):
        super().__init__()
        
        # 1. Ekran Bilgileri
        screen = QGuiApplication.primaryScreen().geometry()
        
        # 2. Dosya Yolları
        img_path = os.path.join(BASE_DIR, "bocchi-balonlu-bitsi.png")
        font_path = os.path.join(BASE_DIR, font_filename)
        
        # 3. Özel Font Yükleme
        self.font_family = "Arial"
        if os.path.exists(font_path):
            fid = QFontDatabase.addApplicationFont(font_path)
            fams = QFontDatabase.applicationFontFamilies(fid)
            if fams:
                self.font_family = fams[0]
        else:
            print(f"Uyarı: Font bulunamadı -> {font_path}")

        # 4. Görsel Boyutlandırma
        self.pixmap = QPixmap(img_path)
        self.display_pixmap = self.pixmap.scaledToWidth(target_width, Qt.TransformationMode.SmoothTransformation)
        self.setFixedSize(self.display_pixmap.width(), self.display_pixmap.height())
        
        self.orig_w = self.pixmap.width()
        self.orig_h = self.pixmap.height()
        
        # 5. Konumlandırma
        self.move(pos_x, pos_y)
        
        # 6. MASAÜSTÜNE SABİTLEME VE TIKLANAMAZ YAPMA (KESİN ÇÖZÜM)
        # Sadece Çerçevesiz, En Altta Kalma ve Araç (Görev çubuğunda gizlenme) bayrakları kullanıldı.
        # X11BypassWindowManagerHint tamamen KALDIRILDI!
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnBottomHint | 
            Qt.WindowType.Tool 
        )
        
        # Saydam arkaplan
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        # Linux Masaüstü penceresi gibi davranması için
        self.setAttribute(Qt.WidgetAttribute.WA_X11NetWmWindowTypeDesktop, True)
        # Tıklamaları tamamen arkaya (masaüstüne) geçir
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        
        self.font_size = font_size
        self.font_color = font_hex_color

        # 7. Zamanlayıcı
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.display_pixmap)
        
        current_w = self.width()
        current_h = self.height()
        
        scale_x = current_w / self.orig_w
        scale_y = current_h / self.orig_h
        
        x1 = int(877 * scale_x)
        y1 = int(434 * scale_y)
        x2 = int(2145 * scale_x)
        y2 = int(981 * scale_y)
        
        box_rect = QRect(x1, y1, x2 - x1, y2 - y1)
        
        now = datetime.now()
        text = now.strftime("%H:%M:%S")
        
        scaled_font_size = int(self.font_size * scale_x)
        painter.setFont(QFont(self.font_family, scaled_font_size, QFont.Weight.Bold))
        painter.setPen(QColor(self.font_color))
        
        painter.drawText(
            box_rect, 
            Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap, 
            text
        )

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            QApplication.quit()
        else:
            super().keyPressEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # --- KULLANICI AYARLARI ---
    SECILEN_GENISLIK = 500                    
    KONUM_X = 780                             
    KONUM_Y = 740                             
    
    FONT_DOSYASI = "Cause-Bold.ttf"           
    FONT_BOYUTU = 250                         
    FONT_RENGI = "#ba2fa3"                    
    # -------------------------

    widget = BocchiWidget(
        target_width=SECILEN_GENISLIK, 
        pos_x=KONUM_X, 
        pos_y=KONUM_Y, 
        font_filename=FONT_DOSYASI, 
        font_size=FONT_BOYUTU, 
        font_hex_color=FONT_RENGI
    )
    
    widget.show()
    # PENCEREYİ ZORLA EN ALTA İT (Linux ortamları için ekstra güvenlik)
    widget.lower()
    
    sys.exit(app.exec())