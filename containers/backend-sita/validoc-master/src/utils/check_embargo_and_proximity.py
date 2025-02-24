def check_embargo_and_proximity(exporting_country, importing_country, items, embargo_data):
    """
    Combined function to check embargo status and proximity risk using Azure OpenAI.

    :param exporting_country: Alpha-2 code of the exporting country.
    :param importing_country: Alpha-2 code of the importing country.
    :param items: List of items being shipped.
    :param embargo_data: JSON data containing embargoed countries and restrictions.
    :return: Dictionary with embargo status, flagged items, and alerts.
    """
    embargoed_countries = embargo_data.get('embargoed_countries', [])
    alert_data = {'is_embargoed': False, 'flagged_items': [], 'alerts': []}
    for embargo_entry in embargoed_countries:
        if embargo_entry['country'] == importing_country:
            alert_data['is_embargoed'] = True
            alert_data['alerts'].append(f'{importing_country} is embargoed. ❌ ')
            return alert_data
    for embargo_entry in embargoed_countries:
        restricted_items = embargo_entry['restrictions']['items']
        flagged = [item for item in items if item in restricted_items]
        if flagged:
            alert_data['flagged_items'].extend(flagged)
            alert_data['alerts'].append(f"Items {', '.join(flagged)} are restricted due to proximity to embargoed country {embargo_entry['country']}.")
    try:
        proximity_risk_prompt = f"Assess the proximity risk: Is {importing_country} close to any of these embargoed countries: {', '.join([entry['country'] for entry in embargoed_countries])}? If so, check if the items being shipped ({', '.join(items)}) are restricted due to proximity."
        messages = [{'role': 'system', 'content': 'You are an AI assistant assessing embargo and proximity risks.'}, {'role': 'user', 'content': [{'type': 'text', 'text': proximity_risk_prompt}]}]
        response = azure_client.chat.completions.create(model='gpt-4o', messages=messages, temperature=0.7)
        ai_response = response.choices[0].message.content.strip()
        if 'yes' in ai_response.lower():
            alert_data['alerts'].append(f'Proximity risk detected for {importing_country} based on Azure OpenAI assessment.')
    except AttributeError as e:
        alert_data['alerts'].append(f'Unable to assess risks with Azure OpenAI: {str(e)}')
    except Exception as e:
        alert_data['alerts'].append(f'Unable to assess risks with Azure OpenAI: {str(e)}')
    return alert_data
