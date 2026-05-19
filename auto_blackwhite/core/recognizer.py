# 图像识别（数字OCR、规划队列圆圈检测、职位文字）

import cv2
import numpy as np
import pytesseract
import logging

logger = logging.getLogger("GameBot")


class Recognizer:
    def __init__(self, controller):
        self.controller = controller

    # 基础工具

    def _crop(self, img, region):
        x1, y1, x2, y2 = region
        return img[y1:y2, x1:x2]

    def _preprocess_for_ocr(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 自适应阈值
        bw = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11, 2
        )

        # 放大
        bw = cv2.resize(bw, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

        return bw

    # 数字识别

    def read_number(self, img, region):
        crop = self._crop(img, region)
        proc = self._preprocess_for_ocr(crop)

        text = pytesseract.image_to_string(
            proc,
            config='--psm 7 -c tessedit_char_whitelist=0123456789,'
        ).strip()

        text = text.replace(",", "")

        if text.isdigit():
            return int(text)

        logger.debug(f"OCR failed: {text}")
        return None

    # 圆形检测

    def has_circle(self, img, region):
        crop = self._crop(img, region)
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

        # 边缘检测 + 轮廓
        edges = cv2.Canny(gray, 50, 150)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 10:
                continue

            (x, y), radius = cv2.minEnclosingCircle(cnt)

            if 3 < radius < 20:
                return True

        return False

    # 文本识别

    def read_text(self, img, region):
        crop = self._crop(img, region)

        text = pytesseract.image_to_string(
            crop,
            lang='chi_sim',
            config='--psm 6'
        ).strip()

        return text

    def ocr_number(self, region):
        img = self.controller.screenshot()
        if img is None:
            return None
        return self.read_number(img, region)