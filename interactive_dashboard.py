import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import base64

# --- Custom CSS for styling ---
st.markdown("""
<style>
    /* Makes the selectbox label white for readability on the dark background */
    div.stSelectbox > label {
        color: #FFFFFF !important;
    }
    
    /* Makes the text inside the selectbox dark for readability on its white background */
    div.stSelectbox div[data-baseweb="select"] > div:first-child {
        color: #154D71 !important;
    }

    /* Style for the main content containers (the "cards") */
    .st-emotion-cache-1w723zb {
        background-color: #2C85BE; 
        border-radius: 10px; 
        padding: 20px; 
        margin-top: 60px; 
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2); 
    }
    
    /* Override Streamlit's default container padding for a consistent look */
    .st-emotion-cache-1gsv8b2 {
        padding-top: 0px;
        padding-bottom: 0px;
    }
</style>
""", unsafe_allow_html=True)

# --- Load your cleaned dataframe ---
try:
    df = pd.read_csv('cleaned_customer_data.csv')
except FileNotFoundError:
    st.error("Error: 'cleaned_customer_data.csv' not found. Please make sure the file is in the same directory.")
    st.stop()

# --- Main title of the dashboard ---
st.title("Customer Income and Satisfaction Analysis")

# --- Create the selection box centered in the page ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    option = st.selectbox(
        "Choose a section to explore:",
        ("Project Overview", "Age & Income Analysis", "Income & Demographics", "Final Conclusions")
    )

# --- Display content based on the selected option ---
if option == "Project Overview":
    with st.container():
        st.header("Project Overview")
        st.markdown("""
        This exploratory data analysis project is focused on understanding customer demographics, income, and satisfaction from a dataset of Indian customers.
        
        Our goal is to identify key relationships and patterns that can inform business decisions.
        """)
        try:
            st.image("dashboard_image.jpg", caption="Sample Customer Data", use_container_width=True)
        except:
            st.image("https://images.unsplash.com/photo-1551288049-6291b5c8aa6c?q=80&w=1770&auto=format&fit=crop", caption="Sample Customer Data", use_container_width=True)

elif option == "Age & Income Analysis":
    with st.container():
        st.header("Analysis of Age and Income")
        st.markdown("""
        Here we analyze the relationship between the customer's age and their monthly income.
        The findings reveal a positive correlation, suggesting that as age increases, income also tends to increase.
        """)
        st.subheader("Correlation Heatmap")
        
        corr_matrix = df[['Age', 'Monthly Income']].corr()
        fig_corr = px.imshow(corr_matrix, text_auto=True, color_continuous_scale='RdBu_r', 
                            labels=dict(x="Variable", y="Variable", color="Correlation"),
                            title="Correlation Matrix")
        fig_corr.update_layout(plot_bgcolor='white', font_color='black')
        st.plotly_chart(fig_corr, use_container_width=True)

