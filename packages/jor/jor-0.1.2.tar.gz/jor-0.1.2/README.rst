jor
===

**jor** (JOb Runner) keeps track of jobs. Jobs are specified 
in a simple format and can then be run collectively with a 
simple command, mindful of which outputs already exist.
Jobs can optionally be run in a *conda* environment or in a 
*Singularity* container, and can be run either locally or 
submitted to a compute node with *slurm*.

**jor** is particularly useful

* if a large number of different jobs needs to be run
* for parameter sweeps
* in an HPC environment: **jor** can submit jobs with ``slurm``
* for reproducible research results: **jor** can run jobs in a Singularity container

Usage
-----

To use **jor** requires 3 preparatory steps:

#. Write a simple Python wrapper around the actual computations, specifying the job's inputs and outputs
#. Collect all the jobs in a todo-list
#. Write up some runtime-arguments in a config file

These steps are described in detail below.

Once these preparations are done, all jobs can be run with

.. code-block:: bash

    jor run

and the status of the jobs specified in the todo-list can be inspected with

.. code-block:: bash

    jor status

Preparatory steps
-----------------

.. _the-job-wrapper:

1. The Job-wrapper
..................

This is the most complex of the 3 steps. It requires to implement 4-5 functions that specify

#. the parameters for each job
#. the output folder for each job
#. the name of the output file for each job
#. the actual computation for each job
#. if applicable, how to concatenate all outputs of this job into a single file

.. note::

    All these steps would be necessary no matter if ``jor`` is used to perform 
    the jobs' computations or not, the only difference is that, to use ``jor`` they 
    need to be specified in a particular way. Thus ``jor`` doesn't lead to much
    code overhead.

Here is a template:

.. code-block:: Python

    import pathlib
    import jor


    class Jobs(jor.JobsBase):

        # slurm options
        name = 'job'
        time = '0-23:59:59'
        mem = '5G'
        cpus_per_task = 1

        def __init__(self, n=3, path_prefix='.'):

            # init base class
            super().__init__(path_prefix=path_prefix)

            # store job-specific keyword arguments
            self.n = int(n)
            
            # assemble a list of jobs
            self._mk_jobs()

        def _mk_jobs(self):
            """Generates the attribute ``self._jobs``

            ``self._jobs`` is a list of dictionaries, containing one dictionary
            for each jobs to be run. Each of these dictionaries specifies the 
            parameters for each individual job.
            """
            self._jobs = [
                dict(index=i)
                for i in range(self.n)
            ]

        def _get_output_folder(self):
            """Return output folder for jobs

            Output folder is the ``path_prefix``, followed by the name of a subfolder
            encoding the arguments given in the constructor.
            """
            output_folder = pathlib.Path(self.path_prefix) / f'example{self.n}'
            return str(output_folder)

        def _get_output_fname(self, index):
            """Return output file name for a given job

            The particular job is specified by the arguments to this function,
            which match the keys of the dictionaries in ``self._jobs`` (cf.
            :func:`self._mk_jobs`).
            """
            outfname = f'ind{index}.txt'
            return outfname

        def execute(self, i):
            """This function performs the actual work

            Parameters
            ----------
            i : int between 0 and number of jobs (``len(self._jobs)``)
                indicating the index in ``self._jobs`` from which to take
                the dictionary with this job's parameter values
            """
            myargs = self._jobs[i]
            output_path = self._get_output_path(**myargs)

            # do the work and write outcomes to file ``output_path``
            with open(output_path, 'wt') as f:
                f.write(str(myargs) + '\n')

        def collect(self):
            """Concatenates all outputs into a common output

            This function is optional and can be implemented if desired for 
            the particular job. It is called by running ``jor collect`` on the 
            command line.
            """ 
            pass

.. note::

    #. The wrapper needs to be a Python file containaing a class ``Jobs``, derived from ``jor.JobsBase``
    #. The indicated ``slurm`` options are defaults inherited from ``jor.JobsBase``, i.e. they only need to be specified if a different value is desired

