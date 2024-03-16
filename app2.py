import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from plotly import graph_objs as go

df = pd.read_csv("C:/Users/thoma/OneDrive/Documents/DSAIS/Semester 2 courses\Data Science Mission/APP/CRM_certideal_final.csv")

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div(style={'backgroundColor': '#1e2130', 'color': 'white', 'padding': '30px'}, children=[
    html.H1("Cluster Feature Visualization", style={'textAlign': 'center', 'color': 'white'}),
    
    dcc.Dropdown(
        id='feature-dropdown',
        options=[{'label': feature, 'value': feature} for feature in [
            'id_order', 'id_order_detail', 'id_customer', 'id_product', 'product_price',
            'reduction_percent', 'reduction_amount', 'customer_name', 'total_paid',
            'total_price_tax_incl', 'total_discounts', 'total_shipping', 'payment',
            'module', 'name', 'date_add', 'postcode', 'is_company', 'price_category',
            'code_type', 'code_used', 'payment_category', 'year', 'month', 'day',
            'quarter', 'departement', 'region', 'gender', 'income_num', 'income_cat',
            'inflation_rate', 'first_order', 'last_order', 'recency', 'frequency_sum_orders',
            'frequency_lag', 'frequency_avg_gap', 'monetary', 'is_covid_period', 'is_black_friday', 'is_back_school'
        ]],
        value='id_customer', # Default selection
        style={'width': '50%', 'color': '#1e2130'}
    ),
    
    dcc.Graph(id='feature-bar-chart')
])

@app.callback(
    Output('feature-bar-chart', 'figure'),
    [Input('feature-dropdown', 'value')]
)
def update_graph(selected_feature):
    feature_counts = df.groupby('Cluster_Labels_4')[selected_feature].nunique().reset_index()
    feature_counts.columns = ['Cluster_Labels_4', 'Count']

    fig = px.bar(feature_counts, x='Cluster_Labels_4', y='Count', text='Count',
                 color='Cluster_Labels_4',
                 color_discrete_map={0: '#636EFA', 1: '#EF553B', 2: '#00CC96', 3: '#AB63FA'},
                 labels={'Cluster_Labels_4': 'Clusters', 'Count': selected_feature},
                 category_orders={"Cluster_Labels_4": [str(i) for i in range(0, 4)]})
    
    # Update x-axis to display integer cluster labels without decimals
    fig.update_xaxes(tickvals=[0, 1, 2, 3], ticktext=['0', '1', '2', '3'], title='Clusters')

    # Customize layout
    fig.update_layout(plot_bgcolor='#1e2130', paper_bgcolor='#1e2130', font={'color': '#FFFFFF'},
                      legend_title_text='Clusters')

    fig.update_traces(texttemplate='%{text}', textposition='outside')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
