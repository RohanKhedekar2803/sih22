import streamlit as st
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import date, datetime
import images

st.set_page_config(page_title="Theis Recovery", page_icon="🌊",
                   layout="wide", initial_sidebar_state="auto", menu_items=None)

st.title(f"*Theis Recovery Method*")
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
t_when_pumping_stopped = st.number_input(
    "Time when pumping was stopped (mins)", min_value=0.000, format="%.3f")

if 'theis_recovery_time' not in st.session_state:
    st.session_state.theis_recovery_time = list()
if 'theis_recovery_drawdown' not in st.session_state:
    st.session_state.theis_recovery_drawdown = list()


def form_callback(t, s):
    st.session_state.theis_recovery_time.append(t)
    st.session_state.theis_recovery_drawdown.append(s)


def delete():
    del st.session_state.theis_recovery_time[del_index]
    del st.session_state.theis_recovery_drawdown[del_index]


st.markdown("""---""")

input_method = st.radio('Choose a method for input of data',
                        ('Upload File', 'Fill Form'), horizontal=True)

if(input_method == 'Fill Form'):

    col1, col2 = st.columns(2)

    with col1:
        st.write('Add Reading')
        time_data = st.number_input(
            'Time since cessation of pumping (mins)', min_value=0.0, format="%.2f")
        drawdown_data = st.number_input(
            'Residual Drawdown (m)', min_value=0.0, format="%.2f")
        submit = st.button(label='Enter data', on_click=form_callback, args=(
            time_data, drawdown_data))

    with col2:
        st.write('Delete Reading')
        del_index = st.number_input(
            label='Index', min_value=0, help='Index of reading to be deleted')
        del_button = st.button(label='Delete', on_click=delete)

    if 'theis_recovery_time' in st.session_state:
        df = pd.DataFrame({'t_dash': st.session_state.theis_recovery_time,
                           'Residual_Drawdown': st.session_state.theis_recovery_drawdown})
        st.table(df)

if(input_method == 'Upload File'):

    uploaded_file = st.file_uploader("Choose a file")
    st.warning('Please keep the data in two columns as Time since cessation of pumping (mins) and Recovery Drawdown (m) resepectively')
    if(uploaded_file):
        df = pd.read_csv(uploaded_file)
        st.table(df)

if "theis_recovery_calculated_button_clicked" not in st.session_state:
    st.session_state.theis_recovery_calculated_button_clicked = False


def callback():
    st.session_state.theis_recovery_calculated_button_clicked = True


calculate_theis_recovery = st.button(label='Calculate', on_click=callback)
st.markdown("""---""")

if calculate_theis_recovery or st.session_state.theis_recovery_calculated_button_clicked:
    cols = df.columns
            
    t_list = np.array(df['t_dash'])+t_when_pumping_stopped
    df['t'] = t_list
    df['t_by_t_dash'] = df['t']/df['t_dash']
    df = df[['t', 't_dash', 't_by_t_dash', 'Residual_Drawdown']]

    x_data = list(df['t_by_t_dash'])
    y_data = list(df['Residual_Drawdown'])
    slope, y_intercept = np.polyfit(np.log(x_data), y_data, 1)
    fig, ax = plt.subplots()
    ax.semilogx(x_data, y_data, marker='.',
                color='black', label='Actual Data')
    ax.semilogx(np.exp((y_data - y_intercept)/slope),
                y_data, 'r--', label='Fitting Line')
    plt.xlabel("log t/t'")
    plt.ylabel('Residual Drawdown')
    plt.title('Time vs Drawdown')
    plt.grid(True)
    plt.legend(loc='best')
    plt.savefig('fig.png')
    st.pyplot(fig)

    delta_s_dash = abs((slope*math.log(100) + y_intercept) -
                       (slope*math.log(10) + y_intercept))
    T = (2.303*Q)/(4*math.pi*delta_s_dash)

    ratio_of_S = np.exp((-y_intercept)/slope)

    st.info('Transmissivity = {} (m2/day)'.format(T))
    st.info('Relative change of Storativity = {}'.format(ratio_of_S))
    st.warning("In the absence of boundary effects, S/S′ should be close to unity. A value of S/S′>1 suggests recharge during the test; whereas S/S′<1 may indicate a no-flow boundary")
    st.markdown("""---""")

    st.table(df)
    st.download_button(label="Download CSV", data=df.to_csv().encode(
        'utf-8'), file_name='Theis_Recovery'+datetime.now().strftime("/%d/%m/%Y,%H:%M:%S")+'.csv')
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
    pdf.cell(0, 10, 'Theis Recovery Test Report', align='C', ln=1)
    pdf.line(10, int(pdf.get_y()), 210 - 10, int(pdf.get_y()))
    pdf.ln(5)

    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Location : {location}', align='L')
    pdf.cell(0, 10, f'Coordinates : {coordinates}', align='R', ln=1)
    pdf.cell(0, 10, f'Performed by : {test_employee}', align='L')
    pdf.cell(0, 10, f'Performed on : {date_performed}', align='R', ln=1)
    pdf.ln(5)

    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Well Discharge (Q) : {round(Q,5)} m3/day', align='L')
    pdf.cell(
        0, 10, f'Time when pumping was stopped : {round(t_when_pumping_stopped,5)} mins', align='R', ln=1)
    pdf.ln(5)

    pdf.set_font('Arial', 'B', 13)
    pdf.cell(0, 10, 'Data Table', ln=1)

    pdf.set_font('Arial', '', 12)
    output_df_to_pdf(pdf, df)
    pdf.ln(5)

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f'Transmissivity : {round(T, 5)} m2/day', ln=1)
    pdf.cell(
        0, 10, f'Relative change of Storativity : {round(ratio_of_S, 5)}', ln=1)
    pdf.ln(4)

    pdf.set_font('Arial', 'B', 13)
    pdf.cell(0, 10, "Graphical Interpretation", ln=1)
    pdf.image('fig.png', w=200, h=200)
    pdf.ln(5)
    pdf.dashed_line(10, int(pdf.get_y()), 210 - 10,
                    int(pdf.get_y()), dash_length=1, space_length=1)

    filename = "Theis_Recovery_Test_Report_" + \
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