#Import the required Libraries
import streamlit as st
import numpy as np
from  PIL import Image
from skimage import color
import sys
import os

### custom import
import tkinter as tk
from tkinter import filedialog

Image.MAX_IMAGE_PIXELS = 1e10
			      

###################### TODO's

def select_folder():
   root = tk.Tk()
   root.withdraw()
   folder_path = filedialog.askdirectory(master=root)
   root.destroy()
   return folder_path


# def scale_to_width_keep_aspect_ratio(img, width=1000):
#     a = np.sqrt(width / float(img.size[1]))
#     img = img.resize((int(img.size[0]*a),int(img.size[1]*a)), Image.Resampling.LANCZOS)
#     return img
        
def segment_img(img_rgb, lower_bound, upper_bound):
    hsv_img = color.rgb2hsv(img_rgb)*180

    mask = np.all((hsv_img >= lower_bound) & (hsv_img <= upper_bound), axis=-1)
    num_tumor_pixel = np.sum(mask)
    perc = num_tumor_pixel/(hsv_img.shape[0]*hsv_img.shape[1] )*100

    hsv_img = np.zeros(img_rgb.shape, dtype=np.uint)
    hsv_img[mask]=img_rgb[mask]
    
    return hsv_img, num_tumor_pixel, np.round(perc, decimals=2)



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

st.sidebar.header("Sidebar")

app_mode = st.sidebar.selectbox('Select Page',['Segmentation'] ) #three pages
   



st.markdown(""" <style> .font0 {
font-size:35px ; font-family: 'Cooper Black'; color: black;} 
</style> """, unsafe_allow_html=True)

st.markdown(""" <style> .font1 {
font-size:20px ; font-family: 'Cooper Black'; color: black;} 
</style> """, unsafe_allow_html=True)

st.markdown(""" <style> .font2 {
font-size:20px ; font-family: 'Cooper Black'; color: green;} 
</style> """, unsafe_allow_html=True)

if app_mode == 'Segmentation':
        
    image1 = Image.open('images/logo_ukj.png')
    
    #Create two columns with different width
    col1, col2 = st.columns( [0.7, 0.3])
    with col1:               # To display the header text using css style
        st.markdown('<p class="font0">Image Segmentation</p>', unsafe_allow_html=True)
        st.markdown('<p class="font1">This is a browser app to segment colors in images</p>', unsafe_allow_html=True)
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

    list_of_images = st.session_state.get("list_of_images", None)
    selected_img_path = st.session_state.get("img_path", None)
    img_select_button = st.button("Select the folder with the images you want to segment (jpg, jpeg, png, tif Format)")
    if img_select_button:
        selected_img_path = select_folder()
        st.session_state.img_path = selected_img_path
        st.write('Selected image path:', selected_img_path)
        st.divider()
        list_of_images = []
        for root, dirs, files in os.walk(selected_img_path):
            for file in files:
                if ('.jpg' in file) or ('.JPG' in file) or ('.jpeg' in file)  or ('.JPEG' in file) or ('.png' in file) or ('.PNG' in file) or ('.tif' in file) or ('.TIF' in file) or ('.TIFF' in file) or ('.tiff' in file): 
                    list_of_images.append(os.path.join(  root , file))
        st.session_state.list_of_images = list_of_images
    
    
    lower_bound = st.session_state.get("lower_bound", (144, 27, 0))
    upper_bound = st.session_state.get("upper_bound", (179, 179, 179))
    display_imgs = st.session_state.get("display_imgs", None)
    img_rgb = st.session_state.get("img_rgb", np.array([0]))
    
    if list_of_images:
        
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
            img_rgb = np.asarray(Image.open( list_of_images[0] ).convert('RGB'))
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
            st.write("Example image name:  " + list_of_images[0].split('/')[-1])
            st.write("Selected bounds for Hue: "  + str(lower_bound[0]) + ' - ' + str(upper_bound[0]))
        with c2w:
            st.write("Percent Area:  " + str(perc_01))
            st.write("Selected bounds for Saturation: "  + str(lower_bound[1]) + ' - ' + str(upper_bound[1]))
        with c3w:
            st.write("Number of Tumor Pixels:  "  + str(num_tumor_pixel_01) )
      
            

   
    
    st.divider()
        

    replace_commas = st.session_state.get("replace_commas", None)    
    has_comma = st.session_state.get("commas", None)
    if (has_comma == None) and list_of_images:
        has_comma = False
        for file in list_of_images:
            if ';' in file:
                st.session_state.commas = True
        st.session_state.commas = 'checked'
        
    if (has_comma==True):
        st.warning('Semicolon found in image filenames. This is not recommended as commas are the delimiters in the result.csv file. Commas will be replaced with underscores in the image names in the CSV file.', icon="⚠️")
        st.session_state.replace_commas = True

        
    #with col_down:
    selected_download_path = st.session_state.get("download_path", None)
    csv_name = st.session_state.get("csv_name", None)
    if selected_img_path:
        downl_select_button = st.button("Select folder to save results")
        csv_name = st.text_input('Seclet name for results.csv file:', value="results.csv",  help='File should have .csv extension to be recognized by standard software.' ,  label_visibility="visible")
        if downl_select_button:
            selected_download_path = select_folder()
            st.session_state.download_path = selected_download_path
            st.session_state.csv_name = csv_name
        if selected_download_path:
            st.write("The results will be saved to:", os.path.join(selected_download_path, csv_name).replace("\\","/"))
             
    

