import streamlit as st
import images

st.set_page_config(page_title="AquaProbe", page_icon="🌊",
                   layout="wide", initial_sidebar_state="auto", menu_items=None)

st.title(f"*AquaProbe*")
st.markdown("""---""")

with st.expander("Index", expanded=True):
    st.markdown('''1. [Aquifer](#aquifer)
2. [Aquifer Properties](#aquifer_properties)
3. [Cone of Depression](#cone_of_depression)
4. [Pumping Tests](#pumping_tests)''')

st.markdown("""---""")

st.subheader("Aquifer", anchor = "aquifer")
aquifer = 'An aquifer may be broadly described as saturated fractured rock or sand from which usable volumes of groundwater can be pumped.'
st.write(aquifer)

st.markdown("**1. Confined Aquifer**")
c_aquifer = '- A confined aquifer is a section of rock or sand that is overlain by a confining layer (e.g. clay aquitard on top) \
    that restricts movement of water into another aquifer.  \n' ' - Groundwater in confined aquifers can be under high pressure because of the confining layer on top of the aquifer.'
st.write(c_aquifer)


st.markdown("**1. Unconfined Aquifer**")
uc_aquifer = ' - An unconfined aquifer is a section of rock or sand that does not have a \
        confining layer (e.g. clay aquitard) on top of it.  \n' ' - The top of an unconfined aquifer is the watertable.  \n' \
        ' - An unconfined aquifer acts similar to a sponge, in that the watertable surface can fluctuate up and down depending on \
        the recharge and discharge rate.  \n  \n'
st.write(uc_aquifer)

col1, col2, col3 = st.columns([1.5,6,1])

with col1:
    st.write("")

with col2:
    st.image('images/aquifer.png',caption = "Aquifers", width=500)

with col3:
    st.write("")

st.markdown("""---""")

st.subheader("Aquifer Properties", anchor = "aquifer_properties")

st.markdown("**1. Hydraulic Head (h)**")
head = 'The hydraulic head, or total head, is a measure of the potential of the\
    water fluid at the measurement point. Hydraulic head is the height to which water will rise in a bore. It is the\
    resting groundwater level.  \n' '**Measured in m.**  \n'
st.write(head)

st.markdown("**2. Hydraulic Gradient (i)**")
head_loss = 'Hydraulic head loss per distance, 𝑖 = dℎ/d𝑙. [dimensionless]'
st.write(head_loss)

st.markdown("**3. Aquifer Thickness (b)**")
b = 'Saturated thickness of an aquifer.'
st.write(b)

st.markdown("**4. Drawdown**")
drawdown = 'Change in water level due to an external stress such as pumping. [m]'
st.write(drawdown)

st.markdown("**5. Transmissivity (T)**") 
head = 'The hydraulic head, or total head, is a measure of the potential of the\
    water fluid at the measurement point. Hydraulic head is the height to which water will rise in a bore. It is the\
    resting groundwater level.  \n' 'The product of hydraulic conductivity and saturated thickness,  \n \
        **𝑇 = 𝐾𝑏 [m2/day].**  \n'
st.write(head)

st.markdown("**6. Hydraulic Conductivity (K)**") 
k = 'Hydraulic Conductivity is the ease with which water can move through an aquifer.  \n\
    Hydraulic Conductivity can be determined by dividing the transmissivity of \
        the aquifer by the aquifer thickness.  \n' '**𝐾 = 𝑇/𝑏 [m/day]**'
st.write(k)

st.markdown("**7. Specific Storage (Ss)**")
ss = 'Specific Storage is Volume of water released from storage from a unit volume of aquifer per unit decline in hydraulic head. [1/m3]'
st.write(ss)

st.markdown("**8. Specific Yield (Sy)**")
sy = 'Volume of water released from storage by an unconfined aquifer per unit surface area of aquifer per unit decline of the water table. [dimensionless]'
st.write(sy)

st.markdown("**9. Storativity (S)**")
s = 'Storativity is the volume of water removed from a unit area of an aquifer for a unit drop in hydraulic head.  \n'\
    '- In Confined aquifers: it is equal to the specific storage times the thickness of the aquifer  \n'\
        '**𝑆 = 𝑆s𝑏 [dimensionless]**  \n' \
    '- In Unconfined aquifers: it is equal to the specific storage times the thickness of the aquifer plus the specific yield  \n'\
        '**𝑆 = 𝑆s𝑏 + 𝑆y [dimensionless]**'
st.write(s)

st.markdown("**10. Recharge Rate (R)**")
rr = 'Rate at which  groundwater is replenished by water \
    entering the groundwater system.  \n' '**R = Q/A [m/day]**'
st.write(rr)

st.markdown("**11. Discharge Rate**")
dr = 'Rate at which groundwater leaves the aquifer.'
st.write(dr)

