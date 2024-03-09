import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt

df = pd.read_csv("Startup_Cleaned.csv")
st.set_page_config(layout='wide', page_title='Startup Analysis')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_investor_details(investor):
    st.title(investor)
    st.subheader('Most Recent Investments')
    last5_df = df[df['investors'].str.contains(investor, na=False)].head(5)[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.dataframe(last5_df)
    st.subheader('Maximum Investment')
    last5_dff = df[df['investors'].str.contains(investor, na=False)].groupby('startup')['amount'].sum().sort_values(ascending=False).head(1)
    st.dataframe(last5_dff)

    col1, col2, col3 = st.columns(3)
    with col1:
        big_series = df[df['investors'].str.contains(investor, na=False)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)

    with col2:
        vertical_ser = df[df['investors'].str.contains(investor, na=False)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_ser, labels=vertical_ser.index, autopct="0.01f%%")
        st.pyplot(fig1)

    with col3:
        new_city = df[df['investors'].str.contains(investor, na=False)].groupby('city')['amount'].sum()
        st.subheader('City')
        fig2, ax2 = plt.subplots()
        ax2.pie(new_city, labels=new_city.index)
        st.pyplot(fig2)

    sub1 = df[df['investors'].str.contains(investor, na=False)].groupby('subvertical')['amount'].sum()
    col1.subheader('Subvertical Data')
    fig3, ax3 = plt.subplots()
    ax3.bar(sub1.index, sub1.values)
    col1.pyplot(fig3)

    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    sub2 = df[df['investors'].str.contains(investor, na=False)].groupby('year')['amount'].sum()
    col2.subheader('Yearly Investment')
    fig2, ax2 = plt.subplots()
    ax2.plot(sub2.index, sub2.values)
    col2.pyplot(fig2)


def load_startup_details(startup_name):
    st.title(startup_name + " - Company POV")

    # Fetch startup details from the dataframe
    startup_details = df[df['startup'] == startup_name].iloc[0]

    # Display basic details
    st.subheader("Basic Information")
    st.write(f"Name: {startup_details['startup']}")
    st.write(f"Investor: {startup_details['investors']}")
    st.write(f"Industry: {startup_details['vertical']}")
    st.write(f"Subindustry: {startup_details['subvertical']}")
    st.write(f"Location: {startup_details['city']}")

    # Display funding rounds
    st.subheader("Funding Rounds")
    funding_rounds = df[df['startup'] == startup_name][['date', 'round', 'investors', 'amount']]
    st.dataframe(funding_rounds)

def overall():
    st.title("Overall Analysis")

    # Modified MoM graph or Add New Graph
    st.header("Total Funding Over Time")

    total_funding_over_time = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    st.subheader('Total Funding Over Time')
    fig_time, ax_time = plt.subplots()
    ax_time.plot(total_funding_over_time['year'].astype(str) + '-' + total_funding_over_time['month'].astype(str), total_funding_over_time['amount'])
    st.pyplot(fig_time)

    # Top Cities
    col1, col2, col3 = st.columns(3)
    top_cities = df.groupby('city').size().nlargest(5)
    with col1:
        st.subheader('Top Cities')
        fig_city, ax_city = plt.subplots()
        ax_city.bar(top_cities.index, top_cities.values)
        st.pyplot(fig_city)

    # ... (existing code)


    # Top Investors
    top_investors = df.groupby('investors')['amount'].sum().nlargest(5)
    st.subheader('Top Investors')
    fig9, ax9 = plt.subplots()
    ax9.bar(top_investors.index, top_investors.values)
    st.pyplot(fig9)

st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])

if option == 'Overall Analysis':
    overall()

    total=round(df['amount'].sum())

    max_f=df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]

    avg_f=df.groupby('startup')['amount'].sum().mean()

    num_start=df['startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric('Total',str(total) + 'Cr')

    with col2:
        st.metric('Max',str(max_f) + 'Cr')

    with col3:
        st.metric('Average',str(avg_f) +'Cr')

    with col4:
        st.metric('Funded Startups',str(num_start) + 'Cr')

elif option == 'Startup':
    st.title("Startup Analysis")
    selected_startup = st.sidebar.selectbox('Select One', df['startup'].unique().tolist())
    btn1 = st.sidebar.button('Find Startup Details')
    if btn1:
        load_startup_details(selected_startup)

else:
    st.title('Investor')
    selected_investor = st.sidebar.selectbox('Select One', sorted(set(df['investors'].astype(str).str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investors Details')
    if btn2:
        load_investor_details(selected_investor)
