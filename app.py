import streamlit as st
from google import genai
from tavily import TavilyClient

# ১. ওপরের মেনু ও লোগো হাইড করার CSS
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stAppDeployButton {display:none;}
            </style>
            """

try:
    # সিক্রেটস থেকে এপিআই কি সংগ্রহ
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
except Exception:
    st.error("API Key missing in Streamlit Secrets!")
    st.stop()

# ২. ক্লায়েন্ট সেটআপ
client = genai.Client(api_key=GOOGLE_API_KEY)
tavily = TavilyClient(api_key=TAVILY_API_KEY)

st.set_page_config(page_title="AutoKaaj AI Agent 2.5", page_icon="🚀")
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("🎯 AutoKaaj AI Lead Finder 2.5")
st.caption("Powered by Gemini 2.5 Flash | Developed by Chiranjit Majumdar")

# ৩. ইনপুট সেকশন
platform = st.selectbox("কোন প্ল্যাটফর্ম থেকে লিড খুঁজবেন?", ["Upwork", "Fiverr", "LinkedIn", "Google"])
category = st.text_input("কী ধরণের প্রজেক্ট খুঁজছেন?", placeholder="উদা: n8n automation, AI chatbot expert")

if st.button("ফাইন্ড লিডস (Find Leads)"):
    if category:
        with st.spinner(f"Gemini 2.5 Flash দিয়ে {platform} থেকে লিড এনালাইসিস করা হচ্ছে..."):
            try:
                # Tavily দিয়ে লাইভ সার্চ
                lead_query = f"site:{platform.lower()}.com jobs {category} contact info or project details recently posted"
                search_response = tavily.search(query=lead_query, search_depth="advanced", max_results=8)
                
                context_leads = ""
                for r in search_response['results']:
                    context_leads += f"Title: {r['title']}\nSnippet: {r['content']}\nURL: {r['url']}\n\n"

                # এআই প্রম্পট - এখানে মডেলের নাম gemini-2.5-flash দেওয়া হয়েছে
                prompt_leads = f"""
                You are a Senior Lead Generation Agent. Analyze these results: {context_leads}
                Find the best 5 high-ticket projects on {platform} for an n8n and AI Agent specialist.
                Provide for each:
                - Business/Client Name
                - Project Summary
                - Direct Link to Outreach
                - Why this is a good fit for n8n automation.
                Language: Bengali.
                """
                
                # Gemini 2.5 Flash কল
                response = client.models.generate_content(
                    model="gemini-2.5-flash", 
                    contents=prompt_leads
                )
                
                st.markdown(f"### 🚀 {platform} থেকে প্রাপ্ত সম্ভাব্য লিডসমূহ:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"মডেল কল করার সময় সমস্যা হয়েছে: {str(e)}")
                st.info("টিপস: যদি মডেল পাওয়া না যায়, তবে নিশ্চিত করুন আপনার গুগল এআই স্টুডিওতে ২.৫ ভার্সনটি এনাবেল আছে কি না।")
    else:
        st.warning("দয়া করে কাজের ক্যাটাগরি লিখুন।")

# সাইডবার
st.sidebar.title("AutoKaaj Automation")
st.sidebar.write("Specialist: n8n & AI Agents")
st.sidebar.write("Owner: Chiranjit Majumdar")
st.sidebar.write("Phone: 8910097747")
