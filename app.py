
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="Vie L’Ven Lead Dashboard")

@st.cache_data
def load_data():
    return pd.read_csv("data/vie_lven_leads_dashboard_final_named_enriched.csv")

df = load_data()

female_names = ['Isabelle', 'Chloe', 'Sophie', 'Charlotte', 'Zoe', 'Amelie', 'Lena', 'Maëlle', 'Nora', 'Eva']
def get_avatar(name):
    if any(fname in name for fname in female_names):
        return "https://www.w3schools.com/howto/img_avatar2.png"
    return "https://www.w3schools.com/howto/img_avatar.png"

with st.sidebar:
    st.header("🎯 Filter Leads")
    country = st.multiselect("🌍 Country", df['country'].unique(), default=df['country'].unique())
    language = st.multiselect("🗣️ Language", df['language'].unique(), default=df['language'].unique())
    source = st.multiselect("📲 Lead Source", df['source'].unique(), default=df['source'].unique())
    age_bucket = st.multiselect("👤 Age Bucket", df['age_bucket'].unique(), default=df['age_bucket'].unique())

df_f = df.query("country in @country and language in @language and source in @source and age_bucket in @age_bucket")

st.title("📊 Vie L’Ven AI-Powered Lead Dashboard")
st.markdown("##### Explore and personalize communication with high-value leads using AI-enriched data")

st.dataframe(df_f, use_container_width=True)

col1, col2, col3 = st.columns(3)
col1.metric("Total Leads", len(df_f))
col2.metric("Avg Lead Score", f"{df_f['lead_score'].mean():.1f}")
col3.metric("High Potential (%)", f"{(df_f['lead_score']>75).mean()*100:.1f}%")

st.markdown("## 📈 Lead Score Distribution")
fig, ax = plt.subplots(figsize=(6, 3))
sns.histplot(df_f['lead_score'], bins=10, kde=False, color='skyblue', edgecolor='black', ax=ax)
ax.set_xlabel("Lead Score")
ax.set_ylabel("Number of Leads")
ax.set_title("Distribution of Lead Scores")
st.pyplot(fig)

st.markdown("## 🧠 Lead Detail")
lead = st.selectbox("🔍 Pick a Lead", df_f['name'].unique())
record = df_f[df_f['name'] == lead].iloc[0]
st.image(get_avatar(record['name']), width=100)

st.markdown(f"""
**Name:** {record['name']}  
**Country:** {record['country']}  
**Language:** {record['language']}  
**Source:** {record['source']}  
**Goal:** {record['goal'].capitalize()}  
**Budget:** ${record['budget']:,.0f}  
**Age:** {record['age']} ({record['age_bucket']})  
**Lead Score:** {record['lead_score']}
""")

st.markdown("## ✉️ Personalized Message")
st.text_area("Preview / Edit Message", record['personalized_message'], height=300)

st.markdown("## 🖼️ Featured Properties")
st.image([
    "https://tse2.mm.bing.net/th/id/OIP.EpNXeDwoyexJvCDm0pSkpAHaE8?pid=Api",
    "https://tse2.mm.bing.net/th/id/OIP.5nkOUnsT5UJPJMjQi92qQQHaEK?pid=Api",
    "https://tse1.mm.bing.net/th/id/OIP.sF4-xT2lJFe8WTmEOXWBkAHaJ1?pid=Api"
], caption=["Oceanfront Villa", "Resort Pool Deck", "Panoramic Lounge View"], width=250)

st.download_button(
    label="📥 Download Filtered Leads as CSV",
    data=df_f.to_csv(index=False).encode('utf-8'),
    file_name="filtered_leads.csv",
    mime="text/csv"
)
