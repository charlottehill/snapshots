from hairball.plugins import HairballPlugin
from kelp.kelpplugin import KelpPlugin
import kurt
import os


class SnapshotPlugin(KelpPlugin):

    """The simple plugin name should go on the first comment line.

    The plugin description should start on the third line and can span as many
    lines as needed, though all newlines will be treated as a single space.

    If you are seeing this message it means you need to define a docstring for
    your plugin.

    """
    @staticmethod
    def get_paths(image, project_name, image_name, sprite_name):
        directory = os.path.join('{}images'.format(project_name))
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = '{0}{1}.png'.format(sprite_name,
                                       image_name).replace('/', '_')
        path = os.path.join(directory, filename)
        return path, path

    def save_png(self, projectName, image, image_name, sprite_name=''):
        path, url = self.get_paths(image, projectName, image_name, sprite_name)
        image.save(path)
        return url

    @classmethod
    def to_scratch_blocks(cls, heading, scripts):
        """Output the scripts in an html-ready scratch blocks format."""
        data = []
        for script in scripts:
            data.append('{0}\n'.format(script.stringify(True)))
        return ('<div>{0}</div>\n'.format(''.join(data)))

    def _process(self, path, **kwargs):
        for file in os.listdir(path):
            if file.endswith(".oct"):
                oct = kurt.Project.load(os.path.abspath(os.path.join(path, file)))
                if not getattr(oct, 'hairball_prepared', False):
                    KelpPlugin.tag_reachable_scripts(oct)
        return self.analyze(path, **kwargs)

