import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Pfad zur Excel-Tabelle
excel_file_path = 'station_data_analysis.xlsx'

def visualize_station_data(station_id_requested):
    # Daten aus der Excel-Tabelle lesen, dabei Header-Zeile angeben
    data = pd.read_excel(excel_file_path, header=1)  # Angenommen, Spaltennamen sind in Zeile 2
    
    # Umwandlung des 'timestamp' in ein datetime-Objekt für bessere Darstellung und Sortierung
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data.sort_values(by='timestamp', inplace=True)
    
    # Erstellen des Diagramms
    plt.figure(figsize=(12, 8))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
    plt.gcf().autofmt_xdate()  # Rotation der Datumsangaben für bessere Lesbarkeit
    
    if station_id_requested.lower() == "alle":
        # Plot für alle station_ids
        for station_id in data['station_id'].unique():
            station_data = data[data['station_id'] == station_id]
            plt.plot(station_data['timestamp'], station_data['num_bikes_available'], label=station_id)
    else:
        # Plot für eine spezifische station_id
        station_data = data[data['station_id'] == station_id_requested]
        if station_data.empty:
            print(f"Keine Daten für station_id {station_id_requested} gefunden.")
            return
        plt.plot(station_data['timestamp'], station_data['num_bikes_available'], label=station_id_requested)
    
    plt.title('Verfügbare Fahrräder an Stationen über Zeit')
    plt.xlabel('Timestamp')
    plt.ylabel('Verfügbare Fahrräder')
    plt.legend()
    plt.tight_layout()
    plt.show()

# Benutzereingabe für die station_id
station_id_input = input("Geben Sie die station_id ein (oder 'alle' für alle Stationen): ")
visualize_station_data(station_id_input)
