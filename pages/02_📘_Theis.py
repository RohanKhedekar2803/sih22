import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.special import exp1
from fpdf import FPDF
from datetime import date, datetime
import images

st.set_page_config(page_title="Theis", page_icon="🌊",
                   layout="wide", initial_sidebar_state="auto", menu_items=None)

st.title(f"*Theis Method*")
st.markdown("""---""")

location = st.text_input(
        "Test Location", placeholder='Enter the location of the test well')
coordinates = st.text_input(
        "Coordinates of test location", placeholder='48.8566° N, 2.3522° E')
soils = ['Alluvial Soil', 'Red & Yellow Soil', 'Black Cotton Soil', 'Laterite Soil',
             'Mountainous or Forest Soil', 'Arid or Desert Soil', 'Saline and Alkaline Soil', 'Peaty and Marshy Soil']
soil_select = st.selectbox('Geology', soils, help='Select soil type')
rocks = ['Evaporitic', 'Carbonated', 'Detrital', ' Organic or plant organogenous',
             'Non consolidated', 'Plutonic', 'Volcanic', 'Metamorphic', 'Ortogneissic']
rock_select = st.selectbox('Lithology', rocks, help='Select rock type')
test_employee = st.text_input(
        "Performed by", placeholder='Performed by Mr / Mrs. ____')

column1, column2 = st.columns(2)

with column1:
        start_date = st.date_input('Start Date')

with column2:
        end_date = st.date_input('End Date')

if(end_date < start_date):
        st.error('Invalid date input - End date should be greater than start date')
        st.stop()

with column1:
        st.write('Start time')
        shr = int(st.number_input("hr", min_value=0, max_value=24))
        smin = int(st.number_input("min", min_value=0, max_value=60))

with column2:
        st.write('End time')
        ehr = int(st.number_input("hr ", min_value=0, max_value=24))
        emin = int(st.number_input("min ", min_value=0, max_value=60))

start_date_string = start_date.strftime("%Y/%m/%d")
start_date_year = int(start_date_string[0:4])
start_date_month = int(start_date_string[5:7])
start_date_day = int(start_date_string[8:])

end_date_string = end_date.strftime("%Y/%m/%d")
end_date_year = int(end_date_string[0:4])
end_date_month = int(end_date_string[5:7])
end_date_day = int(end_date_string[8:])

start_datetime = datetime(
        start_date_year, start_date_month, start_date_day, shr, smin, 0)
end_datetime = datetime(end_date_year, end_date_month,
                            end_date_day, ehr, emin, 0)

delta_time = ((end_datetime-start_datetime).total_seconds())/60
st.info(f"Total Duration of test is {delta_time} mins")

st.markdown("""---""")

zone = st.number_input('Zones Tapped in (bgl m)',
                           min_value=0.000, format="%.3f")
well_depth = st.number_input('Well Depth', min_value=0.000, format="%.3f")
well_diameter = st.number_input(
        'Well Diameter', min_value=0.000, format="%.3f")
static_water = st.number_input(
        'Static water level', min_value=0.000, format="%.3f")
st.markdown("""---""")

Q = st.number_input('Pumping rate from well (m3/day)',
                        min_value=0.000, format="%.3f")
r = st.number_input('Distance from well (m)',
                        min_value=0.000, format="%.3f")
st.markdown("""---""")

input_method = st.radio('Choose a method for input of data',
                            ('Upload File', 'Fill Form'), horizontal=True)

if 'theis_time' not in st.session_state:
    st.session_state.theis_time = list()
if 'theis_drawdown' not in st.session_state:
    st.session_state.theis_drawdown = list()
if 'exception_status' not in st.session_state:
    st.session_state.exception_status = False

def form_callback(t, s):
        st.session_state.theis_time.append(t)
        st.session_state.theis_drawdown.append(s)

