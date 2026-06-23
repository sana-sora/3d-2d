// API ベース URL
const API_BASE_URL = 'http://localhost:5000/api';

// グローバル変数
let currentStep = 1;
let uploadedFilename = null;
let maskFilename = null;
let meshFilename = null;
let patternFilename = null;

// UI 要素の取得
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const imagePreview = document.getElementById('imagePreview');
const previewImg = document.getElementById('previewImg');
const nextBtn1 = document.getElementById('nextBtn1');
const uploadStatus = document.getElementById('uploadStatus');

// イベントリスナー登録
document.addEventListener('DOMContentLoaded', () => {
    setupUploadEvents();
    setupNavigationButtons();
});

// ========== アップロード処理 ==========
function setupUploadEvents() {
    // クリックでファイル選択
    uploadArea.addEventListener('click', () => fileInput.click());

    // ドラッグ&ドロップ
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });

    // ファイル入力変更
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });
}

function handleFileSelect(file) {
    // ファイル形式確認
    if (!file.type.startsWith('image/')) {
        showStatus('uploadStatus', 'エラー: 画像ファイルを選択してください', 'error');
        return;
    }

    // ファイルサイズ確認
    if (file.size > 16 * 1024 * 1024) {
        showStatus('uploadStatus', 'エラー: ファイルサイズが大きすぎます（16MB以下）', 'error');
        return;
    }

    // プレビュー表示
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImg.src = e.target.result;
        imagePreview.style.display = 'block';
    };
    reader.readAsDataURL(file);

    // アップロード実行
    uploadImage(file);
}

async function uploadImage(file) {
    showStatus('uploadStatus', 'アップロード中...', 'info');
    showLoading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('アップロード失敗');
        }

        const data = await response.json();
        uploadedFilename = data.filename;

        showStatus('uploadStatus', 'アップロード完了！', 'success');
        nextBtn1.style.display = 'inline-block';

    } catch (error) {
        showStatus('uploadStatus', `エラー: ${error.message}`, 'error');
        console.error(error);
    } finally {
        showLoading(false);
    }
}

// ========== セグメンテーション処理 ==========
function setupNavigationButtons() {
    // ステップ 1 → 2
    document.getElementById('nextBtn1').addEventListener('click', () => {
        goToStep(2);
        performSegmentation();
    });

    // ステップ 2 → 3
    document.getElementById('nextBtn2').addEventListener('click', () => {
        goToStep(3);
        performMeshGeneration();
    });

    // ステップ 3 → 4
    document.getElementById('nextBtn3').addEventListener('click', () => {
        goToStep(4);
        performPatternGeneration();
    });

    // ステップ 4 → 5
    document.getElementById('nextBtn4').addEventListener('click', () => {
        goToStep(5);
    });

    // 戻るボタン
    document.getElementById('prevBtn2').addEventListener('click', () => goToStep(1));
    document.getElementById('prevBtn3').addEventListener('click', () => goToStep(2));
    document.getElementById('prevBtn4').addEventListener('click', () => goToStep(3));
    document.getElementById('prevBtn5').addEventListener('click', () => goToStep(4));

    // ダウンロードボタン
    document.getElementById('downloadPdfBtn').addEventListener('click', downloadPdf);
    document.getElementById('downloadPngBtn').addEventListener('click', downloadPng);

    // リセットボタン
    document.getElementById('resetBtn').addEventListener('click', resetAll);
}

