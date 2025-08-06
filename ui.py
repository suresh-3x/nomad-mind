import streamlit as st
from ingest import download_and_transcribe
from vectorstore import store_transcript
from llm import generate_itinerary, query_llm

st.set_page_config(page_title="NomadMind", layout="centered")
st.title("🧭 NomadMind: Your AI Travel Agent")

st.markdown("### 🎥 Ingest a Travel Vlog")
youtube_url = st.text_input("Paste YouTube video link")

if st.button("Ingest Video"):
    if youtube_url:
        with st.spinner("Downloading and transcribing..."):
            try:
                vid_id, transcript = download_and_transcribe(youtube_url)
                store_transcript(vid_id, transcript)
                st.success(f"Ingested video: {vid_id}")
            except Exception as e:
                st.error(f"Failed: {e}")
    else:
        st.warning("Please paste a valid YouTube link.")

st.markdown("---")
st.markdown("### 💬 Ask a Question About the Video(s)")

question = st.text_input("Ask anything...")

if st.button("Ask AI"):
    if question.strip() != "":
        with st.spinner("Thinking..."):
            try:
                answer = query_llm(question)
                st.markdown("#### 🧠 Answer")
                st.write(answer)
            except Exception as e:
                st.error(f"Failed to get answer: {e}")
    else:
        st.warning("Type a question first.")

@st.cache_data
def get_ingested_videos():
    try:
        with open("memory/video_index.txt", "r") as f:
            lines = f.readlines()
        return [line.strip().split("|") for line in lines]
    except FileNotFoundError:
        return []

with st.sidebar:
    st.markdown("## 🎞️ Ingested Videos")
    videos = get_ingested_videos()
    selected_vids = st.multiselect("Select video(s) to query", [v[0] for v in videos], format_func=lambda x: next(v[1] for v in videos if v[0] == x))
    
import folium
from streamlit_folium import st_folium
from vectorstore import extract_locations

# if "show_map" not in st.session_state:
#     st.session_state["show_map"] = False

# # Button logic
# if st.button("🗺️ Show Location Map"):
#     st.session_state["show_map"] = True

# if st.session_state["show_map"]:
#     if selected_vids:
#         all_text = ""
#         for vid in selected_vids:
#             with open(f"memory/{vid}.txt") as f:
#                 all_text += f.read()
#         locs = extract_locations(all_text)
#         m = folium.Map(location=[20, 0], zoom_start=2)
#         for name, (lat, lon) in locs.items():
#             folium.Marker([lat, lon], popup=name).add_to(m)
#         st_folium(m, width=700)
#     else:
#         st.warning("Select at least one video to map.")

# if st.button("🔄 Reset Map"):
#     st.session_state["show_map"] = False
    

if st.button("🧾 Generate 3-Day Itinerary"):
    if selected_vids:
        itinerary = generate_itinerary(selected_vids)
        st.markdown("### ✈️ Suggested Itinerary")
        st.text(itinerary)
    else:
        st.warning("Please select video(s) first.")
