"""
TF-IDF operations on bag of words.
:file name : tfidf.py
:author : Pilote2Ligne
:creation date : 10/10/18
:last modified : 12/10/18
"""

from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.context import SparkContext


spark = SparkSession.builder.getOrCreate()
sc = SparkContext.getOrCreate()
sqlContext = SQLContext(spark)
print("Spark running")


DATA_FOLDER = "data/"
RESULT_FOLDER = "results/"
STEMMED_KINDLE = "stemsnow_kindle_2kk.parquet"
STEMMED_BOOKS = "stemsnow_books_2kk.parquet"
KINDLE_REVIEWS = "kindle_reduced_reviews.parquet"
BOOKS_REVIEWS = "books_reduced_reviews.parquet"


def load_data_into_bag_of_words(path):
    '''
    Dataframe from file with given filepath.
    A limit of samples to take may be given.
    :param : String
    :param : int
    :return : DataFrame
    '''
    print("Loading reviews datasets ...")
    
    df = spark.read.parquet(path)
    print(df.take(1))
    df.registerTempTable("full_df")
    df = spark.sql("SELECT Words FROM full_df")
    
    print("\n####################\n")
    
    print("Collecting ...")
    review_words = df.collect()
    print("\n####################\n")
    
    print("Flattening ...")
    bag = []
    for r in review_words:
        for l in r[0]:
            bag.append(l)
            
    print("\n####################\n")
    # Taking sublist because of CPU capacity.
    return bag[:10000000]


def build_tf_matrix(words):
    '''
    Build Term Frequency Matrix for the given bag of words. 
    That is, it creates a RDD containing pairs (words, nb_occurences).
    :param : List(String)
    :return : RDD((String, int))
    '''
    nb_words = len(words)
    print("Size of bag of words : {}".format(nb_words))
    bag_rdd = sc.parallelize(words)
    # Filter words not appearing enough times. Corrects typo and removes too rare words.
    # We assume a review is around 600 characters in average : https://minimaxir.com/2014/06/reviewing-reviews/
    # A word is on average 5 characters long + space, which means the average review has 100 words.
    # We have bags of at least 7 million words. Hence a words that appears once every 10k reviews will appear 700 times.
    bag_rdd = bag_rdd.zipWithIndex().groupByKey().filter(lambda (k, l) : len(l) > 5000).map(lambda (k, l) : (k, 1.0*len(l)/nb_words))
    return bag_rdd


def build_idf_matrix(rdd_tf_books, rdd_tf_kindle):
    '''
    Build the Inverse Document Frequency Matrix from the given TF matrices corresponding to each corpus.
    The result is the average of the frequency of each word.
    :param : RDD((String, int))
    :param : RDD((String, int))
    :return : RDD((String, float))
    '''
    return rdd_tf_books.join(rdd_tf_kindle).map(lambda (k, (v1, v2)) : (k, (v1 + v2) / 2))
    

def build_tfidf_matrix(rdd_tf, rdd_idf):
    '''
    Build the TF-IDF matrix for the document corresponding to the TF matrice compared to the corpus corresponding to the IDF matrix.
    The result shows how many times a word is more likely to happen in this document than inside the whole corpus.
    :param : RDD((String, int))
    :param : RDD((String, float))
    :return : RDD((String, float))
    '''
    return rdd_tf.join(rdd_idf).map(lambda (k, (v1, v2)) : (k, v1 / v2)).sortBy(lambda (k, v) : v, False)
    

if __name__ == "__main__":
    
    bag_kindle = load_data_into_bag_of_words(RESULT_FOLDER + STEMMED_KINDLE)
    bag_kindle = load_data_into_bag_of_words(RESULT_FOLDER + STEMMED_KINDLE)
    rdd_tf_kindle = build_tf_matrix(bag_kindle)
    print(rdd_tf_kindle.take(10))
    
    bag_books = load_data_into_bag_of_words(RESULT_FOLDER + STEMMED_BOOKS)
    rdd_tf_books = build_tf_matrix(bag_books)
    print(rdd_tf_books.take(10))
    
    print("Build IDF Matrix ...")
    rdd_idf_matrix = build_idf_matrix(rdd_tf_books, rdd_tf_kindle)
    print("\n####################\n")
    
    print("Specific Kindle words :")
    rdd_tfidf_kindle = build_tfidf_matrix(rdd_tf_kindle, rdd_idf_matrix)
    first = rdd_tfidf_kindle.take(100)
    for f in first:
        print("{} : {}".format(f[0], f[1]))
    print("\n####################\n")
    
    
    print("Specific Books words :")
    rdd_tfidf_books = build_tfidf_matrix(rdd_tf_books, rdd_idf_matrix)
    first = rdd_tfidf_books.take(100)
    for f in first:
        print("{} : {}".format(f[0], f[1]))
    print("\n####################\n")
    
    
    print("Special word selection ...")
    special_list = ["layout", "display", "price", "worth", "easi", "charger"]
    def in_list(w):
        return w in special_list
    rdd_selected = rdd_tfidf_kindle.join(rdd_tfidf_books).filter(lambda (k, (v1, v2)) : in_list(k))
    for (k, (v1, v2)) in rdd_selected.collect():
        print("{} : Kindle : {}, Books : {}".format(k, v1, v2))