import requests

def check(make, model):
    rMake = requests.get("https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json")
    rModel = requests.get(f"https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{make.lower()}?format=json")
    rMake = rMake.json()
    rModel = rModel.json()
    return any(i["Make_Name"] == make.upper() for i in rMake["Results"]) and any(i["Model_Name"].lower() == model.lower() for i in rModel["Results"])
