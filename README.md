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

At first glance, it appears that the datasets are in a standard and well-formed CSV or JSON format. Their sizes are very different, though: between 130MB and 18GB! In general, we think we will be able to handle them without too much difficulty, using appropriate tools (espcially Spark).

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
- __Does the Kindle appeals to new users?__

    We first wish to analyze the adoption rate of Kindle products since its introduction to the market, in 2008. How does the number of newcomers evolve over time? Has the adoption been quick, was it a flop?

- __How do the reading habits of frequent users change in time?__

    Once the Kindle got its pool of users, we wish to know whether newcomers are actually sticking to the Kindle, completely adopting it, or giving it up? Do people tend to choose *their* ultimate reading medium or do they continue using both, how does the Kindle adoption flow behaves?

- __How the ratings of Kindle products evolve over time, compared to book ratings?__

    Finally, since the Kindle is a new-tech product, it most likely had to evolve rather quickly since its launch. The high-tech market is known to expand rapidly, urging companies to adapt their products to stay competitive. In order to measure this phenomenon, we will analyze the evolution of the actual grade that Kindle users give to Kindle products. Do we notice a global increase of users satisfaction towards the product, or on the contrary, do people tend to like it less and less with the arrival of new reading alternatives?

# Part 2 - Context-based analysis
In order to conclude this analysis, we wish to know a little bit more what the reviews are actually about. To do so, we will use the larger datasets and natural language processing techniques to perform a more in-depth analysis of review texts. First, note that all reviews are going to be stemmed for better processing by NLP algorithms. Then, we will use LDA (Latent Dirichlet Allocation) to extract high-level topics from the corpus of reviews. This topic will be given to us as word distributions. We plan to take the most representative words of topics that might we might be interested in to perform a TF-IDF analysis that will give us a better understanding of the context of reviews. In particular, we hope to be table to extract a Kindle-specific topic that might contain words such as "screen", "battery", "layout", "format", etc...

# Who did what?
- Project's guidelines have been widely discussed and set by all members of the group.
- Damian demonstrated his high-level SQL skills in `Part 1`.
- Etienne is the master of disaster in word stemming and TF-IDF analysis.
- Xavier's patience has been a great help in understanding `pyspark`'s API to use LDA methods.
- This project is kindly brought to you by the PMEA (Python MemoryError Association).

# Plots & resources
All plots and figures can be found in high resolution in the `figures/` folder.

# TODO
*[TBD]*
