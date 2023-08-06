[**中文**](./README_CN.md)

![](preview.png)

# InterpretDL: Interpretation of Deep Learning Models based on PaddlePaddle

InterpretDL is short for *interpretation of deep learning models*.

It is a model interpretation toolkit for [PaddlePaddle](https://github.com/PaddlePaddle/Paddle) models.

It provides many useful interpretation algorithms, like LIME, Grad-CAM, IntergratedGradients, etc.

It also contains (and will contain) SOTA and new interpretation algorithms.

*InterpretDL is under active construction and all contributions are welcome!*

# Demo

Interpretation algorithms give a hint of why the black-box model makes this decision.

The following table gives visualizations of several interpretation algorithms applied to the original image with respect to the label "bull_mastiff."
Original Image | Integrated Gradients | SmoothGrad | LIME | Grad-CAM
:--------------:|:-----------:|:-----------:|:-----------:|:-----------:
![](imgs/catdog.jpg)|![](imgs/catdog_ig.jpg)|![](imgs/catdog_sg.jpg)|![](imgs/catdog_lime.jpg)|![](imgs/catdog_gradcam.jpg)

For NLP tasks, one can visualize the results of a sentiment classification model as follows.

![](imgs/sentiment.jpg)


# Contents

* [Demo](#demo)
* [Installation](#Installation)
    * [Pip installation](#pip-installation)
    * [Developer installation](#developer-installation)
* [Documentation](#Documentation)
* [Usage Guideline](#Usage-Guideline)
* [Contribution](#Contribution)
* [Roadmap](#Roadmap)
    * [Algorithms](#Algorithms)
    * [Tutorials](#Tutorials)
* [Copyright and License](#Copyright-and-License)

# Installation

It requires the deep learning framework [paddlepaddle](https://www.paddlepaddle.org.cn/install/quick), recommendation with CUDA support.

## Pip installation

```bash
pip install interpretdl

# or with baidu mirror
pip install interpretdl -i https://mirror.baidu.com/pypi/simple
```

## Developer installation

```bash
git clone https://github.com/PaddlePaddle/InterpretDL.git
# ... fix bugs or add new features
python setup.py install
# welcome to propose pull request and contribute
```


# Documentation

Online link: [interpretdl.readthedocs.io](https://interpretdl.readthedocs.io/en/latest/interpretdl.html).

Or generate the docs locally:

```bash
git clone https://github.com/PaddlePaddle/InterpretDL.git
cd docs
make html
open _build/html/index.html
```


# Usage Guideline

All interpreters inherit the abstract class [`Interpreter`](https://github.com/PaddlePaddle/InterpretDL/blob/4f7444160981e99478c26e2a52f8e40bd06bf644/interpretdl/interpreter/abc_interpreter.py), of which `interpret(**kwargs)` is the function to call.

```python
# an example of SmoothGradient Interpreter.

# import ...

def paddle_model(data):
    class_num = 1000
    model = ResNet50()
    logits = model.net(input=data, class_dim=class_num)
    probs = fluid.layers.softmax(logits, axis=-1)
    return probs

img_path = 'assets/deer.png'
sg = SmoothGradInterpreter(paddle_model, "assets/ResNet50_pretrained")
gradients = sg.interpret(img_path, visual=True, save_path='sg_test.jpg')
```



More tutorials will be released.

# Roadmap

We are planning to create a useful toolkit for offering the model interpretation.

## Algorithms

We are planning to implement the algorithms below (categorized into sensitivity interpreters and algorithmic interpreters):

- [x] LIME
- [x] FastNormLIME
- [x] NormLIME
- [x] LIMEPrior
- [x] SmoothGrad
- [x] Occlusion
- [ ] DeepLIFT
- [x] GradientSHAP
- [x] GradCAM
- [x] IntegratedGradients
- [ ] InfluenceFunction
- [x] ForgettingEvent
- [ ] SGDNoise
- [ ] More ...

## Tutorials

We plan to provide at least one example for each interpretation algorithm, and hopefully on different applications, as in CV and NLP.

## References of Algorithms

* `IntegratedGraients`: [Axiomatic Attribution for Deep Networks, Mukund Sundararajan et al. 2017](https://arxiv.org/abs/1703.01365)
* `GradCAM`: [Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization, Ramprasaath R. Selvaraju et al. 2017](https://arxiv.org/abs/1610.02391.pdf)
* `SmoothGrad`: [SmoothGrad: removing noise by adding noise, Daniel Smilkov et al. 2017](https://arxiv.org/abs/1706.03825)
* `GradientShap`: [A Unified Approach to Interpreting Model Predictions, Scott M. Lundberg et al. 2017](http://papers.nips.cc/paper/7062-a-unified-approach-to-interpreting-model-predictions)
* `Occlusion`: [Visualizing and Understanding Convolutional Networks, Matthew D Zeiler and Rob Fergus 2013](https://arxiv.org/abs/1311.2901)
* `Lime`: ["Why Should I Trust You?": Explaining the Predictions of Any Classifier, Marco Tulio Ribeiro et al. 2016](https://arxiv.org/abs/1602.04938)
* `NormLime`: [NormLime: A New Feature Importance Metric for Explaining Deep Neural Networks, Isaac Ahern et al. 2019](https://arxiv.org/abs/1909.04200)
* `ScoreCAM`: [Score-CAM: Score-Weighted Visual Explanations for Convolutional Neural Networks, Haofan Wang et al. 2020](https://arxiv.org/abs/1910.01279)
* `ForgettingEvents`: [An Empirical Study of Example Forgetting during Deep Neural Network Learning, Mariya Toneva et al. 2019](http://arxiv.org/abs/1812.05159)

# Copyright and License

InterpretDL is provided under the [Apache-2.0 license](https://github.com/PaddlePaddle/InterpretDL/blob/master/LICENSE).
