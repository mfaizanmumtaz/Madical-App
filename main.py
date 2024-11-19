import streamlit as st
from app import get_medical_chain

# Set page config
st.set_page_config(
    page_title="Treatment to Diagnosis Matching Using AI for Claim Acceptance",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Treatment to Diagnosis Matching Using AI for Claim Acceptance")

# Create the main input area
user_input = st.text_area(
    "Please enter the claim details:",
    height=150,
    placeholder="Example:"
)

claim_id = st.text_input("Please enter the claim ID:")

# Add a submit button
if st.button("Submit", type="primary"):
    if user_input and claim_id:
        with st.spinner("Getting data related to claim details..."):
            try:
                # Get results from the medical chain
                results = get_medical_chain(user_input,claim_id)
                
                # Display results
                st.write("### Retrieved Medical Context")
                if not results:
                    st.write("No records found related to the claim details.")
                else:
                    for doc in results:
                        with st.expander(f"Medical Record {results.index(doc) + 1}"):
                            st.write(   doc.page_content)
                            if hasattr(doc, 'metadata') and doc.metadata:
                                st.write("**Metadata:**")
                                for key, value in list(doc.metadata.items())[-2:]:
                                    if key == "Status":
                                        st.write(f"- Predicted {key}: {value}")
                                    else:
                                        st.write(f"- {key.title()}: {value}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter claim details.")
