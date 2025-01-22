00:02:09 : [Bengio 2003](https://www.jmlr.org/papers/volume3/bengio03a/bengio03a.pdf)

00:03:12 : 17, 000 words embedded in 30 dimensional space .

00:03:35 : Tune the embeddings with backpropagation .

00:04:00 : Modeling approach \
Using the Multi-Layer Neural Netowrk to predict the next word, given the previous words.

00:04:00 : Maximizing the log likelihood of the training data.

00:04:40 : An "out of distribution" example

00:05:20 : A "transfer knowledge" example

00:07:00 : size of the hidden layer is a hyperparameter

00:08:05 : Apply softmax function to logits( raw, unnormalized score )

00:08:30 : target word index in training data \
maximize the probability of this word, with respect to the parameters of the Neural Net

00:08:40 : parameters \
1. weights and bias of output layer \
2. weights and bias of hidden layer \
3. embedding look up table \
