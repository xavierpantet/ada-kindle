# Title

# Abstract
Amazon's' Kindle is the most popular e-reader on the market right now. Since we have
access to the review datasets for the physical books sold on amazon and also for 
the Kindle e-books, we want to know if the Kindle is better than an old school
paper book. We will compare books consumers' behaviour depending on the medium 
they're using to read the book. We would like to analyze the difference between 
the two supports, the evolution of these, the shift or switch of users from a 
form of reading to another. We would like to see what change of trends it
induced with the consumers' relationship towards the reading experience.
The biggest motivation is to determine if the Kindle's worth it. We want to know
what is the best available reading experience.With the increasing digitalization 
of the world that's been going for several decades, how has the very traditional 
reading experience been affected?

# Research questions
Among the people buying books how many also buy kindle e-books? Among the readers
owning a Kindle, how is the proportion of e-books compared to physical ones changing 
over time? Do people switch from one medium to another one definitively? Do they
restrict themselves to only one support? Among people owning boths kinds of books
are their reviews more favorable towards physical ones or Kindle's ones overall?
What are the main topics of concerns in the reviews for each kind of medium, similar
or totally different?

# Dataset
We are using the amazon datasets available at http://jmcauley.ucsd.edu/data/amazon/.
In particular we will be using the following four subdatasets:
- Books 5-core
- Books ratings only
- Kindle Store 5-core
- Kindle ratings only

We are provided with two kinds of datasets the 5-core and the ratings only one.
The 5-core has the advantage being more rich in the terms of the data available
in each of the data entry. It has the actual review text, the helpfulness of
the review but its biggest drawback that it has been "reduced" to include 5 reviews
per users and per product.
On the other hand the ratings only is less rich than the 5-core in terms of the 
available fields for each entry but provides the complete set of reviews.

The biggest advantage of the way the dataset was built is that the userID is consistent
throughout all the subsets. Hence it makes possible to join on this field to 
compare habits of a same user regarding the two mediums. Unfortunately, the same
reasoning is not possible to do this with the products compared. Indeed, the 
digital book identification number (ASIN) is not the same as one corresponding to 
the physical version of it.

At first glance, it appears that the dataset is in a standard and well-formed 
csv or json format. The overall size of the files is approximatively 11Go which
makes it relatively easy to still handle it given appropriate tools.


# A list of internal milestones up until project milestone 2
- Make extensively sure that the data is indeed well formed and do not present
any anomalies that could have been overseen at first glance.
- Given the in-between scales size of the data, determine the most appropriate
tools to be used to handle it efficiently.
- Compute some basic statistics as the number of users using both mediums,etc.
- Investigate the best metrics to answer properly the high level questions asked
at the beginning i.e. how effective is the Kindle is it getting more consumer
approval over time?

# Questions for TAa
Add here some questions you have for us, in general or project-specific.
