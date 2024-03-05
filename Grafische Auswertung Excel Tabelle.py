import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

data_excel_file_path = 'station_data_analysis.xlsx'
stations_excel_file_path = 'MobiData API - ID.xlsx'

stations_data = pd.read_excel(stations_excel_file_path, usecols="B:C", header=2)
id_to_name = pd.Series(stations_data['Name / Beschreibung'].values, index=stations_data['ID']).to_dict()

def visualize_station_data(station_id_requested):
    data = pd.read_excel(data_excel_file_path, header=1)
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data.sort_values(by='timestamp', inplace=True)

    plt.figure(figsize=(12, 8))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
    plt.gcf().autofmt_xdate()

    if station_id_requested.lower() == "alle":
        for station_id in data['station_id'].unique():
            station_name = id_to_name.get(station_id, station_id)
            station_data = data[data['station_id'] == station_id]
            plt.plot(station_data['timestamp'], station_data['num_bikes_available'], label=station_name)
    else:
        station_name = id_to_name.get(station_id_requested, station_id_requested)
        station_data = data[data['station_id'] == station_id_requested]
        if station_data.empty:
            print(f"Keine Daten für {station_name} gefunden.")
            return
        plt.plot(station_data['timestamp'], station_data['num_bikes_available'], label=station_name)

    plt.title('Verfügbare Fahrräder an Stationen über Zeit')
    plt.xlabel('Timestamp')
    plt.ylabel('Verfügbare Fahrräder')
    plt.legend()
    plt.tight_layout()
    plt.show()

station_id_input = input("Geben Sie die station_id ein (oder 'alle' für alle Stationen): ")
visualize_station_data(station_id_input)
