# GameAutomation


What do I need to submit?
Please write a program for the Challenge below.
You can use any language and frameworks you choose.
We must be able to run the program; provide any documentation necessary to accomplish this as part of the
repository you submit.
Please assume the user has not executed an application in your language/framework before when developing your
documentation.
Game
Given a balance scale and 9 gold bars of the same size and look. You don’t know the exact weight of each
bar, but you know they are the same weight, except for only one fake bar. It weighs less than others. You need to
find the fake gold bar by only bars and balance scales.
You can only place gold bars on scale plates (bowls) and find which scale weighs more or less.
Website
Website http://ec2-54-208-152-154.compute-1.amazonaws.com/ allows you to simulate the scaling process. You can
write gold bar number(s) in left and right bowl grids. Press the “Weigh” button and it will tell you which site weighs
more or less or they are the same weight. The weighing result will be shown in the “Weighing” list so you can track
records.
After you are done with one weighing you can press the “Reset” button to reset the plates grid to empty values so you
can do another weighing.
When you find the fake gold bar click on the button with a number corresponding to the fake gold bar at the bottom of
the screen and check if you were right or wrong: alert will pop up with two possible messages: “Yay! You find it!” or
“Oops! Try Again!”.
NOTE: Do not refresh the page as it will reset the fake bar to random
NOTE: Buttons at the bottom with numbers DO NOT represent weights. It’s just the sequential number.
Challenge
1. Play around with the website and find the best algorithm (minimum number of weighings for any possible
fake bar position) to find the fake gold bar.
2. Create the selenium based project using any preferable language to perform
a. clicks on buttons (“Weigh”, “Reset”)
b. Getting the measure results (field between “bowls”)
c. filling out the bowls grids with bar numbers (0 to 8)
d. getting list of weighings
e. Clicking on gold bar number at the bottom of the website and checking alert message
3. Code the algorithm from the step 1 which is using set of actions from step 2 to finds the fake gold bar
The algorithm should populate and weigh gold bars until a fake one is found, click on a fake bar number, output the
alert message, number of weighing and list of weighing were made.
Example
Here is an example of possible algorithms using pseudocode for demonstration purposes:
1. Open website
2. Insert number 0 in the first cell of the left bowl’s grid
3. Insert number 1 in the first cell of the right bowl’s grid
4. Press “Weigh” button
5. Get the result of weighing. In this example bar #0 is the same weight as bar #1
6. Make decision based on the result
7. Press “Reset button”
8. “Insert number 0 in the first cell” and “Insert number 1 in the second cell” of the left bowl’s grid
9. “Insert number 7 in the first cell” and “Insert number 8 in the second cell” of the left bowl’s grid
10. Press the “Weigh” button. In this example weight of bars #0 and #1 is greater than weight of bars #7 and #8.
So this means fake bar is #7 or #8
11. Continue with your algorithm
……….
12. Found the fake gold bar is number 7
13. Press button “7”
14. Get alert message and output it
15. Get list of “Weighings” and output them
