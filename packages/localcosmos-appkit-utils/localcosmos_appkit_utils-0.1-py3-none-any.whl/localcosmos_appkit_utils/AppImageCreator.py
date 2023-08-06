import os, shutil
from PIL import Image

from app_kit_utils.image_utils import (create_png_from_svg, create_resized_png_from_svg, create_png_border,
                                       remove_alpha_channel_from_png)

###########################################################################################
# GENERATE IMAGES
# - generate app images from svg
# - fixed dimensions: simply create a png image from svg via inkscape export
# - varying dimensions: use the shorter side to create png, cut afterwards
# - the extension might differ from the existing_image_diskpath
# - android adaptive launchers (foreground + background)

APP_THEME_IMAGE_NAMES = {
    'launcher' : 'app_launcher_icon',
    'splashscreen' : 'app_splashscreen',
    'launcher_background' : 'app_launcher_background',
}


FALLBACK_IMAGES = {
    'launcher_background' : 'resources/images/adaptive_launcher_background.svg', # relative to this file
}


class AppImageCreator:

    def __init__(self, meta_app_definition, app_cordova_folder, user_content_folder, app_theme):
        
        self.meta_app_definition = meta_app_definition
        self.user_content_folder = user_content_folder
        self.app_theme = app_theme
        self.app_cordova_folder = app_cordova_folder

        self.root = os.path.dirname(os.path.abspath(__file__))


    def iterate_over_default_image_files(self):
        raise NotImplementedError()
        

    def generate_images_from_svg(self, image_type, varying_ratios=False, remove_alpha_channel=False):

        filename, image_path = self._get_source_image_diskpath(image_type)

        if filename is None or image_path is None:
            raise ValueError('No {0} image found'.format(image_type))

        # get the svg image filepath
        image_svg_filepath = image_path

        for icon_folder, filename in self.iterate_over_default_image_files(image_type):

            cordova_default_image_path = os.path.join(icon_folder, filename)

            # scan the file and overwrite it via a file generated from svg
            cordova_default_image = Image.open(cordova_default_image_path)

            width, height = cordova_default_image.size

            cordova_default_image.close()

            if varying_ratios == False:

                if filename == 'ic_launcher_foreground.png' and self.platform == 'android':
                    self._generate_adaptive_launcher(image_svg_filepath, width, height,
                                                     cordova_default_image_path)

                else:
                    create_png_from_svg(image_svg_filepath, width, height,
                                        cordova_default_image_path)

            else:
                create_resized_png_from_svg(image_svg_filepath, width, height,
                                            cordova_default_image_path)

            if remove_alpha_channel == True:
                remove_alpha_channel_from_png(cordova_default_image_path)

    
    # source svg file
    def _get_source_image_diskpath(self, image_type):

        images_folder = os.path.join(self.user_content_folder, 'images')

        app_theme_image_name = APP_THEME_IMAGE_NAMES[image_type]

        # the adaptive background image might not be in self.app_theme.user_content['images']
        if app_theme_image_name in self.app_theme.user_content['images']:
            theme_image_definition = self.app_theme.user_content['images'][app_theme_image_name]
            filetypes = theme_image_definition['restrictions'].get('file_type', [])

            for filename in os.listdir(images_folder):

                image_path = os.path.join(images_folder, filename)

                name, ext = filename.split('.')
                
                if name == app_theme_image_name:

                    if filetypes:
                        if ext in filetypes:
                            return filename, image_path
                        else:
                            continue
                    else:
                        return filename, image_path


        # no image file found, check fallback images
        fallback_image = FALLBACK_IMAGES.get(image_type, None)

        if fallback_image is not None:
            fallback_image_path = os.path.join(self.root, fallback_image)

            if os.path.isfile(fallback_image_path):

                fallback_filename = os.path.basename(fallback_image_path)

                return fallback_filename, fallback_image_path

        return None, None


    ##############################################################################################################
    # ANDROID ADAPTIVE ICONS
    #
    # 108x108dp outer dimensions, the inner 72dpx72dp show the icon, outer 18dp are reserved for the system
    # user uploads square icon
    # scale down this icon to 72dp
    # create a 108dp icon with transparent background
    # paste the 72dp icon in the center of the 108dp image
    def _generate_adaptive_launcher(self, svg_filepath, width, height, destination_filepath):

        inner_width = 90 # 90 or 72

        # width and height are both 108dp
        icon_width = int((width/108) * inner_width)
        icon_height = int((height/108) * inner_width)

        create_png_from_svg(svg_filepath, icon_width, icon_height, destination_filepath)

        border_width = int((width/108) * (108-inner_width))

        border_color = (255,255,255,0)

        create_png_border(destination_filepath, border_width, border_color)