def delete():
    try:
        del st.session_state.theis_time[del_index]
        del st.session_state.theis_drawdown[del_index]
    except:
        st.session_state.exception_status = True

    if(input_method == 'Fill Form'):

        col1, col2 = st.columns(2)

        with col1:
            st.write('Add Reading')
            time_data = st.number_input(
                'Time (days)', min_value=0.0, format="%.2f")
            drawdown_data = st.number_input(
                'Drawdown (m)', min_value=0.0, format="%.2f")
            submit = st.button(label='Enter data', on_click=form_callback, args=(
                time_data, drawdown_data))

        with col2:
            st.write('Delete Reading')
            del_index = st.number_input('Index', min_value=0)
            del_button = st.button('Delete', on_click=delete)
            if st.session_state.exception_status == True:
                st.warning('Incorrect Index Entered')
                st.session_state.exception_status = False

        if 'theis_time' in st.session_state:
            df = pd.DataFrame({'Time': st.session_state.theis_time,
                               'Drawdown': st.session_state.theis_drawdown})
            st.table(df)

    if(input_method == 'Upload File'):

        uploaded_file = st.file_uploader("Choose a file")
        st.warning(
            'Please keep the data in two columns as Time (days) and Drawdown (m) resepectively')
        if(uploaded_file):
            df = pd.read_csv(uploaded_file)
            st.table(df)

    if "theis_calculated_button_clicked" not in st.session_state:
        st.session_state.theis_calculated_button_clicked = False

    def callback():
        st.session_state.theis_calculated_button_clicked = True

    calculate_theis = st.button(label='Calculate', on_click=callback)
    st.markdown("""---""")

    if calculate_theis or st.session_state.theis_calculated_button_clicked:

        if(Q == 0 or r == 0):
            st.error('Invalid user input - entered value is zero')
            st.stop()

        if 'df' not in locals():
            st.error('Invalid user input - please enter data')
            st.stop()

        s = np.array(df['Drawdown'])
        t = np.array(df['Time'])

        t = np.divide(t, 1440)

        def calculate_u(r, S, T, t):
            return (r*r*S)/(4*T*t)

        def calculate_theis_drawdown(t, S, T, Q, r):
            u = calculate_u(r, S, T, t)
            s_theis = Q/(4*np.pi*T)*exp1(u)
            return s_theis

        def theis_function(t, S, T):
            return calculate_theis_drawdown(t, S, T, Q, r)

        fig, ax = plt.subplots()
        plt.plot(t, s, 'x')
        plt.xlabel('Time')
        plt.ylabel('Drawdown')
        st.pyplot(fig)
        fig, ax = plt.subplots()
        lnt = np.log(t)
        coeffs = np.polyfit(np.log(t), s, 1)
        plt.plot(lnt, s, ls='', marker='o', label='Field Data')
        fit_line = np.poly1d(coeffs)(lnt)
        plt.plot(lnt, fit_line, label='Theis Fit')
        plt.xlabel('Time')
        plt.ylabel('Drawdown')
        plt.legend(loc='best')
        plt.savefig('fig.png')
        st.pyplot(fig)
        st.markdown("""---""")

        rms_residual = np.sqrt(np.sum((fit_line - s)**2))
        m, c = coeffs

        def get_S_and_T(m, c):
            Tfit = Q / 4 / np.pi / m
            Sfit = 4 * Tfit / r**2 * np.exp(-(c/m + np.euler_gamma))
            return Sfit, Tfit

        S, T = get_S_and_T(m, c)

        st.info('Transmissivity = {} m2/day'.format(round(T, 5)))
        st.info('Storativity = {}'.format(round(S, 5)))

        st.success(f'RMS residual = {round(rms_residual, 5)}')
        st.markdown("""---""")

        def output_df_to_pdf(pdf, df):
            table_cell_width = 35
            table_cell_height = 10
            pdf.set_font('Arial', 'B', 8)
            cols = df.columns
            for col in cols:
                pdf.cell(table_cell_width, table_cell_height,
                         col, align='C', border=1)
            pdf.ln(table_cell_height)
            pdf.set_font('Arial', '', 10)
            for row in df.itertuples():
                for col in cols:
                    value = str(round(getattr(row, col), 5))
                    pdf.cell(table_cell_width, table_cell_height,
                             value, align='C', border=1)
                pdf.ln(table_cell_height)
                
        def output_df_to_pdf1(pdf, df):
          table_cell_width = 90
          table_cell_height = 12
          pdf.set_font('Arial', '', 12)
          cols = df.columns
          for row in df.itertuples():
              for col in cols:
                  value = str(getattr(row, col))
                  if (value[:9] == 'Performed'):
                      table_cell_width = 180
                      pdf.cell(table_cell_width, table_cell_height, value, align='L', border=1)
                  elif (value == ''):
                      pass
                  else:
                      table_cell_width = 90
                      pdf.cell(table_cell_width, table_cell_height, value, align='L', border=1)
              pdf.ln(table_cell_height)

        pdf = FPDF()
        pdf.add_page()

        pdf.image('images/logo.jpg', w=25, h=30)

        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 10, 'CENTRAL GROUND WATER BOARD (CGWB)', ln=1)
        pdf.ln(5)

        pdf.set_font('Arial', 'BU', 18)
        pdf.cell(0, 10, 'Theis Test Report', align='C', ln=1)
        pdf.ln(5)

        pdf.set_font('Arial', '', 12)
        lst1 = list()
        lst2 = list()
        lst1.append(f' location: {location} ')
        lst2.append(f' coordinate: {coordinates} ')
        lst1.append(f' Geology: {soil_select} ')
        lst2.append(f' Lithology: {rock_select} ')
        lst1.append(f'Performed by: {test_employee} ')
        lst2.append('')
        lst1.append(f'Start time: {shr}:{smin} ')
        lst2.append(f'End time:  {ehr}:{emin}')
        lst1.append(f' Start Date: {start_date} ')
        lst2.append(f' End date:  {end_date} ')

        df_1 = pd.DataFrame({'properties': lst1, 'values': lst2})
        output_df_to_pdf1(pdf, df_1)

        pdf.ln(15)

        lst3 = list()
        lst4 = list()
        lst3.append(f' Zones tapped in : {zone} (bgl m)')
        lst4.append(f' Well depth : {well_depth} m')
        lst3.append(f' Well diameter : {well_diameter} m')
        lst4.append(f' Static water level : {static_water} m')
        df_2 = pd.DataFrame({'properties': lst3, 'values': lst4})
        output_df_to_pdf1(pdf, df_2)
        pdf.ln(5)

        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'Well Discharge (Q) : {Q} m3/day', ln=1)
        pdf.cell(0, 10, f'Radial Distance (r) : {r} m', ln=1)
        pdf.ln(5)

        pdf.set_font('Arial', 'B', 13)
        pdf.cell(0, 10, "Graphical Interpretation", ln=1)
        pdf.image('fig.png', w=200, h=200)
        pdf.ln(5)

        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, f'Transmissivity : {round(T, 5)} m2/day', ln=1)
        pdf.cell(0, 10, f'Storativity : {round(S, 5)}', ln=1)
        pdf.cell(
            0, 10, f'Mean Fitting Error = {round(rms_residual, 5)}%', ln=1)
        pdf.ln(5)

        pdf.set_font('Arial', 'B', 13)
        pdf.cell(0, 10, 'Data Table', ln=1)

        pdf.set_font('Arial', '', 12)
        output_df_to_pdf(pdf, df)
        pdf.ln(4)

        pdf.dashed_line(10, int(pdf.get_y()), 210 - 10,
                        int(pdf.get_y()), dash_length=1, space_length=1)

        filename = "Theis_Test_Report_" + \
            datetime.now().strftime("%d-%m-%Y,%H:%M:%S")+".pdf"
        st.download_button("Download Report", data=pdf.output(
            dest='S').encode('latin-1'), file_name=filename)

        firebaseConfig = {
            'apiKey': "AIzaSyC42lNhRM9iJ2yvvbVEmttCMSA_tDlGgVY",
            'authDomain': "aquaprobedb.firebaseapp.com",
            'projectId': "aquaprobedb",
            'databaseURL': "https://aquaprobedb-default-rtdb.firebaseio.com/",
            'storageBucket': "aquaprobedb.appspot.com",
            'messagingSenderId': "176700935107",
            'appId': "1:176700935107:web:4f8550ef564458d4718b76"
        }

        firebase = pyrebase.initialize_app(firebaseConfig)
        auth = firebase.auth()

        db = firebase.database()
        storage = firebase.storage()

        user = st.session_state.user
        handle = db.child(user['localId']).child("Handle").get().val()
        upload_path_on_cloud = f"{handle}/{location}/{filename}"

        def upload_file_to_storage(file):
            storage.child(upload_path_on_cloud).put(file)

        upload_file = st.button('Upload to Archives')
        if upload_file:
            upload_file_to_storage(pdf.output(dest='S').encode('latin-1'))
            st.success('File uploaded to Archive!')

        st.markdown("""---""")
