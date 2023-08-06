import os, json

class AppTheme:

    def __init__(self, disk_path, *args, **kwargs):
        self.disk_path = disk_path

        config_file_path = os.path.join(self.disk_path, 'config.json')

        with open(config_file_path, 'r') as f:
            settings = json.load(f)

        for key, value in settings.items():
            setattr(self, key, value)


    def get_online_content_path(self):
        return os.path.join(self.disk_path, 'online_content')


    def get_locale(self, language_code):

        locale_filename = '{0}.json'.format(language_code)
        locale_path = os.path.join(self.disk_path, 'locales', locale_filename)

        if os.path.isfile(locale_path):
            with open(locale_path, 'r') as f:
                theme_locale = json.load(f)
            return theme_locale

        return {}
            
