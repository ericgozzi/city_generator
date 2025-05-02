import streamlit as st

from literate import *
from pixels import Color
from metrika import Graph


def get_connections_of_a_question(theka, question):

    topic = question


    library = Library.from_library_folder(f'app/theke/{theka}')
    answers = library.ask(topic,  question, print_answers=False);


    quotebook = Quotebook(answers)
    text, footnotes, title = quotebook.build_text(create_title=True, n=deepness)

    narrative = filter_by_places(text)
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
        'cookbooks': Color.OLIVE

    }

    city = g.draw(show_nodes=False, 
                  label_color=Color.WHITE, 
                  edge_color=Color.WHITE,
                  background_color = bck_colors.get(library, Color.BLACK),
                  label_size=30, 
                  edge_direction=False, 
                  graph_type="KAMADA-KAWAI")

    return city







library = st.selectbox(
    "Library",
    ("urbotheka", "hitchhikers_guide", "cookbooks")
)

questions = st.text_input("Concepts", 'house museum apple')



# BUTTONS LAYOUT
settings_col, generate_col = st.columns(2)


# ADVANCED SETTINGS
with settings_col.popover('Advanced Settings', use_container_width=True, icon="⚙️"):
    deepness = st.slider('Deepness', 1, 100, 30, 1)
    resume = st.checkbox('Show resume')


# GENERATE BUTTON
if generate_col.button('Generate City', use_container_width=True, icon="🌆", type="primary"):
    questions = questions.lower()
    questions = questions.split(' ')
    try:
        with st.spinner("HAL is reading the books...", show_time=True):
            image = build_the_city(library, questions)
        st.image(image.np_array)
        if resume:
            st.text(f'Library: {library} \nConcepts: {', '.join(questions)} \nDeepness: {deepness}')
    except:
        st.error('This is embarassing... try to change the concepts.', icon="😳")