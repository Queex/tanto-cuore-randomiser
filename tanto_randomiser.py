#!/usr/env/python

# Tanto Cuore Dealer

import random
import argparse
import sys

debug=False

# argparse
p=argparse.ArgumentParser(description='Make a random Tanto Cuore game.')
p.add_argument('-a','--optional-chapel', action='store_true', help="make 'Chapel' building optional alongside Meet-Ups")
p.add_argument('-d','--drama', action='store_true', help="let 'drama' deck count as an optional mechanic")
p.add_argument('-f','--fully-random', action='store_true', help='make the general maid draw fully random')
p.add_argument('-i','--ignore-requirements', action='store_true', help="allow maids to appear when a mechanic they rely on is not present")
p.add_argument('-r','--reduce-rems', action='store_true', help="only use tier 1 Reminiscence cards")
p.add_argument('-S','--force-beer-stand', action='store_true', help="make 'Beer Stand' building always appear alongside Beer")
p.add_argument('-T','--force-trial', action='store_true', help="make 'Trial' event always appear alongside Meet-Ups")
p.add_argument('-b','--buildings', type=int, default=3, help="choose this many buildings, where buildings appear (default 3)")
p.add_argument('-e','--events', type=int, default=3, help="choose this many events, where events appear (default 3)")
p.add_argument('-o','--min-optional-rules', type=int, default=2, help="attempt to have at least this many optional mechanics (default 2)")
p.add_argument('-p','--max-private-maids', type=int, default=100, help="maximum size of Private Maid deck")
p.add_argument('-c','--crescent-sisters', type=int, default=0, choices=[0, 2, 3], help="ensure at least this many Crescent sisters appear, if any appear (default 0, which applies no restrictions)")
p.add_argument('sets', nargs='*', help='which sets to draw from (TC, ETH, RV, O, WR). Default is to use all')
args=p.parse_args()
args.sets=[x.upper() for x in args.sets] # fix case for sets

if debug:
    print(args)

# Rules tweaks
rule_cost_distribution=not args.fully_random
rule_drama_is_minor=not args.drama
rule_trial_always_included=args.force_trial
rule_chapel_always_included=not args.optional_chapel
rule_beer_stand_always_included=args.force_beer_stand
rule_ignore_maid_requirements=args.ignore_requirements
rule_reduced_reminiscences=args.reduce_rems
rule_min_extras=args.min_optional_rules
rule_number_of_buildings=args.buildings
rule_number_of_events=args.events
rule_max_private_maids=args.max_private_maids
rule_crescent_sisters=args.crescent_sisters

# Sets
sTC='TC'
sETH='ETH'
sRV='RV'
sO='O'
sWR='WR'
valid_sets=[sTC,sETH,sRV,sO,sWR]
set_dict={sTC:"Tanto Cuore", sETH:"Expanding the House", sRV:"Romantic Vacation", sO: "Oktoberfest", sWR:"Winter Romance"}

wrong=[z for z in args.sets if z not in valid_sets]
if len(wrong)>0:
    sys.exit("Unknown set name(s): %s" % ", ".join(wrong))
    
# Set availability
sets_owned={}
if len(args.sets)>0:
    for sset in valid_sets:
        sets_owned[sset]=(sset in args.sets)
else:
    sets_owned={sset:True for sset in valid_sets}

# Flags
# - Use private maids
# - Use events
# - Use buildings
# - Use beer
# - Use reminiscences
# - Use meet-up spots
# - Use drama deck (minor)
# - Force use of Lily Garden (in conjunction with buildings)
# - Illness
# - Crescent sister
fEvents='events'
fBuildings='buildings'
fBeer='beer'
fRem='reminiscences'
fPrivateMaids='private_maids'
fMeetUps='meet_ups'
fDrama='drama'
fLilyGarden='lily_garden'
fIllness='illness'
fCrescent='Crescent'

