import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import statistics
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon=":chart_with_upwards_trend:"
)


def set_theme():
    st.markdown(
        """
        <style>
        body {
            background-color: #090F17;
            color: #F0F6FC;
        }
        .sidebar .sidebar-content {
            background-color: #090F17;
            color: #F0F6FC;
        }
        .plotly-chart {
            background-color: #090F17;
        }
        .streamlit-data-frame {
            background-color: #090F17;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )



set_theme()

st.header('Bokhabane Analytics')

excel_file = 'bokhabaneData.xlsx'
#excel_file2 = 'bokhabaneData.xlsx'
#sheet_name = 'DATA'

df = pd.read_excel(excel_file,
                    usecols='A:B',
                    header=0)

df_participants = pd.read_excel(excel_file,
                                 usecols='E:F',
                                 header=0)

fd = pd.read_excel(excel_file,
                    usecols='H:K',
                    header=0)

#st.dataframe(df_participants)
pie_chart = px.pie(df,
                    title="Sales From Different Products",
                    values="Amount",
                    names="Product")

st.plotly_chart(pie_chart)

#eggs_column = df_participants[df_participants.columns[1]]  # Assuming the second column is Y-axis data
#eggs_column_numeric = pd.to_numeric(eggs_column, errors='coerce')  # Convert to numeric, coerce errors to NaN



department = fd['Type'].unique().tolist()
ages = fd['Sales'].unique().tolist()

# Streamlit sidebar selections
age_selection = st.slider('Sales:', 
                          min_value=min(ages),
                          max_value=max(ages),
                          value=(min(ages), max(ages)))

department_selection = st.multiselect('Product:', department, default=department)

# Filtering based on selection
mask = (fd['Sales'].between(*age_selection)) & (fd['Type'].isin(department_selection))
filtered_data = fd[mask]

number_of_result = filtered_data.shape[0]
st.markdown(f'*Available Results: {number_of_result}*')

# Grouping by 'November Week' and summing 'Sales'
df_grouped = filtered_data.groupby('Date')['Sales'].sum().reset_index()

# Creating a bar chart using Plotly Express with 'Sales' on the y-axis
bar_chart = px.bar(df_grouped,
                    title="Sales Timeline",
                    x='Date',
                    y='Sales',
                    text='Sales',
                    color_discrete_sequence=['#F63366'] * len(df_grouped),
                    template='plotly_white')

# Displaying the bar chart in Streamlit
bar_chart.update_layout(yaxis_title='Sales')  # Set y-axis title to 'Sales'
st.plotly_chart(bar_chart)

# Read the data from columns H to J
df = pd.read_excel(excel_file, usecols='H:J')

# Checking for numerical columns


# Calculating the frequency of sales per type of product
sales_frequency = df['Type'].value_counts()

# Displaying the frequency of sales per type of product
st.write("Frequency of Sales per Type of Product:")
st.write(sales_frequency)

# Plotting the frequency of sales per type of product
fig = px.bar(sales_frequency, x=sales_frequency.index, y=sales_frequency.values, labels={'x': 'Type of Product', 'y': 'Frequency'}, title='Sales Frequency per Product Type')
fig.update_traces(marker_color='#00897B')  # Updating marker color for better visualization
fig.update_layout(xaxis_title='Type of Product', yaxis_title='Frequency')
st.plotly_chart(fig)

df_sales_expenses = pd.read_excel(excel_file, usecols='P:Q', header=0)



#st.write(df_sales_expenses)

# Reshape the DataFrame for plotting
df = df_sales_expenses.melt(var_name='Category', value_name='Amount')

# Create a bar graph using Plotly
fig = px.bar(df, x='Category', y='Amount', color='Category',
             labels={'Amount': 'Amount', 'Category': 'Category'},
             title='Sales vs Expenses')

# Display the graph in Streamlit
st.plotly_chart(fig)

df = pd.read_excel(excel_file, usecols='P:Q')  # Adjust columns as needed

# Assuming the columns are named 'Total Sales' and 'Total Expenses'
sales_column = 'Total Sales'
expenses_column = 'Total Expenses'

# Remove rows with 'None' values in 'Total Sales' or 'Total Expenses'
df = df.dropna(subset=[sales_column, expenses_column])

# Calculate Net Profit and Profit Margin
if sales_column in df.columns and expenses_column in df.columns:
    df['Net Profit'] = df[sales_column] - df[expenses_column]
    df['Profit Margin (%)'] = (df['Net Profit'] / df[sales_column]) * 100

    # Display Net Profit and Profit Margin
    st.write("Net Profit and Profit Margin:")
    st.write(df[['Net Profit', 'Profit Margin (%)']])
else:
    st.write("Sales or Expenses columns not found in the DataFrame.")
                
# Read the data from columns E and F
df_eggs = pd.read_excel(excel_file, usecols='E:F')

# Calculating mean, variance, mode, median, min, max, and standard deviation of 'Number of eggs'
mean_eggs = df_eggs['Number of eggs'].mean()
variance_eggs = df_eggs['Number of eggs'].var()
mode_eggs = statistics.mode(df_eggs['Number of eggs'])
median_eggs = df_eggs['Number of eggs'].median()
min_eggs = df_eggs['Number of eggs'].min()
max_eggs = df_eggs['Number of eggs'].max()
std_dev_eggs = df_eggs['Number of eggs'].std()

# Plotting variance
variance_chart_eggs = px.line(df_eggs, x='Day', y='Number of eggs', title='Egg Production')
variance_chart_eggs.update_traces(mode='markers+lines')

# Displaying the variance chart in Streamlit
st.plotly_chart(variance_chart_eggs)

# Displaying statistics of number of eggs
st.write(f"Mean number of eggs: {mean_eggs}")
st.write(f"Variance of number of eggs: {variance_eggs}")
st.write(f"Mode of number of eggs: {mode_eggs}")
st.write(f"Median of number of eggs: {median_eggs}")
st.write(f"Minimum number of eggs: {min_eggs}")
st.write(f"Maximum number of eggs: {max_eggs}")
st.write(f"Standard deviation of number of eggs: {std_dev_eggs}")
