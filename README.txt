Warlick and Lemire Dungeon Adventure Assignment TCSS-502

GitHub Repo: https://github.com/warlicks/dungon-adventrue

## Challenges
The biggest challenge by far was figuring out how to generate the maze randomly.
We eventually found a resource, [Complete Roguelike Tutorial](https://roguebasin.com/index.php/Complete_Roguelike_Tutorial,_using_python3+libtcod,_part_3?utm_source=pocket_shared),
that was really helpful for the algorithm development. This tutorial was set up
for creating a maze game with a GUI so, but we managed to adapt it to a text based game.

This adaptation led to one of the games short comings. In a GUI based games the
connections are represented by tunnels. Given that we built a command line game,
the concept of tunnels doesn't translate well, so the connections between rooms
are hard to visualize.

## Short Comings
While we create an entrance to each maze we start the player at a random point
in the maze. Given that the rooms are connected sequentially as the dungeon is
built, this makes the navigation harder. The downside to this is that the entrance
to maze rather pointless. In fact we don't really use the entrance and treat the
entrance room as a dead end. We could have used the entrance as another way to
exit the game.

There are a few cases that we didn't develop good unit tests for. One spot where
were were not successful in writing automated unit testing that methods
accepting user input would handle invalid input correctly. We ultimately tested
this manually.

## Playing the game
```python
python main.py
```