# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tf_raft', 'tf_raft.datasets', 'tf_raft.layers', 'tf_raft.losses']

package_data = \
{'': ['*']}

install_requires = \
['albumentations>=0.4.6,<0.5.0',
 'tensorflow-addons>=0.11.1,<0.12.0',
 'tensorflow>=2.3.0,<3.0.0']

setup_kwargs = {
    'name': 'tf-raft',
    'version': '0.1.2',
    'description': 'RAFT (Recurrent All Pairs Field Transforms for Optical Flow) implementation via tf.keras',
    'long_description': "# tf-raft\nRAFT (Recurrent All Pairs Field Transforms for Optical Flow, Teed et. al., ECCV2020) implementation via tf.keras\n\n## Original resources\n- [RAFT: Recurrent All Pairs Field Transforms for Optical Flow](https://arxiv.org/abs/2003.12039)\n- https://github.com/princeton-vl/RAFT\n\n## Installation\n\n```\n$ pip install tf-raft\n```\n\nor you can simply clone this repository.\n\n### Dependencies\n- TensorFlow\n- TensorFlow-addons\n- albumentations\n\nsee details in `pyoroject.toml`\n\n## Optical flow datasets\n[MPI-Sintel](http://sintel.is.tue.mpg.de/) or [FlyingChairs](https://lmb.informatik.uni-freiburg.de/resources/datasets/FlyingChairs.en.html#flyingchairs) datasets are relatively light. See more datasets in the [oirignal repository](https://github.com/princeton-vl/RAFT)\n\n## Usage\n\n``` python\nfrom tf_raft.model import RAFT, SmallRAFT\nfrom tf_raft.losses import sequence_loss, end_point_error\n\n# iters means number of recurrent update of flow \nraft = RAFT(iters=iters)\nraft.compile(\n    optimizer=optimizer,\n    loss=sequence_loss,\n    epe=end_point_error\n)\n\nraft.fit(\n    dataset,\n    epochs=epochs,\n    callbacks=callbacks,\n)\n```\n\nIn practice, you are required to prepare dataset, optimizer, callbacks etc, check details in `train.py`.\n\n## Note\nThough I have tried to reproduce the original implementation faithfully, there is some difference between it and my implementation (mainly because of used framework: PyTorch/TensorFlow);\n\n- The original implements cuda-based correlation function but I don't. My TF-based implementation works well, but cuda-based one may runs faster.\n- I have trained my model only on MPI-Sintel dataset in my private environment (GCP with P100 accelerator). The model has been trained well, but not reached the best score reported in the paper (trained on multiple datasets).\n- The original uses mixed-precision. This may get traininig much faster, but I don't. TensorFlow also enables mixed-precision with few additional lines, see https://www.tensorflow.org/guide/mixed_precision if interested.\n\n## References\n- https://github.com/princeton-vl/RAFT\n- https://github.com/NVIDIA/flownet2-pytorch\n- https://github.com/NVlabs/PWC-Net\n",
    'author': 'Daigo Hirooka',
    'author_email': 'daigo.hirooka@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/daigo0927/tf-raft',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
