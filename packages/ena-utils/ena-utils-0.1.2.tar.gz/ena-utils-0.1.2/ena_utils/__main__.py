import click
import os
import requests
import ast
from ena_utils.project import Project, ProjectSet
from ena_utils.project import write_table_template as write_project_template
from ena_utils.experiment import Experiment, ExperimentSet
from ena_utils.experiment import write_table_template as write_experiment_template
from ena_utils.run import Run, RunSet
from ena_utils.run import write_table_template as write_run_template
from ena_utils.sample import Sample, SampleSet
from ena_utils.sample import write_table_template as write_sample_template
from ena_utils.submission import Submission
from ena_utils.ftp import FtpConnect

@click.group()
@click.option('-v', '--verbose',
    is_flag = True,
    help = 'Print various messages.')
@click.pass_context
def cli(ctx, **kwargs):
    """ \b
A simple CLI toolbox to submit sequences to the European Nucleotide Archive (ENA)
    """
    ctx.obj = kwargs
    pass

@cli.command(help = 'Upload nucleotide sequences files.')
@click.pass_context
@click.option('-u', '--user',
    help = 'Webin user ID (ex: "Webin-12345").',
    prompt = 'Webin user ID',
    required = True)
@click.option('-p', '--password',
    help = 'Webin user password.',
    prompt = 'Webin user password',
    hide_input = True,
    required = True)
@click.option('-f', '--file_path',
    help = 'Path to the sequence files - wildcards are supported - (ex: "data/exp01_*.fastq.gz").',
    required = True)
@click.option('-h', '--host_address',
    help = 'FTP server address.',
    default = 'webin2.ebi.ac.uk',
    show_default = True)
@click.option('-v', '--verbose',
    is_flag = True,
    help = 'Print various messages.')
def upload(ctx, **kwargs):
    ctx.obj.update(kwargs)
    ftpconnect = FtpConnect(user = ctx.obj['user'],
        password = ctx.obj['password'],
        host = ctx.obj['host_address'])
    out = ftpconnect.mput(local = ctx.obj['file_path'],
        verbose = ctx.obj['verbose'])
    return out

@cli.group()
@click.option('-u', '--user',
    help = 'Webin user ID (ex: "Webin-12345").',
    prompt = 'Webin user ID',
    required = True)
@click.option('-p', '--password',
    help = 'Webin user password.',
    prompt = 'Webin user password',
    hide_input = True,
    required = True)
@click.option('--type',
    help = 'Type of submission.',
    default = 'ADD',
    show_default = True)
@click.option('-h', '--hold',
    help = 'A date in YYYY-MM-DD format until which the submission will be held confidential.')
@click.option('-s', '--server_address',
    help = 'Server address (default to the development server. Change "wwwdev" to "www" to submit to the production server).',
    default = "https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit/",
    show_default = True)
@click.option('--submission_xml',
    help = 'Path to the XML submission file that will be created.',
    default = 'submission.xml',
    show_default = True)
@click.pass_context
def submit(ctx, **kwargs):
    """ \b
Submit studies, experiments, runs and samples. \
- A study can be associated to multiple experiments. \
- An experiment can be associated to multiple runs. \
- An experiment can be associated to only one sample. \
- A run can be associated to only one experiment. \
- A sample can be associated to multiple experiments and runs.
    """
    ctx.obj.update(kwargs)
    pass

@submit.command(help = 'Submit a single study.')
@click.pass_context
@click.option('-a', '--alias',
    help = 'Study alias (ex: "my_new_great_study").',
    required = True)
@click.option('-t', '--title',
    help = 'Study title (ex: "A great study.").',
    required = True)
@click.option('-d', '--description',
    help = 'Study description (ex: "A longer study description.").',
    required = True)
@click.option('--study_xml',
    help = 'Path to the XML project file that will be created.',
    default = 'project.xml',
    show_default = True)
@click.option('-v', '--verbose',
    is_flag = True,
    help = 'Print various messages.')
