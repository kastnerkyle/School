#!/usr/bin/env python
from pylearn2.models import mlp, maxout
from pylearn2.training_algorithms import sgd
from pylearn2.termination_criteria import EpochCounter
from pylearn2.datasets import cifar10
from pylearn2.space import Conv2DSpace
from pylearn2.train import Train
from pylearn2.train_extensions import best_params

trn = cifar10.CIFAR10('train',
                      toronto_prepro=True,
                      one_hot=True,
                      axes=('c', 0, 1, 'b'))

tst = cifar10.CIFAR10('test',
                      toronto_prepro=True,
                      one_hot=True,
                      axes=('c', 0, 1, 'b'))

in_space = Conv2DSpace(shape=(32, 32),
                       num_channels=3,
                       axes=('c', 0, 1, 'b'))

h1 = maxout.MaxoutConvC01B(num_channels=32,
                           num_pieces=1,
                           kernel_shape=(5, 5),
                           pool_shape=(3, 3),
                           pool_stride=(2, 2),
                           layer_name='conv1',
                           irange = .01)

output_layer = mlp.Softmax(layer_name='output',
                           n_classes=10,
                           irange=.01)

layers = [h1, output_layer]

ann = mlp.MLP(layers,
              input_space=in_space)

trainer = sgd.SGD(learning_rate=.01,
                  init_momentum=.9,
                  batch_size=128,
                  termination_criterion=EpochCounter(10),
                  monitoring_dataset=tst)

watcher = best_params.MonitorBasedSaveBest(
    channel_name="output_misclass",
    save_path="cifarpl2_best.pkl")

experiment = Train(dataset=trn,
                   model=ann,
                   algorithm=trainer,
                   extensions=[watcher])

experiment.main_loop()