st.markdown("**12. Radius of Influence (r0)**")
r0 = 'Maximum distance from the well over which recharge rates become equal to discharge rates, \
    i.e. the water flowing in becomes equal to the water flowing out.  \n' '**r0 = √(A/π) [m]**'
st.write(r0)

st.markdown("""---""")

st.subheader("Cone of Depression", anchor = "cone_of_depression")
cone = '- Groundwater pumping creates a cone of depression (drawdown) of the\
    watertable or potentiometric surface surrounding the pumped bore.  \n'\
    '- The distance the drawdown cone extends depends primarily on the nature\
    of the aquifer, the pumping rate and the pumping period.  \n'\
    ' - Deep and Narrow cones: Low Transmissivity \n'\
    ' - Shallow and Wide cones: High Transmissivity'
st.write(cone)

col1, col2, col3 = st.columns([1.5,6,1])

with col1:
    st.write("")

with col2:
    st.image('images/cone.png', caption = "Cone of Depression", width=500)

with col3:
    st.write("")

st.markdown("""---""")

st.subheader("Pumping Tests", anchor = "pumping_tests")
st.write("A pumping test is a field experiment in which a well is pumped at a controlled rate and water-level response (drawdown)\
    is measured in one or more surrounding observation wells and optionally in the pumped well (control well) itself.  \n\
    Response data from pumping tests are used to estimate the hydraulic properties of aquifers, evaluate well performance and identify aquifer boundaries.")

theis, cooper, thiem, dupuit, theis_recovery = st.tabs(["Theis", "Cooper Jacob", "Thiem", "Dupuit Forchheimer", "Theis Recovery"])

with theis:
    st.write("The Theis (1935) solution is useful for determining the transmissivity of **nonleaky confined aquifers** from pumping tests.")
    st.write("C.V. Theis first published in 1935 'The Relation Between the Lowering of the Piezometric surface and the \
        Rate and Duration of Discharge of a Well Using Groundwater Storage'.  \nHe developed an analytic solution for the drawdown for a non-steady flow in a confined aquifer.  \n\
        Theis found the non-steady flow of groundwater to be analagous to the unsteady flow of heat in a homogeneous solid.")

    link = '[Link to the Theis (1935) paper](https://water.usgs.gov/ogw/pubs/Theis-1935.pdf)'
    st.markdown(link, unsafe_allow_html=True)

    st.markdown("**Assumptions:**")
    st.markdown("1. Aquifer has infinite areal extent\
        \n2. Aquifer is homogeneous, isotropic and of uniform thickness\
        \n3. Control well is fully penetrating \
        \n4. Flow to control well is horizontal\
        \n5. Aquifer is nonleaky confined\
        \n6. Flow is unsteady\
        \n7. Water is released instantaneously from storage with decline of hydraulic head\
        \n8. Diameter of pumping well is very small so that storage in the well can be neglected")

    st.markdown("**Equations:**")

    st.write("The Theis equation for flow to a fully penetrating line sink discharging at a constant rate in a homogeneous, isotropic and nonleaky confined aquifer of infinite extent is as follows:")
    st.image('images/theis4.png')
    st.image('images/theis2.png')
    st.write("The integral in equation (1) is commonly referred to as the Theis well function, abbreviated as w(𝑢). Hence, the equation becomes: ")
    st.image('images/theis1.png')
    st.image('images/theis3.png')
    st.write("where,\
        \n - 𝑄 is pumping rate [m3/day]\
        \n - 𝑟 is radial distance from pumping well to observation well [m]\
        \n - 𝑠 is drawdown [m]\
        \n - 𝑆 is storativity [dimensionless]\
        \n - 𝑡 is elapsed time since start of pumping\
        \n - 𝑇 is transmissivity [m²/day]\
        \n - w(𝑢) is the Theis well function for nonleaky confined aquifers [dimensionless]")

    st.markdown("**Data Requirements:**")
    st.write("- 𝑄, pumping rate [m3/day]\
            \n- distance from well [m]\
            \n- observation well measurements (time and displacement)")
    
    st.markdown("**Estimated Parameters:**")
    st.write("- S, Storativity\
            \n- T, Transmissivity [m²/day]\
            \n- RMS Residual")