def study(ctx, **kwargs):
    ctx.obj.update(kwargs)
    project_set = ProjectSet(project = Project(**kwargs))
    project_set.write_xml(file = ctx.obj['study_xml'])
    if ctx.obj['verbose']:
        print("Project XML file created in " + ctx.obj['study_xml'])
    submission = Submission(**ctx.obj)
    submission.write_xml(file = ctx.obj['submission_xml'])
    if ctx.obj['verbose']:
        print("Submission XML file created in " + ctx.obj['submission_xml'])
    response = requests.post(ctx.obj['server_address'],
        files = {
        'SUBMISSION': (os.path.basename(ctx.obj['submission_xml']), open(ctx.obj['submission_xml'], 'rb')),
        'PROJECT': (os.path.basename(ctx.obj['study_xml']), open(ctx.obj['study_xml'], 'rb')),
        },
        auth = (ctx.obj['user'], ctx.obj['password']))
    print(response.content.decode())
    return response

@submit.command(help = 'Submit multiple studies using a tab-delimited table.')
@click.pass_context
@click.option('--table',
    help = 'Path to a tab-delimited text file containing a list of studies \
to submit and their parameters. \
The file must contain one row per study and the first row must contain columns \
headers for alias, title and description.')
@click.option('-a', '--alias',
    help = 'Name of the table column containing studies aliases.',
    default = 'alias',
    show_default = True)
@click.option('-t', '--title',
    help = 'Name of the table column containing studies titles.',
    default = 'title',
    show_default = True)
@click.option('-d', '--description',
    help = 'Name of the table column containing studies descriptions.',
    default = 'description',
    show_default = True)
@click.option('--study_xml',
    help = 'Path to the XML project file that will be created.',
    default = 'study.xml',
    show_default = True)
@click.option('-v', '--verbose',
    is_flag = True,
    help = 'Print various messages.')
def study_set(ctx, **kwargs):
    ctx.obj.update(kwargs)
    project_set = ProjectSet(project = ctx.obj['table'],
        **kwargs)
    project_set.write_xml(file = ctx.obj['study_xml'])
    if ctx.obj['verbose']:
        print("Project XML file created in " + ctx.obj['study_xml'])
    submission = Submission(**ctx.obj)
    submission.write_xml(file = ctx.obj['submission_xml'])
    if ctx.obj['verbose']:
        print("Submission XML file created in " + ctx.obj['submission_xml'])
    response = requests.post(ctx.obj['server_address'],
        files = {
        'SUBMISSION': (os.path.basename(ctx.obj['submission_xml']), open(ctx.obj['submission_xml'], 'rb')),
        'PROJECT': (os.path.basename(ctx.obj['study_xml']), open(ctx.obj['study_xml'], 'rb')),
        },
        auth = (ctx.obj['user'], ctx.obj['password']))
    print(response.content.decode())
    return response


@submit.command(help = 'Submit a single experiment.')
@click.pass_context
@click.option('--study',
    help = 'Associated study accession number (ex: "PRJEB12345").',
    required = True)
@click.option('--sample',
    help = 'Associated sample name (ex: "sample_01").',
    required = True)
@click.option('-a', '--alias',
    help = 'Experiment alias (ex: "my_experiment_01").',
    required = True)
@click.option('-c', '--center',
    help = 'Center name.',
    required = True)
@click.option('-t', '--title',
    help = 'Experiment title (ex: "A great experiment").',
    required = True)
@click.option('-d', '--design',
    help = 'Experiment design (ex: "Targeted sequencing of gene X with primers A/B.").',
    required = True)
@click.option('--lib_name',
    help = 'Library name (ex: "LIB_01").')
@click.option('--lib_strategy',
    help = 'Library strategy (ex: "AMPLICON").',
    required = True)
@click.option('--lib_source',
    help = 'Library source (ex: "METAGENOMIC").',
    required = True)
@click.option('--lib_selection',
    help = 'Library selection (ex: "PCR").',
    required = True)
@click.option('--lib_length',
    help = 'Library nominal length (ex: "311").',
    required = True)
@click.option('--lib_protocol',
    help = 'Library construction protocol (ex: "As described previously in XY et al.").',
    required = True)
