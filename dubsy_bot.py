import math
from kaggle_environments.envs.kore_fleets.helpers import *
from kaggle_environments import utils
from kaggle_environments.helpers import Point, Direction
from random import random, sample, randint


#runs through shipyards and assigns attacks if valid (presets actions, set in dubsy bot)
#returns list of preassigned shipyards and actions
#add to dubsy bot code???

#box mining
#best path (iterate through each step)
#---from mine path while iterating through gap find where cutoff should be

#NEXT APPLICATIONS:
# - intercept
# - make bolster command work
# - rank shipyards prioritize defending shipyards??

#no implementation yet
"""check quadrant function
set box mine start of game
in agent:
more flagships more protection
"""

#numbers of friendly ships in proximity
def check_proximity(board, start, me):
    prox_ships = 0
    for i in range(-3,4):
        for j in range(-3,4):
            #pos = loc.translate(Point(i, j), board.configuration.size)
            current = start.translate(Point(i,j), board.configuration.size)
            if board.cells.get(current).fleet != None:
                if board.cells.get(current).fleet.player == me:
                    prox_ships += board.cells.get(current).fleet.ship_count
    return prox_ships



#mine to quadrant

def check_quadrant(board, start, me):
    idx = 0
    #quad 0-3, E,N,W,S
    #quad 0-3, N,E,S,W
    quad = [(0,10),(10,0),(0,-10), (-10,0)]
    best_kore = 0
    for xy in quad:
        kore = 0
        current = start.translate(Point(xy[0], xy[1]), board.configuration.size)
        #good?
        best_cell = [0,0,0,0]
        best_pt = [[0,0],[0,0],[0,0],[0,0]]
        for i in range(-5, 6):
            for j in range(-5, 6):
                pos = current.translate(Point(i, j), board.configuration.size)
                kore += board.cells.get(pos).kore
                if(board.cells.get(pos).kore >= best_cell[idx]):
                    best_cell[idx] = board.cells.get(pos).kore
                    best_pt[idx][0] = xy[0] + i
                    best_pt[idx][1] = xy[1] + j
        if(kore>best_kore):
            #index of best quad in quad
            best_quad = idx
        idx+=1
        if(idx==4):
            idx =3
    if idx%2 == 0:
        coor = best_pt[idx][1] -1
        if(coor<= 9 and coor>= -9):
            find = coor
        else:
            find = 9 if coor > 0 else -9
    else:
        coor = best_pt[idx][0] -1
        if(coor<= 9 and coor>= -9):
            find = coor
        else:
            find = 9 if coor > 0 else -9
    find = abs(find)
    dirs = Direction.list_directions()
    first_two = dirs[idx].to_char() + str(find)
    return first_two
    

#returns direction of most valuable neighboring cell from position (return dir as number 0:3)
def best_neighbor(board, start):
    dirs = Direction.list_directions()
    best_kore = 0
    for idx, d in enumerate(dirs):
        current = start
        kore = 0
        current = current.translate(d.to_point(), board.configuration.size)
        kore =  int(board.cells.get(current).kore or 0)
        if kore>=best_kore:
            best_kore = kore
            best_dir = idx
    #returns index of best directions
    return best_dir

#returns direction
def what_dir(dir_char):
    dirs = Direction.list_directions()
    for idx, d in enumerate(dirs):
        curr_char = d.to_char()
        if dir_char == curr_char:
            return d