valid_flags=[fEvents, fBuildings, fBeer, fRem, fPrivateMaids, fMeetUps, fDrama, fLilyGarden, fIllness, fCrescent] # conditions for extra rules in the game
valid_extras=set() # rules sets that can be added freely, without requiring specific maid cards. Left empty until set ownership resolved
minor_extras=[fLilyGarden, fIllness, fCrescent] # rules sets that are minor enough that they don't add much extra complexity, and don't get counted when limiting the complexity
if rule_drama_is_minor:
    minor_extras.append(fDrama) 

# Requirement flags
rBeer='req_beer'
rEvents='req_events'
rBuildings='req_buildings'
rMeetUps='req_meet_ups'
rIllness='req_illness' # special case for Nord Twilight
# The special 'lily-garden requires Rirko or garden' requirement is handled explicitly.
valid_reqs=[rBeer, rEvents, rBuildings, rIllness, rMeetUps]
req_dict={rBeer:fBeer, rEvents:fEvents, rBuildings:fBuildings, rMeetUps:fMeetUps, rIllness:fIllness}

all_valid=valid_flags+valid_reqs+valid_sets

# Define sets
# Each set is a list of cards
# Each cards is a tuple of name/cost/triggers
# Triggers are lists of flags

# Main sets
tanto_cuore_set=[('Azure Crescent',2,[fCrescent]),('Rouge Crescent',2,[fCrescent]),('Viola Crescent',2,[fCrescent]),
        ('Claire Saint-Juste',3,[fEvents]),
        ('Eliza Rosewater',3,[]),('Kagari Ichinomiya',3,[]),('Safran Virgine',3,[]),('Esquine Forêt',4,[]),
        ('Geneviéve Daubigny',4,[]),('Moine de Lefévre',4,[]),('Natsumi Fujikawa',5,[]),('Nena Wilder',5,[fEvents]),
        ('Sainsbury Lockwood',5,[]),('Tenalys Trent',5,[]),('Ophelia Grail',6,[]),('Anise Greenaway',7,[])]
expanding_the_house_set=[('Pauline Dumond',2,[]),('Ririko Hiiragi',2,[fBuildings,fLilyGarden]),('Felicity Horn',3,[]),
        ('Grace Saulsbury',3,[]),('Lilac Hawkwind',3,[]),('Phyllis Lumley',3,[]),('Rutile der Sar',3,[]),
        ('Suzuna Kamikawa',3,[]),('Amaretto Renard',4,[]),('Domino Bonaparte',4,[]),('Emily Raymond',4,[fBuildings]),
        ('Victoria Calderan',4,[fBuildings]),('Carillon Vandoor',5,[]),('Francine Barbier',5,[]),
        ('Renée R Rieussec',5,[]),('Tiffany Wise',7,[fPrivateMaids])]
romantic_vacation_set=[('Hyacinth Arrow',2,[fRem]),('Nonnette Soyeux',2,[]),('Daphne Coraille',3,[]),('Evita Catala',3,[]),
        ('Germaine Mahle',3,[]),('Margereta Torrente',3,[]),('Valencia Pretre',3,[]),('Caldina Alley',4,[]),
        ('Chinatsu Kooriyama',4,[]),('Fea Primrose',4,[]),('Riya Naragashi',4,[]),('Romina Vautrin',4,[]),
        ('Cynthia Lakes',5,[]),('Florence Spring',5,[]),('Lydia Leon',5,[]),('Clorinde Sea',6,[]),('Laura',6,[]),
        ('Fryda Viento',7,[])]
oktoberfest_set=[('Nicole Schmieg',2,[]),('Paula Lauenburg',2,[]),('Aileen Hammerschmidt',3,[]),('Anna Hartmann',3,[]),
        ('Kaori Hamasaki',3,[]),('Renata Abendroth',3,[]),('Uta Krombach',3,[]),('Gina Kersten',4,[fBeer]),
        ('Julia Kunster',4,[rBeer]),('Kirika Heidemann',4,[]),('Sara Leonhardt',4,[]),('Nadia Kirsten',5,[fBeer]),
        ('Nora Morgenstern',5,[]),('Toni Darling',5,[]),('Hermina Baum',6,[]),('Elsa Reinmaier',7,[])]
