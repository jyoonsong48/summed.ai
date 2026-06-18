from Bio import Entrez
import streamlit as st
from groq import Groq
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from datetime import datetime

Entrez.email = st.secrets["NCBI_EMAIL"]
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
custom_stopwords = STOPWORDS.update({
    "expression", "analysis", "role", "study", "protective", "disease", "RNA", "horizontal", "subtilis", "syndrome", "sequencing", "prostate", "lung", "injury", "receptor",
    "function", "level", "using", "based", "combinations", "cell", "cells", "single", "whole", "medicine", "positive", "transfer", "cancer", "disorder", "acid", "small", "therapy", "targeted",
})
chormosome_mask = np.array(Image.open("chromosome_for_masking.png"))
logo = Image.open("summed.png")
today = datetime.today().strftime("%Y-%m-%d")

st.set_page_config(
    page_title = "SUMMED.ai",
    page_icon = logo,
    initial_sidebar_state= None,
    menu_items={
        "Report a bug" : "https://mail.google.com/mail/?view=cm&to=jyoon.song48@gmail.com&su=%5BBug%20Report%5D&body=%5BPlease%20describe%20a%20bug%20or%20copy%26paste%20error%20message%20here.%5D",
        "About" : """
        A super cool tool to summarise papers and see research trends! 
        ( •̀ ω •́ )✧ 
        Further Info here: https://github.com/jyoonsong48/summed.ai/blob/main/README.md
        """}
)

st.title("🔬 PubMed Trend Charts & Summrisation Tool")
st.write("Search or Set publication year range")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bitcount+Prop+Single:wght@100..900&family=Playfair+Display:ital,wght@0,400..900;1,400..900&family=Tektur:wght@400..900&display=swap');
            
* {
  font-family: "Tektur", sans-serif;
  font-optical-sizing: auto;
  font-weight: <weight>;
  font-style: normal;
  font-variation-settings:
    "wdth" 100;
}

