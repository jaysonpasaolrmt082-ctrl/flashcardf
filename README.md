# SciMath Battle Arena

An interactive practice game for the DOST Caraga SciMath Battle (Grade 6).
Open `index.html` in a browser. No install needed.

## How to play
- **Full SciMath Battle**: 10 Easy (1 pt), 10 Average (2 pts), and 10 Difficult (3 pts) questions, timed like the real contest. Top score is 60.
- **Pick a round**, then choose:
  - **Contest round**: 10 timed questions, then a score and rank (Champion, 2nd, 3rd, Finalist).
  - **Master it**: every card, no timer. Wrong answers come back until they are right.
  - **Learn first**: each question with its answer and memory trick.
- Multiple-choice questions: tap A–D (or press A–D / 1–4).
- Other questions: type the answer. Small spelling slips, units, commas and ₱ signs are OK.
  **Show choices** gives 4 options for half points. If the answer means the same thing but was marked wrong, tap **Count it**.
- Every correct answer earns a star; 3 stars = mastered. Wrong answers lose a star and go to **Fix my mistakes**.
- The **Hall of Fame** keeps the best contest scores on this device. Progress is saved in the browser.
- Key words to remember are highlighted in yellow.
- **↺ Start over** (top of the page, or the box at the bottom of the home screen): **New player** clears the name, stars and mistakes; **Clear Hall of Fame** removes saved scores; **Reset everything** goes back to the very beginning. Each asks "Are you sure?" first.

## Committee picks: Science (170 new questions)
Written by studying the 2025 science questions (waves and sound, the human body, chemistry and heat,
Earth and weather, space, local news, Filipino knowledge, expert scenarios, data reading):
- **Easy science** (40), **Average science** (40), **Difficult science** (35 scenarios)
- **True or false blitz** (30) and **Caraga & PH science** (25)
- **Science Battle** on the home screen: 30 science-only questions, contest style.

## No memorizing
- **Shuffled choices**: A–D are in a new order every time (true/false stays True, False).
- **Tricky choices**: wrong options are look-alikes (perihelion / perigee / aphelion / apogee,
  reflection / refraction) and common mistakes (8:41 AM vs PM, 3:5 vs 5:3, doubled or halved numbers).
- **Question style changes** in contests: some typed questions become multiple choice, and some
  multiple-choice questions must be typed with no choices shown.
- **🔀 New numbers**: 18 kinds of number problems (ratios, LCM, discounts, dilution, painted cube,
  wave speed, lightning distance and more) get fresh numbers whenever they come back.
  The **New numbers every time** decks are made only of these.
- **Least-recently-seen first**: rounds pick questions you have not seen lately.

## Files
- `cards.js`: the 280 questions from the reviewer and 2025 slides
- `sci.js`: 170 extra science questions (Committee picks)
- `gen.js`: fresh-number question makers and tricky-choice builder
- `keys.js`: highlighted words, extra accepted answers, and self-check cards.
- `check.js`: typed-answer checker.

Note: the official 2025 slide for Average Q8 says 8:41 PM; the correct answer is 8:41 AM (LCM of 12, 30, 66 s = 11 minutes).
