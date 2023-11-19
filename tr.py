from bs4 import BeautifulSoup
import re
import requests
import fileinput
import os
import win32api
from get_date import get_date_range



view_all_gangs = {
    "ttb":"tsarbratva",
    "rdt":"reddragon",
    "gsb":"greenstreet",
    "vdt":"verdant",
    "vtb":"vietnamese",
    "sp":"southernpimps",
    "avispa":"avispa",
    "69":"69pier",
    "elc":"elloco"
}
parse_war_gangs={
    "ttb":"The Tsar Bratva",
    "rdt":"Red Dragon Triad",
    "gsb":"Green Street Bloods",
    "vdt":"Verdant Family",
    "vtb":"Vietnamese Boys",
    "sp":"Southern Pimps",
    "avispa":"Avispa Rifa",
    "69":"69 Pier Mobs",
    "elc":"El Loco Cartel"
}


def main():
    try:
        links_missing = False
        date_counter = 1
        incl_sec = False
        date_arr = []
        lista_invoiri = []
        lista_inactivitati = []
        cnt=0
        asd = []
        turf_names=[]
        sort_by_kills = False
        sort_by_kd = False
        sort_by_secunde = False
        start_date_input = input("Start Date: ")
        end_date_input = input("End Date: ")
        if input("Afiseaza Secundele? (y/n):  ") == "y":
            incl_sec = True
        else:
            incl_sec = False 
        sort_by = input("Sort by (kills/kd/secunde) : ")
        if sort_by.lower().strip() == "kills":
            sort_by_kills = True
        elif sort_by.lower().strip() == "kd":
            sort_by_kd = True
        elif sort_by.lower().strip() == "secunde":
            sort_by_secunde = True
        else:
            sort_by_kills = True
        date_arr = get_date_range(start_date_input,end_date_input)
        print(date_arr)
        gang = prompt()
        ##
        while gang.lower() not in view_all_gangs:
            print('Gang name Invalid')
            gang = prompt()

        links = get_war_link(date_arr,view_all_gangs[gang.lower()])
        if links == []:
            print(f'Gangul {gang.upper()} nu a avut waruri in data de {date_arr[0]}-{date_arr[len(date_arr)-1]}')
        else:
            links.sort()
            print("Links: ",links)
            
            asd = parse_war(parse_war_gangs[gang.lower()],links,lista_invoiri,lista_inactivitati)

            lista_invoiri = asd[0]
            lista_inactivitati = asd[1]
            ## got the wars/wars1..wars2..etc

            
                
            player_stats = todo(len(links),lista_invoiri,lista_inactivitati)
            ### Got the scrapper working and into a .csv, now work on the CSV
            # print("invoiri: ",lista_invoiri)
            # print("inactivitati: ",lista_inactivitati)
            # print("PLAYER STATS: ",player_stats)
            with open(f"evidente/evidenta.csv", "a+") as f:
                        for xy in player_stats:
                            try:
                                name,kills,kd,secunde =player_stats[xy].values()
                                f.write(f'{name} {kills} {kd} {secunde}\n')
                            except ValueError:
                                f.write(f"Couldn't unpack values! \n")
            date_counter +=1

        final_player_stats = final_add()
        #print("Final player stats:",final_player_stats)
        
        if (sort_by_kills == True):
            res = sorted(final_player_stats.items(), key = lambda x: int(x[1]['kills']),reverse=True)
        elif (sort_by_kd == True):
            res = sorted(final_player_stats.items(), key = lambda x: int(x[1]['kd']),reverse=True)
        elif (sort_by_secunde == True):
            res = sorted(final_player_stats.items(), key = lambda x: int(x[1]['secunde']),reverse=True)
        ##
        #print("Sorted: ",res)
        with open(f"final{gang}{date_arr[0]}-{date_arr[len(date_arr)-1]}.txt", "a+") as f:
                        if incl_sec:
                            f.write(f"Nume Kills KD Secunde \n")
                        else:
                            f.write(f"Nume Kills KD \n")
                        for u in res:
                            try:
                                news = str(u[1].values()).lstrip("dict_values([)").rstrip("])")
                                #print(news)
                                name, kills , kd, secunde = news.split(",")
                                name = name.lstrip("'").rstrip("'")
                                kills = kills.replace("'","")
                                kd = kd.replace("'","")
                                secunde = secunde.replace("'","")
                                if incl_sec:
                                    f.write(f'{name} {kills} {kd} {secunde}\n')
                                else:
                                    f.write(f'{name} {kills} {kd}\n')
                            except ValueError:
                                f.write(f"Couldn't unpack values! \n")
        print("### DONE ###")
        
        ### Got them from 4 csvs into 1 csv and now export to excel ###
        # df = pd.read_csv(txt_file, sep=" ",)
        # df.to_excel("color.xlsx",startcol=coloana_inceput,columns=["Nume","Scor","Secunde","Prezenta"])
        # match len(links):
        #     case 1:
        #         writer = ExcelWriter('color.xlsx',mode='a', if_sheet_exists='overlay', engine='openpyxl')
        #         wb  = writer.book
        #         df = read_csv("evidenta.csv", sep=" ", names=["Nume","Kills","Scor","Secunde",'a', 'b', 'c', 'd', 'f', 'g' ,'i','k', 'y' ,'z',"sanctiuneScor","sanctiunePrezenta","x",])
        #         df.to_excel(writer,index=False, columns=["Nume","Kills","Scor","Secunde",'a', 'b', 'c', 'd', 'f', 'g','i','k', 'y' ,'z',"sanctiuneScor","sanctiunePrezenta","x"], header=["Nume","Kills","Scor","Secunde","","","","","","","","","","sanctiuneScor","sanctiunePrezenta","",""])
        #         wb.save(f'{gang}{date}.xlsx')
        #         wb.close()
        #     case 2:
        #         writer = ExcelWriter('color.xlsx',mode='a', if_sheet_exists='overlay', engine='openpyxl')
        #         wb  = writer.book
        #         df = read_csv("evidenta.csv", sep=" ", names=["Nume","Kills","Scor","Secunde","Kills2","Scor2","Secunde2",'a', 'b', 'c', 'd', 'f', 'g' ,"sanctiuneScor","sanctiunePrezenta","x",])
        #         df.to_excel(writer,index=False, columns=["Nume","Kills","Scor","Secunde","Kills2","Scor2","Secunde2",'a', 'b', 'c', 'd', 'f', 'g',"sanctiuneScor","sanctiunePrezenta","x"], header=["Nume","Kills","Scor","Secunde","Kills","Scor","Secunde","","","","","","","sanctiuneScor","sanctiunePrezenta","",])
        #         wb.save(f'{gang}{date}.xlsx')
        #         wb.close()
        #     case 3:
        #         writer = ExcelWriter('color.xlsx',mode='a', if_sheet_exists='overlay', engine='openpyxl')
        #         wb  = writer.book
        #         df = read_csv("evidenta.csv", sep=" ", names=["Nume","Kills","Scor","Secunde","Kills2","Scor2","Secunde2","Kills3","Scor3","Secunde3",'a','b','c',"sanctiuneScor","sanctiunePrezenta","x"])
        #         df.to_excel(writer,index=False, columns=["Nume","Kills","Scor","Secunde","Kills2","Scor2","Secunde2","Kills3","Scor3","Secunde3","a","b","c",'sanctiuneScor',"sanctiunePrezenta","x"], header=["Nume","Kills","Scor","Secunde","Kills","Scor","Secunde","Kills","Scor","Secunde","","","","sanctiuneScor","sanctiunePrezenta","",])
        #         wb.save(f'{gang}{date}.xlsx')
        #         wb.close()
        #     case 4:
        #         writer = ExcelWriter('color.xlsx',mode='a', if_sheet_exists='overlay', engine='openpyxl')
        #         wb  = writer.book
        #         df = read_csv("evidenta.csv", sep=" ", names=["Nume","Kills","Scor","Secunde","Kills2","Scor2","Secunde2","Kills3","Scor3","Secunde3","Kills4","Scor4","Secunde4",'sanctiuneScor',"sanctiunePrezenta"])
        #         df.to_excel(writer,index=True, index_label="Nume", columns=["Nume","Kills","Scor","Secunde","Kills2","Scor2","Secunde2","Kills3","Scor3","Secunde3","Kills4","Scor4","Secunde4",'sanctiuneScor',"sanctiunePrezenta"], header=["Kills","Scor","Secunde","Kills","Scor","Secunde","Kills","Scor","Secunde","Kills","Scor","Secunde",'sanctiuneScor',"sanctiunePrezenta","",])
        #         wb.save(f'{gang}{date}.xlsx')
        #         wb.close()
        
        # CLEANUP ###
        cleanup()
    except Exception:
        cleanup()
    finally:
        cleanup()


