#Import the required Libraries
import streamlit as st
import numpy as np
from  PIL import Image
from skimage import color
import sys
import os
import io
from zipfile import ZipFile



Image.MAX_IMAGE_PIXELS = 1e12
			      
       
def segment_img(img_rgb, lower_bound, upper_bound):
    hsv_img = color.rgb2hsv(img_rgb)*180

    mask = np.all((hsv_img >= lower_bound) & (hsv_img <= upper_bound), axis=-1)
    num_tumor_pixel = np.sum(mask)
    perc = num_tumor_pixel/(hsv_img.shape[0]*hsv_img.shape[1] )*100

    hsv_img = np.zeros(img_rgb.shape, dtype=np.uint)
    hsv_img[mask]=img_rgb[mask]
    
    return hsv_img, num_tumor_pixel, np.round(perc, decimals=2)


def file_process_in_memory(images):
    """ Converts PIL image objects into BytesIO in-memory bytes buffers. """

    for i, (image_name, pil_image) in enumerate(images):
        file_object = io.BytesIO()
        pil_image.save(file_object, "PNG")
        pil_image.close()
        images[i][1] = file_object  # Replace PIL image object with BytesIO memory buffer.

    return images  # Return modified list.

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 100px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# st.sidebar.header("Sidebar")

# app_mode = st.sidebar.selectbox('Select Page',['Segmentation'] ) #three pages
   



st.markdown(""" <style> .font0 {
font-size:35px ; font-family: 'Cooper Black'; color: black;} 
</style> """, unsafe_allow_html=True)

st.markdown(""" <style> .font1 {
font-size:20px ; font-family: 'Cooper Black'; color: black;} 
</style> """, unsafe_allow_html=True)

st.markdown(""" <style> .font2 {
font-size:20px ; font-family: 'Cooper Black'; color: green;} 
</style> """, unsafe_allow_html=True)


image1 = Image.open('images/logo_ukj.png')

#Create two columns with different width
col1, col2 = st.columns( [0.7, 0.3])
with col1:               # To display the header text using css style
    st.markdown('<p class="font0">Image Color Segmentation</p>', unsafe_allow_html=True)
    st.markdown('<p class="font1">This is a streamlit app to segment colors in images</p>', unsafe_allow_html=True)
with col2:               # To display brand logo
    st.image(image1,  width=200) 


st.markdown(
    """
<style>
.stButton > button {
color: black;
background: white;
width: auto;
height: auto;
}
</style>
""",
    unsafe_allow_html=True,
)

upload_file = st.file_uploader('Load image files', type=['jpg','jpeg','png','tif'], accept_multiple_files=True, label_visibility="collapsed" )
 



lower_bound = st.session_state.get("lower_bound", (144, 27, 0))
upper_bound = st.session_state.get("upper_bound", (179, 179, 179))
display_imgs = st.session_state.get("display_imgs", None)
img_rgb = st.session_state.get("img_rgb", np.array([0]))

if upload_file:
    
    st.write("Select bounds for Segmentation:")
    c1l, c2l, c3l = st.columns( [0.3, 0.3, 0.3])
    with c1l:
        Hue_l = st.slider('Hue lower bound:', 0, 179, 144)
    with c2l:
        Sat_l = st.slider('Saturation lower bound:', 0, 179, 27)
        
    st.session_state.lower_bound = (Hue_l,Sat_l,0)

    
    c1u, c2u, c3u = st.columns( [0.3, 0.3, 0.3])
    with c1u:
        Hue_u = st.slider('Hue upper bound:', 0, 179, 179)
        #st.image('/home/ralf/Documents/21_segementation/GUI_streamlit/images/hue_spektrum.jpg')
    with c2u:
        Sat_u = st.slider('Saturation upper bound:', 0, 179, 179)

        
    st.session_state.upper_bound = (Hue_u,Sat_u,179)

    
    if img_rgb.shape[0]==1:
        img_rgb = np.asarray(Image.open( upload_file[0] ).convert('RGB'))
        st.session_state.img_rgb = img_rgb
    
    lower_bound = st.session_state.get("lower_bound", (144, 27, 0))
    upper_bound = st.session_state.get("upper_bound", (179, 179, 179))
    img_segm, num_tumor_pixel_01, perc_01 = segment_img( img_rgb , lower_bound, upper_bound)

    col1_img, col2_img = st.columns( [0.5, 0.5])
    with col1_img: 
        st.image(img_rgb)
    with col2_img: 
        st.image(img_segm)
        
    c1w, c2w, c3w = st.columns( [0.3, 0.3, 0.3])
    with c1w:
        st.write("Example image name:  " + upload_file[0].name)
        st.write("Selected bounds for Hue: "  + str(lower_bound[0]) + ' - ' + str(upper_bound[0]))
    with c2w:
        st.write("Percent Area:  " + str(perc_01))
        st.write("Selected bounds for Saturation: "  + str(lower_bound[1]) + ' - ' + str(upper_bound[1]))
    with c3w:
        st.write("Number of Tumor Pixels:  "  + str(num_tumor_pixel_01) )
  
        
    csv_name = st.text_input('Seclet name for results.csv file:', value="results.csv",  help='File should have .csv extension to be recognized by standard software.' ,  label_visibility="visible")
   

