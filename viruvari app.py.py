import streamlit as st
import pandas as pd
import plotly.express as px

# पेज की सेटिंग
st.set_page_config(page_title="Data Analyst Cloud Studio", layout="wide")

st.title("🚀 मेरा पहला Data Analyst Cloud Studio")
st.write("यह ऐप वीडियो में दिखाए गए *Data Plugin, **Task Board, और **Custom Skills* को एक साथ समझाता है।")

# तीन मुख्य टैब बनाना
tab1, tab2, tab3 = st.tabs(["📊 Data Visualizer (चैट व चार्ट)", "📋 Course Task Board", "🧠 Custom AI Skill (SKILL.md)"])

# --- TAB 1: DATA VISUALIZER ---
with tab1:
    st.header("1. डेटा अपलोड करें और तुरंत चार्ट बनाएं")
    
    # वीडियो वाला सैंपल डेटा
    sample_data = pd.DataFrame({
        "Region": ["North America", "EMEA", "Asia", "Latin America"],
        "Revenue":[1450000,820000,610000,310000],
        "Growth_Percent": [12, 8, 15, 5]
    })
    
    uploaded_file = st.file_uploader("अपनी CSV या Excel फाइल अपलोड करें (या नीचे दिए गए सैंपल डेटा का उपयोग करें)", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.success("आपकी फाइल सफलतापूर्वक लोड हो गई है!")
    else:
        df = sample_data
        st.info("अभी वीडियो वाला सैंपल डेटा दिख रहा है। आप ऊपर से अपनी Excel/CSV फाइल भी डाल सकते हैं।")

    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.subheader("डेटा तालिका (Data Table)")
        st.dataframe(df, use_container_width=True)
        
    with col2:
        st.subheader("विज़ुअलाइज़ेशन (Chart)")
        # कॉलम चुनने का विकल्प
        text_cols = df.select_dtypes(include=['object']).columns.tolist()
        num_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if text_cols and num_cols:
            name_col = st.selectbox("नाम वाला कॉलम चुनें (Category):", text_cols)
            val_col = st.selectbox("संख्या वाला कॉलम चुनें (Value):", num_cols)
            chart_type = st.radio("चार्ट का प्रकार:", ["Pie Chart (पाई चार्ट)", "Bar Chart (बार चार्ट)"], horizontal=True)
            
            if chart_type == "Pie Chart (पाई चार्ट)":
                fig = px.pie(df, names=name_col, values=val_col, title=f"{name_col} के अनुसार {val_col}")
            else:
                fig = px.bar(df, x=name_col, y=val_col, title=f"{name_col} के अनुसार {val_col}", color=name_col)
                
            st.plotly_chart(fig, use_container_width=True)
            st.caption("💡 सीख: वीडियो में बताया गया था कि 'Growth %' की जगह 'Revenue' चुनना सही है, क्योंकि कुल संख्या का जोड़ ही 100% हिस्सा बनाता है।")

# --- TAB 2: TASK BOARD ---
with tab2:
    st.header("2. मेरा Data Analysis कोर्स टास्क बोर्ड")
    
    if "tasks" not in st.session_state:
        st.session_state.tasks = [
            {"task": "Excel VLOOKUP और XLOOKUP का अभ्यास", "status": "Done"},
            {"task": "Pivot Table असाइनमेंट पूरा करना", "status": "In Progress"},
            {"task": "Data Cleaning के नियम सीखना", "status": "To Do"}
        ]
    
    new_task = st.text_input("नया काम जोड़ें (जैसे: SQL की बेसिक क्वेरी सीखना):")
    if st.button("टास्क जोड़ें"):
        if new_task:
            st.session_state.tasks.append({"task": new_task, "status": "To Do"})
            st.rerun()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("📌 To Do")
        for i, t in enumerate(st.session_state.tasks):
            if t["status"] == "To Do":
                st.warning(t["task"])
                if st.button("शुरू करें ➡️", key=f"start_{i}"):
                    st.session_state.tasks[i]["status"] = "In Progress"
                    st.rerun()
    with c2:
        st.subheader("⏳ In Progress")
        for i, t in enumerate(st.session_state.tasks):
            if t["status"] == "In Progress":
                st.info(t["task"])
                if st.button("पूरा हुआ ✅", key=f"done_{i}"):
                    st.session_state.tasks[i]["status"] = "Done"
                    st.rerun()
    with c3:
        st.subheader("✅ Done")
        for t in st.session_state.tasks:
            if t["status"] == "Done":
                st.success(t["task"])

# --- TAB 3: CUSTOM AI SKILL ---
with tab3:
    st.header("3. मेरी कस्टम AI Skill (SKILL.md)")
    st.write("वीडियो के अंत में जो SKILL.md फाइल दिखाई गई थी, यह वैसा ही एक नियम है। इसे कॉपी करके किसी भी AI को दें:")
    
    skill_text = """# SKILL: Excel Data Analyst Helper
## Role
आप एक अनुभवी Data Analyst और Excel शिक्षक हैं।
## Rules
1. जब भी मैं कोई Excel समस्या पूछूं, तो सबसे पहले सबसे आसान फॉर्मूला (जैसे XLOOKUP या SUMIFS) बताएं।
2. फॉर्मूले के हर हिस्से को आसान हिंदी में समझाएं।
3. हमेशा एक छोटा उदाहरण (Example Table) देकर दिखाएं कि डेटा कैसा दिखेगा।
4. अगर मेरे डेटा में कोई गलती हो सकती है (जैसे #N/A एरर), तो उससे बचने के लिए IFERROR का उपयोग जरूर बताएं।"""
    
    st.code(skill_text, language="markdown")
