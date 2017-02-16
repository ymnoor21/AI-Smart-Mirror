import time
from config import Config

class Helper(object):
    def set_timer(self):
        Config.TIMER = time.time()

    def reset_timer(self):
        self.set_timer()

    def is_timer_set(self):
        if Config.TIMER:
            return True
        else:
            return False

    def timer_expired(self):
        return self.is_expired(Config.EXPIRY_TIME)

    def is_session_expired(self):
        return self.is_expired(Config.MAX_FR_DETECT_EXPIRY_TIME)

    def is_expired(self, value):
        current_time = time.time()
        diff = current_time

        if Config.TIMER:
            diff = current_time - Config.TIMER

        if diff >= value:
            return True
        else:
            return False

    def is_personalized_data_accessible(self):
        if Config.PERSONALIZED_INFO:
            return True
        else:
            return False

    def reset_personalized_data(self):
        Config.PERSONALIZED_INFO = None

    def get_personalized_data(self):
        return Config.PERSONALIZED_INFO

    def set_personalized_data(self, list_of_persons):
        Config.PERSONALIZED_INFO = list_of_persons