#take 4
#currently in use
def miner_flight(board, start, coll_rate):
    dirs = Direction.list_directions()
    best_val = 0
    npv = 0.98
    right = None
    best_gap1 = None
    best_gap2 = None
    flight_plan = ""
    for idx, d in enumerate(dirs):
        for gap1 in range(1,11):
            for gap2 in range(1,11):
                current = start
                kore = 0
                for _ in range(0,gap1):
                    current = current.translate(d.to_point(),board.configuration.size)
                    kore += board.cells.get(current).kore * coll_rate
                #1 = right (idx +1)
                next_dir = dirs[(idx+1)%4]
                #2 = left (idx -1)
                other_dir = dirs[(idx+3)%4]
                #turn right or left
                current1 = current
                kore1 = kore
                current2 = current
                kore2 = kore
                for _ in range(0,gap2):
                    current1 = current1.translate(next_dir.to_point(),board.configuration.size)
                    kore1 += board.cells.get(current1).kore * coll_rate
                    current2 = current2.translate(other_dir.to_point(),board.configuration.size)
                    kore2 += board.cells.get(current2).kore * coll_rate
                
                steps = gap1+gap2
                val1 = math.pow(npv, steps) * kore1 / (2 * (steps))
                val2 = math.pow(npv, steps) * kore2 / (2 * (steps))
                #val1 = kore1
                #val2 = kore2
                if val1 > best_val:
                    best_val = val1
                    right = True
                    best_gap1 = gap1
                    best_gap2 = gap2
                    start_dir = d
                    start_dir_idx = idx
                if val2 > best_val:
                    best_val = val2
                    right = False
                    best_gap1 = gap1
                    best_gap2 = gap2
                    start_dir = d
                    start_dir_idx = idx
    
    prefpg1 = best_gap1 - 1
    fpg1 = str(prefpg1) if prefpg1 != 0 else ""
    prefpg2 = best_gap2 - 1
    fpg2 = str(prefpg2) if prefpg2 != 0 else ""
    start_dir = dirs[start_dir_idx]
    cstart_dir = start_dir.to_char()
    if right:
        next_idx = (start_dir_idx + 1)%4
    else:
        next_idx = (start_dir_idx + 3)%4
    next_dir = dirs[next_idx]
    cnext_dir = next_dir.to_char()
    cr1_dir = dirs[(next_idx+2)%4].to_char()
    cr2_dir = dirs[(start_dir_idx+2)%4].to_char()
        
    
    flight_plan += cstart_dir + fpg1 + cnext_dir + fpg2 + cr1_dir + fpg2 + cr2_dir
    print(flight_plan)
    return flight_plan

#take 3
#killed minerf

        
#remaking best path function
#optimized version of best path function
#returns str flight plan
#no double digit ints

#2nd revision

#killed mine_path

    
# reiterate best direction and (returns kore/step) for >=21 fleet, 
#when flight plan length = max length -3, get shortest path between position and closest shipyard
#large fleet mining, returns flight path

#optimized version is mine_path
#killed best_path

# checks a path to see how profitable it is, using net present value to discount 
# the return time (from documents)
def check_path(board, start, dirs, dist_a, dist_b, collection_rate):
    kore = 0
    npv = .98
    current = start
    steps = 2 * (dist_a + dist_b + 2)
    for idx, d in enumerate(dirs):
        for _ in range((dist_a if idx % 2 == 0 else dist_b) + 1):
            current = current.translate(d.to_point(), board.configuration.size)
            kore += int((board.cells.get(current).kore or 0) * collection_rate)
    return math.pow(npv, steps) * kore / (2 * (dist_a + dist_b + 2))

#from a point, returns most profitable flight plan, straight path and back
def dir_flight(board, start, collection_rate, already_chosen = False, chosen_dir = None):
    dirs = Direction.list_directions()
    best_val = 0
    best_gap = 0
    if not(already_chosen):
        for idx, d in enumerate(dirs):
            current = start
            #move for cardinal direction
            current = current.translate(d.to_point(), board.configuration.size)
            kore = board.cells.get(current).kore
            for gap in range (1, 10):
                    current = current.translate(d.to_point(), board.configuration.size)
                    kore += int(board.cells.get(current).kore)
                #adjustment
                    val = kore/(gap+1)
                    if (val>=best_val):
                        best_val = val
                        best_dir = d.to_char()
                        best_gap = gap
                        next_dir_id = (idx+2)%4
                        next_dir = Direction.list_directions()[next_dir_id].to_char()
        flight_plan = str(best_dir) + str(best_gap) + str(next_dir)
    else:
        best_dir = chosen_dir.to_char()
        best_val = 0
        kore = 0
        current = start.translate(chosen_dir.to_point(), board.configuration.size)
        d = chosen_dir
        for gap in range(1,10):
            current = current.translate(d.to_point(), board.configuration.size)
            kore += int(board.cells.get(current).kore)
            val = kore/gap
            if (val>=best_val):
                best_val = val
                best_gap = gap
        flight_plan = best_gap
    return flight_plan


