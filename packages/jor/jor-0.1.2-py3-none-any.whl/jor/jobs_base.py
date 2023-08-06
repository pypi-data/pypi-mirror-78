import os


class JobsBase:

    # slurm options
    name = 'job'
    time = '0-23:59:59'
    mem = '5G'
    cpus_per_task = 1

    def __init__(self, path_prefix=None):
        if path_prefix is None:
            self.path_prefix = '.'
        self.path_prefix = path_prefix

    def __len__(self):
        return len(self._jobs)

    def _get_output_path(self, *args, **kwargs):
        output_folder = self._get_output_folder()
        output_fname = self._get_output_fname(*args, **kwargs)
        return os.path.join(output_folder, output_fname)

    def _get_output_folder(self):
        output_folder = self.name
        if self.path_prefix is not None:
            output_folder = os.path.join(self.path_prefix, output_folder)
        return output_folder

    def _get_output_fname(self, *args, **kwargs):

        if (len(args) == 0) and (len(kwargs) == 0):
            raise ValueError("No parameters given, can't automatically generate filename")

        outfname = ''
        for arg in args:
            outfname += f'{arg}_'
        for k, v in kwargs.items():
            outfname += f'{k}{v}_'
        outfname = outfname[:-1]  # drop trailing '_'
        if outfname == '':
            raise ValueError

        outfname += f'.{self.output_suffix}'

        return outfname

    @property
    def output_paths(self):
        return [self._get_output_path(**self._jobs[i])
                for i in range(len(self))]

    @property
    def missing_outputs(self):
        return [output for output in self.output_paths
                if not os.path.exists(output)]

    @property
    def is_output_complete(self):
        if len(self.missing_outputs) == 0:
            return True
        else:
            return False

    def collect(self):
        pass  # assume that, by default, nothing needs to be collected
    