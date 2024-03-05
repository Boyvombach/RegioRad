import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

excel_file_path = 'station_data_analysis.xlsx'

def visualize_station_data(station_id_requested):
    data = pd.read_excel(excel_file_path)
    
    if station_id_requested.lower() != "alle":
        data = data[data['station_id'] == station_id_requested]
        if data.empty:
            print(f"Keine Daten für station_id {station_id_requested} gefunden.")
            return
    
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data.sort_values(by='timestamp', inplace=True)
    
    if station_id_requested.lower() == "alle":
        station_ids = data['station_id'].unique()
        station_id_mapping = {station_id: i for i, station_id in enumerate(station_ids, start=1)}
        data['station_id_mapped'] = data['station_id'].map(station_id_mapping)
        y_data = data['station_id_mapped']
        y_ticks = list(station_id_mapping.values())
        y_tick_labels = list(station_id_mapping.keys())
    else:
        y_data = pd.Series(1, index=data.index) 
        y_ticks = [1]
        y_tick_labels = [station_id_requested]
    
    # Erstellen des Scatter-Plots
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(data['timestamp'], y_data, c=data['num_bikes_available'], cmap='viridis', alpha=0.6)
    
    plt.colorbar(scatter, label='Verfügbare Fahrräder')
    plt.title('Verfügbare Fahrräder an Stationen über Zeit')
    plt.xlabel('Timestamp')
    plt.ylabel('Station ID')
    
    plt.yticks(ticks=y_ticks, labels=y_tick_labels)
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
    plt.gcf().autofmt_xdate()  # Rotation
    
    plt.tight_layout()
    plt.show()

station_id_input = input("Geben Sie die station_id ein (oder 'alle' für alle Stationen): ")
visualize_station_data(station_id_input)