# used to see how much kore is around a spot to potentially put a new shipyard
def check_location(board, loc, me):
    if board.cells.get(loc).shipyard and board.cells.get(loc).shipyard.player.id == me.id:
        return 0
    kore = 0
    for i in range(-3, 4):
        for j in range(-3, 4):
            pos = loc.translate(Point(i, j), board.configuration.size)
            kore += board.cells.get(pos).kore or 0
    return kore

                                              
#build new shipyard decide wear
                        #-spread
                        #towards center / enemies
                        #valurable area
                                              
def new_shipyard_pos(board, start, me):
    #expand towards center
    max_kore = 0
    for i in range(-15,16,5):
        if(i<-4 or i>4):
            for j in range(-15,16,5):
                if(j<-4 or j>4):
                    kore = 0
                    new_pos = start.translate(Point(i,j), board.configuration.size)
                    test_kore = check_location(board, new_pos, me)
                    if test_kore > max_kore:
                        max_kore = test_kore
                        best_pos = new_pos
    return best_pos
                                              
                                              
# returns list of positions of allied shipyards in 4x4
# use board,cells.get(allied_position).shipyard to fetch allied shipyards
# only returns ally SYs with >= ships
def check_for_allies(board, position, me, if_busy):
    shipyards = me.shipyards
    start = position
    allies = []
    for i in range(-4, 5):
        for j in range(-4,5):
            pos = start.translate(Point(i,j), board.configuration.size)
            if(board.cells.get(pos).shipyard and board.cells.get(pos).shipyard.player_id == me.id):
                if(board.cells.get(pos).shipyard.ship_count >= 21):
                    if(board.cells.get(pos).shipyard in if_busy):
                        continue
                    else:
                        allies.append(pos)
    return allies

def defending_allies(board, position, me, if_busy):
    #length 5 flight plan requires 12 ships
    #return shipyard positions
    shipyards = me.shipyards
    start = position
    reinforcements = []
    for i in range(-10, 11):
        for j in range(-10,11):
            pos = start.translate(Point(i,j), board.configuration.size)
            if(board.cells.get(pos).shipyard and board.cells.get(pos).shipyard.player_id == me.id):
                if(board.cells.get(pos).shipyard.ship_count >= 12):
                    if(board.cells.get(pos).shipyard in if_busy):
                        continue
                    else:
                        reinforcements.append(board.cells.get(pos).shipyard)
    return reinforcements
                                              
                                                                                                       
def collection_rate(num_ships):
    return math.log(num_ships) / 20

def get_closest_enemy_shipyard(board, position, me):
    min_dist = 1000000
    enemy_shipyard = None
    for shipyard in board.shipyards.values():
        if shipyard.player_id == me.id:
            continue
        dist = position.distance_to(shipyard.position, board.configuration.size)
        if dist < min_dist:
            min_dist = dist
            enemy_shipyard = shipyard
    return enemy_shipyard

def closest_friendly_loc(board,pos,me):
    min_dist = 100000
    friendly_pos = None
    for shipyard in me.shipyards:
        dist = pos.distance_to(shipyard.position, board.configuration.size)
        if dist < min_dist:
            min_dist = dist
            friendly_pos = shipyard.position
            
    return friendly_pos

def get_closest_friendly_shipyard(board, position, me):
    min_dist = 1000000
    friendly = None
    for shipyard in board.shipyards.values():
        if shipyard.player_id == me.id:
            dist = position.distance_to(shipyard.position, board.configuration.size)
            if dist < min_dist:
                min_dist = dist
                friendly = shipyard
    return friendly
                                              