winter_romance_set=[('Keena Solista',2,[]),('Shanti Bell',2,[]),('Anemone Seiya',3,[]),('Elizabeth Coran',3,[fMeetUps]),('Herbie Fortz',3,[fMeetUps]),('Jimmy Hariston',3,[]),('Nicholas Garibaldi',3,[]),('Benoit Ibsen',4,[]),('Kimberly Evan',4,[]),('Shirley Pollock',4,[]),('Dante Gagne',5,[]),('Shishido Kurogane',5,[]),('Menou Tatehira',6,[]),('Sonny Crosscalent',6,[]),('Michaela Fidelity',7,[]),('Dermot Gherin',8,[fDrama])]

# Private Maids
tanto_cuore_private_maids=[('Sora Nakachi',7,[rEvents]), ('Nord Twilight',4,[rIllness]),('Lucienne de Marlboro',5,[]),
        ('Amber Twlight',5,[]),('Lalanda Dreyfus',6,[]),('Eugenie Fontaine',5,[]),('Fay Longfang',6,[]),('Rosa Topaz',5,[]),
        ('Milly Violet',5,[]),('Tanya Petrushka',4,[])]
expanding_the_house_private_maids=[('Courtney Jewel',6,[]),('Roanna Shiraz',6,[]),('Aurelie Lambert',6,[]),
        ('Clymene Silvestri',6,[]),('Chrysta Antibes',5,[]),('Eve Valentine',5,[]),('Shion Tsuwabuki',5,[]),
        ('Mika Yakushido',6,[]),('Silk Amanohara',4,[rBuildings])]
        
# Events
card_illness=('Illness',4,[fIllness,sTC])
events=[('Envy',5,[sO]),('Heavy Storm',5,[rBuildings,sO]),('Bad Habit',2,[sTC]),card_illness,
        ('Let Me Drink!',5,[rBeer,sO]),('Blizzard',6,[rBuildings,sWR])]

# Buildings
card_garden=('Garden',4,[sETH])
card_lily_garden=('Lily Garden',6,[sETH])
buildings=[card_garden,('Estate',5,[sETH]),card_lily_garden]

# Beer stuff to add
card_beer_stand=('Beer Fest',4,[sO,rBeer])
if rule_beer_stand_always_included:
    beer_buildings=[card_beer_stand]
else:
    buildings.append(card_beer_stand)
    beer_buildings=[]

# Meetup stuff to add
card_chapel=('Chapel',6,[sWR,rMeetUps])
card_trial=('Trial',5,[sWR,rMeetUps])
meetup_extras=[('Social Bonus','-',[sWR,rMeetUps]),('Friends','-',[sWR,rMeetUps])]
meetup_buildings=[]
deck_meetup=[('Meet up deck','-',[sWR,rMeetUps])]
meetup_events=[]
if rule_trial_always_included:
    meetup_events.append(card_trial)
else:
    events.append(card_trial)
if rule_chapel_always_included:
    meetup_buildings.append(card_chapel)
else:
    buildings.append(card_chapel)
    
maid_chiefs=[('Marianne Soleil',9,[sTC]),('Claudine de La Rochelle',8,[sETH]),('Sophia Marfil',8,[sRV]),
        ('Anja Brunner',10,[sO]),('Leopold Niebling',10,[sWR])]
chambermaid_chiefs=[('Colette Framboise',3,[sTC]),('Aline Du Roy',2,[sETH]),('Beatrice Escudo',2,[sRV]),
        ('Matilde Wiese',2,[sO]),('Beverly Snowfeldt',2,[sWR])]

