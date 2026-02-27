import streamlit as st
from google import genai
from tavily import TavilyClient

# ১. প্রফেশনাল লুকের জন্য CSS (লোগো হাইড করা)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stAppDeployButton {display:none;}
            </style>
            """

try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
except Exception:
    st.error("API Key missing! Please check Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=GOOGLE_API_KEY)
tavily = TavilyClient(api_key=TAVILY_API_KEY)

st.set_page_config(page_title="AutoKaaj Lead Agent", page_icon="💼")
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("🎯 AutoKaaj High-Ticket Lead Finder")
st.subheader("n8n, AI Agent ও ওয়েবসাইট প্রজেক্টের লিড খুঁজুন")

# ইনপুট অপশন
platform = st.selectbox("কোন প্ল্যাটফর্ম থেকে লিড খুঁজবেন?", ["Upwork", "Fiverr", "LinkedIn", "Google Jobs"])
category = st.text_input("কী ধরণের প্রজেক্ট খুঁজছেন?", placeholder="উদা: n8n automation, AI chatbot, Real estate website")

if st.button("ফাইন্ড লিডস (Find Leads)"):
    if category:
        with st.spinner(f"{platform} থেকে আপনার জন্য কাজ খোঁজা হচ্ছে..."):
            # বিশেষ সার্চ কুয়েরি যা নির্দিষ্ট প্ল্যাটফর্মকে টার্গেট করবে
            lead_query = f"site:{platform.lower()}.com jobs {category} contact info or business names recently posted"
            
            search_response = tavily.search(query=lead_query, search_depth="advanced", max_results=10)
            
            context_leads = ""
            for r in search_response['results']:
                context_leads += f"Title: {r['title']}\nSnippet: {r['content']}\nURL: {r['url']}\n\n"

            # এআই প্রম্পট - কাস্টমারের নাম ও নম্বর খুঁজে বের করার জন্য
            prompt_leads = f"""
            You are a professional Lead Generation Expert for an Automation Specialist.
            Based on this context: {context_leads}
            Identify 5 potential clients from {platform} who need {category}.
            Extract the following for each:
            1. Client/Business Name
            2. Project/Job Description
            3. Contact Link/Source URL
            4. Estimated project value (if mentioned)
            Note: If phone numbers aren't publicly visible on {platform}, provide their website or profile link for outreach.
            Language: Bengali.
            """
            
            response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt_leads)
            
            st.markdown(f"### 🚀 {platform} থেকে প্রাপ্ত সম্ভাব্য লিডসমূহ:")
            st.write(response.text)
            
            st.info("টিপস: ফ্রিল্যান্স সাইটে সরাসরি ফোন নম্বর পাওয়া কঠিন হতে পারে, তাই সোর্স লিঙ্কে গিয়ে সরাসরি বিড (Bid) করুন বা মেসেজ দিন।")
    else:
        st.warning("দয়া করে কাজের ক্যাটাগরি লিখুন।")

# সাইডবার
st.sidebar.title("AutoKaaj Automation")
st.sidebar.write("Developed by: Chiranjit Majumdar")
st.sidebar.write("Specialist: n8n & AI Agents")
st.sidebar.write("Phone: 8910097747")
