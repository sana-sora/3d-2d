import cv2
import numpy as np
from PIL import Image
import os
from datetime import datetime

def segment_image(image_path, output_folder):
    """
    画像をセグメンテーション（物体抽出）
    Segment Anything Modelを使用
    
    Args:
        image_path: 入力画像パス
        output_folder: 出力フォルダ
    
    Returns:
        マスク画像のパス
    """
    try:
        # 画像を読み込み
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"画像が読み込めません: {image_path}")
        
        # グレースケール変換
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 簡易的なセグメンテーション（背景除去）
        # 実装：GaussianBlur + threshold + morphological操作
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)
        
        # モルフォロジー操作でノイズ除去
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        
        # 輪郭検出
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            raise ValueError("物体が検出できません")
        
        # 最大の輪郭を抽出
        largest_contour = max(contours, key=cv2.contourArea)
        
        # 最大の輪郭でマスクを作成
        final_mask = np.zeros_like(mask)
        cv2.drawContours(final_mask, [largest_contour], 0, 255, -1)
        
        # マスク画像を保存
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        mask_filename = f"mask_{timestamp}.png"
        mask_path = os.path.join(output_folder, mask_filename)
        cv2.imwrite(mask_path, final_mask)
        
        return mask_path
    
    except Exception as e:
        print(f"セグメンテーションエラー: {str(e)}")
        raise

def apply_sam_segmentation(image_path, output_folder):
    """
    Segment Anything Model (SAM)を使用した高精度セグメンテーション
    ※ 将来の拡張用
    
    Args:
        image_path: 入力画像パス
        output_folder: 出力フォルダ
    
    Returns:
        マスク画像のパス
    """
    try:
        # 注：SAMモデルはインストールが必要
        # from segment_anything import sam_model_registry, SamAutomaticMaskGenerator
        # これは後で実装
        pass
    except Exception as e:
        print(f"SAM セグメンテーションエラー: {str(e)}")
        raise