def final_add():
    path = os.listdir(os.getcwd()+"/evidente")
    names = set()
    player_stats = {}
    csv_path = []
    for x in path:
        if x.endswith(f".csv"):
            csv_path.append(f"evidente/{x}")

    with fileinput.input(files=csv_path, encoding="utf-8") as f:
        for line in f:
            filename = f.filename()
            name,kills,kd,secunde = line.strip('\n').split(" ")
            if name not in names:
                player = {
                "name":name,
                "kills":kills,
                "kd":kd,
                "secunde":secunde
                }
                names.add(name)
                player_stats[name] = player.copy()
                    
            else:
                player_stats[name].update({
                    f"kills":int(player_stats[name]['kills'])+int(kills),
                    f"kd":int(player_stats[name]['kd'])+int(kd),
                    f"secunde":int(player_stats[name]['secunde'])+int(secunde),
                })
                        
                   
    # print(player_stats)
    return player_stats

# CLEANUP ###
def cleanup():
    path_wars_OS = os.getcwd() +"/wars"
    path_wars = os.listdir(os.getcwd()+ "/wars")
    path_evd_OS = os.getcwd() +"/evidente"
    path_evd= os.listdir(os.getcwd()+ "/evidente")
    path_OS = os.getcwd()
    path = os.listdir(os.getcwd())
    for x  in path_evd:
        if x.endswith(".csv"):
            os.remove(f"{path_evd_OS}/{x}")
    for x in path_wars:
        if x.endswith(".csv"):
            os.remove(f"{path_wars_OS}/{x}")
    return

