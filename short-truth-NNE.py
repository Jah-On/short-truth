import httpx
import time
import datetime
import sys

if (len(sys.argv) != 2):
    raise Exception("Invalid arguments!")

baseURL = ["https://cdn.finra.org/equity/regsho/daily/", "shvol", ".txt"]

def main(args):
    ticker = bytes(args[1].upper(), "utf-8")
    request = httpx.get("https://finance.yahoo.com/quote/" + args[1])
    if (request.status_code != 200):
        raise Exception("Symbol not found!")
    data = request.read()
    symdex = data.find(b'floatShares":{"raw":')
    floatShares = int(data[symdex + 20 : symdex + data[symdex:].index(b',')])
    totalShortVolume = 0
    failedRequests = 0
    year = "2009"
    for month in ["08", "09", "10", "11", "12"]:
            for day in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]:
                for exchange in ["FNYX", "FNSQ", "FNQC"]:
                    pastTime = time.time()
                    try:
                        request = httpx.get(baseURL[0] + exchange + baseURL[1] + year + month + day + baseURL[2])
                    except:
                        failedRequests += 1
                        try:
                            time.sleep(1 - (time.time() - pastTime))
                        except:
                            pass
                        continue
                    if (request.status_code != 200):
                        try:
                            time.sleep(1 - (time.time() - pastTime))
                        except:
                            pass
                        continue
                    data = request.read()
                    symdex = data.find(b'|' + ticker + b'|')
                    if (symdex == -1):
                        try:
                            time.sleep(1 - (time.time() - pastTime))
                        except:
                            pass
                        continue
                    try:
                        data = data[data[:symdex].rfind(b'\n') + 1 : symdex + data[symdex:].find(b'\r')]
                        dataList = data.split(b'|')
                        offset = 6 - len(dataList)
                        # Data format --> Date|Symbol|ShortVolume|ShortExemptVolume|TotalVolume|Market OR Date|Symbol|ShortVolume|TotalVolume|Market
                        totalVolume = int(dataList[4 - offset])
                        if (offset):
                            shortVolume = int(dataList[2])
                        else:
                            shortVolume = int(dataList[2]) - int(dataList[3])
                        nonShortVolume = totalVolume - shortVolume
                        uncoveredVolume = shortVolume - nonShortVolume
                        totalShortVolume += uncoveredVolume
                        if (totalShortVolume < 0):
                            totalShortVolume = 0
                    except:
                        pass
                    try:
                        time.sleep(1 - (time.time() - pastTime))
                    except:
                        pass
    for year in ["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021"]:
        for month in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
            for day in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]:
                for exchange in ["FNYX", "FNSQ", "FNQC"]:
                    pastTime = time.time()
                    try:
                        request = httpx.get(baseURL[0] + exchange + baseURL[1] + year + month + day + baseURL[2])
                    except:
                        failedRequests += 1
                        try:
                            time.sleep(1 - (time.time() - pastTime))
                        except:
                            pass
                        continue
                    if (request.status_code != 200):
                        try:
                            time.sleep(1 - (time.time() - pastTime))
                        except:
                            pass
                        continue
                    data = request.read()
                    symdex = data.find(b'|GME|')
                    if (symdex == -1):
                        try:
                            time.sleep(1 - (time.time() - pastTime))
                        except:
                            pass
                        continue
                    try:
                        data = data[data[:symdex].rfind(b'\n') + 1 : symdex + data[symdex:].find(b'\n') - 1]
                        dataList = data.split(b'|')
                        offset = 6 - len(dataList)
                        # Data format --> Date|Symbol|ShortVolume|ShortExemptVolume|TotalVolume|Market OR Date|Symbol|ShortVolume|TotalVolume|Market
                        totalVolume = int(dataList[4 - offset])
                        if (offset):
                            shortVolume = int(dataList[2])
                        else:
                            shortVolume = int(dataList[2]) - int(dataList[3])
                        nonShortVolume = totalVolume - shortVolume
                        uncoveredVolume = shortVolume - nonShortVolume
                        totalShortVolume += uncoveredVolume
                        if (totalShortVolume < 0):
                            totalShortVolume = 0
                    except:
                        pass
                    try:
                        time.sleep(1 - (time.time() - pastTime))
                    except:
                        pass
    print("Failed requests: " + str(failedRequests))
    print(totalShortVolume)
    print("or ...")
    print(str(round((totalShortVolume/floatShares) * 100, 2)) + "% of the current float.")

if (__name__ == "__main__"):
    main(sys.argv)