with cooper:
    st.write("The Cooper and Jacob (1946) solution (sometimes called Jacob's modified nonequilibrium method) is a late-time approximation derived from the Theis type-curve method.")
    st.write("Hilton Hammond Cooper (1913-1990) and Charles Edward Jacob (1914-1970), \
        ground­water hydrologists with the U.S. Geological Survey,\
        devised a widely used graphical technique for the determination of hydraulic properties (transmissivity and storativity) of **nonleaky confined aquifers**.")

    link = '[Link to the Cooper Jacob (1946) paper](https://www.nrc.gov/docs/ML1429/ML14290A600.pdf)'
    st.markdown(link, unsafe_allow_html=True)

    st.markdown("**Assumptions:**")
    st.markdown("1. Aquifer has infinite areal extent\
        \n2. Aquifer is homogeneous, isotropic and of uniform thickness\
        \n3. Control well is fully penetrating \
        \n4. Flow to control well is horizontal\
        \n5. Aquifer is nonleaky confined\
        \n6. Flow is unsteady\
        \n7. Water is released instantaneously from storage with decline of hydraulic head\
        \n8. Diameter of pumping well is very small so that storage in the well can be neglected\
        \n9. values of 𝑢 are small (i.e., 𝑟 is small and 𝑡 is large)")

    st.markdown("**Equations:**")

    st.write("Cooper and Jacob (1946) derived a modified form of the Theis (1935) solution\
        for transient flow to a well discharging at a constant rate from an homogeneous and isotropic nonleaky confined aquifer\
        of infinite extent and uniform thickness. The Theis equation for drawdown is given in compact notation as follows:")
    st.image('images/theis1.png')
    st.image('images/theis2.png')
    st.write("where,\
        \n - 𝑄 is pumping rate [m3/day]\
        \n - 𝑟 is radial distance from pumping well to observation well [m]\
        \n - 𝑠 is drawdown [m]\
        \n - 𝑆 is storativity [dimensionless]\
        \n - 𝑡 is elapsed time since start of pumping\
        \n - 𝑇 is transmissivity [m²/day]\
        \n - w(𝑢) is the Theis well function for nonleaky confined aquifers [dimensionless]")
    st.write("The Theis well function, w(𝑢), in (1) may be evaluated using the following infinite series expression: ")
    st.image('images/theis3.png')
    st.write("where 𝑢 is given in (2). For small values of 𝑢 (i.e., large values of 𝑡 and small values of 𝑟), Cooper and Jacob found that the Theis well function may be approximated using only the first two terms in (3): ")
    st.image('images/cj1.png')
    st.write("The critical value of 𝑢 required to achieve reasonable accuracy with the Cooper and Jacob approximation is alternately given as 𝑢≤0.05 (Driscoll 1986) and 𝑢≤0.01 (Kruseman and de Ridder 1994). \
        A smaller value for the critical value of 𝑢 leads to a more accurate approximation of the Theis well function.")

    st.write("The effective equation after approximation becomes: ")
    st.image('images/cj2.png')
    st.write("Transmissivity can be calculated as follows: ")
    st.image('images/cj3.png')

    st.markdown("**Data Requirements:**")
    st.write("- 𝑄, pumping rate [m3/day]\
            \n- distance from well [m]\
            \n- observation well measurements (time and displacement)")
    
    st.markdown("**Estimated Parameters:**")
    st.write("- S, Storativity\
            \n- T, Transmissivity [m²/day]\
            \n- Mean fitting error")

with thiem:
    st.write("Theim is used for the determination of hydraulic properties (well discharge, radius of influence) of **nonleaky confined aquifers**.")

    link = '[Link to the Thiem paper](https://core.ac.uk/download/pdf/189480423.pdf)'
    st.markdown(link, unsafe_allow_html=True)

    st.markdown("**Assumptions:**")
    st.markdown("1. Aquifer has infinite areal extent\
        \n2. Aquifer is homogeneous, isotropic and of uniform thickness\
        \n3. Control well is fully penetrating \
        \n4. Flow to control well is horizontal\
        \n5. Aquifer is nonleaky confined\
        \n6. Flow is unsteady\
        \n7. Water is released instantaneously from storage with decline of hydraulic head\
        \n8. Coefficient of transmissivity or permeability (hydraulic conductivity) is constant at all times and at all locations.\
        \n9. Values of 𝑢 are small (i.e., 𝑟 is small and 𝑡 is large)")

    st.markdown("**Equations:**")

    st.write("In 1906 C. Theim  derived equations for steady radial flow to a fully penetrating well\
        with 100 % penetration and open hole using some assumptions.  \n\
        Its is mathematical model used for  computing constant pumping rate (Q).")
    st.image('images/thiem1.png')
    st.write("where,\
        \n - 𝑄 is pumping rate [m3/day]\
        \n - 𝑟 is radial distance from pumping well to observation well [m]\
        \n - 𝑇 is transmissivity [m²/day]\
        \n - h is the hydraulic head [m]")

    st.markdown("**Data Requirements:**")
    st.write("- T, Transmissivity [m²/day]\
            \n- r, distance from well [m]\
            \n- h, hydraulic head [m]")
    
    st.markdown("**Estimated Parameters:**")
    st.write("- 𝑄, pumping rate [m3/day]") 

