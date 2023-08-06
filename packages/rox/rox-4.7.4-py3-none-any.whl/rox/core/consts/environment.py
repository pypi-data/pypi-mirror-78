import os


class classproperty(object):
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)


class Environment:
    ROXY_INTERNAL_PATH = 'device/request_configuration'

    @classproperty
    def CDN_PATH(self):
        rollout_mode = os.getenv('ROLLOUT_MODE', '')
        if rollout_mode == 'QA':
            return 'https://qa-conf.rollout.io'
        elif rollout_mode == 'LOCAL':
            return 'https://development-conf.rollout.io'
        return 'https://conf.rollout.io'

    @staticmethod
    def API_PATH(server_url='https://x-api.rollout.io'):
        rollout_mode = os.getenv('ROLLOUT_MODE', '')
        if rollout_mode == 'QA':
            return 'https://qa-api.rollout.io/device/get_configuration'
        elif rollout_mode == 'LOCAL':
            return 'http://127.0.0.1:8557/device/get_configuration'
        return '%s/device/get_configuration' % server_url

    @classproperty
    def CDN_STATE_PATH(self):
        rollout_mode = os.getenv('ROLLOUT_MODE', '')
        if rollout_mode == 'QA':
            return 'https://qa-statestore.rollout.io'
        elif rollout_mode == 'LOCAL':
            return 'https://development-statestore.rollout.io'

        return 'https://statestore.rollout.io'

    @staticmethod
    def API_STATE_PATH(server_url='https://x-api.rollout.io'):
        rollout_mode = os.getenv('ROLLOUT_MODE', '')
        if rollout_mode == 'QA':
            return 'https://qa-api.rollout.io/device/update_state_store'
        elif rollout_mode == 'LOCAL':
            return 'http://127.0.0.1:8557/device/update_state_store'

        return '%s/device/update_state_store' % server_url

    @classproperty
    def ANALYTICS_PATH(self):
        rollout_mode = os.getenv('ROLLOUT_MODE', '')
        if rollout_mode == 'QA':
            return 'https://qaanalytic.rollout.io'
        elif rollout_mode == 'LOCAL':
            return 'http://127.0.0.1:8787'

        return 'https://analytic.rollout.io'

    @classproperty
    def NOTIFICATIONS_PATH(self):
        rollout_mode = os.getenv('ROLLOUT_MODE', '')
        if rollout_mode == 'QA':
            return 'https://qax-push.rollout.io/sse'
        elif rollout_mode == 'LOCAL':
            return 'http://127.0.0.1:8887/sse'

        return 'https://push.rollout.io/sse'