@click.option('--instrument',
    help = 'Instrument model (ex: "Illumina MiSeq").',
    required = True)
@click.option('--experiment_xml',
    help = 'Path to the XML experiment file that will be created.',
    default = 'experiment.xml',
    show_default = True)
@click.option('-v', '--verbose',
    is_flag = True,
    help = 'Print various messages.')
def experiment(ctx, **kwargs):
    ctx.obj.update(kwargs)
    experiment_set = ExperimentSet(experiment = Experiment(**kwargs))
    experiment_set.write_xml(file = ctx.obj['experiment_xml'])
    if ctx.obj['verbose']:
        print("Experiment XML file created in " + ctx.obj['experiment_xml'])
    submission = Submission(**ctx.obj)
    submission.write_xml(file = ctx.obj['submission_xml'])
    if ctx.obj['verbose']:
        print("Submission XML file created in " + ctx.obj['submission_xml'])
    response = requests.post(ctx.obj['server_address'],
        files = {
        'SUBMISSION': (os.path.basename(ctx.obj['submission_xml']), open(ctx.obj['submission_xml'], 'rb')),
        'EXPERIMENT': (os.path.basename(ctx.obj['experiment_xml']), open(ctx.obj['experiment_xml'], 'rb')),
        },
        auth = (ctx.obj['user'], ctx.obj['password']))
    print(response.content.decode())
    return response

@submit.command(help = 'Submit multiple experiments using a tab-delimited table.')
@click.pass_context
@click.option('--table',
    help = 'Path to a tab-delimited text file containing a list of experiments \
to submit and their parameters. \
The file must contain one row per experiment and the first row must contain columns \
headers for associated study accession number, associated sample name, alias, center, title, \
design, library name, library strategy, \
library source, library selection method, library nominal lenght, library protocol, \
and library sequencing instrument.')
@click.option('--study',
    help = 'Name of the table column containing associated study accession numbers.',
    default = 'study',
    show_default = True)
@click.option('--sample',
    help = 'Name of the table column containing associated sample names.',
    default = 'sample',
    show_default = True)
@click.option('-a', '--alias',
    help = 'Name of the table column containing aliases.',
    default = 'alias',
    show_default = True)
@click.option('-c', '--center',
    help = 'Name of the table column containing centers.',
    default = 'center',
    show_default = True)
@click.option('-t', '--title',
    help = 'Name of the table column containing titles.',
    default = 'title',
    show_default = True)
@click.option('-d', '--design',
    help = 'Name of the table column containing designs.',
    default = 'design',
    show_default = True)
@click.option('--lib_name',
    help = 'Name of the table column containing libraries names.',
    default = 'lib_name',
    show_default = True)
@click.option('--lib_strategy',
    help = 'Name of the table column containing libraries strategies.',
    default = 'lib_strategy',
    show_default = True)
@click.option('--lib_source',
    help = 'Name of the table column containing libraries sources.',
    default = 'lib_source',
    show_default = True)
@click.option('--lib_selection',
    help = 'Name of the table column containing libraries selection methods.',
    default = 'lib_selection',
    show_default = True)
@click.option('--lib_length',
    help = 'Name of the table column containing libraries nominal lengths.',
    default = 'lib_length',
    show_default = True)
@click.option('--lib_protocol',
    help = 'Name of the table column containing libraries protocols.',
    default = 'lib_protocol',
    show_default = True)
@click.option('--instrument',
    help = 'Name of the table column containing libraries sequencing instrument name.',
    default = 'instrument',
    show_default = True)
@click.option('--experiment_xml',
    help = 'Path to the XML experiment file that will be created.',
    default = 'experiment.xml',
    show_default = True)
@click.option('-v', '--verbose',
    is_flag = True,
    help = 'Print various messages.')
