# Uncharted Realms
Uncharted Realms is a collectible card game where the cards are generated and re-balanced entirely by machine learning. Every card in the game is brand new, never seen before. As battles go on, the game is observing play patterns and card performance to keep re-balancing itself and keeping the game fair.

## How to run! 
Generate cards and write them to the database using
```
> python3 main.py
```
This should be run in a cron job or timed in some way to run it at a set interval to ensure consistent releases of new card sets.

## How it's built
The neural network for generating cards is built using Scikit Learn. A linear regression is created by fitting the stats of existing cards against their cost. Numerical values have a simple linear fit, but more complex stats like specific words had to be turn into numerical representations called "one hot". Cards were then generated for users to play games with, and these cards were then sent back to the network and were used to retrain the network and improve its confidence.

## Client repository
https://github.com/RyanAbraham/Uncharted-Realms

## Server repository
https://github.com/RyanAbraham/Uncharted-Realms-Server