st.divider()
    

replace_commas = st.session_state.get("replace_commas", None)    
has_comma = st.session_state.get("commas", None)
if (has_comma == None) and upload_file:
    has_comma = False
    for file in upload_file:
        if ';' in file.name:
            st.session_state.commas = True
    st.session_state.commas = 'checked'
    
if (has_comma==True):
    st.warning('Semicolon found in image filenames. This is not recommended as commas are the delimiters in the result.csv file. Commas will be replaced with underscores in the image names in the CSV file.', icon="⚠️")
    st.session_state.replace_commas = True

    

######################################

run = st.button('**Run calculation**' )

placeholder = st.empty()
if run: 
    if upload_file:
        
        name_images_pairs = []

        # create output csv and write headings
        sep = ';'
        result_csv = 'sep=;' + '\n'  # for excel to recognize the column seperator
        
        result_csv += 'img_file;' + 'NumPixels;' + 'PercArea;' + '\n'

        my_bar = st.progress(0)

        with st.spinner("Operation in progress. Please wait and don't refresh your browser."):
        
            for n in range(len(upload_file)):
                
                img_name = upload_file[n].name

                placeholder.text('Calculation for image:   ' + img_name)

                
                if replace_commas:
                    img_name = img_name.replace(";", "_")
                    
                lower_bound = st.session_state.get("lower_bound", (144, 27, 20))
                upper_bound = st.session_state.get("upper_bound", (179, 255, 255))
                    
                img_tmp = np.asarray(Image.open(upload_file[n]  ).convert('RGB'))
                img_segmented, num_tumor_pixel, perc = segment_img(   img_tmp  , lower_bound, upper_bound)
                
                # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                print(img_segmented, img_segmented.shape)
                
                pil_image = Image.fromarray(img_segmented.astype('uint8'), 'RGB')
                name_images_pairs.append([img_name, pil_image])
                

                result_csv += img_name + sep + str(num_tumor_pixel).replace('.',',') + sep + str(np.round(perc, decimals=2)).replace('.',',') + sep + '\n'


                my_bar.progress( int( (n+1)/len(upload_file) * 100) )

        result_csv += "Selected bounds for Hue: "  + str(lower_bound[0]) + ' - ' + str(upper_bound[0]) + '\n'
        result_csv += "Selected bounds for Saturation: "  + str(lower_bound[1]) + ' - ' + str(upper_bound[1]) + '\n'
        
        
        images = file_process_in_memory(name_images_pairs )
        zip_file_bytes_io = io.BytesIO()
        
        with ZipFile(zip_file_bytes_io, 'w') as zip_file:
            for image_name, bytes_stream in images:
                zip_file.writestr(image_name+".png", bytes_stream.getvalue())
            zip_file.writestr(csv_name, result_csv)
              
    else:
        st.write('No image files found. Load images first.')

    
if run and upload_file:
    st.success('Calculations finished. A csv-file has been created in your selected results folder.', icon="✅")
    download = st.download_button('Download segmented images and results', zip_file_bytes_io, file_name='segmented_imgs_and_results.zip')  # Defaults to 'text/plain'
    
  


    