def experiment_set(ctx, **kwargs):
    ctx.obj.update(kwargs)
    experiment_set = ExperimentSet(experiment = ctx.obj['table'],
        **kwargs)
    experiment_set.write_xml(file = ctx.obj['experiment_xml'])
    if ctx.obj['verbose']:
        print("Experiment XML file created in " + ctx.obj['experiment_xml'])
    submission = Submission(**ctx.obj)
    submission.write_xml(file = ctx.obj['submission_xml'])
    if ctx.obj['verbose']:
        print("Submission XML file created in " + ctx.obj['submission_xml'])
    response = requests.post(ctx.obj['server_address'],
        files = {
        'SUBMISSION': (os.path.basename(ctx.obj['submission_xml']), open(ctx.obj['submission_xml'], 'rb')),
        'EXPERIMENT': (os.path.basename(ctx.obj['experiment_xml']), open(ctx.obj['experiment_xml'], 'rb')),
        },
        auth = (ctx.obj['user'], ctx.obj['password']))
    print(response.content.decode())
    return response

@submit.command(help = 'Submit a single run.')
@click.pass_context
@click.option('-e', '--experiment',
    help = 'Experiment reference (ex: "my_experiment_01").',
    required = True)
@click.option('-a', '--alias',
    help = 'Run alias (ex: "my_run_01.").',
    required = True)
@click.option('-c', '--center',
    help = 'Center name.',
    required = True)
@click.option('--filename',
    help = 'Comma-delimited paths to the sequence files (ex: "data/exp01_01_R1.fastq.gz,data/exp01_01_R2.fastq.gz").',
    required = True)
@click.option('--filetype',
    help = 'Comma-delimited type descriptions for the sequence files (ex: "fastq,fastq").',
    required = True)
@click.option('--run_xml',
    help = 'Path to the XML run file that will be created.',
    default = 'run.xml',
    show_default = True)
@click.option('-v', '--verbose',
    is_flag = True,
    help = 'Print various messages.')
def run(ctx, **kwargs):
    ctx.obj.update(kwargs)
    run_set = RunSet(run = Run(**kwargs))
    run_set.write_xml(file = ctx.obj['run_xml'])
    if ctx.obj['verbose']:
        print("Run XML file created in " + ctx.obj['run_xml'])
    submission = Submission(**ctx.obj)
    submission.write_xml(file = ctx.obj['submission_xml'])
    if ctx.obj['verbose']:
        print("Submission XML file created in " + ctx.obj['submission_xml'])
    response = requests.post(ctx.obj['server_address'],
        files = {
        'SUBMISSION': (os.path.basename(ctx.obj['submission_xml']), open(ctx.obj['submission_xml'], 'rb')),
        'RUN': (os.path.basename(ctx.obj['run_xml']), open(ctx.obj['run_xml'], 'rb')),
        },
        auth = (ctx.obj['user'], ctx.obj['password']))
    print(response.content.decode())
    return response

@submit.command(help = 'Submit multiple runs using a tab-delimited table.')
@click.pass_context
@click.option('--table',
    help = 'Path to a tab-delimited text file containing a list of runs to submit and their parameters. \
The file must contain one row per run and the first row must contain columns headers for alias, center, \
and files. \
The command options must be replaced by their corresponding parameters file headers. \
Using a parameters files allows to submit multiple runs at one time.')
@click.option('-e', '--experiment',
    help = 'Name of the table column containing references to associated experiments.',
    default = 'experiment',
    show_default = True)
@click.option('-a', '--alias',
    help = 'Name of the table column containing runs aliases.',
    default = 'alias',
    show_default = True)
@click.option('-c', '--center',
    help = 'Name of the table column containing center names.',
    default = 'center',
    show_default = True)
@click.option('--filename',
    help = 'Name of the table column containing comma-delimited paths to the associated sequence files.',
    default = 'filename',
    show_default = True)
@click.option('--filetype',
    help = 'Name of the table column containing comma-delimited type description for the associated sequence files.',
    default = 'filetype',
    show_default = True)
@click.option('--run_xml',
    help = 'Path to the XML run file that will be created.',
    default = 'run.xml',
    show_default = True)
@click.option('-v', '--verbose',
    is_flag = True,
    help = 'Print various messages.')
