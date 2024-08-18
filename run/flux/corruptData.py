import numpy as np
import pandas as pd

data = pd.read_csv('./q_carotid.csv', sep=";", names=['time', 'Q_carotid'])

# Определение максимального значения потока крови
max_flow = data['Q_carotid'].max()
max_time = data.loc[data["Q_carotid"] == max_flow].iloc[0]['time']
print(f'Global extremum: {max_time} {max_flow}')

# Разделим данные на систолическую и диастолическую фазы
systolic_phase = data[data['time'] <= max_time].copy()
diastolic_phase = data[data['time'] > max_time].copy()

# Уменьшаем значения в диастолической фазе на 20%
systolic_phase['Q_carotid'] *= 0.8
diastolic_phase['Q_carotid'] *= 0.8

# Добавляем случайный шум (например, в пределах 5% от значения)
noise = np.random.normal(0, 0.005 * diastolic_phase['Q_carotid'], diastolic_phase.shape[0])
diastolic_phase['Q_carotid'] += noise

# Объединяем фазы обратно
modified_data = pd.concat([systolic_phase, diastolic_phase]).sort_index()

# Сохраняем модифицированные данные в новый CSV файл
modified_data_path = './q_carotid_dysfunction.csv'
modified_data.to_csv(modified_data_path, index=False, header=False, sep=";")

print(f'Written to ./q_carotid_dysfunction.csv', end='\r')