elif option == "Income & Demographics":
    with st.container():
        st.header("Income by Occupation, Gender, and Marital Status")
        st.markdown("""
        This section presents a breakdown of average monthly income across various demographic categories to identify key customer segments.
        """)
        
        sub_option = st.selectbox(
            "Select a question:",
            ("Average Monthly Income by Occupation", "Average Monthly Income by Gender", "Average Monthly Income by Marital Status", "Average Family Size by Marital Status")
        )

        custom_colors = ['#ADD8E6', '#66CDAA', '#1A5A90', '#00809D']

        if sub_option == "Average Monthly Income by Occupation":
            st.subheader("Average Monthly Income by Occupation")
            income_by_occupation = df.groupby('Occupation')['Monthly Income'].mean().round(1).reset_index()
            max_y = income_by_occupation['Monthly Income'].max()
            fig_occup = px.bar(income_by_occupation, x='Occupation', y='Monthly Income',
                               title='Average Monthly Income by Occupation',
                               labels={'Monthly Income': 'Average Monthly Income (Rs.)'},
                               color='Occupation',
                               text='Monthly Income',
                               color_discrete_sequence=custom_colors)
            fig_occup.update_traces(texttemplate='%{text}', textposition='outside', textfont_color='black')
            fig_occup.update_layout(yaxis_range=[0, max_y * 1.1], plot_bgcolor='white', font_color='black')
            fig_occup.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.2)', griddash='dot')
            st.plotly_chart(fig_occup, use_container_width=True)

        elif sub_option == "Average Monthly Income by Gender":
            st.subheader("Average Monthly Income by Gender")
            avg_income_gender = df.groupby('Gender')['Monthly Income'].mean().round(1).reset_index()
            max_y = avg_income_gender['Monthly Income'].max()
            fig_gender_income = px.bar(avg_income_gender, x='Gender', y='Monthly Income',
                                       title='Average Monthly Income by Gender',
                                       labels={'Monthly Income': 'Average Monthly Income (Rs.)'},
                                       color='Gender',
                                       text='Monthly Income',
                                       color_discrete_sequence=custom_colors)
            fig_gender_income.update_traces(texttemplate='%{text}', textposition='outside', textfont_color='black')
            fig_gender_income.update_layout(yaxis_range=[0, max_y * 1.1], plot_bgcolor='white', font_color='black')
            fig_gender_income.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.2)', griddash='dot')
            st.plotly_chart(fig_gender_income, use_container_width=True)

        elif sub_option == "Average Monthly Income by Marital Status":
            st.subheader("Average Monthly Income by Marital Status")
            avg_income_marital = df.groupby('Marital Status')['Monthly Income'].mean().round(1).reset_index()
            max_y = avg_income_marital['Monthly Income'].max()
            fig_marital_income = px.bar(avg_income_marital, x='Marital Status', y='Monthly Income',
                                        title='Average Monthly Income by Marital Status',
                                        labels={'Monthly Income': 'Average Monthly Income (Rs.)'},
                                        color='Marital Status',
                                        text='Monthly Income',
                                        color_discrete_sequence=custom_colors)
            fig_marital_income.update_traces(texttemplate='%{text}', textposition='outside', textfont_color='black')
            fig_marital_income.update_layout(yaxis_range=[0, max_y * 1.1], plot_bgcolor='white', font_color='black')
            fig_marital_income.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.2)', griddash='dot')
            st.plotly_chart(fig_marital_income, use_container_width=True)
        
        elif sub_option == "Average Family Size by Marital Status":
            st.subheader("Average Family Size by Marital Status")
            family_size_by_marital_status = df.groupby('Marital Status')['Family size'].mean().round(1).reset_index()
            max_y = family_size_by_marital_status['Family size'].max()
            fig_family = px.bar(family_size_by_marital_status, x='Marital Status', y='Family size',
                                title='Average Family Size by Marital Status',
                                labels={'Family size': 'Average Family Size'},
                                color='Marital Status',
                                text='Family size',
                                color_discrete_sequence=custom_colors)
            fig_family.update_traces(texttemplate='%{text}', textposition='outside', textfont_color='black')
            fig_family.update_layout(yaxis_range=[0, max_y * 1.1], plot_bgcolor='white', font_color='black')
            fig_family.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.2)', griddash='dot')
            st.plotly_chart(fig_family, use_container_width=True)

elif option == "Final Conclusions":
    with st.container():
        st.header("Key Findings & Business Recommendations")
        st.markdown("""
        ### Key Findings
        * **Correlation between Age and Income**: The data shows a strong positive correlation between age and monthly income. As customers get older, their income tends to increase.
        * **Feedback Behavior**: Counter to expectations, customers with higher monthly incomes tend to provide more negative feedback, while those with lower incomes give positive feedback. This suggests that the expectations of high-income customers are not being met.
        * **Demographic Groups**: The largest and most representative customer group in our dataset is **""" + str(df['Occupation'].mode()[0]) + """.** This segment should be a primary focus for business strategies.

        ### Business Recommendations
        1. **Improve Experience for High-Income Customers**: It is crucial to investigate the reasons for their dissatisfaction. This may include improving product quality, customer service, or personalization options to align the service with their high expectations.
        2. **Retain Low-Income Customers**: Since this group shows higher satisfaction, loyalty programs should be implemented to maintain their loyalty and turn them into brand advocates.
        3. **Targeted Marketing and Segmented Products**: Use demographic findings (occupation, marital status, and segment) to create more effective marketing campaigns and develop products or services that meet the specific needs of the most valuable customer segments.

        """)
