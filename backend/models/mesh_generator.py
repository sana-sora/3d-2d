import cv2
import numpy as np
import open3d as o3d
import os
from datetime import datetime

def generate_mesh(mask_path, output_folder):
    """
    マスク画像から3Dメッシュを生成
    
    Args:
        mask_path: マスク画像パス
        output_folder: 出力フォルダ
    
    Returns:
        メッシュファイル（PLY形式）のパス
    """
    try:
        # マスク画像を読み込み
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        if mask is None:
            raise ValueError(f"マスク画像が読み込めません: {mask_path}")
        
        # 輪郭を検出
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            raise ValueError("輪郭が検出できません")
        
        # 最大の輪郭を取得
        largest_contour = max(contours, key=cv2.contourArea)
        
        # 輪郭から3D座標を生成（簡易版）
        contour_points = largest_contour.squeeze()
        
        if len(contour_points.shape) == 1:
            contour_points = contour_points.reshape(-1, 2)
        
        # 2D座標を3D座標に変換（Z軸を高さとして使用）
        # 簡易的には、マスクの値を高さとして使用
        points_3d = []
        for point in contour_points:
            x, y = point
            # 距離を計算して高さを決定（内側が高い）
            distance_from_edge = cv2.pointPolygonTest(largest_contour, (x, y), True)
            z = max(0, distance_from_edge / 10)  # スケーリング
            points_3d.append([x, y, z])
        
        points_3d = np.array(points_3d)
        
        # Open3Dで点群を作成
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points_3d)
        
        # 色を付与（グレースケール）
        colors = np.random.rand(points_3d.shape[0], 3)
        pcd.colors = o3d.utility.Vector3dVector(colors)
        
        # ポアソン再構成でメッシュを生成
        try:
            # 法線を推定
            pcd.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=10, max_nn=30))
            
            # ポアソン再構成
            mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9)
        except:
            # ポアソン再構成が失敗した場合は、凸包を生成
            mesh = o3d.geometry.TriangleMesh.create_box(width=1, height=1, depth=1)
        
        # メッシュをファイルに保存
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        mesh_filename = f"mesh_{timestamp}.ply"
        mesh_path = os.path.join(output_folder, mesh_filename)
        
        o3d.io.write_triangle_mesh(mesh_path, mesh)
        
        return mesh_path
    
    except Exception as e:
        print(f"メッシュ生成エラー: {str(e)}")
        raise

def create_simplified_mesh(mask_path, output_folder, simplification_target=10000):
    """
    マスク画像から簡略化されたメッシュを生成
    
    Args:
        mask_path: マスク画像パス
        output_folder: 出力フォルダ
        simplification_target: ターゲット三角形数
    
    Returns:
        メッシュファイル（PLY形式）のパス
    """
    try:
        mesh_path = generate_mesh(mask_path, output_folder)
        
        # メッシュを読み込み
        mesh = o3d.io.read_triangle_mesh(mesh_path)
        
        # メッシュを簡略化
        simplified_mesh = mesh.simplify_quadric_decimation(simplification_target)
        
        # 簡略化されたメッシュを保存
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        simplified_filename = f"mesh_simplified_{timestamp}.ply"
        simplified_path = os.path.join(output_folder, simplified_filename)
        
        o3d.io.write_triangle_mesh(simplified_path, simplified_mesh)
        
        return simplified_path
    
    except Exception as e:
        print(f"メッシュ簡略化エラー: {str(e)}")
        raise
