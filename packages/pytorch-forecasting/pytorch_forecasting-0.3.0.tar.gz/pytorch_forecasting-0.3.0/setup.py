# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytorch_forecasting',
 'pytorch_forecasting.data',
 'pytorch_forecasting.models',
 'pytorch_forecasting.models.nbeats',
 'pytorch_forecasting.models.temporal_fusion_transformer']

package_data = \
{'': ['*']}

install_requires = \
['cloudpickle',
 'matplotlib',
 'optuna>=2.0.0,<3.0.0',
 'pandas>=1.1.0,<2.0.0',
 'pytorch-lightning>=0.9.0,<0.10.0',
 'scikit-learn>=0.23,<0.24',
 'scipy',
 'statsmodels',
 'torch>=1.6,<2.0']

extras_require = \
{'github-actions': ['pytest-github-actions-annotate-failures']}

setup_kwargs = {
    'name': 'pytorch-forecasting',
    'version': '0.3.0',
    'description': 'Forecasting timeseries with PyTorch - dataloaders, normalizers, metrics and models',
    'long_description': '![](./docs/source/_static/logo.svg)\n\nPytorch Forecasting aims to ease timeseries forecasting with neural networks.\nIt specificially provides a class to wrap timeseries datasets and a number of PyTorch models.\n\n# Installation\n\nIf you are working windows, you need to first install PyTorch with\n\n`pip install torch -f https://download.pytorch.org/whl/torch_stable.html`.\n\nOtherwise, you can proceed with\n\n`pip install pytorch-forecasting`\n\nVisit the documentation at [https://pytorch-forecasting.readthedocs.io](https://pytorch-forecasting.readthedocs.io).\n\n# Available models\n\n- [Temporal Fusion Transformers for Interpretable Multi-horizon Time Series Forecasting](https://arxiv.org/pdf/1912.09363.pdf)\n- [N-Beats](http://arxiv.org/abs/1905.10437)\n\n# Usage\n\n```python\nimport pytorch_lightning as pl\nfrom pytorch_lightning.callbacks import EarlyStopping\n\nfrom pytorch_forecasting import TimeSeriesDataSet, TemporalFusionTransformer\n\n# load data\ndata = ...\n\n# define dataset\nmax_encode_length = 36\nmax_prediction_length = 6\ntraining_cutoff = "YYYY-MM-DD"  # day for cutoff\n\ntraining = TimeSeriesDataSet(\n    data[lambda x: x.date <= training_cutoff],\n    time_idx= ...,\n    target= ...,\n    group_ids=[ ... ],\n    max_encode_length=max_encode_length,\n    max_prediction_length=max_prediction_length,\n    static_categoricals=[ ... ],\n    static_reals=[ ... ],\n    time_varying_known_categoricals=[ ... ],\n    time_varying_known_reals=[ ... ],\n    time_varying_unknown_categoricals=[ ... ],\n    time_varying_unknown_reals=[ ... ],\n)\n\n\nvalidation = TimeSeriesDataSet.from_dataset(training, data, min_prediction_idx=training.index.time.max() + 1, stop_randomization=True)\nbatch_size = 128\ntrain_dataloader = training.to_dataloader(train=True, batch_size=batch_size, num_workers=2)\nval_dataloader = validation.to_dataloader(train=False, batch_size=batch_size, num_workers=2)\n\n\nearly_stop_callback = EarlyStopping(monitor="val_loss", min_delta=1e-4, patience=1, verbose=False, mode="min")\nlr_logger = LearningRateLogger()\ntrainer = pl.Trainer(\n    max_epochs=100,\n    gpus=0,\n    gradient_clip_val=0.1,\n    early_stop_callback=early_stop_callback,\n    limit_train_batches=30,\n    callbacks=[lr_logger],\n)\n\n\ntft = TemporalFusionTransformer.from_dataset(\n    training,\n    learning_rate=0.03,\n    hidden_size=32,\n    attention_head_size=1,\n    dropout=0.1,\n    hidden_continuous_size=16,\n    output_size=7,\n    loss=QuantileLoss(),\n    log_interval=2,\n    reduce_on_plateau_patience=4\n)\nprint(f"Number of parameters in network: {tft.size()/1e3:.1f}k")\n\n# find optimal learning rate\nres = trainer.lr_find(\n    tft, train_dataloader=train_dataloader, val_dataloaders=val_dataloader, early_stop_threshold=1000.0, max_lr=0.3,\n)\n\nprint(f"suggested learning rate: {res.suggestion()}")\nfig = res.plot(show=True, suggest=True)\nfig.show()\n\ntrainer.fit(\n    tft, train_dataloader=train_dataloader, val_dataloaders=val_dataloader,\n)\n```\n',
    'author': 'Jan Beitner',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pytorch-forecasting.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