######################################

    run = st.button('**Run calculation**' )

    placeholder = st.empty()
    if run: 
        if list_of_images:

                print('##############################') 
                # create output txt and write headings

                with open(os.path.join(selected_download_path, csv_name).replace("\\","/"), 'a') as log:
                    log.write('sep=;')
                    log.write('\n')  
                    log.write('Folder;')
                    log.write('img_file;')
                    log.write('NumPixels;')
                    log.write('PercArea;')
                    log.write('\n')     
         
                #progress_text = "Operation in progress. Please wait."
                my_bar = st.progress(0)

                with st.spinner("Operation in progress. Please wait and don't refresh your browser."):
                
                    for n in range(len(list_of_images)):
                        
                        img_name = list_of_images[n].split('\\')[-1]
                        file_path = list_of_images[n]
                        
                        placeholder.text('Calculation for image:   ' + img_name)

                        
                        if replace_commas:
                            img_name = img_name.replace(";", "_")
                            
                        lower_bound = st.session_state.get("lower_bound", (144, 27, 20))
                        upper_bound = st.session_state.get("upper_bound", (179, 255, 255))
                            
                        img_tmp = np.asarray(Image.open(file_path  ).convert('RGB'))
                        img_segmented, num_tumor_pixel, perc = segment_img(   img_tmp  , lower_bound, upper_bound)
                        
                        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                        print(img_segmented, img_segmented.shape)
                        
                        PIL_image = Image.fromarray(img_segmented.astype('uint8'), 'RGB')
                        PIL_image.save( os.path.join(selected_download_path , 'segmented_' + img_name).replace("\\","/") ,  quality=100, subsampling=0)  
                        


                        with open(os.path.join(selected_download_path, csv_name).replace("\\","/"), 'a') as log:                
                            log.write('/'.join(map(str, file_path.split('\\')[:-1] ))      +  ';')
                            log.write(str(img_name) +  ';')
                            log.write(str(num_tumor_pixel).replace('.',',') +  ';')
                            log.write(str(np.round(perc, decimals=2)).replace('.',',') +  ';')
                            log.write('\n')   
                            
                        #my_bar.progress((n+1)* int(100 / (len(upload_file)))  )
                        my_bar.progress( int( (n+1)/len(list_of_images) * 100) )

        
                with open(os.path.join(selected_download_path, csv_name).replace("\\","/"), 'a') as log:
                    log.write("Selected bounds for Hue: "  + str(lower_bound[0]) + ' - ' + str(upper_bound[0]) + '\n')
                    log.write("Selected bounds for Saturation: "  + str(lower_bound[1]) + ' - ' + str(upper_bound[1]) + '\n')
                                    

        else:
            st.write('No image files found. Load images first.')
    

    enable_download = False
    if run and list_of_images:
        enable_download = True
          
    if enable_download:
        st.success('Calculations finished. A csv-file has been created in your selected results folder.', icon="✅")
        
        #download = st.download_button('Download Results', download_file, file_name='SIPmachine_results.csv')  # Defaults to 'text/plain'
        
  
    

    
