import time
from cli_functions import *


def run_create():
    
    all_players = get_all_players()
    all_players = get_all_projections(all_players)
    if find_zero_projection(all_players) == 2:
        print("The program has terminated so that you may adjust the projections")
        return False
    wide_recievers = set_postions("WR", all_players)
    runningbacks = set_postions("RB", all_players)
    quarterbacks = set_postions("QB", all_players)
    tight_ends = set_postions("TE", all_players)
    defenses = set_postions("DST", all_players)
    qb_dst_combos = set_qb_dst_combos(quarterbacks, defenses)
    budget = 50000
    flex_max = set_flex_max(budget, qb_dst_combos)
    two_rb_combos = set_flex_combos(runningbacks, 2)
    three_rb_combos = set_flex_combos(runningbacks, 3)
    three_wr_combos = set_flex_combos(wide_recievers, 3)
    four_wr_combos = set_flex_combos(wide_recievers, 4)
    two_te_combos = set_flex_combos(tight_ends, 2)
    if max_combos(qb_dst_combos, two_rb_combos, three_rb_combos, three_wr_combos, four_wr_combos, tight_ends, two_te_combos) == 2:
        print("The program has ended so that you may reduce the number of players considered for a roster")
        return False
    start = time.time()
    print("Sorting positional combinations...")
    print("")
    two_rb_combos = sort_two(two_rb_combos)
    three_rb_combos = sort_three(three_rb_combos)
    three_wr_combos = sort_three(three_wr_combos)
    four_wr_combos = sort_four(four_wr_combos)
    two_te_combos = sort_two(two_te_combos)
    tight_ends = sort_one(tight_ends)
    print("Finished sorting positional combinations.")
    print("")
    flex_combo_end = time.time()
    runtime = get_time(start, flex_combo_end)
    print("The program has taken " + runtime + " seconds to sort all of the positional combinations")
    print("")
    print("Building the valid flex combinations...")
    print("")
    flex_combos = create_all_flex_combos(two_rb_combos, three_wr_combos, two_te_combos, three_rb_combos, tight_ends, four_wr_combos, flex_max)
    flex_combo_end = time.time()
    runtime = get_time(start, flex_combo_end)
    print("The program has taken " + runtime + " seconds to build all of the flex combinations and write them to the database")
    print("")
    print("Building all valid rosters and writing them to the database.  This may take some time...")
    write_combos(qb_dst_combos, flex_combos)
    build_tables()
    clear_space(["qb_dst", "flex"])
    end = time.time()
    print("")
    print("Finished building all of the valid rosters and writing them to the database.")
    print("The program has taken " + get_time(start, end) + " seconds to complete")
    
    return True