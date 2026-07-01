import streamlit as st
import pandas as pd

# ------------------------------------
# 画面設定
# ------------------------------------
st.set_page_config(
    page_title="筋検索システム",
    layout="wide"
)

# ------------------------------------
# データ読込
# ------------------------------------
@st.cache_data
def load_data():
    return pd.read_excel(
        "筋検索_Access取込用.xlsx",
        sheet_name="Muscles",
        engine="openpyxl"
    )

df = load_data()

# ------------------------------------
# タイトル
# ------------------------------------
st.title("筋検索システム")

# ------------------------------------
# 検索
# ------------------------------------
keyword = st.text_input(
    "検索キーワード",
    placeholder="筋名・作用・神経支配・髄節など"
)

if keyword:

    mask = pd.Series(False, index=df.index)

    for col in df.columns:
        mask = mask | df[col].astype(str).str.contains(
            keyword,
            case=False,
            na=False
        )

    result = df[mask]

else:
    result = df

st.write(f"検索結果：{len(result)} 件")

# ------------------------------------
# 左右レイアウト
# ------------------------------------
left, right = st.columns([1, 2])

# ------------------------------------
# 左：検索結果一覧
# ------------------------------------
with left:

    st.subheader("筋肉一覧")

    if len(result) == 0:

        st.warning("該当データがありません")
        selected_muscle = None

    else:

        muscle_names = result["筋名"].tolist()

        selected_muscle = st.radio(
            "検索結果",
            muscle_names,
            label_visibility="collapsed"
        )

# ------------------------------------
# 右：詳細表示
# ------------------------------------
with right:

    if selected_muscle:

        row = result[
            result["筋名"] == selected_muscle
        ].iloc[0]

        st.header(row["筋名"])

        tab1, tab2, tab3 = st.tabs(
            ["基本情報", "備考", "全データ"]
        )

        # -------------------------
        # 基本情報
        # -------------------------
        with tab1:

            col1, col2 = st.columns(2)

            with col1:

                st.markdown("### 英語名")
                st.info(str(row["筋名（英語）"]))

                st.markdown("### 起始")
                st.write(row["起始"])

                st.markdown("### 停止")
                st.write(row["停止"])

            with col2:

                st.markdown("### 作用")
                st.write(row["作用"])

                st.markdown("### 神経支配")
                st.success(str(row["神経支配"]))

                st.markdown("### 髄節")
                st.warning(str(row["髄節"]))

        # -------------------------
        # 備考
        # -------------------------
        with tab2:

            found = False

            for col in df.columns:

                if "備考" in col:

                    value = row[col]

                    if pd.notna(value):

                        found = True

                        st.markdown(f"#### {col}")
                        st.write(value)
                        st.divider()

            if not found:
                st.info("備考はありません")

        # -------------------------
        # 全データ表示
        # -------------------------
        with tab3:

            detail = {}

            for col in df.columns:

                value = row[col]

                if pd.notna(value):
                    detail[col] = str(value)

            st.json(detail)

# ------------------------------------
# 一覧表表示
# ------------------------------------
st.divider()

st.subheader("検索結果一覧")

display_cols = [
    "筋名",
    "筋名（英語）",
    "作用",
    "神経支配",
    "髄節"
]

available_cols = [
    c for c in display_cols
    if c in result.columns
]

st.dataframe(
    result[available_cols],
    use_container_width=True,
    hide_index=True
)