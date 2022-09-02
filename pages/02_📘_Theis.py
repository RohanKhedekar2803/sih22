import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.special import exp1
from fpdf import FPDF
from datetime import date, datetime
from scipy.optimize import curve_fit
import images

st.set_page_config(page_title="Theis", page_icon="🌊",
                   layout="wide", initial_sidebar_state="auto", menu_items=None)

st.title(f"*Theis Method*")
st.markdown("""---""")

location = st.text_input(
    "Test Location", placeholder='Enter the location of the test well')
coordinates = st.text_input(
    "Coordinates of test location", placeholder='48.8566° N, 2.3522° E')
test_employee = st.text_input(
    "Performed by", placeholder='Performed by Mr / Mrs. ____')
today_date = date.today()
today_date_string = today_date.strftime("%Y/%m/%d")
today_date_year = int(today_date_string[0:4])
today_date_month = int(today_date_string[5:7])
today_date_day = int(today_date_string[8:])
date_performed = st.date_input("Date of performance of test", date(
    today_date_year, today_date_month, today_date_day))
st.markdown("""---""")

Q = st.number_input('Pumping rate from well (m3/day)',
                    min_value=0.000, format="%.3f")
r = st.number_input('Distance from well (m)', min_value=0.000, format="%.3f")
st.markdown("""---""")

input_method = st.radio('Choose a method for input of data',
                        ('Upload File', 'Fill Form'), horizontal=True)

if 'theis_time' not in st.session_state:
    st.session_state.theis_time = list()
if 'theis_drawdown' not in st.session_state:
    st.session_state.theis_drawdown = list()
if 'exception_status' not in st.session_state:
    st.session_state.exception_status= False


def form_callback(t, s):
    st.session_state.theis_time.append(t)
    st.session_state.theis_drawdown.append(s)


def delete():
    try:
        del st.session_state.theis_time[del_index]
        del st.session_state.theis_drawdown[del_index]
    except:
        st.session_state.exception_status=True

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
        if st.session_state.exception_status==True:
            st.warning('Incorrect Index Entered')
            st.session_state.exception_status=False

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

    t = np.array(df['Time'])

    # figure out dimensions of time this is supposed to be days
    # t = np.divide(t, 1440, dtype=np.longdouble)

    s = np.array(df['Drawdown'])

    def calculate_u(r, S, T, t):
        return (r*r*S)/(4*T*t)

    def calculate_theis_drawdown(t, S, T, Q, r):
        u = calculate_u(r, S, T, t)
        s_theis = Q/(4*np.pi*T)*exp1(u)
        return s_theis

    def theis_function(t, S, T):
        return calculate_theis_drawdown(t, S, T, Q, r)

    popt, pcov = curve_fit(theis_function, t, s)
    Sfit, Tfit = popt
    st.info('Storativity = {}'.format(Sfit))
    st.info('Transmissivity = {} m2/day'.format(Tfit))
    theis_fit = calculate_theis_drawdown(t, Sfit, Tfit, Q, r)
    st.markdown("""---""")

    rms = np.sqrt(np.sum((s - theis_fit)**2))
    st.success(f'RMS residual = {rms}')

    fig, ax = plt.subplots()
    plt.plot(t, s, 'x', label='Field Data')
    plt.plot(t, theis_fit, label='Theis Fit')
    plt.title('Drawdown vs Time')
    plt.xlabel('Time (days)')
    plt.ylabel('Drawdown (m)')
    plt.legend(loc='best')
    plt.savefig('fig.png')
    st.pyplot(fig)
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

    pdf = FPDF()
    pdf.add_page()

    pdf.image('images/logo.jpg', w=100, h=30)

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 10, 'CENTRAL GROUND WATER BOARD (CGWB)', ln=1)
    pdf.ln(5)

    pdf.set_font('Arial', 'B', 18)
    pdf.cell(0, 10, 'Theis Test Report', align='C', ln=1)
    pdf.line(10, int(pdf.get_y()), 210-10, int(pdf.get_y()))
    pdf.ln(5)

    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Location : {location}', align='L')
    pdf.cell(0, 10, f'Coordinates : {coordinates}', align='R', ln=1)
    pdf.cell(0, 10, f'Performed by : {test_employee}', align='L')
    pdf.cell(0, 10, f'Performed on : {date_performed}',align='R',ln=1)
    pdf.ln(5)

    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Well Discharge (Q) : {Q} m3/day', ln=1)
    pdf.cell(0, 10, f'Radial Distance (r) : {r} m', ln=1)
    pdf.ln(5)

    pdf.set_font('Arial', 'B', 13)
    pdf.cell(0, 10, 'Data Table', ln=1)

    pdf.set_font('Arial', '', 12)
    output_df_to_pdf(pdf, df)
    pdf.ln(5)

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f'Transmissivity : {round(Tfit, 5)} m2/day', ln=1)
    pdf.cell(0, 10, f'Storativity : {round(Sfit, 5)}', ln=1)
    pdf.cell(0, 10, f'Mean Fitting Error = {round(rms, 5)}%', ln=1)
    pdf.ln(4)

    pdf.set_font('Arial', 'B', 13)
    pdf.cell(0, 10, "Graphical Interpretation", ln=1)
    pdf.image('fig.png', w=200, h=200)
    pdf.ln(5)
    pdf.dashed_line(10, int(pdf.get_y()), 210 - 10,
                    int(pdf.get_y()), dash_length=1, space_length=1)

    filename = "Theis_Test_Report_" + \
        datetime.now().strftime("/%d/%m/%Y,%H:%M:%S")+".pdf"
    st.download_button("Download Report", data=pdf.output(
        dest='S').encode('latin-1'), file_name=filename)

    st.markdown("""---""")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