def rank_shipyards(board, me):
    shipyards = me.shipyards
    order = []
    corr_dist = []
    vicroy = False
    for shipyard in shipyards:
        closest_enemy = get_closest_enemy_shipyard(board, shipyard.position, me)
        if closest_enemy == None:
            vicroy = True
            break
        friendly_pos = shipyard.position
        enemy_pos = closest_enemy.position
        dist_to_enemy = abs(friendly_pos.x - enemy_pos.x) + abs(friendly_pos.y - enemy_pos.y)
        if(len(order) == 0):
            order.append(shipyard)
            corr_dist.append(dist_to_enemy)
        else:
            for i in range(0,len(order)):
                if dist_to_enemy <= corr_dist[i]:
                    order.insert(i, shipyard)
                    corr_dist.insert(i, dist_to_enemy)
                elif i == (len(order) - 1):
                    order.append(shipyard)
                    corr_dist.append(dist_to_enemy)
    return order if vicroy == False else me.shipyards
                                              
                                              
    
def get_shortest_flight_path_between(position_a, position_b, size, trailing_digits=False):
    mag_x = 1 if position_b.x > position_a.x else -1
    abs_x = abs(position_b.x - position_a.x)
    dir_x = mag_x if abs_x < size/2 else -mag_x
    mag_y = 1 if position_b.y > position_a.y else -1
    abs_y = abs(position_b.y - position_a.y)
    dir_y = mag_y if abs_y < size/2 else -mag_y
    flight_path_x = ""
    if abs_x > 0:
        flight_path_x += "E" if dir_x == 1 else "W"
        flight_path_x += str(abs_x - 1) if (abs_x - 1) > 0 else ""
    flight_path_y = ""
    if abs_y > 0:
        flight_path_y += "N" if dir_y == 1 else "S"
        flight_path_y += str(abs_y - 1) if (abs_y - 1) > 0 else ""
    if not len(flight_path_x) == len(flight_path_y):
        if len(flight_path_x) < len(flight_path_y):
            return flight_path_x + (flight_path_y if trailing_digits else flight_path_y[0])
        else:
            return flight_path_y + (flight_path_x if trailing_digits else flight_path_x[0])
    return flight_path_y + (flight_path_x if trailing_digits or not flight_path_x else flight_path_x[0]) if random() < .5 else flight_path_x + (flight_path_y if trailing_digits or not flight_path_y else flight_path_y[0])
               
                                              
 #check opponents flight plan to see if one goes to any of my shipyards 
#returns list of shipyards
#position changes with direction character, fix!!!!!!!!!!!!
def invading_fleets(board, me):
    friendly_shipyards = me.shipyards
    contact = []
    dirs = Direction.list_directions()
    for fleet in board.fleets.values():
        if(fleet.player_id == me.id):
            continue
        else:
            #necessary positional data
            enemy_flight_plan = fleet.flight_plan
            enemy_dir = fleet.direction
            enemy_pos = fleet.position
            #necessary for individualized defence
            enemy_ships = fleet.ship_count
            #random ships causes my shipyards to freeze
            if enemy_ships<=21:
                continue
            contact_occ = False
            #progress through flight plan - for fleet
            was_dir = False
            for i in enemy_flight_plan:
                if(contact_occ):
                    #print("contact occur (1)")
                    break
                was_dir = False
                for idx, d in enumerate(dirs):
                    if(str(d.to_char())==i):
                        enemy_dir = d
                        was_dir = True
                        enemy_pos = enemy_pos.translate(enemy_dir.to_point(), board.configuration.size)
                        
                if(not was_dir):
                    if(i=="C"):
                        break
                    else:
                        #check if double digit flight plan
                        for j in range(0,int(i)):
                            enemy_pos = enemy_pos.translate(enemy_dir.to_point(), board.configuration.size)
                            if contact_occ:
                                break
                            for shipyard in friendly_shipyards:
                                if(enemy_pos == shipyard.position):
                                    contact.append(shipyard)
                                    contact_occ = True
                                    break
            if was_dir or len(enemy_flight_plan)==0:
                for idx, d in enumerate(dirs):
                    if(str(d.to_char())==enemy_dir.to_char()):
                        final_idx = idx
                for shipyard in friendly_shipyards:  
                    if final_idx%2 == 0:
                        if enemy_pos.x == shipyard.position.x:
                            contact.append(shipyard)
                            break
                    else:
                        if enemy_pos.y == shipyard.position.y:
                            contact.append(shipyard)
                            break
                         
    return contact
                                        

