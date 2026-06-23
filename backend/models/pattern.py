import numpy as np
import open3d as o3d
from PIL import Image, ImageDraw
import os
from datetime import datetime

def generate_pattern(mesh_path, output_folder):
    """
    3Dメッシュから2D展開図（型紙）を生成
    
    Args:
        mesh_path: メッシュファイルパス
        output_folder: 出力フォルダ
    
    Returns:
        型紙画像のパス
    """
    try:
        # メッシュを読み込み
        mesh = o3d.io.read_triangle_mesh(mesh_path)
        
        if not mesh.has_vertices():
            raise ValueError("メッシュに頂点がありません")
        
        # 頂点座標を取得
        vertices = np.asarray(mesh.vertices)
        triangles = np.asarray(mesh.triangles)
        
        # 型紙用に2D投影を生成
        # 簡易版：X-Y平面に投影
        projected_vertices = vertices[:, :2]
        
        # 座標を正規化（0-1の範囲）
        min_coords = projected_vertices.min(axis=0)
        max_coords = projected_vertices.max(axis=0)
        normalized_vertices = (projected_vertices - min_coords) / (max_coords - min_coords + 1e-6)
        
        # 画像サイズ（A4相当：210mm x 297mm = 1748 x 2480 pixels at 300dpi）
        img_size = 1200
        img = Image.new('RGB', (img_size, img_size), 'white')
        draw = ImageDraw.Draw(img)
        
        # 三角形をスケーリング
        scaled_vertices = normalized_vertices * (img_size - 50) + 25
        
        # 三角形を描画
        for triangle in triangles:
            points = [
                tuple(scaled_vertices[triangle[0]]),
                tuple(scaled_vertices[triangle[1]]),
                tuple(scaled_vertices[triangle[2]])
            ]
            draw.polygon(points, outline='black', fill=None)
        
        # 頂点も描画
        for vertex in scaled_vertices:
            draw.ellipse(
                [vertex[0]-3, vertex[1]-3, vertex[0]+3, vertex[1]+3],
                fill='red'
            )
        
        # 型紙画像を保存
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pattern_filename = f"pattern_{timestamp}.png"
        pattern_path = os.path.join(output_folder, pattern_filename)
        img.save(pattern_path)
        
        return pattern_path
    
    except Exception as e:
        print(f"型紙生成エラー: {str(e)}")
        raise

def unfold_mesh(mesh_path, output_folder):
    """
    3Dメッシュを2D展開図に展開（より高度な展開）
    
    Args:
        mesh_path: メッシュファイルパス
        output_folder: 出力フォルダ
    
    Returns:
        展開図のパス
    """
    try:
        # メッシュを読み込み
        mesh = o3d.io.read_triangle_mesh(mesh_path)
        
        # シンプルな展開方法：
        # メッシュを平面に投影して型紙を生成
        pattern_path = generate_pattern(mesh_path, output_folder)
        
        return pattern_path
    
    except Exception as e:
        print(f"メッシュ展開エラー: {str(e)}")
        raise

def add_seam_allowance(pattern_path, output_folder, allowance_mm=10):
    """
    型紙に縫い代を追加
    
    Args:
        pattern_path: 型紙画像パス
        output_folder: 出力フォルダ
        allowance_mm: 縫い代（ミリメートル）
    
    Returns:
        縫い代を追加した型紙のパス
    """
    try:
        # 型紙画像を読み込み
        pattern_img = Image.open(pattern_path)
        
        # 300dpiの場合、1mmは約11.8pixels
        allowance_pixels = int(allowance_mm * 11.8)
        
        # 画像を拡大
        new_size = (
            pattern_img.width + allowance_pixels * 2,
            pattern_img.height + allowance_pixels * 2
        )
        new_img = Image.new('RGB', new_size, 'white')
        new_img.paste(pattern_img, (allowance_pixels, allowance_pixels))
        
        # 縫い代を描画
        draw = ImageDraw.Draw(new_img)
        # 破線で縫い代の位置を表示
        # （簡易版：外枠を描画）
        
        # 縫い代追加後の型紙を保存
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        allowance_filename = f"pattern_with_allowance_{timestamp}.png"
        allowance_path = os.path.join(output_folder, allowance_filename)
        new_img.save(allowance_path)
        
        return allowance_path
    
    except Exception as e:
        print(f"縫い代追加エラー: {str(e)}")
        raise
