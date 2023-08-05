## Pytorch Model Summary -- Keras style `model.summary()` for PyTorch
[![PyPI version fury.io](https://badge.fury.io/py/pytorch-model-summary.svg)](https://pypi.python.org/pypi/pytorch-model-summary/)
[![Downloads](https://pepy.tech/badge/pytorch-model-summary)](https://pepy.tech/project/pytorch-model-summary)


It is a Keras style model.summary() implementation for PyTorch

This is an Improved PyTorch library of [modelsummary](https://github.com/graykode/modelsummary). Like in `modelsummary`, **It does not care with number of Input parameter!**

### Improvements:
- For user defined pytorch layers, now `summary` can show layers inside it
    - some assumptions: when is an user defined layer, if any weight/params/bias is trainable, then it is assumed that this layer is trainable (but only trainable params are counted in Tr. Params #)
- Adding column counting only trainable parameters (it makes sense when there are user defined layers)
- Showing all input/output shapes, instead of showing only the first one
    - example: LSTM layer return a Tensor and a tuple (Tensor, Tensor), then output_shape has three set of values
- Printing: table width defined dynamically
- Adding option to add hierarchical summary in output
- Adding batch_size value (when provided) in table footer
- fix bugs

### Parameters
**Default values have keras behavior**
```python
summary(model, *inputs, batch_size=-1, show_input=False, show_hierarchical=False,
        print_summary=False, max_depth=1, show_parent_layers=False):
```

- `model`: pytorch model object
- `*inputs`: ...
- `batch_size`: if provided, it is printed in summary table
- `show_input`: show input shape. Otherwise, output shape for each layer. **(Default: False)**
- `show_hierarchical`: in addition of summary table, return hierarchical view of the model **(Default: False)**
- `print_summary`: when true, is not required to use print function outside `summary` method **(Default: False)**
- `max_depth`: it specifies how many times it can go inside user defined layers to show them **(Default: 1)**
- `show_parent_layer`: it adds a column to show parent layers path until reaching current layer in depth. **(Default: False)**



```python
import torch
import torch.nn as nn
import torch.nn.functional as F

from pytorch_model_summary import summary


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)


# show input shape
print(summary(Net(), torch.zeros((1, 1, 28, 28)), show_input=True))

# show output shape
print(summary(Net(), torch.zeros((1, 1, 28, 28)), show_input=False))

# show output shape and hierarchical view of net
print(summary(Net(), torch.zeros((1, 1, 28, 28)), show_input=False, show_hierarchical=True))

```

```
-----------------------------------------------------------------------
      Layer (type)         Input Shape         Param #     Tr. Param #
=======================================================================
          Conv2d-1      [1, 1, 28, 28]             260             260
          Conv2d-2     [1, 10, 12, 12]           5,020           5,020
       Dropout2d-3       [1, 20, 8, 8]               0               0
          Linear-4            [1, 320]          16,050          16,050
          Linear-5             [1, 50]             510             510
=======================================================================
Total params: 21,840
Trainable params: 21,840
Non-trainable params: 0
-----------------------------------------------------------------------
```
```
-----------------------------------------------------------------------
      Layer (type)        Output Shape         Param #     Tr. Param #
=======================================================================
          Conv2d-1     [1, 10, 24, 24]             260             260
          Conv2d-2       [1, 20, 8, 8]           5,020           5,020
       Dropout2d-3       [1, 20, 8, 8]               0               0
          Linear-4             [1, 50]          16,050          16,050
          Linear-5             [1, 10]             510             510
=======================================================================
Total params: 21,840
Trainable params: 21,840
Non-trainable params: 0
-----------------------------------------------------------------------
```
```
-----------------------------------------------------------------------
      Layer (type)        Output Shape         Param #     Tr. Param #
=======================================================================
          Conv2d-1     [1, 10, 24, 24]             260             260
          Conv2d-2       [1, 20, 8, 8]           5,020           5,020
       Dropout2d-3       [1, 20, 8, 8]               0               0
          Linear-4             [1, 50]          16,050          16,050
          Linear-5             [1, 10]             510             510
=======================================================================
Total params: 21,840
Trainable params: 21,840
Non-trainable params: 0
-----------------------------------------------------------------------
=========================== Hierarchical Summary ===========================
Net(
  (conv1): Conv2d(1, 10, kernel_size=(5, 5), stride=(1, 1)), 260 params
  (conv2): Conv2d(10, 20, kernel_size=(5, 5), stride=(1, 1)), 5,020 params
  (conv2_drop): Dropout2d(p=0.5), 0 params
  (fc1): Linear(in_features=320, out_features=50, bias=True), 16,050 params
  (fc2): Linear(in_features=50, out_features=10, bias=True), 510 params
), 21,840 params
============================================================================
```


## Quick Start 

Just download with **pip**

`pip install pytorch-model-summary` and
```python
from pytorch_model_summary import summary
``` 
or 
```python
import pytorch_model_summary as pms
pms.summary([params])
```
to avoid reference conflicts with other methods in your code

You can use this library like this. If you want to see more detail, Please see examples below.

## Examples using different set of parameters

Run example using Transformer Model in [Attention is all you need paper(2017)](https://arxiv.org/abs/1706.03762)

1) showing **input shape**
```python
# show input shape
pms.summary(model, enc_inputs, dec_inputs, show_input=True, print_summary=True)
```
```
-----------------------------------------------------------------------------------
      Layer (type)                     Input Shape         Param #     Tr. Param #
===================================================================================
         Encoder-1                          [1, 5]      17,332,224      17,329,152
         Decoder-2     [1, 5], [1, 5], [1, 5, 512]      22,060,544      22,057,472
          Linear-3                     [1, 5, 512]           3,584           3,584
===================================================================================
Total params: 39,396,352
Trainable params: 39,390,208
Non-trainable params: 6,144
-----------------------------------------------------------------------------------
```

2) showing **output shape** and **batch_size** in table. In addition, also **hierarchical summary** version
```python
# show output shape and batch_size in table. In addition, also hierarchical summary version
pms.summary(model, enc_inputs, dec_inputs, batch_size=1, show_hierarchical=True, print_summary=True)
```
```
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      Layer (type)                                                                                                                                                                            Output Shape         Param #     Tr. Param #
===========================================================================================================================================================================================================================================
         Encoder-1                                                                                         [1, 5, 512], [1, 8, 5, 5], [1, 8, 5, 5], [1, 8, 5, 5], [1, 8, 5, 5], [1, 8, 5, 5], [1, 8, 5, 5]      17,332,224      17,329,152
         Decoder-2     [1, 5, 512], [1, 8, 5, 5], [1, 8, 5, 5], [1, 8, 5, 5], [1, 8, 5, 5], [1, 8, 5, 5], [1, 8, 5, 5], [1, 8, 5, 5], [1, 8, 5, 5], [1, 8, 5, 5], [1, 8, 5, 5], [1, 8, 5, 5], [1, 8, 5, 5]      22,060,544      22,057,472
          Linear-3                                                                                                                                                                               [1, 5, 7]           3,584           3,584
===========================================================================================================================================================================================================================================
Total params: 39,396,352
Trainable params: 39,390,208
Non-trainable params: 6,144
Batch size: 1
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


================================ Hierarchical Summary ================================

Transformer(
  (encoder): Encoder(
    (src_emb): Embedding(6, 512), 3,072 params
    (pos_emb): Embedding(6, 512), 3,072 params
    (layers): ModuleList(
      (0): EncoderLayer(
        (enc_self_attn): MultiHeadAttention(
          (W_Q): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_K): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_V): Linear(in_features=512, out_features=512, bias=True), 262,656 params
        ), 787,968 params
        (pos_ffn): PoswiseFeedForwardNet(
          (conv1): Conv1d(512, 2048, kernel_size=(1,), stride=(1,)), 1,050,624 params
          (conv2): Conv1d(2048, 512, kernel_size=(1,), stride=(1,)), 1,049,088 params
        ), 2,099,712 params
      ), 2,887,680 params
      (1): EncoderLayer(
        (enc_self_attn): MultiHeadAttention(
          (W_Q): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_K): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_V): Linear(in_features=512, out_features=512, bias=True), 262,656 params
        ), 787,968 params
        (pos_ffn): PoswiseFeedForwardNet(
          (conv1): Conv1d(512, 2048, kernel_size=(1,), stride=(1,)), 1,050,624 params
          (conv2): Conv1d(2048, 512, kernel_size=(1,), stride=(1,)), 1,049,088 params
        ), 2,099,712 params
      ), 2,887,680 params
      (2): EncoderLayer(
        (enc_self_attn): MultiHeadAttention(
          (W_Q): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_K): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_V): Linear(in_features=512, out_features=512, bias=True), 262,656 params
        ), 787,968 params
        (pos_ffn): PoswiseFeedForwardNet(
          (conv1): Conv1d(512, 2048, kernel_size=(1,), stride=(1,)), 1,050,624 params
          (conv2): Conv1d(2048, 512, kernel_size=(1,), stride=(1,)), 1,049,088 params
        ), 2,099,712 params
      ), 2,887,680 params
      (3): EncoderLayer(
        (enc_self_attn): MultiHeadAttention(
          (W_Q): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_K): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_V): Linear(in_features=512, out_features=512, bias=True), 262,656 params
        ), 787,968 params
        (pos_ffn): PoswiseFeedForwardNet(
          (conv1): Conv1d(512, 2048, kernel_size=(1,), stride=(1,)), 1,050,624 params
          (conv2): Conv1d(2048, 512, kernel_size=(1,), stride=(1,)), 1,049,088 params
        ), 2,099,712 params
      ), 2,887,680 params
      (4): EncoderLayer(
        (enc_self_attn): MultiHeadAttention(
          (W_Q): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_K): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_V): Linear(in_features=512, out_features=512, bias=True), 262,656 params
        ), 787,968 params
        (pos_ffn): PoswiseFeedForwardNet(
          (conv1): Conv1d(512, 2048, kernel_size=(1,), stride=(1,)), 1,050,624 params
          (conv2): Conv1d(2048, 512, kernel_size=(1,), stride=(1,)), 1,049,088 params
        ), 2,099,712 params
      ), 2,887,680 params
      (5): EncoderLayer(
        (enc_self_attn): MultiHeadAttention(
          (W_Q): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_K): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_V): Linear(in_features=512, out_features=512, bias=True), 262,656 params
        ), 787,968 params
        (pos_ffn): PoswiseFeedForwardNet(
          (conv1): Conv1d(512, 2048, kernel_size=(1,), stride=(1,)), 1,050,624 params
          (conv2): Conv1d(2048, 512, kernel_size=(1,), stride=(1,)), 1,049,088 params
        ), 2,099,712 params
      ), 2,887,680 params
    ), 17,326,080 params
  ), 17,332,224 params
  (decoder): Decoder(
    (tgt_emb): Embedding(7, 512), 3,584 params
    (pos_emb): Embedding(6, 512), 3,072 params
    (layers): ModuleList(
      (0): DecoderLayer(
        (dec_self_attn): MultiHeadAttention(
          (W_Q): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_K): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_V): Linear(in_features=512, out_features=512, bias=True), 262,656 params
        ), 787,968 params
        (dec_enc_attn): MultiHeadAttention(
          (W_Q): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_K): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_V): Linear(in_features=512, out_features=512, bias=True), 262,656 params
        ), 787,968 params
        (pos_ffn): PoswiseFeedForwardNet(
          (conv1): Conv1d(512, 2048, kernel_size=(1,), stride=(1,)), 1,050,624 params
          (conv2): Conv1d(2048, 512, kernel_size=(1,), stride=(1,)), 1,049,088 params
        ), 2,099,712 params
      ), 3,675,648 params
      (1): DecoderLayer(
        (dec_self_attn): MultiHeadAttention(
          (W_Q): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_K): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_V): Linear(in_features=512, out_features=512, bias=True), 262,656 params
        ), 787,968 params
        (dec_enc_attn): MultiHeadAttention(
          (W_Q): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_K): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_V): Linear(in_features=512, out_features=512, bias=True), 262,656 params
        ), 787,968 params
        (pos_ffn): PoswiseFeedForwardNet(
          (conv1): Conv1d(512, 2048, kernel_size=(1,), stride=(1,)), 1,050,624 params
          (conv2): Conv1d(2048, 512, kernel_size=(1,), stride=(1,)), 1,049,088 params
        ), 2,099,712 params
      ), 3,675,648 params
      (2): DecoderLayer(
        (dec_self_attn): MultiHeadAttention(
          (W_Q): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_K): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_V): Linear(in_features=512, out_features=512, bias=True), 262,656 params
        ), 787,968 params
        (dec_enc_attn): MultiHeadAttention(
          (W_Q): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_K): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_V): Linear(in_features=512, out_features=512, bias=True), 262,656 params
        ), 787,968 params
        (pos_ffn): PoswiseFeedForwardNet(
          (conv1): Conv1d(512, 2048, kernel_size=(1,), stride=(1,)), 1,050,624 params
          (conv2): Conv1d(2048, 512, kernel_size=(1,), stride=(1,)), 1,049,088 params
        ), 2,099,712 params
      ), 3,675,648 params
      (3): DecoderLayer(
        (dec_self_attn): MultiHeadAttention(
          (W_Q): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_K): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_V): Linear(in_features=512, out_features=512, bias=True), 262,656 params
        ), 787,968 params
        (dec_enc_attn): MultiHeadAttention(
          (W_Q): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_K): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_V): Linear(in_features=512, out_features=512, bias=True), 262,656 params
        ), 787,968 params
        (pos_ffn): PoswiseFeedForwardNet(
          (conv1): Conv1d(512, 2048, kernel_size=(1,), stride=(1,)), 1,050,624 params
          (conv2): Conv1d(2048, 512, kernel_size=(1,), stride=(1,)), 1,049,088 params
        ), 2,099,712 params
      ), 3,675,648 params
      (4): DecoderLayer(
        (dec_self_attn): MultiHeadAttention(
          (W_Q): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_K): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_V): Linear(in_features=512, out_features=512, bias=True), 262,656 params
        ), 787,968 params
        (dec_enc_attn): MultiHeadAttention(
          (W_Q): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_K): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_V): Linear(in_features=512, out_features=512, bias=True), 262,656 params
        ), 787,968 params
        (pos_ffn): PoswiseFeedForwardNet(
          (conv1): Conv1d(512, 2048, kernel_size=(1,), stride=(1,)), 1,050,624 params
          (conv2): Conv1d(2048, 512, kernel_size=(1,), stride=(1,)), 1,049,088 params
        ), 2,099,712 params
      ), 3,675,648 params
      (5): DecoderLayer(
        (dec_self_attn): MultiHeadAttention(
          (W_Q): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_K): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_V): Linear(in_features=512, out_features=512, bias=True), 262,656 params
        ), 787,968 params
        (dec_enc_attn): MultiHeadAttention(
          (W_Q): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_K): Linear(in_features=512, out_features=512, bias=True), 262,656 params
          (W_V): Linear(in_features=512, out_features=512, bias=True), 262,656 params
        ), 787,968 params
        (pos_ffn): PoswiseFeedForwardNet(
          (conv1): Conv1d(512, 2048, kernel_size=(1,), stride=(1,)), 1,050,624 params
          (conv2): Conv1d(2048, 512, kernel_size=(1,), stride=(1,)), 1,049,088 params
        ), 2,099,712 params
      ), 3,675,648 params
    ), 22,053,888 params
  ), 22,060,544 params
  (projection): Linear(in_features=512, out_features=7, bias=False), 3,584 params
), 39,396,352 params


======================================================================================
```

3) showing **layers until depth 2**
```python
# show layers until depth 2
pms.summary(model, enc_inputs, dec_inputs, max_depth=2, print_summary=True)
```
```
-----------------------------------------------------------------------------------------------
      Layer (type)                                Output Shape         Param #     Tr. Param #
===============================================================================================
       Embedding-1                                 [1, 5, 512]           3,072           3,072
       Embedding-2                                 [1, 5, 512]           3,072               0
    EncoderLayer-3                   [1, 5, 512], [1, 8, 5, 5]       2,887,680       2,887,680
    EncoderLayer-4                   [1, 5, 512], [1, 8, 5, 5]       2,887,680       2,887,680
    EncoderLayer-5                   [1, 5, 512], [1, 8, 5, 5]       2,887,680       2,887,680
    EncoderLayer-6                   [1, 5, 512], [1, 8, 5, 5]       2,887,680       2,887,680
    EncoderLayer-7                   [1, 5, 512], [1, 8, 5, 5]       2,887,680       2,887,680
    EncoderLayer-8                   [1, 5, 512], [1, 8, 5, 5]       2,887,680       2,887,680
       Embedding-9                                 [1, 5, 512]           3,584           3,584
      Embedding-10                                 [1, 5, 512]           3,072               0
   DecoderLayer-11     [1, 5, 512], [1, 8, 5, 5], [1, 8, 5, 5]       3,675,648       3,675,648
   DecoderLayer-12     [1, 5, 512], [1, 8, 5, 5], [1, 8, 5, 5]       3,675,648       3,675,648
   DecoderLayer-13     [1, 5, 512], [1, 8, 5, 5], [1, 8, 5, 5]       3,675,648       3,675,648
   DecoderLayer-14     [1, 5, 512], [1, 8, 5, 5], [1, 8, 5, 5]       3,675,648       3,675,648
   DecoderLayer-15     [1, 5, 512], [1, 8, 5, 5], [1, 8, 5, 5]       3,675,648       3,675,648
   DecoderLayer-16     [1, 5, 512], [1, 8, 5, 5], [1, 8, 5, 5]       3,675,648       3,675,648
         Linear-17                                   [1, 5, 7]           3,584           3,584
===============================================================================================
Total params: 39,396,352
Trainable params: 39,390,208
Non-trainable params: 6,144
-----------------------------------------------------------------------------------------------
```

4) showing **deepest layers**
```python
# show deepest layers
pms.summary(model, enc_inputs, dec_inputs, max_depth=None, print_summary=True)
```
```
-----------------------------------------------------------------------
      Layer (type)        Output Shape         Param #     Tr. Param #
=======================================================================
       Embedding-1         [1, 5, 512]           3,072           3,072
       Embedding-2         [1, 5, 512]           3,072               0
          Linear-3         [1, 5, 512]         262,656         262,656
          Linear-4         [1, 5, 512]         262,656         262,656
          Linear-5         [1, 5, 512]         262,656         262,656
          Conv1d-6        [1, 2048, 5]       1,050,624       1,050,624
          Conv1d-7         [1, 512, 5]       1,049,088       1,049,088
          Linear-8         [1, 5, 512]         262,656         262,656
          Linear-9         [1, 5, 512]         262,656         262,656
         Linear-10         [1, 5, 512]         262,656         262,656
         Conv1d-11        [1, 2048, 5]       1,050,624       1,050,624
         Conv1d-12         [1, 512, 5]       1,049,088       1,049,088
         Linear-13         [1, 5, 512]         262,656         262,656
         Linear-14         [1, 5, 512]         262,656         262,656
         Linear-15         [1, 5, 512]         262,656         262,656
         Conv1d-16        [1, 2048, 5]       1,050,624       1,050,624
         Conv1d-17         [1, 512, 5]       1,049,088       1,049,088
         Linear-18         [1, 5, 512]         262,656         262,656
         Linear-19         [1, 5, 512]         262,656         262,656
         Linear-20         [1, 5, 512]         262,656         262,656
         Conv1d-21        [1, 2048, 5]       1,050,624       1,050,624
         Conv1d-22         [1, 512, 5]       1,049,088       1,049,088
         Linear-23         [1, 5, 512]         262,656         262,656
         Linear-24         [1, 5, 512]         262,656         262,656
         Linear-25         [1, 5, 512]         262,656         262,656
         Conv1d-26        [1, 2048, 5]       1,050,624       1,050,624
         Conv1d-27         [1, 512, 5]       1,049,088       1,049,088
         Linear-28         [1, 5, 512]         262,656         262,656
         Linear-29         [1, 5, 512]         262,656         262,656
         Linear-30         [1, 5, 512]         262,656         262,656
         Conv1d-31        [1, 2048, 5]       1,050,624       1,050,624
         Conv1d-32         [1, 512, 5]       1,049,088       1,049,088
      Embedding-33         [1, 5, 512]           3,584           3,584
      Embedding-34         [1, 5, 512]           3,072               0
         Linear-35         [1, 5, 512]         262,656         262,656
         Linear-36         [1, 5, 512]         262,656         262,656
         Linear-37         [1, 5, 512]         262,656         262,656
         Linear-38         [1, 5, 512]         262,656         262,656
         Linear-39         [1, 5, 512]         262,656         262,656
         Linear-40         [1, 5, 512]         262,656         262,656
         Conv1d-41        [1, 2048, 5]       1,050,624       1,050,624
         Conv1d-42         [1, 512, 5]       1,049,088       1,049,088
         Linear-43         [1, 5, 512]         262,656         262,656
         Linear-44         [1, 5, 512]         262,656         262,656
         Linear-45         [1, 5, 512]         262,656         262,656
         Linear-46         [1, 5, 512]         262,656         262,656
         Linear-47         [1, 5, 512]         262,656         262,656
         Linear-48         [1, 5, 512]         262,656         262,656
         Conv1d-49        [1, 2048, 5]       1,050,624       1,050,624
         Conv1d-50         [1, 512, 5]       1,049,088       1,049,088
         Linear-51         [1, 5, 512]         262,656         262,656
         Linear-52         [1, 5, 512]         262,656         262,656
         Linear-53         [1, 5, 512]         262,656         262,656
         Linear-54         [1, 5, 512]         262,656         262,656
         Linear-55         [1, 5, 512]         262,656         262,656
         Linear-56         [1, 5, 512]         262,656         262,656
         Conv1d-57        [1, 2048, 5]       1,050,624       1,050,624
         Conv1d-58         [1, 512, 5]       1,049,088       1,049,088
         Linear-59         [1, 5, 512]         262,656         262,656
         Linear-60         [1, 5, 512]         262,656         262,656
         Linear-61         [1, 5, 512]         262,656         262,656
         Linear-62         [1, 5, 512]         262,656         262,656
         Linear-63         [1, 5, 512]         262,656         262,656
         Linear-64         [1, 5, 512]         262,656         262,656
         Conv1d-65        [1, 2048, 5]       1,050,624       1,050,624
         Conv1d-66         [1, 512, 5]       1,049,088       1,049,088
         Linear-67         [1, 5, 512]         262,656         262,656
         Linear-68         [1, 5, 512]         262,656         262,656
         Linear-69         [1, 5, 512]         262,656         262,656
         Linear-70         [1, 5, 512]         262,656         262,656
         Linear-71         [1, 5, 512]         262,656         262,656
         Linear-72         [1, 5, 512]         262,656         262,656
         Conv1d-73        [1, 2048, 5]       1,050,624       1,050,624
         Conv1d-74         [1, 512, 5]       1,049,088       1,049,088
         Linear-75         [1, 5, 512]         262,656         262,656
         Linear-76         [1, 5, 512]         262,656         262,656
         Linear-77         [1, 5, 512]         262,656         262,656
         Linear-78         [1, 5, 512]         262,656         262,656
         Linear-79         [1, 5, 512]         262,656         262,656
         Linear-80         [1, 5, 512]         262,656         262,656
         Conv1d-81        [1, 2048, 5]       1,050,624       1,050,624
         Conv1d-82         [1, 512, 5]       1,049,088       1,049,088
         Linear-83           [1, 5, 7]           3,584           3,584
=======================================================================
Total params: 39,396,352
Trainable params: 39,390,208
Non-trainable params: 6,144
-----------------------------------------------------------------------
```

5) showing **layers until depth 3** and adding column with **parent layers**
```python
# show layers until depth 3 and add column with parent layers
pms.summary(model, enc_inputs, dec_inputs, max_depth=3, show_parent_layers=True, print_summary=True)
```
```
-----------------------------------------------------------------------------------------------------------------------------
                      Parent Layers                Layer (type)                  Output Shape         Param #     Tr. Param #
=============================================================================================================================
                Transformer/Encoder                 Embedding-1                   [1, 5, 512]           3,072           3,072
                Transformer/Encoder                 Embedding-2                   [1, 5, 512]           3,072               0
   Transformer/Encoder/EncoderLayer        MultiHeadAttention-3     [1, 5, 512], [1, 8, 5, 5]         787,968         787,968
   Transformer/Encoder/EncoderLayer     PoswiseFeedForwardNet-4                   [1, 5, 512]       2,099,712       2,099,712
   Transformer/Encoder/EncoderLayer        MultiHeadAttention-5     [1, 5, 512], [1, 8, 5, 5]         787,968         787,968
   Transformer/Encoder/EncoderLayer     PoswiseFeedForwardNet-6                   [1, 5, 512]       2,099,712       2,099,712
   Transformer/Encoder/EncoderLayer        MultiHeadAttention-7     [1, 5, 512], [1, 8, 5, 5]         787,968         787,968
   Transformer/Encoder/EncoderLayer     PoswiseFeedForwardNet-8                   [1, 5, 512]       2,099,712       2,099,712
   Transformer/Encoder/EncoderLayer        MultiHeadAttention-9     [1, 5, 512], [1, 8, 5, 5]         787,968         787,968
   Transformer/Encoder/EncoderLayer    PoswiseFeedForwardNet-10                   [1, 5, 512]       2,099,712       2,099,712
   Transformer/Encoder/EncoderLayer       MultiHeadAttention-11     [1, 5, 512], [1, 8, 5, 5]         787,968         787,968
   Transformer/Encoder/EncoderLayer    PoswiseFeedForwardNet-12                   [1, 5, 512]       2,099,712       2,099,712
   Transformer/Encoder/EncoderLayer       MultiHeadAttention-13     [1, 5, 512], [1, 8, 5, 5]         787,968         787,968
   Transformer/Encoder/EncoderLayer    PoswiseFeedForwardNet-14                   [1, 5, 512]       2,099,712       2,099,712
                Transformer/Decoder                Embedding-15                   [1, 5, 512]           3,584           3,584
                Transformer/Decoder                Embedding-16                   [1, 5, 512]           3,072               0
   Transformer/Decoder/DecoderLayer       MultiHeadAttention-17     [1, 5, 512], [1, 8, 5, 5]         787,968         787,968
   Transformer/Decoder/DecoderLayer       MultiHeadAttention-18     [1, 5, 512], [1, 8, 5, 5]         787,968         787,968
   Transformer/Decoder/DecoderLayer    PoswiseFeedForwardNet-19                   [1, 5, 512]       2,099,712       2,099,712
   Transformer/Decoder/DecoderLayer       MultiHeadAttention-20     [1, 5, 512], [1, 8, 5, 5]         787,968         787,968
   Transformer/Decoder/DecoderLayer       MultiHeadAttention-21     [1, 5, 512], [1, 8, 5, 5]         787,968         787,968
   Transformer/Decoder/DecoderLayer    PoswiseFeedForwardNet-22                   [1, 5, 512]       2,099,712       2,099,712
   Transformer/Decoder/DecoderLayer       MultiHeadAttention-23     [1, 5, 512], [1, 8, 5, 5]         787,968         787,968
   Transformer/Decoder/DecoderLayer       MultiHeadAttention-24     [1, 5, 512], [1, 8, 5, 5]         787,968         787,968
   Transformer/Decoder/DecoderLayer    PoswiseFeedForwardNet-25                   [1, 5, 512]       2,099,712       2,099,712
   Transformer/Decoder/DecoderLayer       MultiHeadAttention-26     [1, 5, 512], [1, 8, 5, 5]         787,968         787,968
   Transformer/Decoder/DecoderLayer       MultiHeadAttention-27     [1, 5, 512], [1, 8, 5, 5]         787,968         787,968
   Transformer/Decoder/DecoderLayer    PoswiseFeedForwardNet-28                   [1, 5, 512]       2,099,712       2,099,712
   Transformer/Decoder/DecoderLayer       MultiHeadAttention-29     [1, 5, 512], [1, 8, 5, 5]         787,968         787,968
   Transformer/Decoder/DecoderLayer       MultiHeadAttention-30     [1, 5, 512], [1, 8, 5, 5]         787,968         787,968
   Transformer/Decoder/DecoderLayer    PoswiseFeedForwardNet-31                   [1, 5, 512]       2,099,712       2,099,712
   Transformer/Decoder/DecoderLayer       MultiHeadAttention-32     [1, 5, 512], [1, 8, 5, 5]         787,968         787,968
   Transformer/Decoder/DecoderLayer       MultiHeadAttention-33     [1, 5, 512], [1, 8, 5, 5]         787,968         787,968
   Transformer/Decoder/DecoderLayer    PoswiseFeedForwardNet-34                   [1, 5, 512]       2,099,712       2,099,712
                        Transformer                   Linear-35                     [1, 5, 7]           3,584           3,584
=============================================================================================================================
Total params: 39,396,352
Trainable params: 39,390,208
Non-trainable params: 6,144
-----------------------------------------------------------------------------------------------------------------------------
```


## Reference

```python
code_reference = { 	'https://github.com/graykode/modelsummary', 
					'https://github.com/pytorch/pytorch/issues/2001',
					'https://gist.github.com/HTLife/b6640af9d6e7d765411f8aa9aa94b837',
					'https://github.com/sksq96/pytorch-summary',
					'Inspired by https://github.com/sksq96/pytorch-summary'}
```
