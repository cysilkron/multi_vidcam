from datetime import datetime
from pathlib import Path 


class FrameDatetime:
    def __init__(self, save_dir, save_name='timestamp.csv', exist_ok=True):
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        self.save_path = save_dir/save_name
        self.frame_datetimes = []

        if self.save_path.is_file() and not exist_ok:
            raise FileExistsError

        # write header
        with open(self.save_path, 'w') as f:
            f.write('Frame, Date_Timestamp')

    def now(self):
        # format datetime to appropriate format
        # return formatted_dt
        return datetime.now()

    def record(self, frame_id):
        line = f'\n{frame_id}, {self.now()}'
        self.frame_datetimes.append(line)
        
    def save(self, batch_size=True):
        with open(self.save_path, 'a') as f:
            f.writelines(self.frame_datetimes.pop())

    # def batch_save(self, batch_size=10):
    #     if batch_size<
    #     self.frame_datetimes 

    #     with open(self.save_path, 'a') as f:
    #         f.writelines(self.frame_datetimes)