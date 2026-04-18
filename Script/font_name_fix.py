from fontTools.ttLib import TTFont
import os

# --- 設定區 ---
INPUT_FONT = 'MantouSans-Regular.ttf'  # 原始檔案
OUTPUT_FONT = 'MantouSans-Fixed.ttf'   # 修正後檔案

def fix_and_report():
    if not os.path.exists(INPUT_FONT):
        print(f"錯誤：找不到檔案 {INPUT_FONT}，請確認檔案放在相同資料夾。")
        return

    # 1. 載入字體
    tt = TTFont(INPUT_FONT)
    name_table = tt['name']

    # 2. 定義要注入的 Macintosh 紀錄 (platformID=1, platEncID=0, langID=0)
    # 格式：(NameID, 字串內容)
    # ID 1: Family, ID 2: Subfamily, ID 4: Full Name, ID 6: PostScript
    mac_metadata = [
        (1, "Mantou Sans"),
        (2, "Regular"),
        (4, "Mantou Sans"),
        (6, "MantouSans"),
    ]

    print(f"開始注入 Macintosh (Platform 1) 紀錄...")
    
    for nid, val in mac_metadata:
        name_table.setName(
            val,
            nameID=nid,
            platformID=1,    # Macintosh
            platEncID=0,     # Roman
            langID=0         # English
        )

    # 3. 儲存字體
    tt.save(OUTPUT_FONT)
    print(f"修正完成！檔案已儲存為：{OUTPUT_FONT}\n")

    # 4. 讀取新檔案並顯示結果表格
    print("=" * 70)
    print(f"{'ID':<6} | {'平台 (Platform)':<15} | {'語言 (Lang)':<10} | {'內容 (Value)'}")
    print("-" * 70)
    
    fixed_tt = TTFont(OUTPUT_FONT)
    # 過濾出我們關心的 NameID 並排序
    records = sorted(fixed_tt['name'].names, key=lambda x: (x.nameID, x.platformID))
    
    for r in records:
        if r.nameID in (1, 2, 4, 6):
            p_name = "Macintosh (1)" if r.platformID == 1 else "Windows (3)"
            try:
                content = r.toUnicode()
            except:
                content = str(r.string)
            
            print(f"{r.nameID:<6} | {p_name:<15} | {r.langID:<10} | {content}")
    print("=" * 70)
    print("提示：請檢查 ID 6 是否完全沒有空格。現在您的字體已具備完美的跨平台相容性！")

if __name__ == "__main__":
    fix_and_report()