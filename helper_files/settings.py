'''
This file holds global variable information
'''
#bot user id
bot_id = 1195150720261967913

#role ID's
mod = 921431410697469997
leader = 921431410697469998

clan_info_array = [("Death", 921431410697469994), ("Haunt", 1205456253921533972), ("D34TH", 1187768994187452457)]


gen_none = 1195782189510578233
death = 921431410697469994
haunt = 1205456253921533972
d34th = 1187768994187452457
member_id = 921431410303172634

cap_gen_1_8 = 1190972582447558746

cap_gen_1 = 1195548086269911061
gen_1 = 934152325822562314

cap_gen_2_v1 = 1190972230847443056
cap_gen_2_v2 = 1192968512600285304
gen_2 = 1192968945033023508

cap_gen_3 = 1190974110478639134
gen_3 = 1192968989794635817

cap_gen_4 = 1190972169128267896
gen_4 = 1192969046312878172

cap_gen_5 = 1190974046226096170
gen_5 = 1192963554593230848

cap_gen_6 = 1195137151189385327
gen_6 = 1195137538411724830

cap_gen_7 = 1195137185838546964
gen_7 = 1195137556971528312

cap_gen_8 = 1195137208793960508
gen_8 = 1195137602421006357

gen_9 = 1212843022371528705

tryout_manager = 921431410697469996


novice = 1202050829033676830
rookie = 1202050794166157402
newcomer = 1202050758338674718	
freshman = 1202050711009886208
recruit = 1202050669734023208
member = 1202050634501849130
regular = 1202050585352736830
active = 1202050544890560592
veteran = 1202050506743095306
senior = 1202050467388215359
dedicated = 1202050424790585354
seasoned = 1202050384919793734
established	= 1202050333225000960
longtime = 1202050284743053332
elder = 1202050231039164486

age_roles = [novice, rookie, newcomer, freshman, recruit, member,
             regular, active, veteran, senior, dedicated, seasoned,
             established, longtime, elder]


comp = 1202055417144803328
casual = 1202055381740683357

global_elite = 1192970721186558043

master_I = 1192970679436464289
master_II = 1192970657051451462
master_III = 1192970637191430225
master_IV = 1192970599669170247

platinum_I = 1192970576583733448
platinum_II = 1192970539640303706
platinum_III = 1192970515309138041
platinum_IV = 1192970459801718877

elite_I = 1192970431972511764
elite_II = 1192970406534074528
elite_III = 1192970377853411378
elite_IV = 1192970333108572251

gold_I = 1192970273251655750
gold_II = 1192970222769016944
gold_III = 1192970196319752242
gold_IV = 1192970175482445914

silver_I = 1192970099984969858
silver_II = 1192970059669319690
silver_III = 1192969996301762630
silver_IV = 1192969928937058395

bronze_I = 1192969881793085502
bronze_II = 1192969836364578867
bronze_III = 1192969729820864662
bronze_IV = 1190980584751767562

#league index: 0, 1-4, 5-8, 9-12, 13-16, 17-20, 21-24
global_rank_list = [global_elite, master_I, master_II, master_III, master_IV,
                    platinum_I, platinum_II, platinum_III, platinum_IV,
                    elite_I, elite_II, elite_III, elite_IV, gold_I, gold_II,
                    gold_III, gold_IV, silver_I, silver_II, silver_III, silver_IV,
                    bronze_I, bronze_II, bronze_III, bronze_IV]

#easy list to go through each rank ID
rank_list = [cap_gen_1, gen_1, cap_gen_2_v1, cap_gen_2_v2, 
             gen_2, cap_gen_3, gen_3, cap_gen_4, gen_4, cap_gen_5, 
             gen_5, cap_gen_6, gen_6, cap_gen_7, gen_7, cap_gen_8, gen_8, gen_9, gen_none]

rank_milestones = [1700,    #cap_gen_1      
                   1600,    #gen_1          
                   1500,    #cap_gen_2_v1   
                   1400,    #cap_gen_2_v2   
                   1300,    #gen_3          
                   1200,    #cap_gen_3      
                   1100,    #gen_3          
                   1000,    #cap_gen_4      
                   900,     #gen4           
                   800,     #cap_gen_5      
                   700,     #gen_5          
                   600,     #cap_gen_6      
                   500,     #gen_6          
                   400,     #cap_gen_7      
                   300,     #gen_7          
                   200,     #cap_gen_8      
                   100,     #gen_8          
                   90,      #gen_9          
                   50]      #gen_none       

#scores for win,lose, or tie. Corresponds with rank list index
rank_win_score = [5,        #cap_gen_1      
                  5,        #gen_1          
                  7,        #cap_gen_2_v1   
                  7,        #cap_gen_2_v2   
                  7,        #gen_3          
                  10,       #cap_gen_3      
                  10,       #gen_3          
                  15,       #cap_gen_4      
                  15,       #gen4           
                  20,       #cap_gen_5      
                  20,       #gen_5          
                  25,       #cap_gen_6      
                  25,       #gen_6          
                  28,       #cap_gen_7      
                  28,       #gen_7          
                  30,       #cap_gen_8      
                  30,       #gen_8          
                  25,       #gen_9          
                  25]       #gen_none       