# Add set tag to each card
def add_set_flag(card_tuple, set_name):
    tmp=card_tuple[2]
    tmp.append(set_name)
    return (card_tuple[0],card_tuple[1],tmp)
    
tanto_cuore_set=[add_set_flag(x,sTC) for x in tanto_cuore_set]
expanding_the_house_set=[add_set_flag(x,sETH) for x in expanding_the_house_set]
romantic_vacation_set=[add_set_flag(x,sRV) for x in romantic_vacation_set]
oktoberfest_set=[add_set_flag(x,sO) for x in oktoberfest_set]
winter_romance_set=[add_set_flag(x,sWR) for x in winter_romance_set]
tanto_cuore_private_maids=[add_set_flag(x,sTC) for x in tanto_cuore_private_maids]
expanding_the_house_private_maids=[add_set_flag(x,sETH) for x in expanding_the_house_private_maids]

# Sorting function
def card_sort(card):
    return "%s  %s" % (card[1],card[0])

# Check flags are all valid
all_cards=tanto_cuore_set+expanding_the_house_set+romantic_vacation_set+oktoberfest_set+winter_romance_set+ \
            tanto_cuore_private_maids+expanding_the_house_private_maids+events+buildings+beer_buildings+ \
            meetup_extras+meetup_buildings+meetup_events+deck_meetup+maid_chiefs+chambermaid_chiefs
for card in all_cards:
    for flag in card[2]:
        if(flag not in all_valid):
            raise NameError('Invalid flag in %s: %s' % (card[0], flag))

# Make master card lists

usable_sets=[x for x in valid_sets if sets_owned[x]]
valid_cards=[]
valid_private_maids=[]
valid_extras=set()
if sets_owned[sTC]:
    valid_cards=valid_cards+tanto_cuore_set
    valid_private_maids=tanto_cuore_private_maids
    valid_extras.add(fEvents)
    valid_extras.add(fPrivateMaids)
if sets_owned[sETH]:
    valid_cards=valid_cards+expanding_the_house_set
    valid_private_maids=valid_private_maids+expanding_the_house_private_maids
    valid_extras.add(fBuildings)
    valid_extras.add(fPrivateMaids)
if sets_owned[sRV]:
    valid_cards=valid_cards+romantic_vacation_set
    valid_extras.add(fRem)
if sets_owned[sO]:
    valid_cards=valid_cards+oktoberfest_set
    if not rule_beer_stand_always_included:
        valid_extras.add(fBuildings)
    valid_extras.add(fEvents)
if sets_owned[sWR]:
    valid_cards=valid_cards+winter_romance_set
    valid_extras.add(fMeetUps)
    valid_extras.add(fEvents)
    if not rule_chapel_always_included:
        valid_extras.add(fBuildings)

# Report card value distribution
values={2:0,3:0,4:0,5:0,6:0,7:0,8:0}
for card in valid_cards:
    values[card[1]]=values[card[1]]+1
if debug:
    print(values)

# Stratify by card costs
cost_band_1=[x for x in valid_cards if x[1]==2]
cost_band_2=[x for x in valid_cards if x[1]==3]
cost_band_3=[x for x in valid_cards if x[1]==4]
cost_band_4=[x for x in valid_cards if x[1]==5]
cost_band_5=[x for x in valid_cards if x[1]>=6] #6, 7, 8

# Function to pull general maids
def select_general_maids():
    # Select 10 cards
    selected_cards=[]
    if rule_cost_distribution:
        # Start with 1 from each band
        selected_cards.append(random.choice(cost_band_1))
        selected_cards.append(random.choice(cost_band_2))
        selected_cards.append(random.choice(cost_band_3))
        selected_cards.append(random.choice(cost_band_4))
        selected_cards.append(random.choice(cost_band_5))
    # Now add completely at random
    while(len(selected_cards)<10):
        candidate=random.choice(valid_cards)
        if candidate not in selected_cards:
            selected_cards.append(candidate)
            
    return selected_cards
    
