from app_settings import Settings
import pickle, datetime
import os


class File_Manager:
    def __init__(self):
        pass

    def save_last_training_file(self, content_to_be_saved):
        # save these particles to file
        print('save_last_training_file')
        save_path = '{dir}final_drivers-{date:%Y-%m-%d_%H%M%S}.txt'.format( dir=Settings.filesdir, date=datetime.datetime.now() )
        with open(save_path,'wb') as output:
            pickle.dump(content_to_be_saved, output)
            
    def get_files(self, dirpath):
        a = [s for s in os.listdir(dirpath)
            if os.path.isfile(os.path.join(dirpath, s))]
        a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
        return a

    def get_first(self, iterable):
        length = len(iterable) -1
        return iterable[length]

    def load_last_training_file(self):
        print('load_last_training_file')
        all_files = File_Manager.get_files(self, Settings.filesdir)
        racer_file =  Settings.filesdir + File_Manager.get_first(self, all_files)
        print('loading ' + racer_file)
        with open(racer_file,'rb') as input:
            driver_list = pickle.load(input)
        return driver_list

