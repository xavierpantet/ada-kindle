# Amazon Kindle User Experience

# Abstract
Amazon's Kindle is the most popular e-reader on the market right now. Since we have access to the reviews datasets for the physical books sold on Amazon and also for the Kindle e-books, we want to know whether the Kindle is more appreciated from its users than old school paper books. We will compare books consumers' behaviour depending on the medium they're using to read. We would like to analyze the difference between the two supports, the evolution of these, the shift or switch of users from a form of reading to another. We would like to see what change of trends it induced with the consumers' relationship towards the reading experience. The biggest motivation is to determine if the Kindle is worth it. We want to know what is the best available reading experience. With the increasing digitalization of the world that's been going on for several decades, how has the very traditional reading experience been affected?

# Research questions
Among people buying books, how many also buy Kindle e-books? Among readers owning a Kindle, how is the proportion of e-books compared to physical ones changing over time? Do people switch from one medium to another one definitively? Do they restrict themselves to only one support? Among people owning both kinds of books, are their reviews more favorable towards physical or Kindle's ones overall? What are the main topics of concerns in the reviews for each kind of medium, similar or totally different?

# Dataset
We are using the Amazon datasets available at http://jmcauley.ucsd.edu/data/amazon/links.html in the `Files` and `Per-category files` sections.

In particular we will be using the following four subdatasets:
- [Books ratings only](http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Books.csv)
- [Books reviews](http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Books.json.gz)
- [Kindle ratings only](http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Kindle_Store.csv)
- [Kindle reviews](http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Kindle_Store.json.gz)

The `ratings only` datasets contain, as their names suggest, only the ratings (ie the grades) that users have given to the products they have rated, whereas the `reviews` datasets contain the actual review texts as well as other fields such as the usefulness of the comment as evaluated by other Amazon users. Moreover, it is important to note that the `ratings only` datasets are way lighter than their associated `reviews` ones. We are going to use them extensively in the first part of the project, where only quantitative values of the reviews are going to be involved. In contrast, we will need the actual review texts in the second part of it, where we intend to use natural language processing methods to try to extract more context-based data out of the dataset.

The biggest advantage of the way the datasets were built is that the `userID`s are consistent. Hence it makes possible to join on this field to compare habits of a same user regarding the two mediums. Unfortunately, the same reasoning is not possible to do with the products. Indeed, the digital book identification number (`ASIN`) is not the same as one corresponding to the physical version of it.

At first glance, it appears that the datasets are in a standard and well-formed CSV or JSON format. Their sizes are very different, though: between 130MB and 18GB! In general, we think we will be able to handle them without too much difficulty, using appropriate tools (especially Spark).

# Prior work
For completeness, we wish to inform the reader that a similar project has already been realized in the previous edition of the course (denoted *[Lee, Jolles, Lemonato]* in the following):

```
Pierre-Alexandre Lee, Marc Jolles, Yves Lamonato.
"Books versus eBooks : The customers choice."
2017
```

However, although we seek to answer the same kind of questions, we are going to use a totally different approach. Indeed, in [Lee, Jolles, Lamonato], no time-based analysis has been done. We think that this is a key ingredient of the analysis, the Kindle being a relatively new product. Moreover, the datasets mentioned above have been joined on the product key in [Lee, Jolles, Lamonato]. Since the `ASIN` field is not consistent between paper and Kindle versions of the same book, this made the analysis tedious. The group had to use web-scrapping techniques to perform this operation and finally decided to use authors as joining key. As stated before, we will use the `userID` for this task and then compare the evolutions in the behaviour of Amazon customers reading on both mediums. We already know that `userID`s are consistent within our different datasets.

# Part 1 - Quantitative analysis
This part focuses on the evolution of numerical data in time. In particular, we direct the following questions:
- __Does the Kindle appeal to new users?__

    We first wish to analyze the adoption rate of Kindle products since their introduction to the market, in 2008. How does the number of newcomers evolve over time? Has the adoption been quick, was it a flop?

- __How do the reading habits of frequent users change in time?__

    Once the Kindle got its pool of users, we wish to know whether newcomers are actually sticking to the Kindle, completely adopting it, or giving it up? Do people tend to choose *their* ultimate reading medium or do they continue using both, how does the Kindle adoption flow behave?

- __How do the ratings of Kindle products evolve over time, compared to book ratings?__

    Finally, since the Kindle is a new-tech product, it most likely had to evolve rather quickly since its launch. The high-tech market is known to expand rapidly, urging companies to adapt their products to stay competitive. In order to measure this phenomenon, we will analyze the evolution of the actual grade that Kindle users give to Kindle products. Do we notice a global increase of users satisfaction towards the product, or on the contrary, do people tend to like it less and less with the arrival of new reading alternatives?

# Part 2 - Context-based analysis
In order to conclude this analysis, we wish to know a little bit more what the reviews are actually about. To do so, we will use the larger datasets and natural language processing techniques to perform a more in-depth analysis of review texts. First, note that all reviews are going to be stemmed for better processing by NLP algorithms. 

- __Do the users talk about the Kindle e-book in their reviews or only about the stories they read ?__

    To answer this first question, which is the starting point of this second part, we will use LDA (Latent Dirichlet Allocation) to extract high-level topics from the corpus of reviews. These topics will be given to us as word distributions. Among the expected topics related to a book genre, we were able to distinguish a technology-related topic, motivating the rest of the analysis. 
    
- __Which words define a technology-related review ?__
    
    To go on, we needed to extract the words defining the technology-related topic we discovered. For this, we used a variant of the TF-IDF algorithm, allowing us to remove the majority of the story-related words and keeping the ones that interested us. Finally we were able to write a list of words defining what a technology-related review will talk about and enabling us to filter the reviews and categorize them in two sets : technologic / non-technologic reviews.
    
- __Are the users positive on the technologic aspect of the Kindle ?__

    Now that we are able to categorize our dataset into two subsets, we wish to know if the sentiment regarding the technologic aspect of the Kindle (the real difference with the ordinary paper book) is generally better, worse or if their is no difference with the rest of the reviews. For this we run a sentiment analysis using Text-Blob which brought us to the conclusion that a tiny difference was distinguishable between the two subsets. However, this difference not being big enough, we wanted to make sure that it isn't only due to randomness. Hence we removed the dust from our statistic class to compute both the p-value per year and a t-test on the values we found. Both tests gave us the same result : there isn't a shadow of a doubt that the different distributions we observed are due to randomness. Hence we concluded that the users talk about the technologic aspect in a way which is a bit more pessimistic compared to usual reviews. However this has to be put in perspective with the fact that the sentiment analysis for this aspect is still positive.

# Who did what?
- Project's guidelines have been widely discussed and set by all members of the group.
- Damian demonstrated his high-level SQL skills in `Part 1`. He was also responsible of the sentiment analysis and the computation of the t-value.
- Etienne is the master of disaster in word stemming and TF-IDF analysis as well as in p-values computing.
- Xavier's patience has been a great help in understanding `pyspark`'s API to use LDA methods in order to launch the second part of this analysis.
- This project is kindly brought to you by the PMEA (Python MemoryError Association).

# Plots & resources
All plots and figures can be found in high resolution in the `figures/` folder.

# TODO
- Etienne and Xavier are in charge of the poster prepartation
- Damian will do the apple-style keynote presentation of the project
