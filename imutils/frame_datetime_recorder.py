from datetime import datetime
from pathlib import Path 


class FrameDatetime:
    def __init__(self, save_dir, exist_ok=True):
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        self.save_path = Path(save_dir.parent.name)/f'timestamp{save_dir.name[-1]}.csv'
        self.frame_datetimes = []

        if self.save_path.is_file() and not exist_ok:
            raise FileExistsError

        # write header
        with open(self.save_path, 'w') as f:
            f.write('Frame Number, Date, Timestamp')

    def now(self):
        # format datetime to appropriate format
        date_time = datetime.now()
        date, time = date_time.date(), date_time.time()
        # return formatted_dt
        return date, time

    def record(self, frame_id):
        date, time = self.now()
        line = f'\n{frame_id}, {date}, {time}'
        self.frame_datetimes.append(line)
        
    def save(self, batch_size=True):
        with open(self.save_path, 'a') as f:
            f.writelines(self.frame_datetimes.pop(0))  # first in first out

    # def batch_save(self, batch_size=10):
    #     if batch_size<
    #     self.frame_datetimes 

    #     with open(self.save_path, 'a') as f:
    #         f.writelines(self.frame_datetimes)