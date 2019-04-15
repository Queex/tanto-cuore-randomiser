# Tanto Cuore Randomiser
A python script to randomise setting up the Tanto Cuore card game.

## Concept
I've seen a few randomisers to Tanto Cuore around but none of them have quite met my exacting specifications.
As a python project, I've thrown together my own.

This is a standalone command-line script. It could easily be wrapped by something fancier, and if there's a call for it
I'll make the necessary modifications to make it easier to deal wit the output

## Usage
This script can be run on *nix systems with python installed in the usual place using:

```
./tanto_randomiser.py
```

or on any platform with python available on the path using:

```
python tanto_randomiser.py
```

By default, it assumes you have all 5 sets available. You can specify which sets you have (or wish to limit yourself to)
using abbreviations of the set names: TC, ETH, RV, O, WR. To play with only Oktoberfest and Expanding the House, for example,
you would use:

```
./tanto_randomiser.py O ETH
```

## Details
By default, the algorithm tries to fulfill the following goals:

- There should be neither too many nor too few of the optional mechanics introduced in the different boxes.
- Cards that only make sense in the context of one of those mechanics should not appear if that mechanic is not being used.
- There should not be too many different buildings or events in any one game.
- There should be a fairly even cost distribution among the general maids in town.
- Specific interactions named on Maid Chiefs and Chambermaid Chiefs do not affect the randomisation.

Cards that explicitly interact with certain optional mechanics (Tiffany Wise for Private Maids, for example) guarantee that the
mechanic will be selected for the game. If, after general maids are selected, there are too few of those optional mechanics,
then more are randomly added, where possible.

More specific details are below.

### General Maids
General Maids are split into 5 tiers: 2-cost, 3-cost, 4-cost, 5-cost and 6-cost or more. One maid is selected from each tier to
form the first 5 cards of the town. The other 5 are chosen at random from the remainder.

### Maid Chiefs
The Maid Chief and Chambermaid Chief are chosen completely at random.

### Private Maids
Private Maids that interact with other mechanics, such as Sora Nakachi or Silk Amanohara, are excluded if their accompanying
mechanic isn't included. There is a special case for Nord Twilight, who is only included if the Illness event has been selected.

Private Maids will always appear if Tiffany Wise has been chosen.

### Events
More events are introduced in a number of the expansions, so the total number to appear in one game is limited. Events that are
played on top of other players' buildings are only eligible if buildings are available - including Beer Stand and Meet Ups.

Events will always appear if at least one of Claire Saint-Juste or Nena Wilder has been chosen.

### Buildings
Buildings appear in a number of the expansions, so the total number to appear in one game is limited. Buildings that require
certain other mechanics, such as Beer or Meet Ups, are only eligible if those mechanics have been selected to appear.

There is specific handling of Lily Garden. It is prevented from appearing unless at least one of Garden and Ririko Hiiragi is
present. Disallowed combinations are avoided via rejection sampling.

Buildings will always appear if at least one of Ririko Hiiragi, Emily Raymond or Victoria Calderan has been chosen.

### Reminiscences
There are no restrictions on Reminiscences. although they will always appear if Hyacinth Arrow has been chosen.

### Beer
Beer can only appear if at least one of Gina Kersten and Nadia Kirsten has been chosen.

Julia Kunster interacts with beer cards, but this is pointless unless at least one of the maids that allows beer
to be bought is in the game. Set-ups generated with a pointless Julia are rejected and redrawn.

The Beer Stand building is added to the pool of potential buildings when the beer mechanic is in play, but will 
only appear if the building mechanic is also in play. You can change this behaviour in order to force it to appear 
irrespective of any other buildings using an option.

### Meet-Ups
Meet-Ups are a special kind of building, but they are their own category for the purposes of game randomisation.

Meet-Ups will always appear if at least one of Elizabeth Coran or Herbie Fortz has been chosen.

The Trial event is added to the pool of potential events when the Meet-Up mechanic is in play, but will 
only appear if the building mechanic is also in play. You can change this behaviour in order to force it to appear 
irrespective of any other events using an option.

The Chapel building is forced to be included when Meet-Ups are in play. You can change the behaviour to instead add 
it to the pool of potential buildings using an option.

### Drama
The Drama deck is only included when Dermot Gherin is chosen. This is not considered a full mechanic in its own right,
as it is linked to a single butler card.

## Options:
Brief help can be viewed using the `-h` flag.

- `-a`, `--optional-chapel`: By default, the Chapel will always appear where Meet Ups are used. This flags disables that
behavoiour, instead adding the Chapel to the pool of available buildings.
- `-d`, `--drama`: Forces the Drama deck to be counted as a full optional mechanic when setting the minimum number of 
optional mechanics.
- `-f`, `--fully-random`: Disables the behaviour that guarantees a spread of general maid costs and makes the selection
fully random.
- `-i`, `--ignore-requirements`: Disables the check for requirements for General Maids (currently only affects Julia Kunster).
- `-r`, `--reduce-rems`: Winter Romance optional rules include a suggestion to only use the tier 1 Reminiscence cards. This 
option adds a reminder to to do to the output.
- `-S`, `--force-beer-stand`: Forces the Beer Stand building to be available if Beer is included in the game.
- `-T`, `--force-trial`: Forces the Trial event to be available if Meet-Ups are included in the game.
- `-b N`, `--buildings N`: Choose this many buildings, where buildings appear (default 3). Note that any mandatory buildings 
included (such as Chapel and optionally Beer Stand) count against this total, but Meet-Ups do not.
- `-e N`, `--events N`: Choose this many events, where events appear (default 3). Note that abt mandatory events included 
(optionally Trial) count against this total.
- `o N`, `--min-optional-rules N`: Ensures there are at least this many optional mechanics, where possible (default 2).
- `p N`, `--max-private-maids N`: Provides an upper limit on the number of Private Maids to pu in the deck, where used (default
no limit).
- `c {0,2,3}`, `--crescent-sisters {0,2,3}`: special behaviour for the Crescent sisters. The default, 0, does nothing. Setting 
this to 2 will guarantee that there will never be a lone Crescent Sister. Setting this to 3 will guarantee that the game will 
have either all of them or none of them.
- `sets ...`: Any combination of TC, ETH, RV, O, WR, specifying the set(s) to use. If not provided, uses all 5.
