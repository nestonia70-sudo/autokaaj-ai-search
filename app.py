import streamlit as st
from google import genai
from tavily import TavilyClient

# ১. ওপরের গিটহাব লোগো এবং মেনু বার লুকানোর জন্য CSS কোড
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stAppDeployButton {display:none;}
            </style>
            """

# ২. সিক্রেটস থেকে এপিআই কি নেওয়া
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
except Exception:
    st.error("API Key খুঁজে পাওয়া যায়নি। দয়া করে Streamlit Advanced Settings চেক করুন।")
    st.stop()

# ৩. ক্লায়েন্ট কনফিগারেশন
client = genai.Client(api_key=GOOGLE_API_KEY)
tavily = TavilyClient(api_key=TAVILY_API_KEY)

# ৪. পেজ সেটিংস ও সিএসএস অ্যাপ্লাই
st.set_page_config(page_title="AutoKaaj AI Search", page_icon="🔍")
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("🚀 AutoKaaj AI Search Engine")
st.caption("কলকাতার লেটেস্ট তথ্য এবং স্মার্ট এআই উত্তর। Developed by Chiranjit Majumdar.")

# ৫. ইউজার ইনপুট ও প্রসেসিং
query = st.text_input("আপনি কী জানতে চান?", placeholder="উদা: আজকে কলকাতায় সোনার দাম কত?")

if query:
    with st.spinner("ইন্টারনেট থেকে লাইভ তথ্য খোঁজা হচ্ছে..."):
        try:
            # Tavily দিয়ে সার্চ
            search_response = tavily.search(query=query, search_depth="advanced", max_results=5)
            context = ""
            sources = []
            for r in search_response['results']:
                context += f"Source: {r['url']}\nContent: {r['content']}\n\n"
                sources.append(r)

            # Gemini দিয়ে উত্তর তৈরি (আপনার বর্তমান সময় অনুযায়ী আপডেট করা)
            prompt = f"আজকের তারিখ: ২৮ ফেব্রুয়ারি ২০২৬। Context: {context}\nQuestion: {query}\nAnswer in Bengali with proper formatting."
            response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
            
            st.markdown("### 🤖 এআই উত্তর:")
            st.write(response.text)
            
            st.markdown("---")
            st.markdown("#### 🔗 তথ্যসূত্র:")
            for s in sources:
                st.markdown(f"- [{s['title']}]({s['url']})")
                
        except Exception as e:
            st.error(f"দুঃখিত, কোনো সমস্যা হয়েছে: {e}")

# সাইডবার ইনফরমেশন
st.sidebar.markdown("### বিজ্ঞাপনের জন্য যোগাযোগ")
st.sidebar.write("Owner: Chiranjit Majumdar")
st.sidebar.write("Phone: 8910097747")
