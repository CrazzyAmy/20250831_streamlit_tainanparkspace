"""
範例01：基礎網頁抓取
目標：學習使用requests庫抓取網頁內容
"""

import requests

def fetch_webpage(url: str):
    """抓取網頁內容的基礎函數"""
    
    # 設定目標網址
    # url = "https://httpbin.org/html"
    
    try:
        # 發送GET請求
        response = requests.get(url)
        
        # 檢查請求是否成功
        if response.status_code == 200:
            print("✅ 網頁抓取成功！")
            print(f"狀態碼：{response.status_code}")
            print(f"內容長度：{len(response.text)} 字符")
            print("=" * 50)
            print("網頁內容前500字符：")
            print(response.text[:])
            return response.json()
        else:
            print(f"❌ 請求失敗，狀態碼：{response.status_code}")
            
    except requests.exceptions.RequestException as error:
        print(f"❌ 發生錯誤：{error}")

if __name__ == "__main__":
    print("範例01：基礎網頁抓取")
    print("=" * 30)
    fetch_webpage() 