# Hive

This is an implementation of the board game Hive, see http://www.gen42.com/downloads/rules/Hive_Carbon_English_Rules.pdf for its rules.

This has been created as an hobby project and to learn more about Django and various web technologies.

In its current condition the game is far from complete. 
Under 'hive/core' you can find the the main logic for playing a game of hive. Main things missing from the main logic:
- Logic about the game progression (e.g. asking player to to an action and checking on correctness of action).
- Two pieces of the expension: lady bug and mosquito.

The hive/core/game.board has a function 'output_board_hexjson' which can save the current board to a file in hexjson 
(https://odileeds.org/projects/hexmaps/hexjson.html). Under hive/core/static/hive you can see multiple examples of saved boards in hexjson.

Using D3 we can load the hexjson board and visualise it in svg, see images/screenshot_board.png for an example board representation.


With inspiration from http://www.redblobgames.com/grids/hexagons.
