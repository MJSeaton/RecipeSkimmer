RecipeSkimmer
=============
RecipeSkimmer is a tool designed to allow for easy custom data-mining of user-submitted recipes from Reddit. It requires an active registered reddit account, along with the package PRAW. It takes in the path to a data folder with the following structure:
The only thing in the data folder must be .txt files, one for each subreddit to be scanned, and one named IDList to keep track of submissions that have already been analyzed. 
Recipes will be stored in these text files.

A sample data folder is included.

USAGE:
python RecipeSkimmer <DATA FOLDER> <REDDIT USERNAME> <REDDIT PASSWORD>
