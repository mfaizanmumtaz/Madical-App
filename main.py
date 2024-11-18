import streamlit as st
from app import get_medical_chain

# Set page config
st.set_page_config(
    page_title="Medical RAG App",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Medical RAG Assistant")

# Create the main input area
st.write("### Enter Patient Symptoms")
user_input = st.text_area(
    "Please enter the symptoms:",
    height=150,
    placeholder="Example:"
)

# Add a submit button
if st.button("Get Corresponding Data Related to Symptoms", type="primary"):
    if user_input:
        with st.spinner("Getting data related to symptoms..."):
            try:
                # Get results from the medical chain
                results = get_medical_chain(user_input)
                
                # Display results
                st.write("### Retrieved Medical Context")
                if not results:
                    st.write("No records found related to the symptoms.")
                else:
                    for doc in results:
                        with st.expander(f"Medical Record {results.index(doc) + 1}"):
                            st.write(   doc.page_content)
                            if hasattr(doc, 'metadata') and doc.metadata:
                                st.write("**Metadata:**")
                                for key, value in doc.metadata.items():
                                    st.write(f"- {key}: {value}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter symptom.")