# Repeatedly sample until requirements for general maids are met (currently only 1 req in general maids, but wth)
while True:
    selected_cards=select_general_maids()
    # Discover mandatory extras
    set_flags=set()
    for flag in valid_flags:
        if( any(flag in x[2] for x in selected_cards) ):
            set_flags.add(flag)
    # Discover requirements
    set_reqs=set()
    for req in valid_reqs:
        if( any(req in x[2] for x in selected_cards) ):
            set_reqs.add(req)
            
    # Check all requirements are met
    if all(x in set_flags for x in set_reqs) or rule_ignore_maid_requirements:
        
        # Check Crescent sisters rule
        if rule_crescent_sisters>0:
            num=len([item for sublist in [x[2] for x in selected_cards] for item in sublist if item==fCrescent])
            if num==0 or num>=rule_crescent_sisters:
                break
        else:
            break

# Sort
selected_cards=sorted(selected_cards,key=card_sort)

if debug:
    print("Extras included by general maids: %s" % ",".join([x for x in set_flags if x not in minor_extras]))

# Want at least minimum non-minor extras. Some extra rules automatically add others later, but here we only consider 'first class' extras
while True:
    num_flags=len([x for x in set_flags if x not in minor_extras])
    available_extras=[x for x in valid_extras if x not in set_flags]
    if num_flags >= rule_min_extras or len(available_extras)==0:
        break
    candidate=random.choice(available_extras)
    set_flags.add(candidate)
    if debug:
        print("Adding extra: %s" % candidate)

# Respond to flags
selected_buildings=[]
selected_events=[]

if fBeer in set_flags:
    # Add beer buildings
    selected_buildings=selected_buildings+beer_buildings
    
if fMeetUps in set_flags:
    # Add meetup buildings/events
    selected_buildings=selected_buildings+meetup_buildings
    selected_events=selected_events+meetup_events # flag is set later so as not to interfere with regular event selection

if fBuildings in set_flags:
    candidates=[card for card in buildings if not any([flag for flag in card[2] if flag in valid_reqs and req_dict[flag] not in set_flags])]
    candidates=[card for card in candidates if not any([flag for flag in card[2] if flag in valid_sets and flag not in usable_sets])]
    num_needed=rule_number_of_buildings - len(selected_buildings) # mandatory buildings count against the total
    if debug:
        print(candidates)
        print(num_needed)
    reject=True
    while reject:
        selected=random.sample(candidates,min(num_needed,len(candidates)))
        if debug:
            print(card_lily_garden in selected)
            print(card_garden in selected)
            print(fLilyGarden in set_flags)
        if ((card_lily_garden in selected) == (fLilyGarden in set_flags)) or (card_lily_garden in selected and card_garden in selected):
            reject=False
            selected_buildings=selected_buildings+selected
    if len(selected_buildings)==0: # Special case where buildings were a selected extra rule but no buildings had their requirements met
        set_flags.remove(fBuildings)

if fMeetUps in set_flags: # revisit meetups for buildings if relevant
    set_flags.add(fBuildings) # set this as buildings now forced to be included (the meetups themselves are buildings)
    selected_buildings=selected_buildings+deck_meetup # Add here so as not to count against the number of building piles

if fEvents in set_flags:
    # Choose events
    min_events=rule_number_of_events-len(selected_events)
    choice_list=[card for card in events if not any([flag for flag in card[2] if flag in valid_reqs and req_dict[flag] not in set_flags])]
    choice_list=[card for card in choice_list if not any([flag for flag in card[2] if flag in valid_sets and flag not in usable_sets])]
    selected_events=selected_events+random.sample(choice_list,min(min_events,len(choice_list)))
    if card_illness in selected_events:
        set_flags.add(fIllness)

