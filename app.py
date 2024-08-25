import streamlit as st
from streamlit_option_menu import option_menu
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from openai import OpenAI
import gensim.utils

### --- TITLE BAR --- ###
st.title('Data Scientist - Job Taster')
st.write('M. Farhan Rais | The Astronauts Collective')
# Input Field for URL
url = st.text_input("Paste the news article URL here:")
# Submit Button
# Declare a global string variable to store the article text
article_text = ""

if st.button('Submit'):
    if url:
        try:
            # Fetch the Webpage Content
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP errors

            # Parse the HTML
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract the Article Text (You might need to adjust this based on the website structure)
            article_text = soup.find('article').get_text(strip=True)
            st.success("Article text extracted successfully!")
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching the webpage: {e}")
    else:
        st.warning("Please enter a URL first.")

### --- TOP NAVIGATION BAR --- ###
selected = option_menu(
    menu_title = None,
    options = ['1. Analyse HTML', '2. Removing Stop Words','3. Prompt Engineering'],
    icons = ['body-text','sign-stop','chat-dots'],
    default_index = 0, # which tab it should open when page is first loaded
    orientation = 'horizontal',
    styles={
        'nav-link-selected': {'background-color': '#ff0e16'}
        }
    )

### --- 1st SECTION --- ###
if selected == '1. Analyse HTML':
    st.header('1. Analyse HTML', divider="red")
    # Display Results in Tabs
    tab1, tab2, tab3 = st.tabs(["HTML Source Code", "Article Text", "Word Cloud"])

    try:
        with tab1:
            st.code(response.text, language='html')

        with tab2:
            st.write(article_text)

        with tab3:
            if url and 'article_text' in locals():  # Check if article_text exists
                # 1. Get the article_text
                text_to_analyze = article_text

                # 2. Remove stop words and punctuation
                #word_tokens = word_tokenize(text_to_analyze)
                #filtered_text = word_tokens

                # Tokenize using gensim instead of nltk
                filtered_text = gensim.utils.simple_preprocess(text_to_analyze)

                # 3. Create word cloud
                wordcloud = WordCloud(width=800, height=400).generate(' '.join(filtered_text))

                # 1. Display the word cloud
                fig, ax = plt.subplots()
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
    except NameError:
        st.warning("Please extract the article text first.")


### --- 2nd SECTION --- ###
if selected == '2. Removing Stop Words':
    st.header('2. Removing Stop Words', divider="red")
    st.write("Stop words from: https://gist.github.com/sebleier/554280")
    # Display Results in Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Original Article", "Stop Words Highlighted", "Stop Words Removed", "Word Cloud"])

    try:
        with tab1:
            st.write(article_text)
        
        with tab2:
            stop_words = nltk.corpus.stopwords.words('english')
            highlighted_text = ""
            for word in word_tokenize(article_text):
                if word.lower() in stop_words:
                    highlighted_text += f"<mark style='background-color:yellow'>{word}</mark> "
                else:
                    highlighted_text += word + " "
            st.markdown(highlighted_text, unsafe_allow_html=True)

        with tab3:
            text_to_analyze = article_text
            #word_tokens = word_tokenize(text_to_analyze)
            filtered_text = gensim.utils.simple_preprocess(text_to_analyze)
            filtered_text = [word for word in word_tokens if word.lower() not in stop_words]
            
            st.write(' '.join(filtered_text))

        with tab4:
            if url and 'article_text' in locals():  # Check if article_text exists
                # 1. Get the article_text
                text_to_analyze = article_text

                # 2. Remove stop words and punctuation
                stop_words = set(stopwords.words('english'))
                word_tokens = word_tokenize(text_to_analyze)
                filtered_text = [word for word in word_tokens if word.lower() not in stop_words and word not in string.punctuation]

                # 3. Create word cloud
                wordcloud = WordCloud(width=800, height=400).generate(' '.join(filtered_text))

                # 1. Display the word cloud
                fig, ax = plt.subplots()
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
    except NameError:
        st.warning("Please extract the article text first.")

### --- 3rd SECTION --- ###
if selected == '3. Prompt Engineering':
    st.header('3. Prompt Engineering', divider="red")
    st.write("GovTech's CO-STAR: https://www.developer.tech.gov.sg/products/collections/data-science-and-artificial-intelligence/playbooks/prompt-engineering-playbook-beta-v3.pdf")

    # Input fields for prompt generation
    context = st.text_input("Context:", value="I am a student learning about data science.")
    objective = st.text_input("Objective:", value="Input question here.")
    style = st.selectbox("Style:", ["Political Analyst", "Economics Consultant", "Social Worker", "Teacher", "Singaporen Uncle"])
    tone = st.selectbox("Tone:", ["Formal", "Casual", "Humorous", "Empathetic", "Autoritative", "Inspirational", "Nonchalant"])
    audience = st.text_input("Audience:", value="Student")
    response_format = st.text_input("Desired Response Format:", value="A brief answer to the question in the Objective.")

    # 2. Set your OpenAI API key
    client = OpenAI(
        api_key=st.secrets["my_api_key"]
    )

    # 4. Submit Button
    if st.button('Ask ChatGPT'):
        if url and 'article_text' in locals():
                    # Construct the prompt
                    message = f"""
                    # CONTEXT #
                    {context}

                    # OBJECTIVE #
                    Answer the following question based on the provided text. 
                    If the answer cannot be found in the text, say "I don't have enough information to answer that."
                    Question: {objective}

                    # STYLE #
                    {style}

                    # TONE #
                    {tone}

                    # AUDIENCE #
                    {audience}

                    # RESPONSE #
                    {response_format}

                    # TEXT #
                    {article_text}
                    """

                    # Call ChatGPT API
                    response = client.completions.create(
                        model="gpt-4o-mini",  # or any suitable model
                        prompt=message,
                        max_tokens=200,  # Adjust as needed
                        temperature=0.7,  # Adjust for creativity vs. determinism
                    )

                    # Display ChatGPT's response
                    st.write(response.choices[0].text.strip())