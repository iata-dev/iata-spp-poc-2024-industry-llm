from dash.dependencies import Input, Output
from dash import dcc, html

@dash_app.callback([Output('essential-content', 'children'), Output('less-essential-content', 'children'), Output('non-essential-content', 'children'), Output('cargo-weight-chart', 'figure'), Output('cargo-weight-chart', 'figure_total')], [Input('interval-update', 'n_intervals')])
def update_dashboard(_):
    total_weight = calculate_total_cargo_weight()
    data = load_json_data()
    document_details = data.get('document_details', {})
    essential = document_details
    essential_content = [html.P(f"AWB Number: {essential.get('awb_number', 'N/A')}"), html.P(f"Shipper: {essential.get('shipper', {}).get('name', 'N/A')}"), html.P(f"Consignee: {essential.get('consignee', {}).get('name', 'N/A')}"), html.P(f"Cargo Pieces: {essential.get('cargo', {}).get('pieces', 'N/A')}"), html.P(f"Cargo Weight: {essential.get('cargo', {}).get('weight', 'N/A')} {essential.get('cargo', {}).get('unit', 'N/A')}"), html.P(f'Total Cargo Weight: {total_weight} Kgs')]
    less_essential = document_details.get('charges', {})
    less_essential_content = [html.P(f"Freight Charges: {less_essential.get('freight', 'N/A')} {less_essential.get('currency', 'N/A')}"), html.P(f"Prepaid Charges: {less_essential.get('prepaid', 'N/A')}"), html.P(f"Total Prepaid: {less_essential.get('total_prepaid', 'N/A')}")]
    non_essential_content = [html.P(f"Requested Flight Date: {essential.get('requested_flight_date', 'N/A')}")]
    figure_total = go.Figure(go.Indicator(mode='gauge+number', value=total_weight, title={'text': 'Total Cargo Weight (Kgs)'}, gauge={'axis': {'range': [0, 5000]}, 'bar': {'color': 'cyan'}}))
    cargo_weight = float(essential.get('cargo', {}).get('weight', 0))
    figure = go.Figure(go.Indicator(mode='gauge+number', value=cargo_weight, title={'text': 'Cargo Weight (Kgs)'}, gauge={'axis': {'range': [0, 5000]}, 'bar': {'color': 'cyan'}}))
    figure.update_layout(paper_bgcolor='black', font={'color': 'white'})
    figure_total.update_layout(paper_bgcolor='black', font={'color': 'white'})
    return (essential_content, less_essential_content, non_essential_content, figure, figure_total)