To adapt this to a specific application:

#. Adapt the constructor to take job-specific arguments
#. Reimplement ``_mk_jobs``
#. Reimplement ``_get_output_folder``
#. Reimplement ``_get_output_fname``
#. Reimplement ``execute``
#. If applicable, reimplement ``collect``

2. The todo-list
................

The file containing the todo-list is a *YAML* file named 
``todo.yaml`` by default.
It has the following format:

.. code-block:: yaml

    jobs:
    - jobmodule: ./jobs_example.py
      jobargs: n=3
    - jobmodule: ./jobs_example.py
      jobargs: n=4

There can be an arbitrary number of jobs specified in this file.

.. note::
    
    #. The file needs to start with ``jobs:``
    #. Each job is specified by 2 lines, 1 starting with ``- jobmodule:`` the other with an indented ``jobargs:``.
    #. The argument for ``jobmodule:`` is the name (or path to) the Python file containing the wrapper code.
    #. The argument to ``jobargs:`` is a comma-separated list of keyword-arguments for the constructor of the ``Jobs`` class in the wrapper file. It needs to be valid Python and can be empty if no keyword arguments are necessary.

3. The config file
..................

The config file needs to be named ``jor.cfg`` and needs to 
reside in the working directory from which ``jor`` is called.
It has the following format:

.. code-block:: cfg

    [global]
    path-prefix = output
    overwrite-output = False

    [run]
    todo-list = todo.yaml

    [submit]
    scheduler = local
    partition = day
    sif =
    condaenv =

    [collect]
    missing-output = ignore

The configuration options have the following meaning:

.. list-table:: Configuration options
    :header-rows: 1

    * - Keyword
      - Allowed values
      - Meaning
    * - ``path-prefix``
      - file-system paths
      - the job-wrapper should receive ``path_prefix`` as a keyword argument in the ``Jobs`` constructor, and should prefix all internally generated output-paths with the value of ``path-prefix``
    * - ``overwrite-output``
      - ``True`` or ``False``
      - if ``False`` ``jor`` will check which outputs already exist and only run jobs that result in the remaining outputs
    * - ``todo-list``
      - a filename
      - file name containing todo-list, by default this is ``todo.yaml``, there's probably no reason to change this
    * - ``scheduler``
      - ``local`` or ``slurm``
      - if ``local`` jobs will be run in order locally; if ``slurm`` one job-array will be submitted via ``slurm``'s ``sbatch`` command per entry in the todo-list
    * - ``partition``
      - a valid ``slurm`` partition (queue) name
      - ignored if ``scheduler = local``
    * - ``sif``
      - either empty or path to a Singularity container
      - if not empty all jobs will be run in this container
    * - ``condaenv``
      - either empty of name of a ``conda`` environment
      - if not empty, this ``conda`` environment will be activated before running each job
    * - ``missing-output``
      - ``ignore`` or ``raise``
      - in case the job-wrapper implements a ``collect`` method to concatenate outputs, this specifies how missing files are handled: if ``ignore`` missing outputs will be ignored, if ``raise`` missing outputs will cause concatenation to abort

.. note:: 

    All configuration-options in ``jor.cfg`` can be 
    overwritten in the command-line call to ``jor``.

Example
-------

An example is provided in the ``examples`` subfolder. The file ``jobs_example.py`` 
contains the code shown `above <the-job-wrapper_>`__. Likewise the ``todo.yaml`` 
and ``jor.cfg`` files from above can be found there. Calling

.. code-block:: bash

    jor run

returns

.. code-block:: bash

    [jor] Submitting job: ./jobs_example.py
    [jor] Submitting job: ./jobs_example.py

and inspecting the ``output`` folder

.. code-block:: bash

    ls -R output

shows that all output files are present:

.. code-block:: bash

    example3 example4

    output/example3:
    ind0.txt ind1.txt ind2.txt

    output/example4:
    ind0.txt ind1.txt ind2.txt ind3.txt