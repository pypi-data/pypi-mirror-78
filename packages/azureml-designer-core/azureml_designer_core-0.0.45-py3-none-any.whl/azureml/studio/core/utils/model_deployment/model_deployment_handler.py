import os
from pathlib import Path
from shutil import copyfile
from azureml.studio.core.utils.jsonutils import dump_to_json_file
from azureml.studio.core.io.any_directory import AnyDirectory


CONDA_FILE_NAME = 'conda_env.yaml'
SCORE_FILE_NAME = 'score.py'
SAMPLE_FILE_NAME = AnyDirectory._SAMPLES_FILE_PATH
SCHEMA_FILE_NAME = AnyDirectory._SCHEMA_FILE_PATH


class ModelDeploymentHandler:
    score_template_path = ''
    conda_template_path = ''

    def __init__(self):
        self._data_schema = None
        self._sample_data = None

    @property
    def data_schema(self):
        return self._data_schema

    @data_schema.setter
    def data_schema(self, value):
        self._data_schema = value

    @property
    def sample_data(self):
        return self._sample_data

    @sample_data.setter
    def sample_data(self, value):
        self._sample_data = value

    def dump_score_file(self, save_to):
        src_file = Path.resolve(Path(__file__)).parent / self.score_template_path
        copyfile(src_file, save_to)

    def dump_conda_file(self, save_to):
        src_file = Path.resolve(Path(__file__)).parent / self.conda_template_path
        copyfile(src_file, save_to)

    def dump_schema_file(self, save_to):
        dump_to_json_file(self.data_schema, save_to)

    def dump_sample_file(self, save_to):
        dump_to_json_file(self.sample_data, save_to)

    def dump_deployment_files(self, save_to):
        self.dump_score_file(os.path.join(save_to, SCORE_FILE_NAME))
        self.dump_conda_file(os.path.join(save_to, CONDA_FILE_NAME))
        if self.data_schema:
            self.dump_schema_file(os.path.join(save_to, SCHEMA_FILE_NAME))
        if self.sample_data:
            self.dump_sample_file(os.path.join(save_to, SAMPLE_FILE_NAME))


class BaseLearnerDeploymentHandler(ModelDeploymentHandler):
    score_template_path = 'resources/base_learner/score.py'
    conda_template_path = 'resources/base_learner/conda_env.yaml'


class ClusterModelDeploymentHandler(ModelDeploymentHandler):
    score_template_path = 'resources/cluster_model/score.py'
    conda_template_path = 'resources/cluster_model/conda_env.yaml'


class PytorchModelDeploymentHandler(ModelDeploymentHandler):
    score_template_path = 'resources/pytorch_model/score.py'
    conda_template_path = 'resources/pytorch_model/conda_env.yaml'


class SVDRecommendationDeploymentHandler(ModelDeploymentHandler):
    score_template_path = 'resources/svd_recommender/score.py'
    conda_template_path = 'resources/svd_recommender/conda_env.yaml'


class VowpalWabbitModelDeploymentHandler(ModelDeploymentHandler):
    score_template_path = 'resources/vowpal_wabbit_model/score.py'
    conda_template_path = 'resources/vowpal_wabbit_model/conda_env.yaml'


class WideAndDeepRecommendationDeploymentHandler(ModelDeploymentHandler):
    score_template_path = 'resources/wide_and_deep_recommender/score.py'
    conda_template_path = 'resources/wide_and_deep_recommender/conda_env.yaml'
