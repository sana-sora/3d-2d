from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import cm, mm
from reportlab.pdfgen import canvas
from PIL import Image
import os
from datetime import datetime

def create_pattern_pdf(pattern_path, output_folder):
    """
    型紙画像をPDFに変換
    
    Args:
        pattern_path: 型紙画像パス
        output_folder: 出力フォルダ
    
    Returns:
        PDF ファイルパス
    """
    try:
        # 型紙画像を読み込み
        pattern_img = Image.open(pattern_path)
        
        # A4サイズでPDFを作成
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pdf_filename = f"pattern_{timestamp}.pdf"
        pdf_path = os.path.join(output_folder, pdf_filename)
        
        # 画像をA4に合わせてリサイズ
        a4_width = 210  # mm
        a4_height = 297  # mm
        
        # 画像のアスペクト比を保持しながらリサイズ
        img_aspect = pattern_img.width / pattern_img.height
        a4_aspect = a4_width / a4_height
        
        if img_aspect > a4_aspect:
            # 幅に合わせる
            new_width = a4_width - 2  # 1cm余白
            new_height = new_width / img_aspect
        else:
            # 高さに合わせる
            new_height = a4_height - 2  # 1cm余白
            new_width = new_height * img_aspect
        
        pattern_img = pattern_img.resize(
            (int(new_width * 11.8), int(new_height * 11.8)),
            Image.Resampling.LANCZOS
        )
        
        # PDF を作成
        c = canvas.Canvas(pdf_path, pagesize=A4)
        width, height = A4
        
        # ページに画像を配置（中央）
        x = (width - new_width * mm) / 2
        y = (height - new_height * mm) / 2
        
        # 一時的に画像を保存
        temp_img_path = os.path.join(output_folder, f"temp_{timestamp}.png")
        pattern_img.save(temp_img_path)
        
        # PDFに画像を埋め込み
        c.drawImage(temp_img_path, x, y, width=new_width*mm, height=new_height*mm)
        
        # タイトルを追加
        c.setFont("Helvetica", 14)
        c.drawString(1*cm, height - 1*cm, "Plush Toy Sewing Pattern")
        
        # 指示を追加
        c.setFont("Helvetica", 10)
        c.drawString(1*cm, height - 1.5*cm, "Scale: 1:1")
        c.drawString(1*cm, height - 2*cm, "Seam allowance: 1cm")
        
        # PDFを保存
        c.save()
        
        # 一時ファイルを削除
        os.remove(temp_img_path)
        
        return pdf_path
    
    except Exception as e:
        print(f"PDF生成エラー: {str(e)}")
        raise

def create_multi_page_pattern_pdf(pattern_paths, output_folder):
    """
    複数の型紙を1つのPDFにまとめる
    
    Args:
        pattern_paths: 型紙画像パスのリスト
        output_folder: 出力フォルダ
    
    Returns:
        PDF ファイルパス
    """
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pdf_filename = f"multi_pattern_{timestamp}.pdf"
        pdf_path = os.path.join(output_folder, pdf_filename)
        
        c = canvas.Canvas(pdf_path, pagesize=A4)
        width, height = A4
        
        for i, pattern_path in enumerate(pattern_paths):
            pattern_img = Image.open(pattern_path)
            
            # 画像をA4に合わせてリサイズ
            a4_width = 190  # mm
            a4_height = 275  # mm
            
            img_aspect = pattern_img.width / pattern_img.height
            a4_aspect = a4_width / a4_height
            
            if img_aspect > a4_aspect:
                new_width = a4_width
                new_height = new_width / img_aspect
            else:
                new_height = a4_height
                new_width = new_height * img_aspect
            
            pattern_img = pattern_img.resize(
                (int(new_width * 11.8), int(new_height * 11.8)),
                Image.Resampling.LANCZOS
            )
            
            # ページに画像を配置
            x = (width - new_width * mm) / 2
            y = (height - new_height * mm) / 2
            
            temp_img_path = os.path.join(output_folder, f"temp_{i}_{timestamp}.png")
            pattern_img.save(temp_img_path)
            
            c.drawImage(temp_img_path, x, y, width=new_width*mm, height=new_height*mm)
            
            # ページタイトル
            c.setFont("Helvetica", 12)
            c.drawString(1*cm, height - 0.8*cm, f"Pattern Page {i+1}")
            
            # 次のページへ
            if i < len(pattern_paths) - 1:
                c.showPage()
            
            os.remove(temp_img_path)
        
        c.save()
        return pdf_path
    
    except Exception as e:
        print(f"マルチページPDF生成エラー: {str(e)}")
        raise
