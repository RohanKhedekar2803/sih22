import streamlit as st
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import date, datetime
import images

st.set_page_config(page_title="Dupuit-Forchheimer", page_icon="🌊",
                   layout="wide", initial_sidebar_state="auto", menu_items=None)

st.title(f"*Dupuit-Forchheimer Method*")
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

R = st.number_input('Recharge Rate (m/day)', min_value=0.0000, format="%.4f")
Q = st.number_input('Well Discharge (m3/day)', min_value=0.0000, format="%.3f")
K = st.number_input("Hydraulic Conductivity (m/day)",
                    min_value=0.000, format="%.3f")
h0 = st.number_input('Head at Outer Radius (m)',
                     min_value=0.000, format="%.3f")

st.markdown("""---""")

r1 = st.number_input(
    'Enter the radius at which you want to obtain the head / drawdown (m)', min_value=0.000, format="%.3f")

if "dupoit_calculated_button_clicked" not in st.session_state:
    st.session_state.dupoit_calculated_button_clicked = False


def callback():
    st.session_state.dupoit_calculated_button_clicked = True


calculate_dup = st.button('Calculate', on_click=callback)
st.markdown("""---""")

if calculate_dup or st.session_state.dupoit_calculated_button_clicked:

    if(R == 0 or Q == 0 or K == 0 or h0 == 0):
        st.error('Invalid user input - entered value is zero')
        st.stop()

    area = Q/R
    r0 = math.sqrt(area/math.pi)
    st.success("Radius of Influence = {} (m)".format(r0))

    def calculate_h(r):
        if(r >= r0 or r == 0):
            return h0
        return math.sqrt((h0**2)-(Q*(math.log(r0/r)))/(K*math.pi))

    h1 = calculate_h(r1)
    st.info(f"Head at {r1} m = {h1} m")
    st.info(f"Drawdown at {r1} m = {h0-h1} m")
    st.markdown("""---""")

    r_start, r_end = st.slider(
        'Select a range of radii', 0.01, (r0+(0.5*r0)), (0.01, r0+(0.2*r0)))
    n_points = st.slider('Select number of points to interpolate', 3, 50, 20)

    step = (r_end-r_start)/n_points
    r_list = list()
    for x in np.arange(r_start, r_end, step):
        r_list.append(x)
    df = pd.DataFrame({'r': r_list})

    h_list = list()
    s_list = list()
    for index, row in df.iterrows():
        h = calculate_h(row['r'])
        h_list.append(h)
        s = h0-h
        s_list.append(s)

    df['h'] = h_list
    df['s'] = s_list

    st.table(df)
    st.download_button(label="Download CSV", data=df.to_csv().encode(
        'utf-8'), file_name='Dupuit-Forchheimer'+datetime.now().strftime("/%d/%m/%Y,%H:%M:%S")+'.csv')
    st.markdown("""---""")

    fig, ax = plt.subplots()
    plt.plot(df['r'], df['s'])
    plt.xlabel("Distance from pumping well (m)")
    plt.ylabel("Drawdown (m)")
    plt.title("Estimated Steady State Cone of Depression")
    plt.savefig('fig.png')
    arrow_properties = dict(facecolor="red", width=1, headwidth=4, shrink=0.1)
    plt.annotate("r0", (r0,s), arrowprops = arrow_properties)
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
    pdf.cell(0, 10, 'Dupuit-Forchheimer Test Report', align='C', ln=1)
    pdf.line(10, int(pdf.get_y()), 210 - 10, int(pdf.get_y()))
    pdf.ln(5)

    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Location : {location}', align='L')
    pdf.cell(0, 10, f'Coordinates : {coordinates}', align='R', ln=1)
    pdf.cell(0, 10, f'Performed by : {test_employee}', align='L')
    pdf.cell(0, 10, f'Performed on : {date_performed}',align='R',ln=1)
    pdf.ln(5)

    pdf.cell(0, 10, f'Recharge rate : {R} m/day', ln=1)
    pdf.cell(0, 10, f'Well Discharge : {Q} m3/day', align='L', ln=1)
    pdf.cell(0, 10, f'Hydraulic Conductivity : {K} m/day', ln=1)
    pdf.cell(0, 10, f'Head at Outer Radius : {h0} m', align='L')
    pdf.cell(
        0, 10, f'Radius at which head/Drawdown calculated : {r1} m', align='R', ln=1)
    pdf.ln(10)

    pdf.set_font('Arial', 'B', 13)
    pdf.cell(0, 10, 'Data Table', ln=1)

    pdf.set_font('Arial', '', 12)
    output_df_to_pdf(pdf, df)
    pdf.ln(10)

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f'Head : {h1} m', ln=1)
    pdf.cell(0, 10, f'Drawdown : {h0 - h1} m', ln=1)
    pdf.cell(0, 10, f'Radius of influence : {r0} m', ln=1)
    pdf.ln(5)

    pdf.set_font('Arial', 'B', 13)
    pdf.cell(0, 10, "Graphical Interpretation", ln=1)
    pdf.image('fig.png', w=200, h=200)
    pdf.ln(5)
    pdf.dashed_line(10, int(pdf.get_y()), 210 - 10,
                    int(pdf.get_y()), dash_length=1, space_length=1)

    filename = "Dupuit-Forchheimer_Report_" + \
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