def run_set(ctx, **kwargs):
    ctx.obj.update(kwargs)
    run_set = RunSet(run = ctx.obj['table'],
        **kwargs)
    run_set.write_xml(file = ctx.obj['run_xml'])
    if ctx.obj['verbose']:
        print("Run XML file created in " + ctx.obj['run_xml'])
    submission = Submission(**ctx.obj)
    submission.write_xml(file = ctx.obj['submission_xml'])
    if ctx.obj['verbose']:
        print("Submission XML file created in " + ctx.obj['submission_xml'])
    response = requests.post(ctx.obj['server_address'],
        files = {
        'SUBMISSION': (os.path.basename(ctx.obj['submission_xml']), open(ctx.obj['submission_xml'], 'rb')),
        'RUN': (os.path.basename(ctx.obj['run_xml']), open(ctx.obj['run_xml'], 'rb')),
        },
        auth = (ctx.obj['user'], ctx.obj['password']))
    print(response.content.decode())
    return response


@submit.command(help = 'Submit a single sample.')
@click.pass_context
@click.option('-a', '--alias',
    help = 'Sample alias (ex: "sample_01").',
    required = True)
@click.option('--title',
    help = 'Sample title (ex: "My great sample 01.").',
    required = True)
@click.option('--taxon_id',
    help = 'Sample taxon ID attribute (ex: "10090").',
    required = True)
@click.option('--scientific_name',
    help = 'Sample scientific name attribute (ex: "Mus musculus").',
    required = True)
@click.option('--common_name',
    help = 'Sample common name attribute (ex: "house mouse").',
    required = True)
@click.option('--attributes',
    help = 'JSON-formatted string of sample attributes key:value pairs (ex: {"age":"2 weeks","strain":"C57BL/6"}).')
@click.option('--sample_xml',
    help = 'Path to the XML sample file that will be created.',
    default = 'sample.xml',
    show_default = True)
@click.option('-v', '--verbose',
    is_flag = True,
    help = 'Print various messages.')
def sample(ctx, **kwargs):
    ctx.obj.update(kwargs)
    sample_set = SampleSet(sample = Sample(alias = ctx.obj['alias'],
        title = ctx.obj['title'],
        taxon_id = ctx.obj['taxon_id'],
        scientific_name = ctx.obj['scientific_name'],
        common_name = ctx.obj['common_name'],
        **ast.literal_eval(ctx.obj['attributes'])))
    sample_set.write_xml(file = ctx.obj['sample_xml'])
    if ctx.obj['verbose']:
        print("Sample XML file created in " + ctx.obj['sample_xml'])
    submission = Submission(**ctx.obj)
    submission.write_xml(file = ctx.obj['submission_xml'])
    if ctx.obj['verbose']:
        print("Submission XML file created in " + ctx.obj['submission_xml'])
    response = requests.post(ctx.obj['server_address'],
        files = {
        'SUBMISSION': (os.path.basename(ctx.obj['submission_xml']), open(ctx.obj['submission_xml'], 'rb')),
        'SAMPLE': (os.path.basename(ctx.obj['sample_xml']), open(ctx.obj['sample_xml'], 'rb')),
        },
        auth = (ctx.obj['user'], ctx.obj['password']))
    print(response.content.decode())
    return response

@submit.command(help = 'Submit multiple samples using a tab-delimited table.')
@click.pass_context
@click.option('--table',
    help = 'Path to a tab-delimited text file containing a list of samples to submit and their parameters. \
The file must contain one row per sample and the first row must contain columns headers for at least alias, title, \
taxon ID, scientific name and common name. Additional columns are submitted as additional sample attributes. \
Taxon ID, scientific name and common name must comply with ENA standard organism taxonomic description \
(ex: for Mus musculus, taxon ID is "10090", scientific name is "Mus musculus" and common name is "house mouse")',
    required = True)
@click.option('-a', '--alias',
    help = 'Name of the table column containing sample alias.',
    default = 'alias',
    show_default = True)
@click.option('--title',
    help = 'Name of the table column containing sample title.',
    default = 'title',
    show_default = True)
