# Streamlit の覚え書き

## 開発環境

- Windows 10/11
- Python: 3.12 (venv)
- Streamlit 1.38
- PyInstaller 6.10.0

## 環境構築

```cmd
py -3.12 -m venv .venv312

.venv312\Scripts\activate
where python
where pip

python.exe -m pip install --upgrade pip
pip install -r requirements.txt
```

## 実行方法

```cmd
.venv312\Scripts\activate

streamlit run main.py
```

VSCode で開いていれば F5 を押して `(debug) run_main.py` でデバッグ実行できるよう設定済み．
