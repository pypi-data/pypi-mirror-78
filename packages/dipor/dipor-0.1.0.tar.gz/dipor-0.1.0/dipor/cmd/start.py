import pathlib
import shutil
import os
import sys
import dipor
from dipor.main import builder_main
from dipor.server import runserver

'''
MAIN FUNCTIONS -
    - quickstart (the default template)
    - bigbang (nothing is set just the src/content directories/settings)
    - use <github-src> (to use themes from github)
    - dipor dev [-PORT]
    - dipor build [-NOSERVE]
    - help (?)
'''
class EntryPointCommands:

    def __init__(self, args):
        self.ARGS_ACTIONS_MAP = {'quickstart': self.quickstart,
                        'bigbang': self.bigbang,
                        'use': self.use_theme,
                        'dev': self.soft_build,
                        'build': self.hard_build}

        self.src_root = self.get_src_root
        self.dst_root = self.get_dst_root

        self.action = args[1]
        self.ac_parameters = args[2:]

        self.call_action(self.action, self.ac_parameters)
        

    def call_action(self, action, ac_parameters):
        action_fn = self.ARGS_ACTIONS_MAP.get(action, self.default_action)
        action_fn(ac_parameters)


    @property
    def get_src_root(self):
        return os.path.dirname(dipor.__file__)

    @property
    def get_dst_root(self):
        return pathlib.Path().absolute()

    
    def copy_file(self, src, dst, file):
        try:
            shutil.copy(os.path.join(src, file), os.path.join(dst, file))
        except FileExistsError:
            override = input("Hey, looks like a `settings` file already exists, do you want to override the src directory (Y/n): ")
            if override in ["Y", "y", "", "yes"]:
                if os.path.exists(os.path.join(dst, file)):
                    os.remove(os.path.join(dst, file))
                    copy_quickstart_settings(src, dst)
                    print("The `settings` file was overriden.")
            elif override in ["n", "N", "no"]:
                pass
            else:
                override = input("The available options are: [Y/y/yes]/[N/n/no]. Press Enter to default to Y: ")
                if override in ["Y", "y", "yes", ""]:
                    if os.path.exists(os.path.join(dst, file)) and os.path.isdir(os.path.join(dst, file)):
                        os.remove(os.path.join(dst, file))
                        copy_quickstart_settings(src, dst)
                        print("The `settings` file was overriden.")
                elif override in ["n", "N", "no"]:
                    pass

    def copy_tree(self, src, dst, dir):
        try:
            shutil.copytree(os.path.join(src, dir), os.path.join(dst, dir))
        except FileExistsError:
            override = input(f"Hey, looks like a `{dir}` directory already exists, do you want to override the src directory (Y/n): ")
            if override in ["Y", "y", "", "yes"]:
                if os.path.exists(os.path.join(dst, dir)) and os.path.isdir(os.path.join(dst, dir)):
                    shutil.rmtree(os.path.join(dst, dir))
                    self.copy_tree(src, dst, dir)
                    print(f"The `{dir}` directory was overriden.")
            elif override in ["n", "N", "no"]:
                pass
            else:
                override = input("The available options are: [Y/y/yes]/[N/n/no]. Press Enter to default to Y: ")
                if override in ["Y", "y", "yes", ""]:
                    if os.path.exists(os.path.join(dst, dir)) and os.path.isdir(os.path.join(dst, dir)):
                        shutil.rmtree(os.path.join(dst, dir))
                        self.copy_tree(src, dst, dir)
                        print(f"The `{dir}` directory was overriden.")
                elif override in ["n", "N", "no"]:
                    pass
 
    
    def generate_settings(self, app_name, additional_settings):
        '''
        write to settings.py
        the default values, override if something already present
        '''
        SETTINGS = {
            'DIPOR_SOURCE_ROOT': '"src/"',
            'DIPOR_CONTENT_ROOT': '"content/"',
            'DIPOR_INITIAL_APP': '"/"',
            'DIPOR_EXTENSIONS': "['meta']",
            'DIPOR_FILE_FORMATS_ALLOWED': "['md', 'json']",
            'DIPOR_PRETTIFY': "True"
        }

        SETTINGS.update(additional_settings)
        settings_path = os.path.join(self.dst_root, app_name, "dipor_settings.py")
        with open(settings_path, "w") as f:
            for key, val in SETTINGS.items():
                f.write(f"{key} = {val}\n")
            f.write("\n\ninstance = globals()")
    
    def quickstart(self, *args, **kwargs):
        app_name = ""
        if args[0]:
            app_name = args[0][0]

        print ("running quikcstart")
        print("Getting the /src directory...")
        starters_route = os.path.join('starters', 'quickstart')
        self.copy_tree(os.path.join(self.src_root, starters_route), os.path.join(self.dst_root, app_name), 'src')
        print("Getting the /content directory...")
        self.copy_tree(os.path.join(self.src_root, starters_route), os.path.join(self.dst_root, app_name), 'content')
        print("Getting the settings file...")
        settings = {
            'DIPOR_SOURCE_ROOT': f"'{os.path.join(app_name, 'src')}'",
            'DIPOR_CONTENT_ROOT': f"'{os.path.join(app_name, 'content')}'",
            'DIPOR_INITIAL_APP': f"'{app_name}'"
        }
        self.generate_settings(app_name, settings)
        print("Building the /public repo")
        self.build_public(os.path.join(self.dst_root, app_name, 'src'), os.path.join(self.dst_root, app_name, 'content'), os.path.join(self.dst_root, app_name, 'settings.py'), os.path.join(self.dst_root, app_name, 'public'))
        self.serve_public(app_name)

    def bigbang(self, *args, **kwargs):
        app_name = ""
        if args[0]:
            app_name = args[0][0]
            
        print("running bigbang")
        os.mkdir(os.path.join(self.dst_root, app_name, 'src'))
        os.mkdir(os.path.join(self.dst_root, app_name, 'content'))
        settings = {
            'DIPOR_SOURCE_ROOT': f"'{os.path.join(app_name, 'src')}'",
            'DIPOR_CONTENT_ROOT': f"'{os.path.join(app_name, 'content')}'",
            'DIPOR_INITIAL_APP': f"'{app_name}'"
        }
        self.generate_settings(app_name, settings)
        self.build_public(os.path.join(self.dst_root, app_name, 'src'), os.path.join(self.dst_root, app_name, 'content'), os.path.join(self.dst_root, app_name, 'settings.py'), os.path.join(self.dst_root, app_name, 'public'))
        self.serve_public(app_name)

        # create src
        # create content
        # create settings
        # create a hello dipor barren page
        # build to create single page


    def soft_build(self, *args, **kwargs):
        print("running dev")
        # get the content
        # get the src
        # convert to public

    def hard_build(self, *args, **kwargs):
        print("running build")
        # clean the public folder
        # get the directories
        # convert to public
        # do post-processing (prettify/compress/make static easily available)
        # do an accessibility check
        # serve

    def default_action(self, *args, **kwargs):
        print("running default action")

    def use_theme(self, *args, **kwargs):
        print("running use theme")
        print(args)
        app_name = ""
        if args[0]:
            git_path = args[0][0]
            if len(args[0]) >= 2:
                app_name = args[0][1]
            print(f"git clone --quiet {git_path} {app_name}")
            os.system(f"git clone --quiet {git_path} {app_name}")
        else:
            print("Need a git Path")

    def build_public(self, src_path, content_path, settings_path, public_folder):
        '''
        !! actually, call hard_build for this? !!
        -- oh yes, yet to figure out build process --
        Assumes that /src and /content already exist
        In the Destination Directory
        And Builds the Public Directory
        '''
        builder_main(src_path, content_path, settings_path, public_folder)

    def serve_public(self, app_name):
        runserver(app_name)

def main():
    '''
    Entry Point for all Commands
    '''
    args = sys.argv
    cmd_execution = EntryPointCommands(args)