with dupuit:
    st.write("The Dupuit–Forchheimer assumption holds that groundwater flows horizontally in an **unconfined aquifer** and that the groundwater discharge is proportional to the saturated aquifer thickness. It was formulated by \
        Jules Dupuit and Philipp Forchheimer in the late 1800s to simplify groundwater flow equations for analytical solutions.")

    link = '[Read more about Dupuit-Forchheimer method](https://en.wikipedia.org/wiki/Dupuit%E2%80%93Forchheimer_assumption)'
    st.markdown(link, unsafe_allow_html=True)

    st.markdown("**Assumptions:**")
    st.markdown("1. Aquifer has infinite areal extent\
        \n2. Control well is fully penetrating \
        \n3. Flow to control well is horizontal\
        \n4. Aquifer is unconfined\
        \n5. Flow is in steady state\
        \n6. The groundwater discharge is proportional to the saturated aquifer thickness.")

    st.markdown("**Equations:**")

    st.write("The Dupuit–Forchheimer  equation for groundwater flow to pumping wells in unconfined aquifers\
        under steady state can be used to calculate drawdown at specific radius.")
    st.image('images/df1.png')
    st.write("where,\
        \n - K is hydraulic conductivity [m/day]\
        \n - 𝑟 is radial distance from pumping well to observation well [m]\
        \n - h is the hydraulic head [m]")

    
    st.markdown("**Estimated Parameters:**")
    st.write("- Drawdown at given radius [m]")

    st.write("Similarly, Radius of Inflence can also be found out using: ")
    st.image('images/df2.png')
    st.write("where,\
        \nA is the recharge area required [m2]")


with theis_recovery:
    st.write("The Theis (1935) solution is useful for determining the transmissivity of **nonleaky confined aquifers from recovery tests**.  \n\
    Analysis involves matching a straight line to residual drawdown data collected after the termination of a pumping test.\
    The solution assumes a line source for the pumped well and therefore neglects wellbore storage.")

    st.markdown("**Assumptions:**")
    st.markdown("1. Aquifer has infinite areal extent\
        \n2. Aquifer is homogeneous, isotropic and of uniform thickness\
        \n3. Control well is fully penetrating \
        \n4. Flow to control well is horizontal\
        \n5. Aquifer is nonleaky confined\
        \n6. Flow is unsteady\
        \n7. Water is released instantaneously from storage with decline of hydraulic head\
        \n8. Diameter of pumping well is very small so that storage in the well can be neglected\
        \n9. values of 𝑢 are small (i.e., 𝑟 is small and 𝑡 is large)")

    st.markdown("**Equations:**")

    st.write("C.V. Theis, a groundwater hydrologist with the U.S. Geological Survey, derived the following approximate linear equation to predict\
         residual drawdown in a homogeneous, isotropic and nonleaky confined aquifer assuming a fully penetrating line sink that discharged at a constant rate prior to recovery:")
    st.image('images/rec1.png')
    st.write("where,\
        \n - 𝑄 is pumping rate [m3/day]\
        \n - 𝑠' is residual drawdown [m]\
        \n - 𝑆 is storativity during pumping [dimensionless]\
        \n - 𝑆' is storativity during recovery [dimensionless]\
        \n - 𝑡 is elapsed time since start of pumping\
        \n - 𝑡' is elapsed time since pumping stopped\
        \n - 𝑇 is transmissivity [m²/day]")

    st.write("To apply the Theis recovery method given by (1), plot 𝑠′ as a function of log(𝑡/𝑡′) on semi-logarithmic axes and draw a straight line through the data (example). \
        Determine 𝑇 using the following equation:")
    st.image('images/rec2.png')
    st.write("where,\
        \n - Δ𝑠′ is the slope of the fitted line (change in residual drawdown per log cycle equivalent time)")

    st.write("𝑆/𝑆′ is found from the intersection of the line with the log(𝑡/𝑡′) axis of the plot. In the absence of boundary effects, 𝑆/𝑆′ should be close to unity. A value of 𝑆/𝑆′>1 suggests recharge during the test; whereas 𝑆/𝑆′<1 may indicate a no-flow boundary.")

    st.markdown("**Data Requirements:**")
    st.write("- 𝑄, pumping rate [m3/day]\
            \n- distance from well [m]\
            \n- observation well measurements (time and displacement)")
    
    st.markdown("**Estimated Parameters:**")
    st.write("- T, Transmissivity\
        \n - 𝑆/𝑆′ (ratio of storativity during pumping to storativity during recovery)")

st.markdown("""---""")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)




#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# test data for thies - in theis figure out time to mins
# make sure df length >= 3
# deploy with nativefier and docker

# Future Scope
# connect data we want to store to mysql db
# user authentication

# 🌍 1️⃣ 2️⃣ 3️⃣ 4️⃣
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!