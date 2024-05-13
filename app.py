import streamlit as st
import os
from VideoTextClass import Videotext, LinkVideoTimelyText
from GptSummary import Gptresponse
from PromptMessage import system_msg
from extract_information import extract_information
import pytube




# Side Bar Title
st.sidebar.title("Mini Project")

st.sidebar.markdown("<hr>", unsafe_allow_html=True)

# Main Title
st.title("Custom Video and YouTube Video Summarizer")

st.markdown("<hr>", unsafe_allow_html=True)

# Save uploaded file locally.
def save_uploaded_file(uploadedfile):
    with open(os.path.join("uploads", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return

# Process Uploaded video
def process_uploaded_video(video_path):
    vidText = LinkVideoTimelyText(video_path)
    transcript = vidText.getText()
    return transcript


def get_final_summary(system_msg, transcript):
    # Creating object of class for generating summary using gpt.
    gptSumm = Gptresponse(system_msg, transcript)
    final_summary = gptSumm.getSummary()
    return final_summary


# Process Youtube link
def process_youtube_link(url):
    youtube=pytube.YouTube(url)
    stream=youtube.streams.get_audio_only()
    stream.download(output_path=r'youtube_path', filename='youtube_video.mp4') # store in the localhost
    path = r'youtube_path/youtube_video.mp4'
    vidText = LinkVideoTimelyText(path)
    transcript = vidText.getText()
    return transcript


# create function to download the transcript
def download_transcript(trascript):
    text_file = open(r'transcript_path/transcript.doc', 'w')
    trascript = trascript
    text_file.write(trascript)
    text_file.close()
    return


def main():
    st.sidebar.title("Please select below application to use")
    selected_option = st.sidebar.radio("Choose an app", ("Upload Your video", "Paste your YouTube link"))
    
    
    # Add space below radio button options
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    
     # Description for each radio button
    if selected_option == "Upload Your video":
        st.sidebar.markdown("## How to Use?")
        st.sidebar.write("1. Upload a MP4, MOV or MPEG4 file.")
        st.sidebar.write("2. Click on the 'Upload video' button.")
        st.sidebar.write("3. You will get the Topic, Sentiment and Conclusion for uploaded video.")
       
    elif selected_option == "Paste your YouTube link":
        st.sidebar.markdown("## How to Use?")
        st.sidebar.write("1. 'Paste your YouTube link' in the provided text input.")
        st.sidebar.write("2. Click 'Submit' to process the YouTube link.")
        st.sidebar.write("3. You will get the Topic, Sentiment, Conclusion for and summary with time frame for given YT video link.")

    # Add space below radio button options
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    st.sidebar.markdown("## Project Member")
    st.sidebar.write("1. Member-1")
    st.sidebar.write("2. Member-2")
    st.sidebar.write("3. Member-3")
    st.sidebar.write("4. Member-4")
    
    
    # Video Upload
    if selected_option == "Upload Your video":
        st.title("Upload Your Video")
        uploaded_video = st.file_uploader("Upload video", type=["mp4", "mov"])
        
        col_upvd_1, col_upvd_2 = st.columns([2, 1])
        upd_vid_final_summary = None
        
        with col_upvd_1:
            if uploaded_video is not None:
                if st.button("Upload video"):
                    st.success('Your file successfully Submitted.', icon="✅")
                    with st.spinner('Please wait.. Your Video is processing!'):
                        save_uploaded_file(uploaded_video)
                        uploaded_video_path = r"uploads/{}".format(uploaded_video.name)
                        upd_vid_transcript = process_uploaded_video(uploaded_video_path)
                        upd_vid_final_summary = get_final_summary(system_msg, upd_vid_transcript)
                        topic, sentiment, conclusion, summary = extract_information(upd_vid_final_summary)
                            
                        st.write('Topic :',topic)
                        st.write('Sentiment :',sentiment)
                        st.write('Conclusion :',conclusion)
                        st.write('Summary :',summary)
                        # Here you can implement the functionality for processing the uploaded video
                    st.success('Thanks for using  our service!')
                    
        

        with col_upvd_2: # (Write the summary into file)
            if upd_vid_final_summary is not None:
                doc_path = r"transcript_path/transcript.doc"
                with open(doc_path, "wb") as file:
                    doc = upd_vid_transcript
                    st.download_button(label="Download Video Transcript", data=doc, file_name="transcript.doc")

    #youtube
    elif selected_option == "Paste your YouTube link":
        st.title("Paste Your YouTube Link")
        youtube_link = st.text_input("Paste your YouTube link here:")
        
        # Create two columns
        col_yt_1, col_yt_2 = st.columns([2, 1])
        yt_final_summary = None
        with col_yt_1:
            if st.button("Submit"):
                with st.spinner('Please wait.. Your link is processing!'):
                    yt_transcript = process_youtube_link(youtube_link)
                    download_transcript(yt_transcript) # it will store timeluy text into file 
                    yt_final_summary = get_final_summary(system_msg, yt_transcript)
                    # download_transcript(yt_final_summary) # it will store final summary
                    topic, sentiment, conclusion, summary = extract_information(yt_final_summary)
                    
                    st.write('Topic :',topic)
                    st.write('Sentiment :',sentiment)
                    st.write('Conclusion :',conclusion)
                    st.write('Summary :',summary)
                    st.write('')
                st.success('Thanks for using our service!')
                
        # Download button
        with col_yt_2:
            if yt_final_summary is not None:
                doc_path = r"transcript_path/transcript.doc"
                with open(doc_path, "rb") as file:
                    doc = file.read()
                    st.download_button(label="Download Video Transcript", data=doc, file_name="transcript.doc")
            
    
    
    

if __name__ == "__main__":
    main()