import pandas as pd

def make_math_req():
    math_reqs = pd.DataFrame(columns=["requisite_type", "num_required", "course"])
    math_reqs.loc[-1] = ["MATH 31A or 31AL", 2, ["MATH 31A/MATH 31AL"]]
    math_reqs.reset_index(drop=True)
    math_reqs.loc[1] = ["MATH 32A", 1, ["MATH 32A"]]
    math_reqs.loc[2] = ["MATH 32B", 1, ["MATH 32B"]]
    math_reqs.loc[3] = ["MATH 33A", 1, ["MATH 33A"]]
    math_reqs.loc[4] = ["MATH 33B", 1, ["MATH 33B"]]
    math_reqs.loc[5] = ["PHYSICS 1A", 1, ["PHYSICS 1A"]]
    math_reqs.loc[6] = ["PIC 10A", 1, ["PIC 10A"]]
    math_reqs.loc[7] = ["Select of 2", 2, ["CHEM 20A/CHEM 20B/ECON 11/LS 7A/PHILOS 31/PHILOS 13/PHYSICS 1B/PHYSICS 1C/PHYSICS 5B/PHYSICS 5C"]]
    # Required
    math_reqs.loc[9] = ["MATH 110A", 1, ["MATH 110A"]]
    math_reqs.loc[10] = ["MATH 110B", 1, ["MATH 110B"]]
    math_reqs.loc[11] = ["MATH 115A", 1, ["MATH 115A"]]
    math_reqs.loc[12] = ["MATH 120A", 1, ["MATH 120A"]]
    math_reqs.loc[13] = ["MATH 131A", 1, ["MATH 131A"]]
    math_reqs.loc[14] = ["MATH 131B", 1, ["MATH 131B"]]

    # elective
    math_reqs.loc[15] = ["Upper Div Electives", 5, ["MATH 106/MATH 111/MATH 114C/MATH M114S/MATH 115B/MATH 116/MATH 117/MATH 118/MATH 120B/MATH 121/MATH 123/MATH 131C/MATH 132/MATH 133/MATH 134/MATH 135/MATH 136/MATH 142/MATH 146/MATH M148/MATH 151A/MATH 151B/MATH 155/MATH 156/MATH 164/MATH 167/MATH 168/MATH 170A/MATH 170B/MATH 170E/MATH 170S/MATH 171/MATH 174E/MATH 177/MATH 178A/MATH 178B/MATH 178C/MATH 179/MATH 180/MATH 182E/MATH 184/MATH 188SA/MATH 188SB/MATH 188SC/MATH 189/MATH 189HC/MATH 190A/MATH 190B/MATH 190C/MATH 190D/MATH 190E/MATH 184/MATH 184/MATH 184/MATH 184/MATH 184/MATH 184/MATH 184/MATH 184/MATH 184/MATH 184/MATH 191/MATH 191H/MATH M192A/MATH 195/MATH 197/MATH 199"]]
    
    math_reqs["course"] = math_reqs["course"].astype(str)
    return math_reqs