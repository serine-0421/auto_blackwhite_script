# 图像识别（数字OCR、规划队列圆圈检测、职位文字）

import os
import cv2
import numpy as np
import pytesseract
import logging
from datetime import datetime

logger = logging.getLogger("GameBot")
OCR_TIMEOUT = 10


class Recognizer:
    def __init__(self, controller):
        self.controller = controller

    # 基础工具

    def _crop(self, img, region):
        x1, y1, x2, y2 = region
        if isinstance(img, np.ndarray):
            return img[y1:y2, x1:x2]
        else:
            return np.array(img.crop((x1, y1, x2, y2)))

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

        configs = [
        '--psm 7 -c tessedit_char_whitelist=0123456789', 
        '--psm 8 -c tessedit_char_whitelist=0123456789',  
        '--psm 13 -c tessedit_char_whitelist=0123456789', 
        '--psm 6 -c tessedit_char_whitelist=0123456789',   
        ]
    
        best_digits = None
        all_texts = []
        for config in configs:
            try:
                text = pytesseract.image_to_string(proc, config=config, timeout=OCR_TIMEOUT).strip()
            except Exception as e:
                logger.warning(f"OCR config failed for region {region} config={config}: {e}")
                text = ""
            all_texts.append((config, text))
            digits = ''.join(ch for ch in text if ch.isdigit())
            if digits:
                best_digits = digits
                break

        # 放大识别
        if not best_digits:
            h, w = proc.shape[:2]
            if h < 30 or w < 50:
                proc_big = cv2.resize(proc, (w*2, h*2), interpolation=cv2.INTER_CUBIC)
                for config in configs:
                    try:
                        text = pytesseract.image_to_string(proc_big, config=config, timeout=OCR_TIMEOUT).strip()
                    except Exception as e:
                        logger.warning(f"OCR big config failed for region {region} config={config}: {e}")
                        text = ""
                    all_texts.append((config + ' (big)', text))
                    digits = ''.join(ch for ch in text if ch.isdigit())
                    if digits:
                        best_digits = digits
                        break

        if best_digits and best_digits.isdigit():
            return int(best_digits)

        for config, text in all_texts:
            logger.info(f"OCR raw text [{config}] = '{text}'")
        logger.info(f"OCR failed for region {region}, extracted digits: {''.join(ch for ch in all_texts[-1][1] if ch.isdigit())}")
        self._save_debug_screenshot(region, prefix="ocr_number_failed")
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

        try:
            text = pytesseract.image_to_string(
                crop,
                lang='chi_sim',
                config='--psm 6',
                timeout=OCR_TIMEOUT
            ).strip()
        except Exception as e:
            logger.warning(f"Text OCR exception for region {region}: {e}")
            return ""

        return text

    def detect_plan_queue_circle(self, region):
        img = self.controller.screenshot()
        if img is None:
            logger.debug("detect_plan_queue_circle: screenshot failed")
            return False
        return self.has_circle(img, region)

    def _save_debug_screenshot(self, region, prefix="ocr_debug"):
        img = self.controller.screenshot()
        if img is None:
            logger.warning("无法保存调试截图：截图失败")
            return

        debug_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'logs', 'ocr_debug'))
        os.makedirs(debug_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        crop_path = os.path.join(debug_dir, f"{prefix}_{timestamp}.png")

        try:
            crop = self._crop(img, region)
            if hasattr(crop, 'save'):
                crop.save(crop_path)
            else:
                cv2.imwrite(crop_path, crop)
            logger.info(f"OCR 调试截图已保存: {crop_path}")
        except Exception as e:
            logger.warning(f"保存 OCR 调试截图失败: {e}")

    def save_debug_screenshot(self, region, prefix="ocr_debug"):
        return self._save_debug_screenshot(region, prefix)

    def ocr_number(self, region):
        img = self.controller.screenshot()
        if img is None:
            logger.warning("ocr_number: screenshot failed")
            return None
        try:
            return self.read_number(img, region)
        except Exception as e:
            logger.warning(f"ocr_number failed for region {region}: {e}")
            self._save_debug_screenshot(region, prefix="ocr_number_exception")
            return None