if fMeetUps in set_flags: # revisit meetups for events if relevant
    if len(meetup_events)>0:
        set_flags.add(fEvents) # set this as events now forced to be included in display
        
if fBeer in set_flags:
    if len(beer_buildings)>0:
        set_flags.add(fBuildings) # set this as buildings now forced to be included in display

# Private Maids
if fPrivateMaids in set_flags: # Reject some Private Maids if they rely on extras not in the set up. Do this step last
    if rule_ignore_maid_requirements:
        rejected_maids=[]
    else:
        rejected_maids=[maid for maid in valid_private_maids if any([flag for flag in maid[2] if flag in valid_reqs and req_dict[flag] not in set_flags])]
    allowed_private_maids=[pm for pm in valid_private_maids if pm not in rejected_maids]
    if rule_max_private_maids < len(allowed_private_maids):
        random.shuffle(allowed_private_maids)
        rejected_maids=rejected_maids+(allowed_private_maids[rule_max_private_maids:])
        allowed_private_maids=allowed_private_maids[:rule_max_private_maids]
            
# Pick maid chiefs
selected_maid_chief=random.choice([x for x in maid_chiefs if [y for y in x[2] if y in valid_sets][0] in usable_sets])
selected_chambermaid_chief=random.choice([x for x in chambermaid_chiefs if [y for y in x[2] if y in valid_sets][0] in usable_sets])

# Pick love
if len(usable_sets)>1:
    love_cards=random.sample([set_dict[y] for y in set_dict if sets_owned[y]],2)
    multi_set=True
else:
    love_cards=[set_dict[y] for y in set_dict if sets_owned[y]]
    multi_set=False

def format_card(card):
    cost=("(%s)" % str(card[1])).rjust(4)
    return "%s %s-- %s" % (cost,card[0].ljust(30),[set_dict[flag] for flag in card[2] if flag in valid_sets][0])

print("\nHere is your game!\n")
print("Use the following Maid Chief cards:")
print(format_card(selected_chambermaid_chief))
print(format_card(selected_maid_chief))
print("\nAnd the following General Maid cards:")
for card in selected_cards:
    print(format_card(card))
if fPrivateMaids in set_flags:
    if len(rejected_maids)==0:
        print("\nUse all the Private Maids.")
    elif len(allowed_private_maids) <= len(rejected_maids):
        print("\nUse the following Private Maids:")
        allowed_private_maids=sorted(allowed_private_maids,key=card_sort)
        for card in allowed_private_maids:
            print(format_card(card))
    else:
        print("\nRemove these Private Maids and use the rest:")
        rejected_maids=sorted(rejected_maids,key=card_sort)
        for card in rejected_maids:
            print(format_card(card))
    print("Shuffle the Private Maids and reveal 2 of them.")
if fBeer in set_flags:
    print("\nShuffle the Beer cards, put 'Oktoberfest' on top and add them to the town.")
if fRem in set_flags:
    if rule_reduced_reminiscences:
        print("\nShuffle the Reminisence 1 cards and reveal 3 of them.")
    else:
        print("\nShuffle the Reminiscence cards (preserving the 2 tiers) and reveal 3 of them.")
if fBuildings in set_flags:
    print("\nAdd these buildings to the town:")
    selected_buildings=sorted(selected_buildings,key=card_sort)
    for card in selected_buildings:
        print(format_card(card))
if fMeetUps in set_flags:
    print("\nAdd these piles to the town:")
    for card in meetup_extras:
        print(format_card(card))
if fEvents in set_flags:
    print("\nAdd these events to the town:")
    selected_events=sorted(selected_events,key=card_sort)
    for card in selected_events:
        print(format_card(card))
if fDrama in set_flags:
    print("\nShuffle the Drama cards and add them to the town.")
print("\nUse the love cards from %s" % love_cards[0])
if multi_set:
    print("(and also %s if you have more than 4 players)" % love_cards[1])