rank_lose_score = [-2,      #cap_gen_1      
                   -2,      #gen_1          
                   1,       #cap_gen_2_v1   
                   1,       #cap_gen_2_v2   
                   1,       #gen_3          
                   0,       #cap_gen_3      
                   0,       #gen_3          
                   1,       #cap_gen_4      
                   1,       #gen4           
                   2,       #cap_gen_5      
                   2,       #gen_5          
                   3,       #cap_gen_6      
                   3,       #gen_6          
                   4,       #cap_gen_7      
                   4,       #gen_7          
                   5,       #cap_gen_8      
                   5,       #gen_8          
                   10,      #gen_9          
                   10]      #gen_none       

rank_tie_score = [2,        #cap_gen_1      
                  2,        #gen_1          
                  3,        #cap_gen_2_v1   
                  3,        #cap_gen_2_v2   
                  3,        #gen_3          
                  5,        #cap_gen_3      
                  5,        #gen_3          
                  7,        #cap_gen_4      
                  7,        #gen4           
                  10,       #cap_gen_5      
                  10,       #gen_5          
                  12,       #cap_gen_6      
                  12,       #gen_6          
                  14,       #cap_gen_7      
                  14,       #gen_7          
                  15,       #cap_gen_8      
                  15,       #gen_8          
                  20,       #gen_9          
                  20]       #gen_none       


#scrim messages
scrim_msg_array = ["Let's give it our all and make our clan proud!", "Let's show them what we're made of!",
                   "Time to shine, folks!", "Give it your best shot out there!", "Show them our strength!",
                   "Let's dominate the battlefield!", "Make our mark, team!", "It's game time, let's crush it!",
                   "Let's leave it all on the field!", "Aim high and conquer!", "Let's make this victory ours!",
                   "Show them our teamwork!", "Let's paint the battlefield with our colors!", "We've got this, team!",
                   "Victory awaits, let's claim it!"]

scrim_end_msg_array = ["Hey some points have been awarded to ",
                "Hey everyone! Just a quick update: points have been distributed for the scrim. Make sure to check your balances and keep the momentum going!",
                "Attention all members! Points from the recent scrim have been distributed. Check your balances and stay active for more opportunities!",
                "Good news! Points have been awarded for your participation in the recent scrim. Keep up the great work and continue earning those points!",
                "Heads up, clan members! Points have been allocated for your involvement in the recent scrim. Be sure to check your balance and stay engaged!",
                "Hey clan! The points for the recent scrim have been distributed. Check your balance and keep contributing to our success!",
                "Attention members! Points for your participation in the scrim have been credited to your accounts. Keep striving for excellence!",
                "Just a heads up, everyone! Points have been awarded for your involvement in the recent scrim. Keep the momentum going and earn more points!",
                "Great news! Points for the recent scrim have been distributed to all participants. Check your balance and keep up the good work!",
                "Members, rejoice! Points have been awarded for your participation in the recent scrim. Keep grinding and collecting those points!"]

scrim_win_msg_array = ["Well done, team! Victory is ours!", "Congratulations, everyone! We emerged victorious!", "Excellent work, team! Another win for us!",
                       "Fantastic effort, everyone! We clinched the win!", "Bravo, team! Another triumph in the bag!", "Outstanding performance, folks! Victory belongs to us!",
                       "We did it! Victory is sweet!", "Kudos to all! We secured the win!", "Hats off to everyone! We came out on top!",
                       "Cheers to our success! Victory is ours to celebrate!"]

scrim_lose_msg_array = ["Tough loss, team. Let's regroup and come back stronger.", "It was a close one, team. We'll get them next time!",
                        "Keep your heads up, everyone. We'll bounce back from this setback.", "Hard luck, team. We'll learn from this and improve.",
                        "Not our day, team. Let's stay positive and strive for better next time.", "Defeat is never easy, team. Let's use it as motivation for future success.",
                        "Stay focused, team. We'll turn this setback into a comeback.", "We fought hard, team. Let's keep pushing forward despite the loss.",
                        "Chin up, everyone. We'll come back stronger from this defeat.", "It's just one loss, team. Let's keep working hard towards our goals."]

#Channel Ids
roaster_update_id = 955516301135212574
roaster_id = 921431411855069264
leaderboard_roaster_id = 1173725868481335419
owner_id = 921448268913860619
one_vs_one_id = 1192951758578798773
information_id = 1173712097503358986
server_id = 921431410303172629
upcoming_scrim_id = 921449838875389962
team_chat_id = 1073347833920508056
media_id = 1183377080021426237
global_leaderboard_id = 1202073241511022663
general_id = 921431411855069266
log_id = 955197964672987156

#numeric score values used
base_score = 50


def init():
    global active_array
    global max_players
    global current_players
    global winning_points
    global losing_points
    global member_name_array
    member_name_array = []
    active_array = []
    current_players = []
    max_players = 5
    winning_points = "40"
    losing_points = "20"