def max_flight_plan(num_ships):
    return math.floor(2*math.log(num_ships))+1
                                              
                                              
                                        
def total_enemy_shipyards(board, me):
    shipyards = board.shipyards.values()
    counter = 0
    for shipyard in shipyards:
        if(shipyard.player_id == me.id):
            continue
        counter += 1
    return counter
    
                                              
#runs through shipyards and assigns attacks if valid (presets actions, set in dubsy bot)
#returns list of preassigned shipyards and actions
#add to dubsy bot code???
                       
#instead of ids store shipyard objects in list?                                              

#include box mining?? see if flight plan works
#play around with cutoffs to determine behavior
                                              
#keep track of busy shipyards, keep track of remaining kore
                                              
#number of invading ships
def dubsy_agent(obs, config):
    board = Board(obs, config)
    me = board.current_player
    kore_left = me.kore
    #lists friendly shipyards closest to farthest from enemy
    shipyards = rank_shipyards(board, me) 
    fleets = me.fleets
    convert_cost = board.configuration.convert_cost
    size = board.configuration.size
    spawn_cost = board.configuration.spawn_cost
    turn = board.step
                                              
    #use shipard objects
    defending_shipyards = invading_fleets(board, me)
    busy_shipyards = defending_shipyards
    
    for shipyard in shipyards:
        #check if already busy
        if (shipyard in busy_shipyards):
            print("busy.........................................")
            #defending?
            if (shipyard in defending_shipyards):
                if shipyard.ship_count<=70:
                    shipyard.next_action = ShipyardAction.spawn_ships(min(shipyard.max_spawn, int(kore_left/spawn_cost)))
                    kore_left -= spawn_cost * min(shipyard.max_spawn, int(kore_left/spawn_cost))
                    #bolstering defence position/ get reinforcements, list of allied positions
                    if len(me.shipyards) != 1:    
                        bolster = defending_allies(board, shipyard.position, me, busy_shipyards)
                        if (len(bolster)!= 0):
                            for ally_sy in bolster:
                                flight_plan = get_shortest_flight_path_between(ally_sy.position, shipyard.position, board.configuration.size)
                                ally_sy.next_action = ShipyardAction.launch_fleet_with_flight_plan(ally_sy.ship_count, flight_plan)
                                #append to busy_shipyards
                                busy_shipyards.append(ally_sy)
                                print("it happened...............................")
                    continue
        
            else:
                continue
        
        #make busy
        busy_shipyards.append(shipyard)
                                              
        ships = shipyard.ship_count                                   
        
        #check if taken all enemy shipyards
        vicroy = total_enemy_shipyards(board, me)
        if vicroy == 0:
            spawned = min(int(kore_left/spawn_cost),shipyard.max_spawn)
            kore_left -= spawned * spawn_cost
            shipyard.next_action = ShipyardAction.spawn_ships(spawned)
        #early game
        if (turn<10):
            if (ships >= 3):
                shipyard.next_action = ShipyardAction.launch_fleet_with_flight_plan(ships, dir_flight(board, shipyard.position, collection_rate(ships)))
                continue
            elif (kore_left >= spawn_cost):
                shipyard.next_action = ShipyardAction.spawn_ships(min(shipyard.max_spawn, int(kore_left/spawn_cost)))
                kore_left -= spawn_cost * min(shipyard.max_spawn, int(kore_left/spawn_cost))
                continue

        #attacking
        closest_enemy_shipyard = get_closest_enemy_shipyard(board, shipyard.position, me)
        if closest_enemy_shipyard != None:
            friendly_ships = ships
            enemy_ships = closest_enemy_shipyard.ship_count
            num_enemy_shipyards = total_enemy_shipyards(board, me)
            #positions of allied shipyards
            if len(shipyards)>1:
                allies = check_for_allies(board, shipyard.position, me, busy_shipyards)
            else:
                allies = 0
            #changed attack limit to 60 (more aggressive)
            if(friendly_ships>=60 and friendly_ships > enemy_ships):
                flight_plan = get_shortest_flight_path_between(shipyard.position, closest_enemy_shipyard.position, board.configuration.size)
                shipyard.next_action = ShipyardAction.launch_fleet_with_flight_plan(friendly_ships, flight_plan)
                continue

            elif(friendly_ships >= 60 and friendly_ships <= enemy_ships):
                if allies == 0:
                    ally_shipyards = []
                else:
                    ally_shipyards = allies
                num_ships = friendly_ships
                if len(ally_shipyards) != 0:
                    for pos in ally_shipyards:
                        get_ally = board.cells.get(pos).shipyard
                        num_ships += get_ally.ship_count
                if(num_ships > enemy_ships):
                    flight_plan = get_shortest_flight_path_between(shipyard.position, closest_enemy_shipyard.position, board.configuration.size)
                    shipyard.next_action = ShipyardAction.launch_fleet_with_flight_plan(ships, flight_plan)
                    for pos in ally_shipyards:
                        get_ally = board.cells.get(pos).shipyard
                        flight_plan = get_shortest_flight_path_between(get_ally.position, closest_enemy_shipyard.position, board.configuration.size)
                        get_ally.next_action = ShipyardAction.launch_fleet_with_flight_plan(get_ally.ship_count, flight_plan) 
                        busy_shipyards.append(get_ally)
                    continue
                                                                                    
        #new shipyard?
        if turn < 350:
            if(shipyard.max_spawn>=5 and ships>= 50 and kore_left >= 500):
                if len(me.shipyards)<=total_enemy_shipyards(board, me):
                    new_base = new_shipyard_pos(board, shipyard.position, me)
                    short_path = get_shortest_flight_path_between(shipyard.position, new_base, board.configuration.size)
                    flight_plan = short_path + "C"
                    shipyard.next_action = ShipyardAction.launch_fleet_with_flight_plan(ships, flight_plan)
                    continue
                                                                                    
        #otherwise, mine
        
        #wait condition - more shipyards
        close_ships = check_proximity(board, shipyard.position, me) + ships
        
        
        if(ships>=21):
            #new miner agent
            ships_sent = max(int(ships/2),21)
            flight_plan = miner_flight(board, shipyard.position, collection_rate(ships_sent))
            shipyard.next_action = ShipyardAction.launch_fleet_with_flight_plan(ships_sent, flight_plan)
            #use max ships for longest possible flight plan
            #ships = int(max(21, math.floor(ships/3)))
            
            #using mine path instead of best path
            
            #flight_plan = minerf(board, shipyard.position, ships, me)
            #shipyard.next_action = ShipyardAction.launch_fleet_with_flight_plan(ships, flight_plan)
            
            #from_balanced agent
            #miner function based off given code
            
        elif(kore_left>=10 and turn < 375):
            shipyard.next_action = ShipyardAction.spawn_ships(min(shipyard.max_spawn, int(kore_left/spawn_cost)))
            kore_left -= min(shipyard.max_spawn, int(kore_left/spawn_cost))
            continue
        elif(ships>=3):
            shipyard.next_action = ShipyardAction.launch_fleet_with_flight_plan(ships, dir_flight(board, shipyard.position, collection_rate(ships)))
            continue
        else:
            direction = Direction.from_index(turn % 4)
            if ships > 0:   
                shipyard.next_action = ShipyardAction.launch_fleet_with_flight_plan(ships, direction.to_char())
            
    #command given to game
    #pray no errors
    #improve mining
    return me.next_actions
                    
        