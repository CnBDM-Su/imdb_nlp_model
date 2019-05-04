from pyspark.ml.feature import RegexTokenizer, Word2Vec
from pyspark.ml.feature import StopWordsRemover
from pyspark.sql import functions
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.ml.feature import Binarizer
from pyspark.sql.types import DoubleType
from pyspark.sql.functions import regexp_replace

#initialization
sc = SparkContext.getOrCreate()
spark = SparkSession(sc)
nlp = spark.read.format("csv").option("header","true").option("inferSchema","true").load("csvfile.csv")

#add label
nlp = nlp.withColumn("rate",nlp["rate"].cast(DoubleType()))
binarizer = Binarizer(threshold=5, inputCol = "rate", outputCol ="label")
nlp = binarizer.transform(nlp)

#tokenize & remove punctuation
tokenizer = RegexTokenizer(inputCol="content",outputCol="content_t",pattern="\\W")
nlp = tokenizer.transform(nlp)

#remove useless info
nlp = nlp.filter(nlp.label.isNotNull())
nlp = nlp.drop("_c3","_c4","_c5","_c6")
nlp = nlp.drop("content","rate","id")

#remove stopwords
remover = StopWordsRemover(inputCol="content_t",outputCol="content")
nlp = remover.transform(nlp)
nlp = nlp.drop("content_t")

#create word2vec
word2vec = Word2Vec(vectorSize=3,minCount=0,inputCol="content",outputCol="vec")
model = word2vec.fit(nlp)
nlp = model.transform(nlp)
nlp.drop("content")