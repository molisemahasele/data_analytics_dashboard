import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import statistics

st.set_page_config(page_title="Analytics Dashboard")
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

eggs_column = df_participants[df_participants.columns[1]]  # Assuming the second column is Y-axis data
eggs_column_numeric = pd.to_numeric(eggs_column, errors='coerce')  # Convert to numeric, coerce errors to NaN

# Calculate mode and mean after cleaning
eggs_column_numeric = eggs_column_numeric.dropna()  # Remove NaN values
data_mode = statistics.mode(eggs_column_numeric)
data_mean = statistics.mean(eggs_column_numeric)
data_min = min(eggs_column_numeric)
data_max = max(eggs_column_numeric)

# Create the line chart
line_chart = px.line(
    df_participants,
    x=df_participants.columns[0],  # Assuming the first column is X-axis
    y=df_participants.columns[1],  # Assuming the second column is Y-axis
    title='Production of eggs for November'
)

st.plotly_chart(line_chart)

st.write(f"Mode: {data_mode}")
st.write(f"Mean number of eggs: {data_mean}")
st.write(f"Minimum number of eggs: {data_min}")
st.write(f"Maximum number of eggs: {data_max}")

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
df_grouped = filtered_data.groupby('November Week')['Sales'].sum().reset_index()

# Creating a bar chart using Plotly Express with 'Sales' on the y-axis
bar_chart = px.bar(df_grouped,
                    title="Sales Timeline",
                    x='November Week',
                    y='Sales',
                    text='Sales',
                    color_discrete_sequence=['#F63366'] * len(df_grouped),
                    template='plotly_white')

# Displaying the bar chart in Streamlit
bar_chart.update_layout(yaxis_title='Sales')  # Set y-axis title to 'Sales'
st.plotly_chart(bar_chart)

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

sales = df_sales_expenses['Total Sales'].sum()  # Assuming 'Sales' is the column name for sales
expenses = df_sales_expenses['Total Expenses'].sum()  # Assuming 'Expenses' is the column name for expenses
sales_minus_expenses = sales - expenses

# Display the result
st.write(f"Total Profit: {sales_minus_expenses}")
                
df = pd.read_excel(excel_file, usecols='H:J', header=0)

# Grouping by 'November Week' and calculating variance of 'Sales' within each group
df_variance = df.groupby(['November Week', 'Type'])['Sales'].var().reset_index()

# Creating a bar chart using Plotly Express to visualize variance across types for each week
variance_chart = px.bar(df_variance,
                        title="Variance in Sales Across Types for Each Week",
                        x='November Week',
                        y='Sales',
                        color='Type',
                        barmode='group',
                        labels={'Sales': 'Variance', 'Type': 'Product'},
                        template='plotly_white')

# Displaying the variance chart in Streamlit
st.plotly_chart(variance_chart)

variance_per_product = df.groupby('Type')['Sales'].var()

# Displaying the numerical variance for each product
st.write("Variance of Sales for Each Product:")
st.write(variance_per_product)
