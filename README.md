# Uncharted Realms
Uncharted Realms is a collectible card game where the cards are generated and re-balanced entirely by machine learning. Every card in the game is brand new, never seen before. As battles go on, the game is observing play patterns and card performance to keep re-balancing itself and keeping the game fair.

## How to run! 
Start server using
```
> python3 server.py
```
While the server is running, open the web client using the instructions on the web client repository.

## How it's built
The neural network for generating cards is built using Scikit Learn. A linear regression is created by fitting the stats of existing cards against their cost. Numerical values have a simple linear fit, but more complex stats like specific words had to be turn into numerical representations called "one hot". Cards were then generated for users to play games with, and these cards were then sent back to the network and were used to retrain the network and improve its confidence.

## Client repository
https://github.com/RyanAbraham/Uncharted-Realms
