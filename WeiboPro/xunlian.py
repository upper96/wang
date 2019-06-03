from snownlp import sentiment
sentiment.train(
    'xiaoji.txt',
    'jiji.txt'
)
sentiment.save('E:\WeiboPro\sentiment.marshal.2')