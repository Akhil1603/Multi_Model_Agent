import streamlit as st
from agno.agent import Agent
from agno.models.google import Gemini
import tempfile
import os

def apply_custom_css():
    st.markdown("""
        <style>
            .main {
                background-color: #f9fafe;
                padding: 2rem;
                border-radius: 1rem;
            }
            .title {
                font-size: 2.5rem;
                font-weight: bold;
                color: #3366cc;
            }
            .section {
                font-size: 1.1rem;
                color: #444;
                margin-bottom: 1rem;
            }
            .emoji {
                font-size: 2rem;
                margin-right: 0.3rem;
            }
        </style>
    """, unsafe_allow_html=True)

def main():
    apply_custom_css()
    st.markdown('<div class="title">🧠 Multimodal Reasoning AI Agent</div>', unsafe_allow_html=True)
    st.markdown("Upload an image 📷, type your mysterious question 🕵️‍♂️, and let the AI blow your mind 🤯.")
    
    # Initialize AI Agent
    agent = Agent(
        model=Gemini(id="gemini-2.0-flash-thinking-exp-1219"), 
        markdown=True
    )
    
    # For debugging
    st.sidebar.markdown("### Debugging Info")
    debug_expander = st.sidebar.expander("Show agent response structure")
    
    # Upload image
    uploaded_file = st.file_uploader("📸 Upload your image here", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                temp_path = tmp_file.name
            
            st.image(uploaded_file, caption="Nice upload! 👏", use_container_width=True)
            task_input = st.text_area("🤔 Ask something about this image:", placeholder="e.g., What's happening in this photo?")
            
            if st.button("🚀 Analyze with AI"):
                if not task_input.strip():
                    st.warning("Oops! 🤭 You forgot to ask something.")
                else:
                    with st.spinner("Hold tight, my circuits are buzzing... ⚡"):
                        try:
                            # Agent call
                            result = agent.run(task_input, images=[temp_path])
                            
                            # Debug information
                            with debug_expander:
                                st.write("Result type:", type(result))
                                st.write("Result structure:", result)
                            
                            # Don't assume any structure, just show what you got
                            st.markdown("### 🤖 AI Says:")
                            
                            # Handle different result types
                            if isinstance(result, dict) and result.get('text'):
                                st.markdown(result['text'])
                            elif isinstance(result, dict):
                                st.json(result)  # Display as formatted JSON if it's a dict
                            else:
                                st.markdown(str(result))  # Fallback to string representation
                        except Exception as e:
                            st.error(f"🚨 Oops! Something went wrong: {str(e)}")
                        finally:
                            if os.path.exists(temp_path):
                                os.remove(temp_path)
        except Exception as e:
            st.error(f"😵 Image processing failed: {str(e)}")
    else:
        st.info("I'm waiting... patiently... like a ninja 🥷.\n\nUpload something cool!")

if __name__ == "__main__":
    main()