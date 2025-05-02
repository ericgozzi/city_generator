import streamlit as st

from literate import *
from pixels import Color
from metrika import Graph

import io


def get_connections_of_a_question(theka, question):

    topic = question


    library = Library.from_library_folder(f'app/theke/{theka}')
    answers = library.ask(topic,  question, print_answers=False);


    quotebook = Quotebook(answers)
    text, footnotes, title = quotebook.build_text(create_title=True, n=deepness)

    
    filter_list = PLACES + additional_concepts

    # Fileter by places
    words = re.findall(r'\b\w+(?:-\w+)?\b', text.lower())  # Extract words, including hyphenated
    filtered = [word for word in words if word in filter_list]
    narrative = " ".join(filtered)


    
    narrative = clean_whitespaces(narrative)
    connections = get_connection_of_word(narrative)

    return connections



def build_the_city(library: str, questions: list[str]):

    connectivity = Rule([])

    for q in questions:
        conn = get_connections_of_a_question(library, q)
        connectivity.merge(conn)


    g = Graph()
    g.build_graph_from_rules(connectivity)


    bck_colors = {
        'urbotheka': Color.BLACK,
        'hitchhikers_guide': Color.BLUE,
        'cookbooks': Color.OLIVE,
        'posthuman': Color.WHITE

    }

    wrt_color = {
        'posthuman': Color.BLACK
    }

    city = g.draw(show_nodes=False, 
                  label_color=wrt_color.get(library, Color.WHITE), 
                  edge_color=wrt_color.get(library, Color.WHITE),
                  background_color = bck_colors.get(library, Color.BLACK),
                  label_size=30, 
                  edge_direction=False, 
                  graph_type="KAMADA-KAWAI")

    return city







library = st.selectbox(
    "Library",
    ("urbotheka", "posthuman", "hitchhikers_guide", "cookbooks")
)

questions = st.text_input("Concepts", 'house museum apple')



# BUTTONS LAYOUT
settings_col, generate_col, download_col = st.columns(3)


# ADVANCED SETTINGS
with settings_col.popover('Advanced Settings', use_container_width=True):
    deepness = st.slider('Deepness', 1, 100, 30, 1)

    additional_concepts = st.text_input('Additional concepts to show in the city')
    additional_concepts = additional_concepts.lower()
    additional_concepts = additional_concepts.split(' ')

    resume = st.checkbox('Show resume')


# GENERATE BUTTON
if generate_col.button('Generate City', use_container_width=True, type="primary"):
    questions = questions.lower()
    questions = questions.split(' ')
    try:
        with st.spinner("HAL is reading the books...", show_time=True):
            image = build_the_city(library, questions)
        st.image(image.np_array)
        if resume:
            st.text(f'Library: {library} \nConcepts: {', '.join(questions)} \nAdditional Concepts: {', '.join(additional_concepts)} \nDeepness: {deepness}')
    

        # Save to BytesIO buffer
        buffer = io.BytesIO()
        image.image.save(buffer, format="PNG")
        buffer.seek(0)

        download_col.download_button('Download Image', buffer, file_name=f'{library.upper()}_{'-'.join(questions)}.png', mime="image/png", use_container_width=True)
            
    
    except:
        st.error('This is embarassing... try to change the concepts.', icon="😳")

