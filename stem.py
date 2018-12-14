"""
Data precomputation file.
Prepare the reviews into a usable format for further analysis.
:file name : stem.py
:author : Pilote2Ligne
:Creation date : 09/12/18
:Last modified  : 12/12/18
"""


from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *

from nltk.stem import SnowballStemmer

import os

spark = SparkSession.builder.getOrCreate()
sqlContext = SQLContext(spark)

print("Spark running")

DATA_FOLDER = "data/"
RESULT_FOLDER = "results/"
REVIEWS_KINDLE = 'Kindle_Store_5.json'
REVIEWS_BOOKS = 'Books_5.json'

def load_reviews(path, limit = None, slice_=0):
    '''
    Dataframe from file with given filepath.
    A limit of samples to take may be given.
    :param : String
    :param : int
    :return : DataFrame
    '''
    print("Loading reviews datasets ...")
    
    df_reviews_kindle = spark.read.parquet(path)
    if limit != None:
        
        df_reviews_kindle.registerTempTable("reviews")
        df_reviews_kindle = spark.sql("""SELECT * FROM reviews LIMIT """+str(limit))
    
    print("\n####################\n")
    
    return df_reviews_kindle


def write_parquet(df, path, force = False):
    '''
    Writes the given dataframe into a parquet file
    :param : DataFrame
    :param : String
    :param : Boolean
    '''
    if os.path.exists(path) and not force:
        print("You already have an existing file with this name.")
        print("If you want to overwrite it, set force = True")
    else:
        df.write.mode('overwrite').parquet(path)



def stem_ing(w):
    '''
    Remove terminaison of a words, trying to keep only the root word.
    :param : String
    :return : String
    '''
    snowball_stemmer = SnowballStemmer('english')
    return snowball_stemmer.stem(w)


def stem_list(l):
    '''
    Stem every word of a list.
    :param : List(String)
    :return : List(String)
    '''
    return [stem_ing(w) for w in l]


def filter_reject(df_doc_to_stemmed_words, reject_words):
    '''
    Filter the given dataframe by removing the specified words.
    :param : DataFrame(_, List(String))
    :return : DataFrame(_, List(String))
    '''
    def keep_accepted(l):
        '''
        Return a list with only the accepted words in l.
        The word is accepted if its lenght is bigger than 3 and if it is not in the rejected words list.
        :param : List(String)
        :return : List(String)
        '''
        def accepted(w):
            return len(w) > 3 and w not in reject_words
        
        res = []
        for w in l:
            if accepted(w.lower()):
                res.append(w)
        return res
    
    print("Filter ...")
    rdd_filtered = df_doc_to_stemmed_words.rdd.map(lambda (a, l) : (a, keep_accepted(l)))
    struct = StructType([
        StructField("Asin", StringType(), True),
        StructField("Words", ArrayType(StringType()), True)
    ])
    df_filtered = spark.createDataFrame(rdd_filtered, struct)
    print("\n####################\n")
    return df_filtered
    

def gen_file_for_df(df_reviews_kindle, res_file_path):
    '''
    Split and stem the data to put it in usable format (UserId, List(Words)).
    Write the result in the file with the given path.
    :param : DataFrame
    :param : String
    '''
    df_reviews_kindle.registerTempTable("reviews_kindle")
    
    
    def process(s):
        temp = s
        ponctuations = [".", ",", "!", "?", "(", ")", "[", "]", "*", '"', \
                        "#", "&", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        for p in ponctuations:
            temp = temp.replace(p, " ")
        return temp.split(" ")
    
    print("Doc to words...")
    # Replace all the punctuation by spaces, words like 'end.' to be kept.
    sqlContext.udf.register("split", lambda s : process(s), ArrayType(StringType()))
    df_reviews_kindle_text = spark.sql("""SELECT asin, split(reviewText) splitted FROM reviews_kindle""")
    print(df_reviews_kindle_text.take(10))
    print("\n####################\n")
    
    print("Stem_ing ...")
    df_reviews_kindle_text.registerTempTable("doc2words")
    sqlContext.udf.register("stem_all", lambda l : stem_list(l), ArrayType(StringType()))
    df_doc_to_stemmed_words = spark.sql("""SELECT asin, stem_all(splitted) stemmed FROM doc2words""")
    print(df_doc_to_stemmed_words.take(10))
    print("\n####################\n")   
    
    # Remove top 1k common words in english
    most_common_words_file = open(DATA_FOLDER+ "1-1000.txt", 'r')
    reject_words = set([line[:-1] for line in most_common_words_file.readlines()])
    reject_words = filter(lambda w : len(w) > 3, reject_words)
    df_filtered_reject = filter_reject(df_doc_to_stemmed_words, reject_words)
    
    print("Write parquet ...")
    write_parquet(df_filtered_reject, res_file_path, True)
    print("\n####################\n")
    
    
########
# Main #
########

    
if __name__ == "__main__":
    LIMIT = 300000
    df_reviews_kindle = load_reviews(DATA_FOLDER + "kindle_reduced_reviews.parquet", limit = LIMIT)
    gen_file_for_df(df_reviews_kindle, RESULT_FOLDER + "stemsnow_kindle_2kk.parquet")

    df_reviews_books = load_reviews(DATA_FOLDER + "books_reduced_reviews.parquet", limit=LIMIT)
    gen_file_for_df(df_reviews_books, RESULT_FOLDER + "stemsnow_books_2kk.parquet")