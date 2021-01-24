from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
# dict of classes
class_dict = {
    "course": "",
    "courses": "",
    "mathematics": "MATH",
    # "statistics": "STATS",
    # "philosophy": "PHILOS",
    # "mechanical and aerospace engineering": "MECH&AE",
    # "physics": "PHYSICS",
    # "computer science": "COM+SCI",
    # "materials science": "MAT+SCI",
    # "program in computing": "PIC",
    # "chemistry": "CHEM",
    # "economics": "ECON",
    "life science": "LS"
}

num_dict = { 
    'one':   1, 
    'two':   2, 
    'three': 3, 
    'four':  4, 
    'five':  5, 
    'six':   6, 
    'seven': 7, 
    'eight': 8, 
    'nine':  9, 
    'zero' : 0
}

def get_class_name(src):
    temp = src.split(".")
    return temp[0].strip(), temp[1].strip()

def get_hours(src):
    # first line has the hours information
    line = src.split(".")[0].lower().strip()
    
    hours = re.findall(r'\w+(?= hour)', line)
    
    total_hours = 0
    for num in hours:
        total_hours += num_dict[num]
        
    return total_hours
   
def get_requisites(src, curr_dept):
    class_dict["course"] = curr_dept
    class_dict["courses"] = curr_dept
    
    line = src.split(".")[0].lower().strip()
    reqs = []
    req_dept = class_dict["course"]
    
    for i in class_dict.keys():
        line = line.replace(i, class_dict[i])
#     print(line)
    optional = False # boolean check if class is optional
    for word in line.split(" "):
        if word in class_dict.values():
            req_dept = word
        
        if "or " in word + " ":
            optional = True
        
        if any(i.isdigit() for i in word):
            class_code = word.upper().replace(',', "").replace(r")", "")
            class_name = f"{req_dept} {class_code}"
            
            if optional: # optional classes you can take instead
                try: # incase there are no requisites
                    reqs[-1] = f"{reqs[-1]}/{class_name}"
                except:
                    pass
                optional = False
            else:
                reqs.append(class_name)
                
    return reqs

def get_grade_type(src):
    line = src.rsplit(".", 2)[1].lower().strip() # gets last sentence
    if "or" in line:
        return "both"
    elif r"p/np" in line:
        return "pnp"
    else:
        return "letter"
    
def format_df(orig_df):
    
    def calc_num_prereqs(df):
        class_name = df["dept"] + " " + df["class_id"]
        total_reqs = 0
        
        
        total_reqs = 0
        for req in ("requisites", "corequisites"):
            for index, rows in orig_df[req].iteritems():
                for curr_class in rows:
                    if class_name in curr_class.split("/"):
                        total_reqs += 1
                
        return(total_reqs)
    
    orig_df["prereq_score"] = orig_df.apply(calc_num_prereqs, axis=1) # number of classes that require this for prereqs
    
    orig_df["corequisites"] = orig_df["corequisites"].astype(str)
    orig_df["requisites"] = orig_df["requisites"].astype(str)
    return orig_df

def scrape_classes():
    classes = pd.DataFrame()
    for curr_dept in class_dict.values():

        url = f"https://www.registrar.ucla.edu/Academics/Course-Descriptions/Course-Details?SA={curr_dept}&funsel=3"

        req = requests.get(url)
        soup = BeautifulSoup(req.text, "lxml")
        
        for low_up_div in ("lower", "upper"):
            div_classes = soup.find("div",{"id": low_up_div})
            for ucla_class in div_classes.select(".media-body"):
                current_class = {"dept": curr_dept}

                current_class["class_id"], current_class["class_name"] = get_class_name(ucla_class.find("h3").text.strip())
                
                if(r"honors" in current_class["class_name"].lower()):
                    continue
                
                if(r"seminar" in current_class["class_name"].lower()):
                    continue
                
                units_desc = ucla_class.select("p")
                current_class["units"] = float(units_desc[0].text.split(":")[1].split(" ")[-1].strip())

                desc = units_desc[1].text.strip()

                while (r"(" in desc.split(".")[0].lower()) | ("preparation" in desc.split(".")[0].lower()):
                    desc = desc.split(".", 1)[1]

                current_class["hours"] = get_hours(desc)
                desc = desc.split(".", 1)[1] # gets rid of first sentence for course hours

                while ("preparation" in desc.split(".")[0].lower()):
                    desc = desc.split(".", 1)[1]


                if ("requisite" in desc.split(".")[0].lower()):
                    current_class["requisites"] = get_requisites(desc, curr_dept)
                    desc = desc.split(".", 1)[1] # gets rid of second sentence for requisites
                else:
                    current_class["requisites"] = []

                if "corequisite" in desc.split(".")[0].lower():
                    current_class["corequisites"] = get_requisites(desc, curr_dept)
                    desc = desc.split(".", 1)[1] # gets rid of second sentence for requisites
                else:
                    current_class["corequisites"] = []

                current_class["grade_type"] = get_grade_type(desc)
                desc = desc.rsplit(".", 2)[0] # removes last sentence

                current_class["desc"] = desc
                classes = classes.append(current_class, ignore_index=True)
                
    return format_df(classes)
                
                