class AndroidAppImageCreator(AppImageCreator):

    platform = 'android'

    definitions = {
        'launcher' : {
            'subfolders_startwith' : 'mipmap-',
            'folder' : 'platforms/android/app/src/main/res',
            'filenames' : ['ic_launcher.png', 'ic_launcher_foreground.png'],
        },
        'launcher_background' : {
            'subfolders_startwith' : 'mipmap-',
            'folder' : 'platforms/android/app/src/main/res',
            'filenames' : ['ic_launcher_background.png'],
        },
        'splashscreen' : {
            'subfolders_startwith' : 'drawable-',
            'folder' : 'platforms/android/app/src/main/res',
            'filenames' : ['screen.png'],
        }
    }


    def iterate_over_default_image_files(self, image_type):
        icon_parent_folder = os.path.join(self.app_cordova_folder, self.definitions[image_type]['folder'])
        
        # iterate over all subfolders named mipmap-*
        for subfolder in os.listdir(icon_parent_folder):

            icon_folder = os.path.join(icon_parent_folder, subfolder)

            if os.path.isdir(icon_folder) and subfolder.startswith(self.definitions[image_type]['subfolders_startwith']):

                for expected_image_filename in self.definitions[image_type]['filenames']:
                    
                    for filename in os.listdir(icon_folder):

                        cordova_default_image_path = os.path.join(icon_folder, filename)

                        if os.path.isfile(cordova_default_image_path) and filename == expected_image_filename:

                            yield icon_folder, filename


class IOSAppImageCreator(AppImageCreator):

    platform = 'ios'

    definitions = {
        'launcher' : {
            'folder' : 'AppIcon.appiconset',
        },
        'splashscreen' : {
            'folder' : 'LaunchImage.launchimage',
        },
        'storyboard' : {
            'Default@2x~universal~anyany.png' : [2732,2732],
            'Default@3x~universal~anyany.png' : [2732,2732],
        }
    }

    def get_folder(self, image_type):
        folder = 'platforms/ios/{0}/Images.xcassets/{1}'.format(self.meta_app_definition.name,
                                                                self.definitions[image_type]['folder'])

        return folder


    def iterate_over_default_image_files(self, image_type):
        icon_folder = os.path.join(self.app_cordova_folder, self.get_folder(image_type))
                    
        for filename in os.listdir(icon_folder):

            cordova_default_image_path = os.path.join(icon_folder, filename)

            if os.path.isfile(cordova_default_image_path) and filename.endswith('.png'):

                yield icon_folder, filename


    def generate_storyboard_images(self):

        image_type = 'splashscreen'

        res_folder = os.path.join(self.app_cordova_folder, 'res')

        if os.path.isdir(res_folder):
            shutil.rmtree(res_folder)

        screen_folder = os.path.join(res_folder, 'screen', 'ios')
        os.makedirs(screen_folder)

        
        source_filename, source_image_path = self._get_source_image_diskpath(image_type)

        if source_filename is None or source_image_path is None:
            raise ValueError('No {0} image found'.format(image_type))
        

        for storyboard_filename, size in self.definitions['storyboard'].items():

            target_image_path = os.path.join(screen_folder, storyboard_filename)
            width = size[0]
            height = size[1]
            
            create_resized_png_from_svg(source_image_path, width, height, target_image_path)
        
        
