import streamlit as st
import pandas as pd
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from scrawl import fetch_webpage  # Uncomment and adjust if fetch_webpage is needed and available
st.set_page_config(page_title="中文客服檢索回覆", page_icon="💬", layout="wide")

st.title("中文客服檢索回覆系統")

# DEFAULT_FAQ = pd.DataFrame(
#     [
#         {"question":"你們的營業時間是？","answer":"我們的客服時間為週一至週五 09:00–18:00（國定假日除外）。"},
#         {"question":"如何申請退貨？","answer":"請於到貨 7 天內透過訂單頁面點選『申請退貨』，系統將引導您完成流程。"},
#         {"question":"運費如何計算？","answer":"單筆訂單滿 NT$ 1000 免運，未滿則酌收 NT$ 80。"},
#         {"question":"可以開立發票嗎？","answer":"我們提供電子發票，請於結帳時填寫統一編號與抬頭。"},
#     ]
# )
DEFAULT_FAQ = pd.DataFrame(fetch_webpage("https://parkweb.tainan.gov.tw/api/parking.php"))
if "faq_df" not in st.session_state:
    st.session_state.faq_df = DEFAULT_FAQ.copy()
if "vectorizer" not in st.session_state:
    st.session_state.vectorizer = None
if "tfidf" not in st.session_state:
    st.session_state.tfidf = None

st.subheader("上傳知識庫")
# uploaded_file = st.file_uploader("選擇一個 CSV 檔案", type="csv")
uploaded_file = st.file_uploader("選擇一個 JSON 檔案", type="json")
if uploaded_file is not None:
    new_faq = pd.read_json(uploaded_file, encoding="utf-8")
    st.session_state.faq_df = pd.concat([st.session_state.faq_df, new_faq], ignore_index=True)
    st.write(new_faq)
    # 取代前面的DEFAULT_FAQ，去空白紀錄，並讓資料重整理
    st.session_state.faq_df = new_faq.dropna().reset_index(drop=True)
    st.success(f"已成功載入{len(new_faq)}筆資料")
    

with st.expander("檢視資料", expanded=False):
    st.dataframe(st.session_state.faq_df,use_container_width=True)


#建立索引
do_index = st.button("建立/重設索引")

def create_index(text: str):
    # 使用結巴斷詞進行中文分詞
    # jieba.set_dictionary("dict.txt.big")
    # st.session_state.faq_df["question_cut"] = st.session_state.faq_df["question"].apply(lambda x: " ".join(jieba.cut(x)))
    # st.session_state.vectorizer = TfidfVectorizer()
    # st.session_state.tfidf = st.session_state.vectorizer.fit_transform(st.session_state.faq_df["question_cut"])
    # st.success("索引建立完成！")
    return list(jieba.cut(text))

if do_index or (st.session_state.vectorizer is None):
    corpus = (st.session_state.faq_df["typeId"].astype(str)+" "+st.session_state.faq_df["typeName"].astype(str)+" "+st.session_state.faq_df["id"].astype(str)+" "+st.session_state.faq_df["code"].astype(str)+" "+st.session_state.faq_df["name"].astype(str)+" "+st.session_state.faq_df["zoneId"].astype(str)+" "+st.session_state.faq_df["largeCar"].astype(str)+" "+st.session_state.faq_df["car"].astype(str)+" "+st.session_state.faq_df["carDis"].astype(str)+" "+st.session_state.faq_df["carWoman"].astype(str)+" "+st.session_state.faq_df["carGreen"].astype(str)+" "+st.session_state.faq_df["moto"].astype(str)+" "+st.session_state.faq_df["motoDis"].astype(str)+" "+st.session_state.faq_df["largeCar_total"].astype(str)+" "+st.session_state.faq_df["car_total"].astype(str)+" "+st.session_state.faq_df["carDis_total"].astype(str)+" "+st.session_state.faq_df["carWoman_total"].astype(str)+" "+st.session_state.faq_df["carGreen_total"].astype(str)+" "+st.session_state.faq_df["moto_total"].astype(str)+" "+ st.session_state.faq_df["chargeTime"].astype(str)+" "+st.session_state.faq_df["chargeFee"].astype(str)+" "+ st.session_state.faq_df["update_time"].astype(str)+" "+st.session_state.faq_df["lnglat"].astype(str)).tolist() # if st.session_state.vectorizer else []
    v = TfidfVectorizer(tokenizer=create_index)
    tfidf = v.fit_transform(corpus)
    st.session_state.vectorizer = v
    st.session_state.tfidf = tfidf
    st.success("索引已建立或重設！")
    # create_index(user_question)

# 問題輸入
user_question = st.text_input("請輸入您的問題：", placeholder="例如：你們的營業時間是？")
top_k = st.slider("選擇回覆數量", min_value=1, max_value=10, value=3)
c = st.slider("信心門檻", min_value=0.0, max_value=1.0, value=0.5)

if st.button("送出") and user_question.strip():
    if (st.session_state.vectorizer is None) or (st.session_state.tfidf is None):
        st.warning("尚未建立索引，會自動建立!")
        corpus = (st.session_state.faq_df["typeId"].astype(str)+" "+st.session_state.faq_df["typeName"].astype(str)+" "+st.session_state.faq_df["id"].astype(str)+" "+st.session_state.faq_df["code"].astype(str)+" "+st.session_state.faq_df["name"].astype(str)+" "+st.session_state.faq_df["zoneId"].astype(str)+" "+st.session_state.faq_df["largeCar"].astype(str)+" "+st.session_state.faq_df["car"].astype(str)+" "+st.session_state.faq_df["carDis"].astype(str)+" "+st.session_state.faq_df["carWoman"].astype(str)+" "+st.session_state.faq_df["carGreen"].astype(str)+" "+st.session_state.faq_df["moto"].astype(str)+" "+st.session_state.faq_df["motoDis"].astype(str)+" "+st.session_state.faq_df["largeCar_total"].astype(str)+" "+st.session_state.faq_df["car_total"].astype(str)+" "+st.session_state.faq_df["carDis_total"].astype(str)+" "+st.session_state.faq_df["carWoman_total"].astype(str)+" "+st.session_state.faq_df["carGreen_total"].astype(str)+" "+st.session_state.faq_df["moto_total"].astype(str)+" "+ st.session_state.faq_df["chargeTime"].astype(str)+" "+st.session_state.faq_df["chargeFee"].astype(str)+" "+ st.session_state.faq_df["update_time"].astype(str)+" "+st.session_state.faq_df["lnglat"].astype(str)).tolist() # if st.session_state.vectorizer else []
        v = TfidfVectorizer(tokenizer=create_index)
        tfidf = v.fit_transform(corpus)
        st.session_state.vectorizer = v
        st.session_state.tfidf = tfidf
        st.success("索引已建立或重設！")

    vec = st.session_state.vectorizer.transform([user_question])
    sims = linear_kernel(vec, st.session_state.tfidf).flatten()
    idxc = sims.argsort()[::-1][:top_k] #由大到小排序取前top_k個
    rows = st.session_state.faq_df.iloc[idxc].copy()
    rows['score'] = sims[idxc]

    best_ans = None
    best_score = float(rows['score'].iloc[0]) if len(rows) > 0 else 0.0
    if best_score >= c:
        best_ans = rows['answer'].iloc[0]
    if best_ans:
        st.success(f"最佳回覆：{best_ans}")
    else:
        st.warning("沒有找到符合條件的回覆。")

    #展開可能的回答
    with st.expander("檢索結果:", expanded=False):
        st.dataframe(rows[['question', 'answer', 'score']], use_container_width=True)   