def on_exit(signal_type):
    path_wars_OS = os.getcwd() +"/wars"
    path_wars = os.listdir(os.getcwd()+ "/wars")
    path_evd_OS = os.getcwd() +"/evidente"
    path_evd= os.listdir(os.getcwd()+ "/evidente")
    path_OS = os.getcwd()
    path = os.listdir(os.getcwd())
    for x  in path_evd:
        if x.endswith(".csv"):
            os.remove(f"{path_evd_OS}/{x}")
    for x in path_wars:
        if x.endswith(".csv"):
            os.remove(f"{path_wars_OS}/{x}")
   


def prompt():
    print("Exemple Ganguri: ttb rdt gsb vdt vtb sp avispa 69 elc")
    gang = input("Gang: ")
    
    return gang
    
def parse_stats(atac_or_defend_players,player_stats,cnt):
    all_elements={}
    kills = []
    deaths = []
    kd = []
    secunde = []
    incrementer = 0
    counter2 = 0
    for z in range(len(atac_or_defend_players)):
        kills.append(player_stats[0+incrementer])
        kd.append(player_stats[2+incrementer])
        secunde.append(player_stats[3+incrementer])
        player = {
            "name":atac_or_defend_players[z],
            "kills":kills[z],
            "kd":kd[z],
            "secunde":secunde[z]
        }
        all_elements[counter2] = player.copy()
        incrementer +=4
        counter2+=1
        # print(f"{atac_players[z]} Kills:{kills[z]}  Deaths:{deaths[z]},  KD:{kd[z]}  Secunde:{secunde[z]}")
        with open(f"wars/wars{cnt+1}.csv", "a+") as f:
            f.write(f"{atac_or_defend_players[z]},{kills[z]},{kd[z]},{secunde[z]}\n")
    # with open("bla3.csv", "a+") as f:
    #     f.write(f"OVER##########################\n")
        # file = pd.read_csv ('bla3.csv')
        # file.to_excel ('xl.xlsx', index = None, header=True)
    cnt+=1
    return all_elements
        
            
