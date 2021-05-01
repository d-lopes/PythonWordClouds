import stylecloud
import tempfile
import base64
import json
import streamlit as st
from PIL import Image
from io import BytesIO

# -----------------------
# initialisation
# -----------------------
with open('/app/src/config.json') as json_file:
    config = json.load(json_file)
    cmaps_cartocolor_types = config['cmaps']['types']
    cmaps_cartocolors = config['cmaps']['colors']
    icons = config['supported_icons']

# -----------------------
# util functions
# -----------------

def get_image_download_link(img):
        """Generates a link allowing the PIL image to be downloaded
        in:  PIL image
        out: href string
        """
        buffered = BytesIO()
        img.save(buffered, format="PNG") # PNG for lossless compression
        img_str = base64.b64encode(buffered.getvalue()).decode()
        href = f'Result: <a href="data:file/png;base64,{img_str}">Download</a>'
        return href

def fmt_color_palette_type_choice(option):
    retVal = option
    try:
        retVal = cmaps_cartocolor_types.get(option)
    except:
        pass
    return retVal

def fmt_color_palette_choice(option):
    retVal = option
    try:
        retVal = cmaps_cartocolors[color_palette_type].get(option)
    except:
        pass
    return retVal

# -----------------------
# overall page settings
# ------------------------
st.set_page_config( page_title="Word Cloud Generator", layout="wide")
st.title('Word Cloud Generator')

# hide hamburger menu and footer
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# -----------------------
# set options in Sidebar
# -----------------------
st.sidebar.subheader("Settings")

with st.sidebar.beta_expander("Shape"):
    icon_name = st.selectbox(label = "Icon Mask:", options = icons, help = "valid Icon Name for the word cloud shape - see https://fontawesome.com/icons?d=gallery&p=2&m=free for visual representations of icon names")
    invert_mask = st.checkbox(label = 'Invert mask', help = "Whether to invert the icon mask, so the words fill the space except the icon mask.")

with st.sidebar.beta_expander("Colors"):
    # construct color palette name -> based on palettable we can follow this naming convention: cartocolors.<Type>.<Name>_<number of colors>
    color_palette_type = st.selectbox(label = "Palette Type:", options = list(cmaps_cartocolor_types.keys()), format_func = fmt_color_palette_type_choice, help = "Choose one of the available color palette types - see https://jiffyclub.github.io/palettable/cartocolors/ for visual representations of color palette types and associated colors")
    color_palette = st.selectbox(label = "Palette:", options = list(cmaps_cartocolors[color_palette_type].keys()), format_func = fmt_color_palette_choice, help = f"Choose one of the available color palette - see https://jiffyclub.github.io/palettable/cartocolors/{color_palette_type} for visual representations of color palette types and associated colors")
    no_colors = st.slider(label = 'No. of colors:', min_value=2, max_value=7, value=5, step=1, help = "Number of colors to use for the text in the word cloud.")
    palette = f"cartocolors.{color_palette_type}.{color_palette}_{no_colors}"

    bg_color = st.color_picker(label = "Background Color:", value = "#ffffff", help = "Background color of the word cloud")

with st.sidebar.beta_expander("Dimensions"):
    width = st.slider(label = 'Width:', min_value=96, max_value=1024, value=512, step=8, help = "width in pixels of the word cloud.")
    height = st.slider(label = 'Height:', min_value=96, max_value=1024, value=512, step=8, help = "height in pixels of the word cloud.")
    max_font_size = st.slider(label = 'Max. font size:', min_value=10, max_value=400, value=200, step=10, help = "Maximum font size in the word cloud.")

with st.sidebar.beta_expander("Content"):
    max_words = st.text_input(label = "Max. words:", value = "2000", help = "Maximum number of words to include in the wordcloud.")
    collocations = st.checkbox(label = 'Include Collocations', value = True, help = "Whether to include collocations (bigrams) of two words.")

# -----------------------
# Main content
# -----------

# start with Hello in 21 different languages (see https://www.babbel.com/en/magazine/how-to-say-hello-in-10-different-languages)
text = "Bonjour Salut Hola ¿Qué tal? Zdravstvuyte Privet Nǐn hǎo Nǐ hǎo Salve Ciao Konnichiwa Yā, Yō Guten Tag Hallo, Hi Olá Oi Anyoung haseyo Anyoung Asalaam alaikum Ahlan Goddag Hej, Halløj Swahili Habari, Hujambo Goedendag Hoi, Hallo Yassas Yassou Dzień dobry Cześć, Witaj Selamat siang Halo Namaste, Namaskar Hai, Helo Merhaba Selam Shalom Hey God dag Hej, Tjena God dag Hei"
text_input = st.text_area(label = "Word Cloud Text:", value = text, height = 150)

# render the image (if test is given)
if len(text_input) > 0:
    placeholder = st.empty()
    placeholder.write('Result:')
    
    tf = tempfile.NamedTemporaryFile()
    output_file = f'{tf.name}.png'

    try: 
        stylecloud.gen_stylecloud(text = text_input, icon_name = f'fas fa-{icon_name}', invert_mask = invert_mask, palette = palette, background_color = bg_color, size = (int(width), int(height)), 
            max_font_size = int(max_font_size), max_words = int(max_words), collocations = collocations, output_name = output_file)

        image = Image.open(output_file)
        st.image(image, output_format = "PNG") # PNG for lossless compression
        placeholder.markdown(get_image_download_link(image), unsafe_allow_html=True)

    except:
        st.error(f"unable to render word cloud with the given settings")    
