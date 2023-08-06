# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datasetinsights',
 'datasetinsights.commands',
 'datasetinsights.datasets',
 'datasetinsights.datasets.dummy',
 'datasetinsights.datasets.protos',
 'datasetinsights.datasets.unity_perception',
 'datasetinsights.estimators',
 'datasetinsights.evaluation_metrics',
 'datasetinsights.io',
 'datasetinsights.io.downloader',
 'datasetinsights.stats',
 'datasetinsights.stats.visualization']

package_data = \
{'': ['*'],
 'datasetinsights': ['configs/*'],
 'datasetinsights.stats.visualization': ['font/*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'codetiming>=1.2.0,<2.0.0',
 'cython>=0.29.14,<0.30.0',
 'dash==1.12.0',
 'dask[complete]>=2.14.0,<3.0.0',
 'google-cloud-storage>=1.24.1,<=1.28.1',
 'jupyter>=1.0.0,<2.0.0',
 'kornia>=0.1.4,<0.2.0',
 'numpy>=1.17,<1.18',
 'nuscenes-devkit>=1.0.2,<1.0.3',
 'pandas>=1.0.1,<2.0.0',
 'plotly>=4.4.1,<5.0.0',
 'pycocotools>=2.0.0,<3.0.0',
 'pyquaternion>=0.9.5,<0.10.0',
 'pytorch-ignite>=0.3.0,<0.4.0',
 'tensorboardx>=2.0,<3.0',
 'tensorflow>=2.2.0,<3.0.0',
 'torch>=1.4.0,<1.5.0',
 'torchvision>=0.5,<0.6',
 'tqdm>=4.45.0,<5.0.0',
 'yacs>=0.1.6,<0.2.0']

entry_points = \
{'console_scripts': ['datasetinsights = datasetinsights.__main__:entrypoint']}

setup_kwargs = {
    'name': 'datasetinsights',
    'version': '0.2.0rc2',
    'description': 'Synthetic dataset insights.',
    'long_description': "Dataset Insights\n================\nThis repo enables users to understand their synthetic datasets by exposing the metrics collected when the dataset\nwas created e.g. object count, label distribution, etc. The easiest way to use Dataset Insights is\nto run our jupyter notebook provided in our docker image `unitytechnologies/datasetinsights`\n\nRequirements\n============\n\nThe Dataset Insight notebooks assume that the user has already generated a synthetic dataset using the Unity Perception package.\nTo learn how to create a synthetic dataset using Unity please see the\n[perception documentation](https://github.com/Unity-Technologies/com.unity.perception).\n\n\n## Running the Dataset Insights Jupyter Notebook Locally\nYou can either run the notebook by installing our python package or by using our docker image.\n\n### Running a Notebook Locally Using Docker\n\n#### Requirements\n[Docker](https://docs.docker.com/get-docker/) installed.\n\n#### Steps\n1. Run notebook server using docker\n\n```bash\ndocker run \\\n  -p 8888:8888 \\\n  -v $HOME/data:/data \\\n  -t unitytechnologies/datasetinsights:latest\n```\nThis command mounts directory `$HOME/data` in your local filesystem to `/data` inside the container.\nIf you are loading a dataset generated locally from a Unity app, replace this path with the root of your app's persistent data folder.\n\nExample persistent data paths from [SynthDet](https://github.com/Unity-Technologies/synthdet):\n* OSX: `~/Library/Application\\ Support/UnityTechnologies/SynthDet`\n* Linux: `$XDG_CONFIG_HOME/unity3d/UnityTechnologies/SynthDet`\n* Windows: `%userprofile%\\AppData\\LocalLow\\UnityTechnologies\\SynthDet`\n\n\n2. Go to `http://localhost:8888` in a web browser to open the Jupyter browser.\n3. Open and run the example notebook in `/datasetinsights/notebooks/` or create your own.\n   (todo replace docker container gcr.io/unity-ai-thea-test/thea with public links)\n\n## Running a Dataset Insights Jupyter Notebook via Google Cloud Platform (GCP)\n- To run the notebook on GCP's AI platform follow\n[these instructions](https://cloud.google.com/ai-platform/notebooks/docs/custom-container) and use the container `unitytechnologies/datasetinsights:latest`\n- Alternately, to run the notebook on kubeflow follow [these steps](https://www.kubeflow.org/docs/notebooks/setup/)\n\n### Download Dataset from Unity Simulation\n\n[Unity Simulation](https://unity.com/products/simulation) provides a powerful platform for running simulations at large scale. You can use the provided cli script to download Perception datasets generated in Unity Simulation:\n\n```bash\npython -m datasetinsights.scripts.usim_download \\\n  --data-root=$HOME/data \\\n  --run-execution-id=<run-execution-id> \\\n  --auth-token=<xxx>\n```\n\nThe `auth-token` can be generated using the Unity Simulation [CLI](https://github.com/Unity-Technologies/Unity-Simulation-Docs/blob/master/doc/cli.md#usim-inspect-auth). This script will download the synthetic dataset for the requested [run-execution-id](https://github.com/Unity-Technologies/Unity-Simulation-Docs/blob/master/doc/cli.md#argument-descriptions).\n\nIf the `--include-binary` flag is present, the images will also be downloaded. This might take a long time, depending on the size of the generated dataset.\n\n### Download SynthDet Dataset\n\nDownload SynthDet public dataset from GCS, including GroceriesReal and Synthetic dataset. You can use the provided cli script to download public dataset to reproduce our work.\n\nHere is the command line for GroceriesReal dataset download:\n\n```bash\npython -m datasetinsights.scripts.public_download \\\n  --name=GroceriesReal \\\n  --data-root=$HOME/data \\\n```\n",
    'author': 'Unity AI Perception Team',
    'author_email': 'perception@unity3d.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