def parse_war(gang,link,lista_invoiri,lista_inactivitati):
    true_elements = {}
    attacker = False
    defender = False
    atac_players=[]
    defend_players=[]
    player_stats=[]
    cnt = 0
   
    for lin in link:
        atac_players.clear()
        defend_players.clear()
        player_stats.clear()
        attacker = False
        defender = False
        r = requests.get(lin)
        soup = BeautifulSoup(r.text,'html.parser')
        war_top = soup.find("div", class_='viewWarTop')
        a = war_top.find_all('a')
        if gang in a[0]:
            attacker = True
            print("Attacker!")
        else:
            defender = True
            print("Defender")
            ### Part1
        
        if attacker:
            attacker_players = soup.find("div", id='viewWarAttackerPlayers')
            tr = attacker_players.find_all('tr')
            for x in tr:
                a = x.find_all('a')
                nume_jucator = re.search(r'\/players\/general\/([\.\$\_\?@\[]*\w+[_\.@\[]*\w*[\.@\]]*\w*)"',str(a))
                if nume_jucator:
                    atac_players.append(nume_jucator.group(1))
                td = x.find_all('td')
                for y in td:
                    scor = re.search(r'<td>(-?[0-9]+)<\/td>',str(y))
                    if scor:
                        player_stats.append(scor.group(1))
                        ########################################
            print("Link: ",lin)
            parse_stats(atac_players,player_stats,cnt)
            cnt+=1
            atac_players.clear()
            player_stats.clear()
            attacker = False
            defender = False
        
        

        elif defender:
            defender_players = soup.find("div", id='viewWarDefenderPlayers')
            tr = defender_players.find_all('tr')
            for x in tr:
                a = x.find_all('a')
                nume_jucator = re.search(r'\/players\/general\/([\.\$\_\?@\[]*\w+[_\.@\[]*\w*[\.@\]]*\w*)"',str(a))
                if nume_jucator:
                    defend_players.append(nume_jucator.group(1))
                td = x.find_all('td')
                for y in td:
                    scor = re.search(r'<td>(-?[0-9]+)<\/td>',str(y))
                    if scor:
                        player_stats.append(scor.group(1))
                        ########################################
            print("Link: ",lin)
            parse_stats(defend_players,player_stats,cnt)
            atac_players.clear()
            player_stats.clear()
            attacker = False
            defender = False
            cnt+=1
            
        
    
    return lista_invoiri,lista_inactivitati
    print("######################################################################################################")
    # if attacker:
    #     for x in atac_players:
    #         print(x)
    # elif defender:
    #     for x in defend_players:
    #         print(x)

