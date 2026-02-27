import streamlit as st
from google import genai
from tavily import TavilyClient

# এটি সুরক্ষার জন্য স্ট্রিমলিট সিক্রেটস থেকে কি (Key) নেবে
try:
    # গিটহাবে কোডটি পাবলিক থাকলেও এই কি-গুলো কেউ দেখতে পাবে না
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
except Exception:
    st.error("API Key গুলো Streamlit Secrets-এ পাওয়া যায়নি।")
    st.stop()

client = genai.Client(api_key=GOOGLE_API_KEY)
tavily = TavilyClient(api_key=TAVILY_API_KEY)

st.set_page_config(page_title="AutoKaaj AI Search", page_icon="🔍")
st.title("🚀 AutoKaaj AI Search Engine")
st.caption("কলকাতার লেটেস্ট তথ্য এবং স্মার্ট এআই উত্তর। Developed by Chiranjit Majumdar.")

query = st.text_input("আপনি কী জানতে চান?", placeholder="উদা: আজকে কলকাতায় সোনার দাম কত?")

if query:
    with st.spinner("ইন্টারনেট থেকে লাইভ তথ্য খোঁজা হচ্ছে..."):
        try:
            search_response = tavily.search(query=query, search_depth="advanced", max_results=5)
            context = ""
            sources = []
            for r in search_response['results']:
                context += f"Source: {r['url']}\nContent: {r['content']}\n\n"
                sources.append(r)

            prompt = f"Context: {context}\nQuestion: {query}\nAnswer in Bengali with formatting."
            response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            
            st.markdown("### 🤖 এআই উত্তর:")
            st.write(response.text)
            
            st.markdown("---")
            st.markdown("#### 🔗 তথ্যসূত্র:")
            for s in sources:
                st.markdown(f"- [{s['title']}]({s['url']})")
                
        except Exception as e:
            st.error(f"দুঃখিত, কোনো সমস্যা হয়েছে: {e}")

st.sidebar.markdown("### বিজ্ঞাপনের জন্য যোগাযোগ করুন")
st.sidebar.write("Owner: Chiranjit Majumdar")
st.sidebar.write("Phone: 8910097747")
