import json

def test_json__loads():
    
    json_str="""
{
    "gpsId" : "10014350",
    "businessId" : "12723026",
    "orderStatus" : { "$numberInt" : "10" },
    "sttDate" : { "$date" : { "$numberLong" : "1598274573000" } },
    "endDate" : { "$date" : { "$numberLong" : "1598572958000" } },
    "curDate" : { "$date" : { "$numberLong" : "1598572957000" } },
    "carNum" : "冀GC3543",
    "_class" : "com.techbrc.gps.trace.vo.DataInfo" }"""
    print("raw json_str",json_str)
    
    ans = json.loads(json_str)
    c = 0
    print("\nexecute code:\nans = json.loads(json_str)\nthe type of ans is dict")
    
    print("\nthe following is to travel ans\n")
    for k,v in ans.items():
        c += 1
        print(c,k,v)
if __name__ == "__main__":
    test_json__loads()
