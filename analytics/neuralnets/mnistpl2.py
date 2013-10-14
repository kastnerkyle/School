#!/usr/bin/env python
from pylearn2.models import mlp
from pylearn2.costs.mlp import Dropout
from pylearn2.training_algorithms import sgd
from pylearn2.termination_criteria import EpochCounter
from pylearn2.datasets import mnist
from pylearn2.space import Conv2DSpace
from pylearn2.train import Train
from pylearn2.train_extensions import best_params

trn = mnist.MNIST('train',
                  one_hot=True)

tst = mnist.MNIST('test',
                  one_hot=True)

in_space = Conv2DSpace(shape=(28, 28),
                       num_channels=1)

h1 = mlp.ConvRectifiedLinear(output_channels=64,
                             kernel_shape=(5, 5),
                             pool_shape=(4, 4),
                             pool_stride=(2, 2),
                             layer_name='conv1',
                             irange = .01)

h2 = mlp.ConvRectifiedLinear(output_channels=64,
                             kernel_shape=(5, 5),
                             pool_shape = (4, 4),
                             pool_stride = (2, 2),
                             layer_name = 'conv2',
                             irange = .01)

output_layer = mlp.Softmax(layer_name='output',
                           n_classes=10,
                           irange=.01)

layers = [h1, h2, output_layer]

ann = mlp.MLP(layers,
              input_space=in_space)

trainer = sgd.SGD(learning_rate=.05,
                  batch_size=500,
                  termination_criterion=EpochCounter(100),
                  cost=Dropout(input_include_probs={
                               'conv1': .8, 'conv2': .5, 'output': .5}),
                  monitoring_dataset=tst)

watcher = best_params.MonitorBasedSaveBest(
    channel_name="output_misclass",
    save_path="mnistpl2_best.pkl")

experiment = Train(dataset=trn,
                   model=ann,
                   algorithm=trainer,
                   extensions=[watcher])

experiment.main_loop()