def get_war_link(date_arr,gang):
    dates=[]
    links=[]
    primul=""
    found = []
    pages=[]
    i=0

    day,month,year = date_arr[0].split(".")
    # Get X where "Page 1 of X"
    r = requests.get(f"https://www.rpg.b-zone.ro/wars/viewall/gang/{gang}")
    soup = BeautifulSoup((r.text), 'html.parser')
    pagination = soup.find("span", class_="showJumper")
    rgx = re.search(r'Page 1 of ([0-9]{3})',str(pagination))
    if rgx:
        iterate = rgx.group(1)
    for x in range(int(iterate)):
        i+=1
        pages.append(i)
    ##
    for x in pages:
        r = requests.get(f"https://www.rpg.b-zone.ro/wars/viewall/gang/{gang}/{x}")
        soup = BeautifulSoup((r.text), 'html.parser')
        print("Page: ",x)
        table_full = soup.find("div", class_="tableFull")
        tr = table_full.find_all('tr')
        for x in tr:
            td = x.find_all("td")
            for d in td:
                regex = re.search(r'([0-9]{2}\.[0-9]{2}\.[0-9]{4})',str(d))
                if regex:
                    pageDay,pageMonth,pageYear = regex.group(1).split(".")
                    if regex.group(1) in date_arr:
                        # print("pageDay: ",pageDay)
                        # print("pageMonth: ",pageMonth)
                        # print("pageYear: ",pageYear)
                        # print("Day: ",day)
                        # print("Month: ",month)
                        # print("Year: ",year)
                        found.append("found")
                        primul = found.index("found")
                        dates.append(x)
                        # print("Found: ",found)
                        # print("primul: ",primul)
                        # if len(dates) == 4:
                        #         for link in dates:
                        #             regex2 = re.search(r'\/([0-9]{5})',str(link))
                        #             if regex2:
                        #                 links.append(f"https://www.rpg.b-zone.ro/wars/view/{regex2.group(1)}")
                        #         return links
                    elif pageMonth < month and pageYear == year or pageYear < year:
                        if dates:
                            for link in dates:
                                    # print("Dates: ",link)
                                    regex2 = re.search(r'\/([0-9]{5})',str(link))
                                    if regex2:
                                        links.append(f"https://www.rpg.b-zone.ro/wars/view/{regex2.group(1)}")
                        return links
                    else:
                        found.append("cold")
                        # print("Found: ",found)
                        if primul or primul == 0:
                            if found[primul+found.count("found")] == "cold":
                                for link in dates:
                                    # print("Dates: ",link)
                                    regex2 = re.search(r'\/([0-9]{5})',str(link))
                                    if regex2:
                                        links.append(f"https://www.rpg.b-zone.ro/wars/view/{regex2.group(1)}")
                                return links
                                
    #print(f'Gangul {gang.upper()} nu a avut waruri in data de {date}')                              
    return links
                                

def todo(link_length,lista_invoiri,lista_inactivitati,min_sec1=0,min_sec2=0,min_sec3=0,min_sec4=0):
    names =set()
    counter = 0
    n=0
    player_stats = {}
    path = os.listdir(os.getcwd()+"/wars")
    csv_path = []
    print("Number of Wars: ",link_length)
    for x in path:
        if x.endswith(f".csv"):
            csv_path.append(f"wars/{x}")

    with fileinput.input(files=csv_path, encoding="utf-8") as f:
        for line in f:
            filename = f.filename()
            name,kills,kd,secunde = line.strip('\n').split(",")
            if name not in names:
                player = {
                "name":name,
                "kills":kills,
                "kd":kd,
                "secunde":secunde
                }
                names.add(name)
                player_stats[name] = player.copy()
                    
            else:
                player_stats[name].update({
                    f"kills":int(player_stats[name]['kills'])+int(kills),
                    f"kd":int(player_stats[name]['kd'])+int(kd),
                    f"secunde":int(player_stats[name]['secunde'])+int(secunde),
                })
                        
                   
    # print(player_stats)
    return player_stats
        
def get_turf(link):
    r = requests.get(link)
    soup = BeautifulSoup((r.text), 'html.parser')
    war_page = soup.find("div", class_="viewWarPage")
    turf_div = war_page.find('div', style='text-align: center')
    turf = re.search(r'Turf:\s+(\w+\s*\w*\s*\w*)<br\/>',str(turf_div))

    
    return turf.group(1)
                
    
if __name__ == "__main__":
    win32api.SetConsoleCtrlHandler(on_exit,True)
    main()