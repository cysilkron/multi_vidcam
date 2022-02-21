from datetime import datetime 

def get_date_timestamp(save_dir, count):      
    timestamp_csv = f'{save_dir}/timestamp.csv'
    
    if count == 1:
        with open(timestamp_csv, 'w') as f:
            f.write('Frame, Date, Timestamp')
            
    with open(timestamp_csv, 'a') as f:
        f.write(f'\n{count}, {datetime.now().date()}, {datetime.now().time()}')
        