input::placeholder {
  font-family: "Tektur", sans-serif !important;
  font-weight: 400;
}
</style>
""", unsafe_allow_html=True)



with st.form("search"):
    col1, col2 = st.columns(2)
    
    with col1:
        search_user = st.text_input("Search", placeholder="e.g. IRX1, Parkinson's, forensic ... etc.")
        number_user   = st.text_input("Number of Papers",   placeholder="e.g. 67")

    with col2:
        st.markdown("""
        <style>

        div[data-testid="stSlider"] [data-baseweb="slider"] > div > div:first-child > div {
            background-color: #97BFB4 !important;
        }

        div[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
            background-color: #97BFB4 !important;
            border-color: #97BFB4 !important;
            box-shadow: none !important;
        }

        div[data-testid="stSliderThumbValue"] {
            color: #97BFB4 !important;
        }
        </style>
        """, unsafe_allow_html=True)

        year_range = st.slider(
            "Select Publication Year Range",
            min_value=2000,
            max_value=2026,
            value=(2020, 2026)
        )
    
    submitted = st.form_submit_button("🔍")

if not submitted:
    st.subheader("How to Use")
    with st.expander("1. Input Options"):
        st.write("""
                You can combine any of the fields above to customise your analysis (if you don't enter anything, year range will be automatically used to analyse.)
                - Topic/Keyword: Search by specific genes, diseases, or even broad topics.
                - Number of Papers: Maximum number of articles to analyse. (Default: 5)
                - Year Range: Select a specific publication period. (Default: 2020-2026)
                """)
    with st.expander("2. Results"):
        st.write("""       
                - Summary Table: Displayed when a Topic/Keyword is specified. With core targets, evidence levels, key findings, etc.
                - Word Cloud: Displayed when NO Topic/Keyword is specified. Extract & visualising of keywords from the latetest papers.
                """)

if submitted:
    has_topic = bool(search_user.strip())
    has_count = bool(number_user.strip())
    has_pdat = year_range != (2000, 2026)
    if not (has_topic or has_count or has_pdat):
        st.warning("Please fill in at least one field to search!")
    else:
        with st.spinner("Collecting papers from PubMed ..."):
                for_prompt = ""
                show_chart = False
                # topic & count & pdat
                if has_topic and has_count and has_pdat:
                    start_year, end_year = year_range
                    handle = Entrez.esearch(db="pubmed", term=f"{search_user}[Title]", mindate = start_year, maxdate = end_year, datetype="pdat", retmax=int(number_user))
                    record = Entrez.read(handle)

                    id_list = record["IdList"]

                    handle = Entrez.efetch(db="pubmed", id=id_list, rettype="abstract", retmode="xml")
                    records = Entrez.read(handle)
                    handle.close()
                        
                    titles = []
                    abs = []
                    for record in records["PubmedArticle"]:
                        citation = record["MedlineCitation"]
                        article = citation["Article"]
                        title = article["ArticleTitle"]
                        titles.append(title)
                        if "Abstract" in article:
                            abstract_text_list = article["Abstract"]["AbstractText"]
                            abstract = " ".join(abstract_text_list)
                            abs.append(abstract)
                        else:
                            abs.append("N/A")

                    text_data = dict(zip(titles, abs))
                    for title, abstract in text_data.items():
                        for_prompt += f"Title: {title}\nAbstract: {abstract}\n\n"
                
                elif has_topic and has_count:
                    start_year, end_year = 2000, 2026
                    handle = Entrez.esearch(db="pubmed", term=f"{search_user}[Title]", mindate = start_year, maxdate = end_year, datetype="pdat", retmax=int(number_user))
                    record = Entrez.read(handle)

                    id_list = record["IdList"]

                    handle = Entrez.efetch(db="pubmed", id=id_list, rettype="abstract", retmode="xml")
                    records = Entrez.read(handle)
                    handle.close()
                        
                    titles = []
                    abs = []
                    for record in records["PubmedArticle"]:
                        citation = record["MedlineCitation"]
                        article = citation["Article"]
                        title = article["ArticleTitle"]
                        titles.append(title)
                        if "Abstract" in article:
                            abstract_text_list = article["Abstract"]["AbstractText"]
                            abstract = " ".join(abstract_text_list)
                            abs.append(abstract)
                        else:
                            abs.append("N/A")

                    text_data = dict(zip(titles, abs))
                    for title, abstract in text_data.items():
                        for_prompt += f"Title: {title}\nAbstract: {abstract}\n\n"

                elif has_topic and has_pdat:
                    start_year, end_year = year_range
                    handle = Entrez.esearch(db="pubmed", term=f"{search_user}[Title]", mindate = start_year, maxdate = end_year, datetype="pdat", retmax=5)
                    record = Entrez.read(handle)

                    id_list = record["IdList"]

                    handle = Entrez.efetch(db="pubmed", id=id_list, rettype="abstract", retmode="xml")
                    records = Entrez.read(handle)
                    handle.close()
                        
                    titles = []
                    abs = []
                    for record in records["PubmedArticle"]:
                        citation = record["MedlineCitation"]
                        article = citation["Article"]
                        title = article["ArticleTitle"]
                        titles.append(title)
                        if "Abstract" in article:
                            abstract_text_list = article["Abstract"]["AbstractText"]
                            abstract = " ".join(abstract_text_list)
                            abs.append(abstract)
                        else:
                            abs.append("N/A")

                    text_data = dict(zip(titles, abs))
                    for title, abstract in text_data.items():
                        for_prompt += f"Title: {title}\nAbstract: {abstract}\n\n"
                    
                else:
                    show_chart = True
                    if has_count and has_pdat:
                        start_year, end_year = year_range
                        handle = Entrez.esearch(db="pubmed", term="genetics OR genomics", mindate = start_year, maxdate = end_year, datetype="pdat", retmax=int(number_user))
                        record = Entrez.read(handle)

                        id_list = record["IdList"]

                    elif has_count:
                        start_year, end_year = 2000, 2026
                        handle = Entrez.esearch(db="pubmed", term="genetics OR genomics", mindate = start_year, maxdate = end_year, datetype="pdat", retmax=int(number_user))
                        record = Entrez.read(handle)

                        id_list = record["IdList"]


                    elif has_pdat:
                        start_year, end_year = year_range
                        handle = Entrez.esearch(db="pubmed", term="genetics OR genomics", mindate = start_year, maxdate = end_year, datetype="pdat", retmax=20)
                        record = Entrez.read(handle)

                        id_list = record["IdList"]

                    if not id_list:
                        st.warning("No papers found for the selected genomic criteria. Try adjusting the year range!")
                    else:
                        handle = Entrez.efetch(db="pubmed", id=id_list, rettype="abstract", retmode="xml")
                        records = Entrez.read(handle)
                        handle.close()
                            
                        abs = []
                        for record in records["PubmedArticle"]:
                            citation = record["MedlineCitation"]
                            article = citation["Article"]
                            if "Abstract" in article:
                                abstract_text_list = article["Abstract"]["AbstractText"]
                                abstract = " ".join(abstract_text_list)
                                abs.append(abstract)
                            else:
                                abs.append("N/A")

                        for_cloud = "".join(abs)
                        for_reading = client.chat.completions.create(
                            model="meta-llama/llama-4-scout-17b-16e-instruct",
                            temperature= 0.1,
                            messages=[
                                {"role": "system", "content": """You are an expert biomedical text miner and bioinformatician. Your task is to extract highly relevant biological, clinical, and methodological keywords from the provided abstracts for a genomic trend analysis.
                                [Target Entities to Extract]
                                - Specific Genes, Proteins, and Biomarkers
                                - Specific Diseases, Disorders, and Phenotypes
                                - Biological Pathways and Molecular Mechanisms
                                - Advanced Lab Methodologies and Technologies
                                 
                                [EXTRACTION PRIORITY - RANKED]
                                1. HIGHEST: Specific named entities (e.g., BRCA1, mTOR, Alzheimer's disease, CRISPR-Cas9)
                                2. HIGH: Specific pathways with full names (e.g., PI3K/AKT/mTOR signaling)
                                3. MEDIUM: Specific methodologies (e.g., single-cell RNA sequencing, GWAS)
                                4. LOW: Phenotypes only if clinically specific (e.g., HER2-positive breast cancer)
                                5. EXCLUDE: Anything that could appear in 3+ different biological fields without disambiguation

                                [STRICT FILTERING RULES - DO NOT EXTRACT]
                                - General academic verbs/nouns/adjectives: study, effect, role, using, associated, 
                                relationship, analysis, mechanism, expression, function, level, novel, significant,
                                please, ready, keywords, provides, approach, method, findings, evidence, context,
                                potential, important, various, multiple, based, common, known, shows, suggests
                                
                                - Statistical or descriptive data: patient, group, data, result, p-value, increase,
                                decrease, correlated, higher, lower, sample, cohort, control, model, rate, range,
                                number, mean, median, value, score
                                
                                - Overly broad biological terms: gene, protein, cell, tissue, disease, human, mouse,
                                pathway, process, response, activity, regulation, interaction, system, signal,
                                factor, type, subtype
                                 
                                [SELF-VALIDATION BEFORE OUTPUT]
                                - Would this keyword appear in a general biology textbook index? → EXCLUDE
                                - Is this keyword specific enough to search in PubMed and get relevant results? → INCLUDE
                                - Does this keyword have a database entry (OMIM, KEGG, UniProt)? → INCLUDE
                                 
                                [EXAMPLES]
                                Abstract snippet: "...VEGF-mediated angiogenesis in glioblastoma was inhibited by bevacizumab..."
                                BAD output: gene expression, cancer, treatment, inhibition, signaling
                                GOOD output: VEGF, angiogenesis, glioblastoma, bevacizumab

                                Abstract snippet: "...mutations in TP53 and KRAS were identified using whole exome sequencing..."
                                BAD output: mutation, gene, sequencing, identified
                                GOOD output: TP53, KRAS, whole exome sequencing
                                
                                [OUTPUT FORMAT]
                                 - Output multi-word terms as hyphenated or underscored units
                                (e.g., "single-cell RNA sequencing", "whole_exome_sequencing")
                                 - Extract organ/tissue terms ONLY when part of a specific disease or cancer subtype
                                (e.g., "lung cancer", "prostate adenocarcinoma" → INCLUDE)
                                - Do NOT extract standalone anatomical terms
                                (e.g., "lung", "prostate", "breast" alone → EXCLUDE)
                                - Do NOT split compound terms into individual words
                                - Output ONLY the raw keywords separated strictly by commas.
                                - Do NOT include any introductory remarks, conversational fillers, concluding text, or markdown formatting (No bolding, No bullet points, No line breaks)."""},
                                {"role": "user", "content" : for_cloud}
                            ]
                    )

                        response = for_reading.choices[0].message.content
                        wordcloud = WordCloud(
                            width=800,
                            height=400,
                            background_color="white",
                            max_words=50,
                            colormap="viridis",
                            stopwords=custom_stopwords,
                            min_word_length=3,
                            mask=chormosome_mask,
                            font_path="Tektur-Medium.ttf"
                            ).generate(response)
                        fig, ax = plt.subplots(figsize=(6, 3))
                        ax.imshow(wordcloud, interpolation="bilinear")
                        ax.axis("off")
                        st.pyplot(fig)

                        wc_words = sorted(wordcloud.words_.items(), key=lambda x: x[1], reverse=True)[:10]
                        st.subheader("Top 10 Words")
                        for i, (word, _) in enumerate(wc_words, 1):
                            st.write(f"{i}. {word}")

                        st.subheader("This wordcloud still needs devloping!")
                        st.write("""
                                If you see something (a word) that doesn't look right, please report it using 'Report a Bug' on the sidebar. We'll sort it.
                                 """)

                if show_chart == False:
                    result = client.chat.completions.create(
                        model="meta-llama/llama-4-scout-17b-16e-instruct",
                        temperature= 0.1,
                        messages=[
                            {"role": "system", "content": """You are a world-class bioinformatics expert. 

                    Read the biomedical literature abstracts provided below and extract the key information into a Markdown Table format so that researchers can grasp it at a glance. 
                    If the extracted gene is completely different from the user's search query, do not include it, or focus strictly on the relationship with the queried gene.

                    [STRICT RULES]
                    - Do NOT include any conversational filler, introductory remarks, or concluding text (e.g., "Here is the table you requested"). 
                    - Output ONLY the raw Markdown Table.
                    - Each provided abstract must correspond to EXACTLY ONE row in the table.
                    - Do not split a single paper into multiple rows.

                    [Evidence Level Classification Guide]
                    Analyze the methodology of each study mentioned in the abstract and assign an "Evidence Level" (Level A, B, C, or D) based on the following strict criteria:
                    - Level A (High): Large-scale clinical trials, well-designed multi-center cohort studies, or FDA-approved diagnostic/therapeutic consensus.
                    - Level B (Moderate): Small-scale clinical studies, single-center case-control studies, or robust in vivo animal model experiments showing clear phenotypic changes.
                    - Level C (Emerging): Early-stage functional studies, in vitro cell line experiments, or preliminary laboratory benchwork without animal/human validation.
                    - Level D (Low): Single case reports, case series with very limited sample sizes, or purely descriptive observational studies.
                            
                    [Table Columns Requirements]
                    1. Target/Subject: The core entity discussed (e.g., Gene, Drug/Chemical, Disease, or Biological Pathway).
                    2. Title: Given title of the paper.
                    3. Key Variant/Modality: The specific mutation, drug dosage, or specific experimental condition (write 'N/A' if not specified).
                    4. Associated Condition/Context: The disease, clinical condition, or biological context linked to the target.
                    5. Species/Model: The research model or subject used (e.g., Human, Mouse, In vitro/Cell lines, etc.).
                    6. Evidence Level: Assign Level A, B, C, or D based on the Guide above. (write 'N/A' if unapplicable.)
                    7. Key Finding: A concise, one-sentence summary of the main conclusion.

                    [Abstracts Data]"""},
                            {"role": "user", "content" : for_prompt}
                        ]
                    )

                    response = result.choices[0].message.content
                    st.markdown(response)
                    st.download_button(
                        label="Download",
                        data=response,
                        file_name=f"{search_user}_{today}.md",
                        mime="text/markdown"
                    )
                    with st.expander("See original paper links"):
                        for id in id_list:
                            st.write(f"https://pubmed.ncbi.nlm.nih.gov/{id}/")
