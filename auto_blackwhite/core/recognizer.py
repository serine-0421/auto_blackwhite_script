# 图像识别（数字OCR、规划队列圆圈检测、职位文字）
# core/recognizer.py
import cv2
import numpy as np
import pytesseract
from PIL import Image
import logging

logger = logging.getLogger("GameBot")

class Recognizer:
    def __init__(self, controller):
        self.controller = controller
    
    def ocr_number(self, region):
        """识别区域内数字，返回整数"""
        img = self.controller.screenshot()
        crop = img.crop(region)
        # 灰度化
        gray = crop.convert('L')
        # 二值化（可调阈值）
        bw = gray.point(lambda x: 0 if x < 128 else 255, '1')
        # OCR
        text = pytesseract.image_to_string(bw, config='--psm 8 -c tessedit_char_whitelist=0123456789')
        text = text.strip()
        if text.isdigit():
            return int(text)
        # 处理逗号分隔的数字
        text = text.replace(',', '')
        if text.isdigit():
            return int(text)
        logger.warning(f"OCR未能识别数字: {text}")
        return -1
    
    def detect_plan_queue_circle(self, region):
        """
        检测规划队列按钮方框内是否有圆圈
        region: (left, top, right, bottom) 圆圈可能出现的小区域
        返回 True 表示有圆圈（已启用）
        """
        img = self.controller.screenshot()
        crop = img.crop(region)
        # 转换为OpenCV格式
        cv_img = cv2.cvtColor(np.array(crop), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        # 使用霍夫圆检测
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=10,
                                   param1=50, param2=30, minRadius=3, maxRadius=15)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            # 只要检测到圆就认为有圆圈
            return len(circles[0]) > 0
        # 备用方案：检测区域中心是否有亮色区域（简单阈值）
        # 可选，不实现也可
        return False
    
    def ocr_position_text(self, region):
        """识别职位文字（中文）"""
        img = self.controller.screenshot()
        crop = img.crop(region)
        # 可以直接用pytesseract识别中文
        text = pytesseract.image_to_string(crop, lang='chi_sim')
        text = text.strip()
        # 可能包含空格或换行，清理
        positions = ["研究生", "研究员", "资深研究员", "课题组长", "研究主任"]
        for pos in positions:
            if pos in text:
                return pos
        logger.warning(f"无法识别的职位: {text}")
        return None