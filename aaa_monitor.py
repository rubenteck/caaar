import time
import requests
from flask import Flask, request, jsonify
import threading
from bs4 import BeautifulSoup
from slack_sdk.webhook import WebhookClient
import os

app = Flask(__name__)
URL = "https://chargemap.com/cegeka-l-0000194210.html"
SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]

def get_html_page_data():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None # Retourneer None bij fouten
def parse_chargers_from_html(html_data):
    if not html_data:
        return {} # Retourneer een lege dictionary als er geen data is
    soup = BeautifulSoup(html_data, 'html.parser')
    charger_items = soup.find_all('div', class_='item')
    chargers_parsed_data = {}
    index = 1
    for item in charger_items:
        evse_number = item.get('data-default-evse')
        availability_div = item.find('div', class_='label-availability')
        availability = None
        if availability_div:
            availability = availability_div.get_text(strip=True)
        # We zoeken naar de tekst 'Availability' of een soortgelijke indicator voor 'vrij'
        # Check de precieze tekst op de website voor "vrij"
        is_available = (availability == 'Availability' or availability == 'Vrij' or availability == 'Available')
        if evse_number: # evse_number is uniek en essentieel
            chargers_parsed_data[index] = is_available
        index += 1
    return chargers_parsed_data
def send_slack_notification(message):
    try:
        webhook = WebhookClient(SLACK_WEBHOOK_URL)
        webhook.send(text=message)
        print(f"Slack notificatie verstuurd: {message}")
    except requests.exceptions.RequestException as e:
        print(f"Fout bij versturen Slack notificatie: {e}")
    except Exception as e:
        print(f"Onverwachte fout bij versturen Slack notificatie: {e}")
        print(e)
def monitor_chargers():
    currentlyAvailable = set()
    while True:
        print("Controleer laderstatus...")
        html_data = get_html_page_data()
        if html_data:
            new_statuses = parse_chargers_from_html(html_data)
            available = [i for i in new_statuses.keys() if new_statuses[i]]
            new_available = [i for i in available if  i not in currentlyAvailable]
            no_longer_available = [i for i in currentlyAvailable if i not in available]
            print(new_available)
            print(no_longer_available)
            currentlyAvailable.update(new_available)
            for charger in new_available:
                send_slack_notification(f":ruben-cat: charger {charger} is now available :party-racoon:")
            for charger in no_longer_available:
                send_slack_notification(f"charger {charger} is no longer available :sadblob:")
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            print(new_statuses)
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            # # Alleen doorgaan als we daadwerkelijk statusdata hebben kunnen parsen
            # if new_statuses:
            #     for charger_id, new_status in new_statuses.items():
            #         # Zorg ervoor dat de lader_id al in charger_statuses bestaat voordat we old_status opvragen
            #         # Als de lader nieuw is, stellen we de old_status in op False (bezet)
            #         old_status = charger_statuses.get(charger_id, False)
            #         if not old_status and new_status:
            #             notification_message = f":rotating_light: Lader '{charger_id}' is nu VRIJ! :tada:"
            #             send_slack_notification(notification_message)
            # #         charger_statuses[charger_id] = new_status
            # else:
            #     print("Geen geldige laderstatus gevonden in de HTML-data.")
        else:
            print("Kan geen HTML-data ophalen. Sla deze controlecyclus over.")
        time.sleep(30)
@app.route('/status', methods=['GET'])
def get_current_charger_status_route():
    return jsonify(charger_statuses)
if __name__ == '__main__':
    print("Start de lader monitoring thread...")
    thread = threading.Thread(target=monitor_chargers)
    thread.daemon = True
    thread.start()
    print("De Flask server start nu...")
    print("Vergeet niet JOUW_SLACK_WEBHOOK_URL_HIER te vervangen in de code!")
    app.run(debug=True, use_reloader=False)