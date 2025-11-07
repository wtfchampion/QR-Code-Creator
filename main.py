from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.image import FitImage
import qrcode
import numpy as np
import cv2
import subprocess
import os

KV = '''
BoxLayout:
    orientation: 'vertical'
    padding: dp(20)
    spacing: dp(10)

    MDTextField:
        id: input_text
        hint_text: "متن یا لینک خود را وارد کنید"
        mode: "fill"
        multiline: False

    MDRaisedButton:
        text: "ساخت QR Code"
        on_release: app.generate_qr()

    FitImage:
        id: qr_image
        source: ""
        size_hint_y: 0.6
'''

class QRCodeApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def generate_qr(self):
        text = self.root.ids.input_text.text.strip()
        if text:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(text)
            qr.make(fit=True)

            qr_array = np.array(qr.make_image(fill="black", back_color="white"))
            qr_path = "qr_code.png"
            cv2.imwrite(qr_path, qr_array * 255)

            self.root.ids.qr_image.source = qr_path
            self.root.ids.qr_image.reload()

if __name__ == "__main__":
    app = QRCodeApp()
    app.run()

    # بعد از اجرای برنامه، فایل APK ساخته شود
    print("📦 برنامه اجرا شد. در حال ساخت APK...")
    subprocess.run(["python", "build.py"], check=True)