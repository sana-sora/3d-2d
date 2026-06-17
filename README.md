# 3D-2D: ぬいぐるみ型紙生成サイト

写真からぬいぐるみの型紙を自動生成するWebアプリケーション。

## 📋 機能

- 📷 写真アップロード
- 🎯 物体検出・セグメンテーション
- 📐 3Dメッシュ生成・2D展開図化
- 📄 型紙PDF生成
- 🌐 Webインターフェース

## 🛠️ 技術スタック

### バックエンド
- **Python 3.9+**
- **Flask** - Webフレームワーク
- **OpenCV** - 画像処理
- **Pillow** - 画像操作
- **NumPy** - 数値計算
- **Segment Anything (SAM)** - セグメンテーション
- **Open3D** - 3D処理

### フロントエンド
- HTML5
- CSS3
- JavaScript (Vanilla)

## 📁 プロジェクト構成

```
3d-2d/
├── backend/
│   ├── app.py                 # Flask メインアプリ
│   ├── requirements.txt        # Python依存パッケージ
│   ├── models/
│   │   ├── segmentation.py    # セグメンテーション
│   │   ├── mesh_generator.py  # 3Dメッシュ生成
│   │   └── pattern.py         # 型紙生成
│   ├── utils/
│   │   ├── image_processing.py # 画像処理ユーティリティ
│   │   └── pdf_generator.py    # PDF生成
│   └── uploads/               # アップロード画像
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── .gitignore
└── README.md
```

## 🚀 セットアップ手順

### 1. リポジトリをクローン
```bash
git clone https://github.com/sana-sora/3d-2d.git
cd 3d-2d
```

### 2. バックエンド環境設定
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. 実行
```bash
python app.py
```

アプリは `http://localhost:5000` で起動します。

## 📚 使い方

1. ぬいぐるみの写真をアップロード
2. 自動セグメンテーションでぬいぐるみを抽出
3. 3Dメッシュを生成
4. 2D型紙に変換
5. PDF型紙をダウンロード

## 📝 ロードマップ

- [ ] Flask API基本構造
- [ ] 画像アップロード機能
- [ ] セグメンテーション実装
- [ ] 3Dメッシュ生成
- [ ] 2D展開図化
- [ ] PDF生成
- [ ] Webインターフェース
- [ ] デプロイ

## 📖 参考資料

- [Flask Documentation](https://flask.palletsprojects.com/)
- [OpenCV](https://opencv.org/)
- [Segment Anything](https://github.com/facebookresearch/segment-anything)
- [Open3D](http://www.open3d.org/)

## 📄 ライセンス

MIT License

## 👤 作者

sana-sora
