import streamlit as st
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import date, datetime
import images

st.set_page_config(page_title="Cooper Jacob", page_icon="🌊",
                   layout="wide", initial_sidebar_state="auto", menu_items=None)

st.title(f"*Cooper Jacob Method*")
st.markdown("""---""")

cooper_jacob_method = st.selectbox(
    'What would you like to calculate?', ('Time-Drawdown Method', 'Distance-Drawdown Method'))

st.markdown("""---""")

if(cooper_jacob_method == 'Time-Drawdown Method'):

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

    if 'cooper_jacob_time' not in st.session_state:
        st.session_state.cooper_jacob_time = list()
    if 'cooper_jacob_drawdown1' not in st.session_state:
        st.session_state.cooper_jacob_drawdown1 = list()
    if 'exception_status' not in st.session_state:
        st.session_state.exception_status= False

    def form_callback(t, s):
        st.session_state.cooper_jacob_time.append(t)
        st.session_state.cooper_jacob_drawdown1.append(s)

    def delete():
      try:
        del st.session_state.cooper_jacob_time[del_index]
        del st.session_state.cooper_jacob_drawdown1[del_index]
      except:
        st.session_state.exception_status=True

    st.markdown("""---""")

    input_method = st.radio('Choose a method for input of data',
                            ('Upload File', 'Fill Form'), horizontal=True)

    if(input_method == 'Fill Form'):

        col1, col2 = st.columns(2)

        with col1:
            st.write('Add Reading')
            time_data = st.number_input(
                'Time (mins)', min_value=0.0, format="%.2f")
            drawdown_data = st.number_input(
                'Drawdown (m)', min_value=0.0, format="%.2f")
            submit = st.button(label='Enter data', on_click=form_callback, args=(
                time_data, drawdown_data))

        with col2:
            st.write('Delete Reading')
            del_index = st.number_input(
                label='Index', min_value=0, help='Index of reading to be deleted')
            del_button = st.button(label='Delete', on_click=delete)
            if st.session_state.exception_status==True:
              st.warning('Incorrect Index Entered')
              st.session_state.exception_status=False

        if 'cooper_jacob_time' in st.session_state:
            df = pd.DataFrame({'Time': st.session_state.cooper_jacob_time,
                               'Drawdown': st.session_state.cooper_jacob_drawdown1})
            st.table(df)

    if(input_method == 'Upload File'):

        uploaded_file = st.file_uploader("Choose a file")
        st.warning(
            'Please keep the data in two columns as Time (mins) and Drawdown (m) resepectively')
        if(uploaded_file):
            df = pd.read_csv(uploaded_file)
            st.table(df)

    if "cooper_jacob_time_drawdown_calculated_button_clicked" not in st.session_state:
        st.session_state.cooper_jacob_time_drawdown_calculated_button_clicked = False

    def callback():
        st.session_state.cooper_jacob_time_drawdown_calculated_button_clicked = True

    calculate_time_drawdown = st.button(label='Calculate', on_click=callback)
    st.markdown("""---""")

    if calculate_time_drawdown or st.session_state.cooper_jacob_time_drawdown_calculated_button_clicked:

        x_data = list(df['Time'])
        y_data = list(df['Drawdown'])
        slope, y_intercept = np.polyfit(np.log(x_data), y_data, 1)
        fig, ax = plt.subplots()
        ax.semilogx(x_data, y_data, marker='.',
                    color='black', label='Actual Data')
        ax.semilogx(np.exp((y_data - y_intercept)/slope),
                    y_data, 'r--', label='Fitting Line')
        plt.xlabel('log Time')
        plt.ylabel('Drawdown')
        plt.title('Time vs Drawdown')
        plt.grid(True)

        delta_s = abs((slope*math.log(100) + y_intercept) -
                      (slope*math.log(10) + y_intercept))
        t_0 = np.exp((-y_intercept)/slope)

        T = (2.303*Q)/(4*math.pi*delta_s)
        S = (2.25*T*(t_0/1440)) / (r*r)

        st.info('Transmissivity = {} (m2/day)'.format(T))
        st.info('Storativity = {}'.format(S))
        st.markdown("""---""")

        def calculate_drawdown(Q, T, t, S, r):
            return ((2.303*Q)/(4*math.pi*T))*(math.log10((2.25*T*t)/(S*r*r)))

        def calculate_u(r, S, T, t):
            return (r*r*S)/(4*T*t)

        def mse(actual, predicted):
            actual = np.array(actual)
            predicted = np.array(predicted)
            differences = np.subtract(actual, predicted)
            squared_differences = np.square(differences)
            return squared_differences.mean()

        calculate_drawdown_list = list()
        # linefit_drawdown_list = list()
        u_list = list()
        error_list = list()
        for index, row in df.iterrows():
            drawdown = row['Drawdown']
            time = row['Time']/1440
            calculated_drawdown = calculate_drawdown(Q, T, time, S, r)
            calculate_drawdown_list.append(calculated_drawdown)
            # linefit_drawdown_list.append((slope*math.log(time*1440))+y_intercept)
            u = calculate_u(r, S, T, time)
            u_list.append(u)
            error = (drawdown-calculated_drawdown)/drawdown
            error_list.append(error)

        df['Calculated_Drawdown'] = calculate_drawdown_list
        # df['Linefit Drawdown'] = linefit_drawdown_list
        df['u'] = u_list
        df['Error'] = error_list

        def highlight_rows(row):
            value = row.loc['u']
            if value > 0.05:
                color = 'red'
            else:
                color = ''
            return ['background-color: {}'.format(color) for r in row]

        mse_error = mse(df['Drawdown'], df['Calculated_Drawdown'])
        st.success(f'Mean Fitting Error = {mse_error*100}%')
        st.warning(
            'The rows highlighted red have been excluded from analysis since u > 0.05')
        st.table(df.style.apply(highlight_rows, axis=1).format(
            {'Error': '{:,.6%}'.format}))
        st.download_button(label="Download CSV", data=df.to_csv().encode(
            'utf-8'), file_name='Cooper_Jacob'+datetime.now().strftime("/%d/%m/%Y,%H:%M:%S")+'.csv')
        st.markdown("""---""")

        t_for_u = (r*r * S)/(4*T*0.05)*1440
        ax.axvline(x=t_for_u, color='blue', ls=':', label='u = 0.05')
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
        pdf.cell(0, 10, 'Cooper Jacob Test Report', align='C', ln=1)
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
            0, 10, f'Radial Distance (r) : {round(r,5)} m', align='R', ln=1)
        pdf.ln(5)

        pdf.set_font('Arial', 'B', 13)
        pdf.cell(0, 10, 'Data Table', ln=1)

        pdf.set_font('Arial', '', 12)
        output_df_to_pdf(pdf, df)
        pdf.ln(5)

        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, f'Transmissivity : {round(T, 5)} m2/day', ln=1)
        pdf.cell(0, 10, f'Storativity : {round(S, 5)}', ln=1)
        pdf.cell(
            0, 10, f'Mean Fitting Error = {round(mse_error * 100, 5)}%', ln=1)
        pdf.ln(4)

        pdf.set_font('Arial', 'B', 13)
        pdf.cell(0, 10, "Graphical Interpretation", ln=1)
        pdf.image('fig.png', w=200, h=200)
        pdf.ln(5)
        pdf.dashed_line(10, int(pdf.get_y()), 210 - 10,
                        int(pdf.get_y()), dash_length=1, space_length=1)

        filename = "Cooper_Jacob_Test_Report_" + \
            datetime.now().strftime("/%d/%m/%Y,%H:%M:%S")+".pdf"
        st.download_button("Download Report", data=pdf.output(
            dest='S').encode('latin-1'), file_name=filename)

        st.markdown("""---""")