@click.option('--taxon_id',
    help = 'Name of the table column containing sample taxon ID attribute.',
    default = 'taxon_id',
    show_default = True)
@click.option('--scientific_name',
    help = 'Name of the table column containing sample scientific name attribute.',
    default = 'scientific_name',
    show_default = True)
@click.option('--common_name',
    help = 'Name of the table column containing sample common name attribute.',
    default = 'common_name',
    show_default = True)
@click.option('--sample_xml',
    help = 'Path to the XML sample file that will be created.',
    default = 'sample.xml',
    show_default = True)
@click.option('-v', '--verbose',
    is_flag = True,
    help = 'Print various messages.')
def sample_set(ctx, **kwargs):
    ctx.obj.update(kwargs)
    sample_set = SampleSet(sample = ctx.obj['table'],
        **kwargs)
    sample_set.write_xml(file = ctx.obj['sample_xml'])
    if ctx.obj['verbose']:
        print("Sample XML file created in " + ctx.obj['sample_xml'])
    submission = Submission(**ctx.obj)
    submission.write_xml(file = ctx.obj['submission_xml'])
    if ctx.obj['verbose']:
        print("Submission XML file created in " + ctx.obj['submission_xml'])
    response = requests.post(ctx.obj['server_address'],
        files = {
        'SUBMISSION': (os.path.basename(ctx.obj['submission_xml']), open(ctx.obj['submission_xml'], 'rb')),
        'SAMPLE': (os.path.basename(ctx.obj['sample_xml']), open(ctx.obj['sample_xml'], 'rb')),
        },
        auth = (ctx.obj['user'], ctx.obj['password']))
    print(response.content.decode())
    return response

@cli.group()
@click.pass_context
def write_template(ctx, **kwargs):
    """ \b
Write template files.
    """
    ctx.obj.update(kwargs)
    pass

@write_template.command(help = 'Write a template table for study submission.')
@click.pass_context
@click.option('-t', '--table',
    help = 'Path to the table file that will be created.',
    default = 'project.txt',
    show_default = True)
@click.option('-v', '--verbose',
    is_flag = True,
    help = 'Print various messages.')
def study_table(ctx, **kwargs):
    ctx.obj.update(kwargs)
    write_project_template(file = ctx.obj['table'])
    if ctx.obj['verbose']:
        print('Template table writen to ' + ctx.obj['table'])

@write_template.command(help = 'Write a template table for experiment submission.')
@click.pass_context
@click.option('-t', '--table',
    help = 'Path to the table file that will be created.',
    default = 'experiment.txt',
    show_default = True)
@click.option('-v', '--verbose',
    is_flag = True,
    help = 'Print various messages.')
def experiment_table(ctx, **kwargs):
    ctx.obj.update(kwargs)
    write_experiment_template(file = ctx.obj['table'])
    if ctx.obj['verbose']:
        print('Template table writen to ' + ctx.obj['table'])

@write_template.command(help = 'Write a template table for run submission.')
@click.pass_context
@click.option('-t', '--table',
    help = 'Path to the table file that will be created.',
    default = 'run.txt',
    show_default = True)
@click.option('-v', '--verbose',
    is_flag = True,
    help = 'Print various messages.')
def run_table(ctx, **kwargs):
    ctx.obj.update(kwargs)
    write_run_template(file = ctx.obj['table'])
    if ctx.obj['verbose']:
        print('Template table writen to ' + ctx.obj['table'])

@write_template.command(help = 'Write a template table for sample submission.')
@click.pass_context
@click.option('-t', '--table',
    help = 'Path to the table file that will be created.',
    default = 'sample.txt',
    show_default = True)
@click.option('-v', '--verbose',
    is_flag = True,
    help = 'Print various messages.')
def sample_table(ctx, **kwargs):
    ctx.obj.update(kwargs)
    write_sample_template(file = ctx.obj['table'])
    if ctx.obj['verbose']:
        print('Template table writen to ' + ctx.obj['table'])

if __name__ == '__main__':
    cli(obj={})
