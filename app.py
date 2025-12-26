import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="COVID-19 Vaccination Coverage Analysis",
    page_icon="💉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("🌍 COVID-19 Vaccination Coverage Dashboard")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📊 Dashboard Controls")
    st.markdown("### About")
    st.info("""
    This dashboard provides comprehensive analysis of COVID-19 vaccination 
    coverage across different countries and continents.
    
    **Data Source:** Country Vaccinations Dataset
    """)
    
    # File uploader
    uploaded_file = st.file_uploader("Upload your vaccination data (CSV)", type=['csv'])
    
    st.markdown("---")
    st.markdown("### Filters")

# Load data function
@st.cache_data
def load_data(file=None):
    """Load and preprocess the vaccination data"""
    if file is not None:
        df = pd.read_csv(file)
    else:
        # For demo purposes - you should have the actual file
        st.warning("⚠️ Please upload 'country_vaccinations.csv' file to proceed.")
        st.stop()
    
    # Data preprocessing
    df = df.dropna(subset=['total_vaccinations_per_hundred'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(['country', 'date'])
    
    # Create continent mapping (expanded version)
    continent_dict = {
        'Afghanistan': 'Asia', 'Albania': 'Europe', 'Algeria': 'Africa',
        'Andorra': 'Europe', 'Angola': 'Africa', 'Argentina': 'South America',
        'Armenia': 'Asia', 'Australia': 'Oceania', 'Austria': 'Europe',
        'Azerbaijan': 'Asia', 'Bahrain': 'Asia', 'Bangladesh': 'Asia',
        'Barbados': 'North America', 'Belarus': 'Europe', 'Belgium': 'Europe',
        'Belize': 'North America', 'Benin': 'Africa', 'Bhutan': 'Asia',
        'Bolivia': 'South America', 'Bosnia and Herzegovina': 'Europe',
        'Botswana': 'Africa', 'Brazil': 'South America', 'Brunei': 'Asia',
        'Bulgaria': 'Europe', 'Burkina Faso': 'Africa', 'Cambodia': 'Asia',
        'Cameroon': 'Africa', 'Canada': 'North America', 'Cape Verde': 'Africa',
        'Chad': 'Africa', 'Chile': 'South America', 'China': 'Asia',
        'Colombia': 'South America', 'Costa Rica': 'North America',
        'Croatia': 'Europe', 'Cuba': 'North America', 'Cyprus': 'Europe',
        'Czechia': 'Europe', 'Denmark': 'Europe', 'Dominica': 'North America',
        'Dominican Republic': 'North America', 'Ecuador': 'South America',
        'Egypt': 'Africa', 'El Salvador': 'North America', 'England': 'Europe',
        'Estonia': 'Europe', 'Ethiopia': 'Africa', 'Finland': 'Europe',
        'France': 'Europe', 'Gabon': 'Africa', 'Georgia': 'Asia',
        'Germany': 'Europe', 'Ghana': 'Africa', 'Greece': 'Europe',
        'Greenland': 'North America', 'Guatemala': 'North America',
        'Guinea': 'Africa', 'Guyana': 'South America', 'Honduras': 'North America',
        'Hong Kong': 'Asia', 'Hungary': 'Europe', 'Iceland': 'Europe',
        'India': 'Asia', 'Indonesia': 'Asia', 'Iran': 'Asia',
        'Iraq': 'Asia', 'Ireland': 'Europe', 'Israel': 'Asia',
        'Italy': 'Europe', 'Jamaica': 'North America', 'Japan': 'Asia',
        'Jordan': 'Asia', 'Kazakhstan': 'Asia', 'Kenya': 'Africa',
        'Kosovo': 'Europe', 'Kuwait': 'Asia', 'Kyrgyzstan': 'Asia',
        'Laos': 'Asia', 'Latvia': 'Europe', 'Lebanon': 'Asia',
        'Liberia': 'Africa', 'Libya': 'Africa', 'Lithuania': 'Europe',
        'Luxembourg': 'Europe', 'Macao': 'Asia', 'Madagascar': 'Africa',
        'Malawi': 'Africa', 'Malaysia': 'Asia', 'Maldives': 'Asia',
        'Mali': 'Africa', 'Malta': 'Europe', 'Mauritius': 'Africa',
        'Mexico': 'North America', 'Moldova': 'Europe', 'Monaco': 'Europe',
        'Mongolia': 'Asia', 'Montenegro': 'Europe', 'Morocco': 'Africa',
        'Mozambique': 'Africa', 'Myanmar': 'Asia', 'Namibia': 'Africa',
        'Nepal': 'Asia', 'Netherlands': 'Europe', 'New Zealand': 'Oceania',
        'Nicaragua': 'North America', 'Niger': 'Africa', 'Nigeria': 'Africa',
        'North Macedonia': 'Europe', 'Northern Ireland': 'Europe',
        'Norway': 'Europe', 'Oman': 'Asia', 'Pakistan': 'Asia',
        'Palestine': 'Asia', 'Panama': 'North America', 'Paraguay': 'South America',
        'Peru': 'South America', 'Philippines': 'Asia', 'Poland': 'Europe',
        'Portugal': 'Europe', 'Qatar': 'Asia', 'Romania': 'Europe',
        'Russia': 'Europe', 'Rwanda': 'Africa', 'Saudi Arabia': 'Asia',
        'Scotland': 'Europe', 'Senegal': 'Africa', 'Serbia': 'Europe',
        'Singapore': 'Asia', 'Slovakia': 'Europe', 'Slovenia': 'Europe',
        'South Africa': 'Africa', 'South Korea': 'Asia', 'Spain': 'Europe',
        'Sri Lanka': 'Asia', 'Sudan': 'Africa', 'Suriname': 'South America',
        'Sweden': 'Europe', 'Switzerland': 'Europe', 'Syria': 'Asia',
        'Taiwan': 'Asia', 'Thailand': 'Asia', 'Togo': 'Africa',
        'Trinidad and Tobago': 'North America', 'Tunisia': 'Africa',
        'Turkey': 'Asia', 'Uganda': 'Africa', 'Ukraine': 'Europe',
        'United Arab Emirates': 'Asia', 'United Kingdom': 'Europe',
        'United States': 'North America', 'Uruguay': 'South America',
        'Uzbekistan': 'Asia', 'Venezuela': 'South America', 'Vietnam': 'Asia',
        'Wales': 'Europe', 'Yemen': 'Asia', 'Zambia': 'Africa',
        'Zimbabwe': 'Africa'
    }
    
    df['continent'] = df['country'].map(continent_dict)
    
    # Fill NaN values for calculations
    df['total_vaccinations_per_hundred'] = df['total_vaccinations_per_hundred'].fillna(0)
    df['people_fully_vaccinated_per_hundred'] = df['people_fully_vaccinated_per_hundred'].fillna(0)
    
    # Calculate ratio
    df['full_vax_ratio'] = df['people_fully_vaccinated_per_hundred'] / df['total_vaccinations_per_hundred']
    df['full_vax_ratio'] = df['full_vax_ratio'].clip(0, 1)
    
    return df

# Load the data
try:
    df_vax = load_data(uploaded_file)
    
    # Get latest data for each country
    latest_vax = df_vax.groupby('country').tail(1).reset_index(drop=True)
    
    # Sidebar filters
    with st.sidebar:
        # Continent filter
        continents = ['All'] + sorted(latest_vax['continent'].dropna().unique().tolist())
        selected_continent = st.selectbox("Select Continent", continents)
        
        # Country filter
        if selected_continent != 'All':
            countries = latest_vax[latest_vax['continent'] == selected_continent]['country'].tolist()
        else:
            countries = latest_vax['country'].tolist()
        
        selected_countries = st.multiselect(
            "Select Countries for Time Series",
            sorted(countries),
            default=[]
        )
        
        # Top N countries
        top_n = st.slider("Number of top/bottom countries to display", 5, 20, 10)
    
    # Filter data based on selection
    if selected_continent != 'All':
        display_data = latest_vax[latest_vax['continent'] == selected_continent]
    else:
        display_data = latest_vax
    
    # Key Metrics
    st.header("📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Countries",
            len(display_data)
        )
    
    with col2:
        avg_vax = display_data['total_vaccinations_per_hundred'].mean()
        st.metric(
            "Avg Vaccinations per 100",
            f"{avg_vax:.2f}"
        )
    
    with col3:
        avg_full = display_data['people_fully_vaccinated_per_hundred'].mean()
        st.metric(
            "Avg Fully Vaccinated per 100",
            f"{avg_full:.2f}"
        )
    
    with col4:
        latest_date = df_vax['date'].max()
        st.metric(
            "Latest Data Date",
            latest_date.strftime('%Y-%m-%d')
        )
    
    st.markdown("---")
    
    # Top and Bottom Countries
    st.header("🏆 Top & Bottom Performing Countries")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Top {top_n} Countries")
        top_countries = display_data.nlargest(top_n, 'total_vaccinations_per_hundred')
        
        fig_top = px.bar(
            top_countries,
            x='total_vaccinations_per_hundred',
            y='country',
            orientation='h',
            color='total_vaccinations_per_hundred',
            color_continuous_scale='Viridis',
            labels={'total_vaccinations_per_hundred': 'Vaccinations per 100'},
            title=f'Top {top_n} Countries by Vaccination Coverage'
        )
        fig_top.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_top, use_container_width=True)
    
    with col2:
        st.subheader(f"Bottom {top_n} Countries")
        bottom_countries = display_data.nsmallest(top_n, 'total_vaccinations_per_hundred')
        
        fig_bottom = px.bar(
            bottom_countries,
            x='total_vaccinations_per_hundred',
            y='country',
            orientation='h',
            color='total_vaccinations_per_hundred',
            color_continuous_scale='Magma',
            labels={'total_vaccinations_per_hundred': 'Vaccinations per 100'},
            title=f'Bottom {top_n} Countries by Vaccination Coverage'
        )
        fig_bottom.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_bottom, use_container_width=True)
    
    st.markdown("---")
    
    # World Map
    st.header("🗺️ Global Vaccination Coverage Map")
    
    fig_map = px.choropleth(
        latest_vax,
        locations='country',
        locationmode='country names',
        color='total_vaccinations_per_hundred',
        hover_name='country',
        hover_data={
            'total_vaccinations_per_hundred': ':.2f',
            'people_fully_vaccinated_per_hundred': ':.2f'
        },
        color_continuous_scale='Viridis',
        title="Global COVID-19 Vaccination Coverage per 100 People"
    )
    fig_map.update_layout(height=500)
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown("---")
    
    # Continental Analysis
    st.header("🌏 Continental Analysis")
    
    continent_avg = latest_vax.groupby('continent').agg({
        'total_vaccinations_per_hundred': 'mean',
        'people_fully_vaccinated_per_hundred': 'mean',
        'full_vax_ratio': 'mean',
        'country': 'count'
    }).reset_index()
    continent_avg.columns = ['Continent', 'Avg Vaccinations per 100', 
                             'Avg Fully Vaccinated per 100', 'Full Vax Ratio', 'Number of Countries']
    
    tab1, tab2, tab3 = st.tabs(["📊 Total Vaccinations", "💉 Fully Vaccinated", "📈 Vaccination Ratio"])
    
    with tab1:
        fig_cont1 = px.bar(
            continent_avg,
            x='Continent',
            y='Avg Vaccinations per 100',
            color='Avg Vaccinations per 100',
            color_continuous_scale='Viridis',
            title='Average Total Vaccinations per 100 People by Continent',
            text='Avg Vaccinations per 100'
        )
        fig_cont1.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig_cont1.update_layout(height=400)
        st.plotly_chart(fig_cont1, use_container_width=True)
        
        st.markdown("""
        **Key Insights:**
        - Shows the average vaccination coverage across different continents
        - Highlights disparities in vaccine distribution globally
        """)
    
    with tab2:
        fig_cont2 = px.bar(
            continent_avg,
            x='Continent',
            y='Avg Fully Vaccinated per 100',
            color='Avg Fully Vaccinated per 100',
            color_continuous_scale='Cividis',
            title='Average Fully Vaccinated per 100 People by Continent',
            text='Avg Fully Vaccinated per 100'
        )
        fig_cont2.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig_cont2.update_layout(height=400)
        st.plotly_chart(fig_cont2, use_container_width=True)
        
        st.markdown("""
        **Key Insights:**
        - Africa has the lowest fully vaccinated coverage, highlighting equity gaps
        - Europe and South America show strong vaccination completion rates
        """)
    
    with tab3:
        fig_cont3 = px.bar(
            continent_avg,
            x='Continent',
            y='Full Vax Ratio',
            color='Full Vax Ratio',
            color_continuous_scale='Spectral',
            title='Ratio of Fully Vaccinated to Total Vaccinated by Continent',
            text='Full Vax Ratio'
        )
        fig_cont3.update_traces(texttemplate='%{text:.2%}', textposition='outside')
        fig_cont3.update_layout(height=400)
        fig_cont3.update_yaxes(range=[0, 1])
        st.plotly_chart(fig_cont3, use_container_width=True)
        
        st.markdown("""
        **Key Insights:**
        - Shows the efficiency of vaccination programs (completion rate)
        - Higher ratios indicate better follow-through on vaccination schedules
        """)
    
    # Display continent summary table
    st.subheader("📋 Continental Summary Statistics")
    st.dataframe(
        continent_avg.style.format({
            'Avg Vaccinations per 100': '{:.2f}',
            'Avg Fully Vaccinated per 100': '{:.2f}',
            'Full Vax Ratio': '{:.2%}',
            'Number of Countries': '{:.0f}'
        }),
        use_container_width=True
    )
    
    st.markdown("---")
    
    # Time Series Analysis
    if selected_countries and len(selected_countries) > 0:
        st.header("📅 Time Series Analysis")
        
        df_time_series = df_vax[df_vax['country'].isin(selected_countries)]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Total Vaccinations Over Time")
            fig_ts1 = px.line(
                df_time_series,
                x='date',
                y='total_vaccinations_per_hundred',
                color='country',
                title='COVID-19 Vaccination Coverage Over Time',
                labels={
                    'total_vaccinations_per_hundred': 'Vaccinations per 100',
                    'date': 'Date',
                    'country': 'Country'
                }
            )
            fig_ts1.update_layout(height=400)
            st.plotly_chart(fig_ts1, use_container_width=True)
        
        with col2:
            st.subheader("Fully Vaccinated Over Time")
            fig_ts2 = px.line(
                df_time_series,
                x='date',
                y='people_fully_vaccinated_per_hundred',
                color='country',
                title='Fully Vaccinated Coverage Over Time',
                labels={
                    'people_fully_vaccinated_per_hundred': 'Fully Vaccinated per 100',
                    'date': 'Date',
                    'country': 'Country'
                }
            )
            fig_ts2.update_layout(height=400)
            st.plotly_chart(fig_ts2, use_container_width=True)
        
        st.markdown("---")
    
    # Data Explorer
    with st.expander("🔍 Explore Raw Data"):
        st.subheader("Latest Vaccination Data")
        
        # Allow users to search and filter
        search_term = st.text_input("Search for a country:", "")
        
        if search_term:
            filtered_data = display_data[
                display_data['country'].str.contains(search_term, case=False, na=False)
            ]
        else:
            filtered_data = display_data
        
        # Select columns to display
        columns_to_show = [
            'country', 'continent', 'date', 
            'total_vaccinations_per_hundred',
            'people_fully_vaccinated_per_hundred',
            'full_vax_ratio'
        ]
        
        st.dataframe(
            filtered_data[columns_to_show].sort_values(
                'total_vaccinations_per_hundred', 
                ascending=False
            ).reset_index(drop=True),
            use_container_width=True
        )
        
        # Download button
        csv = filtered_data[columns_to_show].to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name="vaccination_data.csv",
            mime="text/csv"
        )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p>💉 COVID-19 Vaccination Coverage Dashboard | Built with Streamlit</p>
        <p>Data represents vaccination coverage across different countries and continents</p>
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.info("Please ensure you've uploaded a valid 'country_vaccinations.csv' file with the required columns.")