if(cooper_jacob_method == 'Distance-Drawdown Method'):

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

    Q = st.number_input("Pumping rate (m3/day)")
    t = st.number_input("Time elapsed since pumping (mins)")
    t = t/1440

    if 'cooper_jacob_distance' not in st.session_state:
        st.session_state.cooper_jacob_distance = list()
    if 'cooper_jacob_drawdown2' not in st.session_state:
        st.session_state.cooper_jacob_drawdown2 = list()

    def form_callback(d, s):
        st.session_state.cooper_jacob_distance.append(d)
        st.session_state.cooper_jacob_drawdown2.append(s)

    def delete():
        del st.session_state.cooper_jacob_distance[del_index]
        del st.session_state.cooper_jacob_drawdown2[del_index]

    st.markdown("""---""")

    input_method = st.radio('Choose a method for input of data',
                            ('Upload File', 'Fill Form'), horizontal=True)

    if(input_method == 'Fill Form'):

        col1, col2 = st.columns(2)

        with col1:
            st.write('Add Reading')
            distance_data = st.number_input(
                'Distance (m)', min_value=0.0, format="%.2f")
            drawdown_data = st.number_input(
                'Drawdown (m)', min_value=0.0, format="%.2f")
            submit = st.button(label='Enter data', on_click=form_callback, args=(
                distance_data, drawdown_data))

        with col2:
            st.write('Delete Reading')
            del_index = st.number_input(
                label='Index', min_value=0, help='Index of reading to be deleted')
            del_button = st.button(label='Delete', on_click=delete)

        if 'cooper_jacob_distance' in st.session_state:
            df = pd.DataFrame({'Distance': st.session_state.cooper_jacob_distance,
                               'Drawdown': st.session_state.cooper_jacob_drawdown2})
            st.table(df)

    if(input_method == 'Upload File'):

        uploaded_file = st.file_uploader("Choose a file")
        st.warning(
            'Please keep the data in two columns as Distance (m) and Drawdown (m) resepectively')
        if(uploaded_file):
            df = pd.read_csv(uploaded_file)
            st.table(df)

    if "cooper_jacob_distance_drawdown_calculated_button_clicked" not in st.session_state:
        st.session_state.cooper_jacob_distance_drawdown_calculated_button_clicked = False

    def callback():
        st.session_state.cooper_jacob_distance_drawdown_calculated_button_clicked = True

    calculate_distance_drawdown = st.button(
        label='Calculate', on_click=callback)
    st.markdown("""---""")

    if calculate_distance_drawdown or st.session_state.cooper_jacob_distance_drawdown_calculated_button_clicked:

        x_data = list(df['Distance'])
        y_data = list(df['Drawdown'])
        slope, y_intercept = np.polyfit(np.log(x_data), y_data, 1)
        fig, ax = plt.subplots()
        ax.semilogx(x_data, y_data, marker='.',
                    color='black', label='Actual Data')
        ax.semilogx(np.exp((y_data - y_intercept)/slope),
                    y_data, 'r--', label='Fitting Line')
        plt.xlabel('log Distance')
        plt.ylabel('Drawdown')
        plt.title('Distance vs Drawdown')
        plt.grid(True)

        delta_s = abs((slope*math.log(100) + y_intercept) -
                      (slope*math.log(10) + y_intercept))
        r_0 = np.exp((-y_intercept)/slope)

        T = (2.303*Q)/(2*math.pi*delta_s)
        S = (2.25*T*t) / (r_0*r_0)

        st.info('Transmissivity = {} (m2/day)'.format(T))
        st.info('Storativity = {}'.format(S))
        st.markdown("""---""")

        def calculate_drawdown(Q, T, t, S, r):
            return ((2.303*Q)/(4*math.pi*T))*(math.log10((2.25*T*t)/(S*r*r)))

        def calculate_u(r, S, T, t):
            return (r*r*S)/(4*T*t)

        def mse(actual, predicted):
            actual = np.array(actual)
            predicted = np.array(predicted)
            differences = np.subtract(actual, predicted)
            squared_differences = np.square(differences)
            return squared_differences.mean()

        calculate_drawdown_list = list()
        # linefit_drawdown_list = list()
        u_list = list()
        error_list = list()
        for index, row in df.iterrows():
            drawdown = row['Drawdown']
            distance = row['Distance']
            calculated_drawdown = calculate_drawdown(Q, T, t, S, distance)
            calculate_drawdown_list.append(calculated_drawdown)
            # linefit_drawdown_list.append((slope*math.log(time*1440))+y_intercept)
            u = calculate_u(distance, S, T, t)
            u_list.append(u)
            error = (drawdown-calculated_drawdown)/drawdown
            error_list.append(error)

        df['Calculated_Drawdown'] = calculate_drawdown_list
        # df['Linefit Drawdown'] = linefit_drawdown_list
        df['u'] = u_list
        df['Error'] = error_list

        def highlight_rows(row):
            value = row.loc['u']
            if value > 0.05:
                color = 'red'
            else:
                color = ''
            return ['background-color: {}'.format(color) for r in row]

        mse_error = mse(df['Drawdown'], df['Calculated_Drawdown'])
        st.success(f'Mean Fitting Error = {mse_error*100}%')
        st.warning(
            'The rows highlighted red have been excluded from analysis since u > 0.05')
        st.table(df.style.apply(highlight_rows, axis=1).format(
            {'Error': '{:,.6%}'.format}))
        st.download_button(label="Download CSV", data=df.to_csv().encode(
            'utf-8'), file_name='Cooper_Jacob'+datetime.now().strftime("/%d/%m/%Y,%H:%M:%S")+'.csv')
        st.markdown("""---""")

        t_for_u = (r_0*r_0 * S)/(4*T*0.05)*1440
        ax.axvline(x=t_for_u, color='blue', ls=':', label='u = 0.05')
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
        pdf.cell(0, 10, 'Cooper Jacob Test Report', align='C', ln=1)
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
            0, 10, f'Time of pumping (t) : {round((t*1440),5)} mins', align='R', ln=1)
        pdf.ln(5)

        pdf.set_font('Arial', 'B', 13)
        pdf.cell(0, 10, 'Data Table', ln=1)

        pdf.set_font('Arial', '', 12)
        output_df_to_pdf(pdf, df)
        pdf.ln(5)

        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, f'Transmissivity : {round(T, 5)} m2/day', ln=1)
        pdf.cell(0, 10, f'Storativity : {round(S, 5)}', ln=1)
        pdf.cell(
            0, 10, f'Mean Fitting Error = {round(mse_error * 100, 5)}%', ln=1)
        pdf.ln(4)

        pdf.set_font('Arial', 'B', 13)
        pdf.cell(0, 10, "Graphical Interpretation", ln=1)
        pdf.image('fig.png', w=200, h=200)
        pdf.ln(5)
        pdf.dashed_line(10, int(pdf.get_y()), 210 - 10,
                        int(pdf.get_y()), dash_length=1, space_length=1)

        filename = "Cooper_Jacob_Test_Report_" + \
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
