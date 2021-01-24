import pandas as pd
import sql_manip
# What we calculate
total_units = 0
num_classes = 0
total_GE = 0
total_hours = 0
# ASSUMPTIONS : After a class is selected, all aspects of it is removed from the list (every value related to it [ pre-reqs, hours, units, etc]) 
# 

def get_recommended_classes():
    classes = sql_manip.SqlManip().get_classes()
    weights = []
    i = 0
    for course in classes: 
        weight= calc_weight(course[0], course[1])
        weights.append((weight,course))
        i+= 1
        
    def take_first(elem):
        return elem[0]
        
    weights.sort(key=take_first)
    top = weights[-5:]
    top_three = []
    for i in top:
        top_three.append(i[1])
    return top_three

# for years in range(1, 5):
#     for quarters in range(1, 4):
#         total_units = 0
#         num_classes = 0
#         total_GE = 0
#         total_hours = 0
#         for classes in range(1, 5):
#             # calc_weight for all classes available
#             # sort classes by weight 
#             # User chooses a class
#             num_classes += 1
#             # add to total_hours, total_GE, and total_Units based on the user's input



def calc_weight(dept, class_id):
    hours, num_pre_reqs = sql_manip.SqlManip().get_hours_num_prereqs(dept, class_id)
    return weight_h(hours) + weight_pr(num_pre_reqs) + weight_r(is_req(dept, class_id), check_req(dept, class_id))


# 2 Helper functions for weight_r (Weight of Required Class)

# Checks the Prerequisites 
def check_req(dept, course_id):
    desc, req, coreq = sql_manip.SqlManip().get_desc(course_id, dept)
    completed = sql_manip.SqlManip().get_finished()
    completed = [x[0] for x in completed]
    req = req.replace(r"'", "").replace(r"[", "").replace(r"]", "").split(",")
    for course in req:
        # empty requisites dont fail
        if course == "":
            continue
        if course.strip() not in completed:
            return True
            
    # Compare the requiredClasses ID to see if they are on the list, if at least one is, return true.
    return False
# Checks if the class is required
def is_req(dept, class_id):
    name = f"{dept} {class_id}"
    req_courses = sql_manip.SqlManip().get_req_courses()
    
    return name in req_courses
    # Compare this to the list of required classes, returns true if the class is required


# These are done -> Can change values though

# Weight of Required Class
def weight_r(isReq, are_Req):
    wR = 0
    if are_Req:
        wR = -100000000
    elif isReq and not are_Req: 
        wR = 50
    else:
        wR = 0
    return wR


# # Weight of Units
# def weight_u(unitsIn):
#     wu = 0
#     if num_classes == 3 and (total_units + unitsIn > 19 or total_units + unitsIn < 12):
#         wu = -10000
#     elif num_classes == 3:
#         wu = 0
#     elif (total_units + unitsIn < 19 and total_units + unitsIn > 12) and unitsIn == 4:
#         wu = 25
#     else:
#         wu = 0
#     return wu


# Weight of num of GE
# def weight_ge(isGe):
#     wge = 0
#     if isGe and total_GE == 0:
#         wge = 50
#     elif isGe and total_GE == 1:
#         wge = 10
#     elif isGe and total_GE >= 2:
#         wge = -30
#     elif not isGe:
#         wge = 0
#     return wge


# Weight of class hours
def weight_h(hoursIn):
    hrw = 0
    if hoursIn == 0:
        hrw = 5
    elif hoursIn in (1, 2):
        hrw = 10
    elif hoursIn in (3, 4):
        hrw = 40
    elif hoursIn in (5, 6):
        hrw = 30
    elif hoursIn in range(7, 20):
        hrw = 10
    return hrw


# # Weight of Prof Rating
# def weight_p(ratingIn):
#     wrate = 0
#     ratingIn *= 10
#     if ratingIn in range(0, 91):
#         wrate = 1
#     if ratingIn in range(91, 191):
#         wrate = 2
#     if ratingIn in range(191, 291):
#         wrate = 3
#     if ratingIn in range(291, 391):
#         wrate = 4
#     if ratingIn in range(391, 501):
#         wrate = 5
#     return wrate


# Weight of Num Pre Reqs it fulfills
def weight_pr(pre_reqIn):
    wpr = 0
    if pre_reqIn == 0:
        wpr = 0
    elif pre_reqIn in range(1, 4):
        wpr = 10
    elif pre_reqIn in range(4, 9):
        wpr = 20
    elif pre_reqIn in range(9, 16):
        wpr = 30
    elif pre_reqIn in range(16, 100):
        wpr = 50
    return wpr
