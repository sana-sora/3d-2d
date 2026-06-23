import cv2
import numpy as np
from PIL import Image

def resize_image(image_path, max_width=1024, max_height=1024):
    """
    画像をリサイズ
    
    Args:
        image_path: 画像ファイルパス
        max_width: 最大幅
        max_height: 最大高さ
    
    Returns:
        リサイズされた画像
    """
    img = Image.open(image_path)
    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
    return img

def enhance_contrast(image_path):
    """
    画像のコントラストを強化
    
    Args:
        image_path: 画像ファイルパス
    
    Returns:
        コントラスト強化後の画像
    """
    img = cv2.imread(image_path)
    
    # ラプラシアンのシャープニング
    kernel = np.array([[-1, -1, -1],
                       [-1,  9, -1],
                       [-1, -1, -1]])
    sharpened = cv2.filter2D(img, -1, kernel)
    
    return sharpened

def remove_background(image_path):
    """
    背景を除去
    
    Args:
        image_path: 画像ファイルパス
    
    Returns:
        背景除去後の画像
    """
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # GrabCutで背景除去
    mask = np.zeros(img.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    
    rect = (10, 10, img.shape[1]-10, img.shape[0]-10)
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    result = img * mask2[:, :, np.newaxis]
    
    return result

def normalize_image_size(image_path, target_size=512):
    """
    画像を指定サイズに正規化
    
    Args:
        image_path: 画像ファイルパス
        target_size: ターゲットサイズ
    
    Returns:
        正規化された画像
    """
    img = cv2.imread(image_path)
    resized = cv2.resize(img, (target_size, target_size))
    return resized
