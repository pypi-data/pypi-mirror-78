import shutil
import subprocess
from pathlib import Path
from unittest import TestCase, mock


from bigflow.cli import cli


class ProjectScaffoldE2ETestCase(TestCase):
    def tearDown(self):
        clear_project_leftovers(Path('my_project'))


class ProjectScaffoldE2E(ProjectScaffoldE2ETestCase):
    @mock.patch('bigflow.cli.gcp_bucket_input')
    @mock.patch('bigflow.cli.gcp_project_input')
    @mock.patch('bigflow.cli.project_type_input')
    @mock.patch('bigflow.cli.project_name_input')
    def test_should_create_basic_project(self, project_name_input_mock, project_type_input_mock, gcp_project_input_mock, gcp_bucket_input_mock):
        # given
        project_name_input_mock.return_value = 'my_project'
        project_type_input_mock.return_value = 'basic'
        gcp_project_input_mock.return_value = 'my_gcp_project'
        gcp_bucket_input_mock.return_value = 'my_gcp_bucket'

        # when
        cli(['start-project'])

        # then
        self.scaffolded_basic_project_should_have_one_environment()

        # and
        self.scaffolded_project_tests_should_work()

    @mock.patch('bigflow.cli.project_number_input')
    @mock.patch('bigflow.cli.environment_name_input')
    @mock.patch('bigflow.cli.gcp_bucket_input')
    @mock.patch('bigflow.cli.gcp_project_input')
    @mock.patch('bigflow.cli.project_type_input')
    @mock.patch('bigflow.cli.project_name_input')
    def test_should_create_advanced_project(self, project_name_input_mock, project_type_input_mock, gcp_project_input_mock, gcp_bucket_input_mock, environment_name_input, project_number_input_mock):
        # given
        project_name_input_mock.return_value = 'my_project'
        project_type_input_mock.return_value = 'advanced'
        gcp_project_input_mock.side_effect = ['dev_project', 'test_project', 'prod_project']
        gcp_bucket_input_mock.side_effect = ['dev_bucket', 'test_bucket', 'prod_bucket']
        environment_name_input.side_effect = ['DEV', 'TEST', 'PROD']
        project_number_input_mock.return_value = '3'

        # when
        cli(['start-project'])

        # then
        self.scaffolded_advanced_project_should_have_three_environments()

        # and
        self.scaffolded_project_tests_should_work()

    def scaffolded_project_tests_should_work(self):
        output = subprocess.getoutput("python -m unittest discover -s my_project/test -p '*.py'")
        self.assertEqual(output[-2:], 'OK')

    def scaffolded_basic_project_should_have_one_environment(self):
        self.check_file_content(Path('my_project') / 'deployment_config.py', '''from bigflow.configuration import Config

deployment_config = Config(name='dev',
                           properties={
                               'docker_repository': 'test_repository',
                               'gcp_project_id': 'my_gcp_project',
                               'dags_bucket': 'my_gcp_bucket'
                           })
''')
        self.check_file_content(Path('my_project') / 'workflows' / 'internationalports' / 'config.py', '''from bigflow.bigquery import DatasetConfig

INTERNAL_TABLES = ['ports', 'more_ports']

EXTERNAL_TABLES = {}

dataset_config = DatasetConfig(env='dev',
                               project_id='my_gcp_project',
                               dataset_name='bigflow_test',
                               internal_tables=INTERNAL_TABLES,
                               external_tables=EXTERNAL_TABLES
                               )''')
        self.check_file_content(Path('my_project') / 'workflows' / 'wordcount' / 'config.py', '''from bigflow.configuration import Config

workflow_config = Config(name='dev',
                           properties={
                               'gcp_project_id': 'my_gcp_project',
                               'staging_location': 'beam_jobs/beam_runner/staging',
                               'temp_location': 'beam_jobs/beam_runner/temp',
                               'region': 'europe-west1',
                               'machine_type': 'n1-standard-1',
                               'bucket': 'my_gcp_bucket'
                           })
''')

    def scaffolded_advanced_project_should_have_three_environments(self):
        self.check_file_content(Path('my_project') / 'deployment_config.py', '''from bigflow.configuration import Config

deployment_config = Config(name='dev',
                           properties={
                               'docker_repository': 'test_repository',
                               'gcp_project_id': 'dev_project',
                               'dags_bucket': 'dev_bucket'
                           }).add_configuration(name='TEST',
                           properties={
                               'gcp_project_id': 'test_project',
                               'dags_bucket': 'test_bucket'
                           }).add_configuration(name='PROD',
                           properties={
                               'gcp_project_id': 'prod_project',
                               'dags_bucket': 'prod_bucket'
                           })
''')
        self.check_file_content(Path('my_project') / 'workflows' / 'internationalports' / 'config.py', '''from bigflow.bigquery import DatasetConfig

INTERNAL_TABLES = ['ports', 'more_ports']

EXTERNAL_TABLES = {}

dataset_config = DatasetConfig(env='dev',
                               project_id='dev_project',
                               dataset_name='bigflow_test',
                               internal_tables=INTERNAL_TABLES,
                               external_tables=EXTERNAL_TABLES
                               ).add_configuration(env='TEST',
                               project_id='test_project').add_configuration(env='PROD',
                               project_id='prod_project')''')
        self.check_file_content(Path('my_project') / 'workflows' / 'wordcount' / 'config.py', '''from bigflow.configuration import Config

workflow_config = Config(name='dev',
                           properties={
                               'gcp_project_id': 'dev_project',
                               'staging_location': 'beam_jobs/beam_runner/staging',
                               'temp_location': 'beam_jobs/beam_runner/temp',
                               'region': 'europe-west1',
                               'machine_type': 'n1-standard-1',
                               'bucket': 'dev_bucket'
                           }).add_configuration(name='TEST',
                           properties={
                               'gcp_project_id': 'test_project',
                               'dags_bucket': 'test_bucket'
                           }).add_configuration(name='PROD',
                           properties={
                               'gcp_project_id': 'prod_project',
                               'dags_bucket': 'prod_bucket'
                           })
''')

    def check_file_content(self, path, template):
        with open(path.resolve(), 'r') as f:
            self.assertEquals(f.read(), template)


def clear_project_leftovers(image_dir: Path):
    shutil.rmtree(image_dir, ignore_errors=True)