async function performSegmentation() {
    if (!uploadedFilename) return;

    showStatus('segmentationStatus', 'セグメンテーション処理中...', 'info');
    showLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/segment`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ filename: uploadedFilename })
        });

        if (!response.ok) {
            throw new Error('セグメンテーション失敗');
        }

        const data = await response.json();
        maskFilename = data.mask_filename;

        showStatus('segmentationStatus', data.message, 'success');

        // プレビュー表示（必要に応じて）
        // const maskUrl = `${API_BASE_URL}/download/${maskFilename}`;
        // document.getElementById('segmentImg').src = maskUrl;
        // document.getElementById('segmentationPreview').style.display = 'block';

        document.getElementById('nextBtn2').style.display = 'inline-block';

    } catch (error) {
        showStatus('segmentationStatus', `エラー: ${error.message}`, 'error');
        console.error(error);
    } finally {
        showLoading(false);
    }
}

async function performMeshGeneration() {
    if (!maskFilename) return;

    showStatus('meshStatus', '3Dメッシュ生成中...', 'info');
    showLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/generate-mesh`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ mask_filename: maskFilename })
        });

        if (!response.ok) {
            throw new Error('メッシュ生成失敗');
        }

        const data = await response.json();
        meshFilename = data.mesh_filename;

        showStatus('meshStatus', data.message, 'success');
        document.getElementById('nextBtn3').style.display = 'inline-block';

    } catch (error) {
        showStatus('meshStatus', `エラー: ${error.message}`, 'error');
        console.error(error);
    } finally {
        showLoading(false);
    }
}

async function performPatternGeneration() {
    if (!meshFilename) return;

    showStatus('patternStatus', '型紙生成中...', 'info');
    showLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/generate-pattern`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ mesh_filename: meshFilename })
        });

        if (!response.ok) {
            throw new Error('型紙生成失敗');
        }

        const data = await response.json();
        patternFilename = data.pattern_filename;

        showStatus('patternStatus', data.message, 'success');

        // プレビュー表示
        const patternUrl = `${API_BASE_URL}/download/${patternFilename}`;
        document.getElementById('patternImg').src = patternUrl;
        document.getElementById('patternPreview').style.display = 'block';

        document.getElementById('nextBtn4').style.display = 'inline-block';

    } catch (error) {
        showStatus('patternStatus', `エラー: ${error.message}`, 'error');
        console.error(error);
    } finally {
        showLoading(false);
    }
}

// ========== ダウンロード処理 ==========
async function downloadPdf() {
    if (!patternFilename) return;

    showLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/generate-pdf`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ pattern_filename: patternFilename })
        });

        if (!response.ok) {
            throw new Error('PDF生成失敗');
        }

        const data = await response.json();
        const pdfUrl = `${API_BASE_URL}/download/${data.pdf_filename}`;

        // ファイルダウンロード
        const link = document.createElement('a');
        link.href = pdfUrl;
        link.download = data.pdf_filename;
        link.click();

        showStatus('downloadStatus', 'PDFをダウンロードしました！', 'success');

    } catch (error) {
        showStatus('downloadStatus', `エラー: ${error.message}`, 'error');
        console.error(error);
    } finally {
        showLoading(false);
    }
}

function downloadPng() {
    if (!patternFilename) return;

    const pngUrl = `${API_BASE_URL}/download/${patternFilename}`;
    const link = document.createElement('a');
    link.href = pngUrl;
    link.download = patternFilename;
    link.click();

    showStatus('downloadStatus', '画像をダウンロードしました！', 'success');
}

// ========== ユーティリティ関数 ==========
function goToStep(step) {
    currentStep = step;

    // ステップ表示の更新
    document.querySelectorAll('.step').forEach((el, i) => {
        el.classList.toggle('active', i + 1 === step);
    });

    // コンテンツの表示更新
    document.querySelectorAll('.step-content').forEach((el, i) => {
        el.classList.toggle('active', i + 1 === step);
    });

    // ページをトップにスクロール
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showStatus(elementId, message, type) {
    const element = document.getElementById(elementId);
    element.textContent = message;
    element.className = `status-message ${type}`;
}

function showLoading(show) {
    document.getElementById('loading').style.display = show ? 'flex' : 'none';
}

function resetAll() {
    // グローバル変数をリセット
    uploadedFilename = null;
    maskFilename = null;
    meshFilename = null;
    patternFilename = null;

    // UI をリセット
    fileInput.value = '';
    imagePreview.style.display = 'none';
    document.getElementById('segmentationPreview').style.display = 'none';
    document.getElementById('patternPreview').style.display = 'none';

    document.querySelectorAll('.status-message').forEach(el => {
        el.className = 'status-message';
        el.textContent = '';
    });

    document.querySelectorAll('.btn-primary').forEach(btn => {
        btn.style.display = 'none';
    });

    // ステップ 1 に戻る
    goToStep(1);
}
