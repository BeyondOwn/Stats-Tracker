import typing
from bs4 import BeautifulSoup
import re
import requests
import fileinput
import os
import win32api
from get_date import get_date_range
import sys
import threading
import customtkinter
import pandas as pd


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

class NewWindow(customtkinter.CTkToplevel):
        def __init__(self,master=None):
            super().__init__(master = master)
            self.title("Output")
            w=900      #width
            h=700      #height
            ws = self.winfo_screenwidth() # width of the screen
            hs = self.winfo_screenheight() # height of the screen

            # calculate x and y coordinates for the Tk root window
            x = (ws/2) - (w/2)
            y = (hs/2) - (h/2)

            # set the dimensions of the screen 
            # and where it is placed

            self.geometry('%dx%d+%d+%d' % (w, h, x, y))
            
            self.attributes('-topmost', 1)
            self.box1 = customtkinter.CTkTextbox(self,text_color='#2fa550',width=800,height=600,font=("Roboto",18,'bold'))
            self.box1.pack(pady=20,padx=40)

            self.buttoni = customtkinter.CTkButton(self,text="Destroy",font=("Roboto",18,'bold'), command=lambda:[self.destroy()])
            self.buttoni.pack(pady=12,padx=10)


            

class MyGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("green")
        self.title("Stats Tracker")
        w=1000      #width
        h=800       #height
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        # set the dimensions of the screen 
        # and where it is placed

        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        self.main_frame = customtkinter.CTkFrame(self,width=900,height=700)
        self.main_frame.pack(padx=60, pady=20,expand=True,fill='both')


        self.main_frame.grid_columnconfigure(0,weight=1)
        self.main_frame.grid_columnconfigure(1,weight=1)
        self.main_frame.grid_columnconfigure(2,weight=1)
        self.main_frame.grid_columnconfigure(3,weight=1)
        self.main_frame.grid_rowconfigure(0,weight=1)
        self.main_frame.grid_rowconfigure(1,weight=1)
        self.main_frame.grid_rowconfigure(2,weight=1)
        self.main_frame.grid_rowconfigure(3,weight=1)
        self.main_frame.grid_rowconfigure(4,weight=10)
        

        self.sort_by = customtkinter.CTkLabel(self.main_frame,text="Sort By: ",font=("Roboto",24,'bold'))
        self.sort_by.grid(row=0,column=2,sticky='we')

        self.sort_by_combo = customtkinter.CTkComboBox(self.main_frame,width=250,values=["Scor", "Kills", "Secunde"],font=('Roboto',18,'bold'),dropdown_font=('Roboto',18,'bold'),dropdown_text_color='#2fa550',text_color='#2fa550')
        self.sort_by_combo.grid(row=0,column=3)
        self.sort_by_combo.set("Scor")

        self.secunde = customtkinter.CTkLabel(self.main_frame,text="Include Secundele: ",font=("Roboto",24,'bold'))
        self.secunde.grid(row = 1,column=2,sticky="we")

        self.secunde_checkbox = customtkinter.CTkCheckBox(self.main_frame,text="")
        self.secunde_checkbox.grid(row = 1,column=3)
        
        self.start = customtkinter.CTkLabel(self.main_frame,text="Start Date: ",font=("Roboto",24,'bold'))
        self.start.grid(row=0, column=0,sticky="we")

        self.start_entry = customtkinter.CTkEntry(self.main_frame,font=("Roboto",18,'bold'),text_color='#2fa550')
        self.start_entry.grid(row=0, column=1,sticky='we')


        self.end = customtkinter.CTkLabel(self.main_frame,text="End Date: ", font=("Roboto",24,'bold'))
        self.end.grid(row=1, column=0,sticky="we")

        self.end_entry = customtkinter.CTkEntry(self.main_frame,font=("Roboto",18,'bold'),text_color='#2fa550')
        self.end_entry.grid(row=1, column=1,sticky='we')
       

        self.gang = customtkinter.CTkLabel(self.main_frame,text="Gang: ", font=("Roboto",24,'bold'))
        self.gang.grid(row=2, column=0,sticky="we")

        self.gang_entry = customtkinter.CTkEntry(self.main_frame,font=("Roboto",18,'bold'),text_color='#2fa550')
        self.gang_entry.grid(row=2, column=1,sticky='we')

        self.button = customtkinter.CTkButton(self.main_frame,text="Start",font=("Roboto",18,'bold'),width=300,height=50, command=lambda:self.work(self.main1,self.start_entry.get(),self.end_entry.get(),self.gang_entry.get(),self.sort_by_combo.get(),self.secunde_checkbox.get()))
        self.button.grid(row=3, columnspan=4,)

        self.box = customtkinter.CTkTextbox(self.main_frame,text_color='#2fa550',font=("Roboto",18,'bold'),activate_scrollbars=True)
        self.box.grid(row=4, columnspan=4,sticky="wens")


        
    def work(self,func,start,end,gang,sort_by,incl_sec):
        t1=threading.Thread(target=func,args=(start,end,gang,sort_by,incl_sec))
        t1.start()
        #t2 = threading.main_thread()


    def test(self,x1,x2):
        print("test")
        print(x1,x2)

    def main1(self,start_date_input,end_date_input,gang,sort_by,incl_sec):
        self.box.delete("1.0",'end')
        date_counter = 1
        date_arr = []
        sort_by_kills = False
        sort_by_secunde = False
        sort_by_kd = False
        
        match sort_by:
            case "Scor":
                sort_by_kd = True
            case "Kills":
                sort_by_kills = True
            case "Secunde":
                sort_by_secunde = True
        date_arr = get_date_range(start_date_input,end_date_input)
        self.box.insert("end", f"{date_arr}\n")
        self.box.see("end")
        #print(date_arr)
        ##
        if gang.lower() not in view_all_gangs:
            #print('Gang name Invalid')
            self.box.insert("end",'Gang name Invalid\n')
            self.box.see("end")
            return

        links = self.get_war_link(date_arr,view_all_gangs[gang.lower()])
        if links == []:
            self.box.insert("end",f'Gangul {gang.upper()} nu a avut waruri in data de {date_arr[0]}-{date_arr[len(date_arr)-1]}\n')
            self.box.see("end")
            #print(f'Gangul {gang.upper()} nu a avut waruri in data de {date_arr[0]}-{date_arr[len(date_arr)-1]}')
        else:
            links.sort()
            #print("Links: ",links)
            self.box.insert("end",f"Links: {links}\n")
            self.box.see("end")

            ##Writing Wars1,Wars2.csv to wars/ Folder
            self.parse_war(parse_war_gangs[gang.lower()],links)

            ## Adding up all Stats from wars1,wars2.etc to 1 dictionary
            player_stats = self.todo(len(links))

            ## Got the player_stats from all wars into a nested dict, now we sort them
            if (sort_by_kills == True):
                res = sorted(player_stats.items(), key = lambda x: int(x[1]['kills']),reverse=True)
            elif (sort_by_kd == True):
                res = sorted(player_stats.items(), key = lambda x: int(x[1]['kd']),reverse=True)
            elif (sort_by_secunde == True):
                res = sorted(player_stats.items(), key = lambda x: int(x[1]['secunde']),reverse=True)
            window = NewWindow(self.main_frame)
            ### Writing the sorted player_stats to file
            with open(f"{gang.upper()}_{date_arr[0]}-{date_arr[len(date_arr)-1]}.txt", "a+") as f:
                        if incl_sec:
                            window.box1.insert("end",f"Nume Kills Scor Secunde\n")
                            #print(f"Nume Kills Scor Secunde")
                            f.write(f"Nume  Kills  Scor  Secunde  \n")
                        else:
                            window.box1.insert("end",f"Nume Kills Scor\n")
                            #print(f"Nume Kills Scor")
                            f.write(f"Nume  Kills  Scor \n")
                        
                        for u in res:
                            news = str(u[1].values()).lstrip("dict_values([)").rstrip("])")
                            #print(news)
                            name, kills , kd, secunde = news.split(",")
                            name = name.lstrip("'").rstrip("'")
                            kills = kills.replace("'","")
                            kd = kd.replace("'","")
                            secunde = secunde.replace("'","")
                            if incl_sec:
                                window.box1.insert("end",f'{name} {kills} {kd} {secunde}\n')
                                #print(f'{name} {kills} {kd} {secunde}')
                                f.write(f'{name} {kills} {kd} {secunde}\n')
                               
                            else:
                                window.box1.insert("end",f'{name} {kills} {kd}\n')
                                #print(f'{name} {kills} {kd}')
                                f.write(f'{name} {kills} {kd}\n')
                                
                        window.box1.insert("end","\n")
                        #print("\n")
                        window.box1.insert("end",f"Number of Wars: {len(links)}\n")
                        #print(f"Number of Wars: {len(links)}\n")
                        f.write("\n")
                        f.write(f"NUMBER OF WARS: {len(links)}\n")
            date_counter +=1
        
        
        if incl_sec:
            writer = pd.ExcelWriter('color.xlsx',mode='a', if_sheet_exists='overlay', engine='openpyxl')
            wb  = writer.book
            df = pd.read_csv(f"{gang.upper()}_{date_arr[0]}-{date_arr[len(date_arr)-1]}.txt", sep="  ",engine="python")
            df.to_excel(writer,index=False, columns=["Nume","Scor","Kills","Secunde"], header=["NUME","SCOR","KILLS","SECUNDE"])
            wb.save(f"{gang.upper()}_{date_arr[0]}-{date_arr[len(date_arr)-1]}.xlsx")
            wb.close()
            
        else:
            writer = pd.ExcelWriter('color.xlsx',mode='a', if_sheet_exists='overlay', engine='openpyxl')
            wb  = writer.book
            df = pd.read_csv(f"{gang.upper()}_{date_arr[0]}-{date_arr[len(date_arr)-1]}.txt", sep="  ",engine="python")
            df.to_excel(writer,index=False, columns=["Nume","Scor","Kills"], header=["NUME","SCOR","KILLS"])
            wb.save(f"{gang.upper()}_{date_arr[0]}-{date_arr[len(date_arr)-1]}.xlsx")
            wb.close()

        window.box1.insert("end","### DONE ###\n")
        print("### DONE ###")
        # CLEANUP ###
        cleanup()

    def parse_war(self,gang,link):
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
                #print("Attacker!")
                self.box.insert("end","Attacker!\n")
                self.box.see("end")
            else:
                defender = True
                self.box.insert("end","Defender\n")
                self.box.see("end")
                #print("Defender")
                ### Part1
            
            if attacker:
                attacker_players = soup.find("div", id='viewWarAttackerPlayers')
                tr = attacker_players.find_all('tr')
                for x in tr:
                    a = x.find_all('a')
                    nume_jucator = re.search(r'\/players\/general\/(.*?)"',str(a))
                    if nume_jucator:
                        atac_players.append(nume_jucator.group(1))
                    td = x.find_all('td')
                    for y in td:
                        scor = re.search(r'<td>(-?[0-9]+)<\/td>',str(y))
                        if scor:
                            player_stats.append(scor.group(1))
                            ########################################
                #print("Link: ",lin)
                self.box.insert("end",f"Link: {lin}\n")
                self.box.see("end")
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
                    nume_jucator = re.search(r'\/players\/general\/(.*?)"',str(a))
                    if nume_jucator:
                        defend_players.append(nume_jucator.group(1))
                    td = x.find_all('td')
                    for y in td:
                        scor = re.search(r'<td>(-?[0-9]+)<\/td>',str(y))
                        if scor:
                            player_stats.append(scor.group(1))
                            ########################################
                self.box.insert("end",f"Link: {lin}\n")
                self.box.see("end")
                #print("Link: ",lin)
                parse_stats(defend_players,player_stats,cnt)
                atac_players.clear()
                player_stats.clear()
                attacker = False
                defender = False
                cnt+=1

    def get_war_link(self,date_arr,gang):
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
            self.box.insert("end",f"Page: {x}\n")
            #print("Page: ",x)
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
    
    def todo(self,link_length):
        names =set()
        counter = 0
        n=0
        player_stats = {}
        path = os.listdir(os.getcwd()+"/wars")
        csv_path = []
        
        self.box.insert("end",f"Number of Wars: {link_length}\n")
        #print("Number of Wars: ",link_length)
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

class TextRedirector(object):
    def __init__(self, widget,top=True, tag="stdout"):
        self.widget = widget
        self.tag = tag
        self.top = top

    def write(self, string):
        self.widget.configure(state="normal")
        self.widget.insert("end", string, (self.tag,))
        if self.top:
            self.widget.see("end")
        self.widget.configure(state="disabled")
 


    


# CLEANUP ###
def cleanup():
    path_wars_OS = os.getcwd() +"/wars"
    path_wars = os.listdir(os.getcwd()+ "/wars")

    for x in path_wars:
        if x.endswith(".csv"):
            os.remove(f"{path_wars_OS}/{x}")

def on_exit(signal_type):
    path_wars_OS = os.getcwd() +"/wars"
    path_wars = os.listdir(os.getcwd()+ "/wars")
    
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
    director = os.getcwd()
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
        with open(f"{director}/wars/wars{cnt+1}.csv", "a+") as f:
            f.write(f"{atac_or_defend_players[z]},{kills[z]},{kd[z]},{secunde[z]}\n")
    # with open("bla3.csv", "a+") as f:
    #     f.write(f"OVER##########################\n")
        # file = pd.read_csv ('bla3.csv')
        # file.to_excel ('xl.xlsx', index = None, header=True)
    cnt+=1
    return all_elements
        
               
        
def get_turf(link):
    r = requests.get(link)
    soup = BeautifulSoup((r.text), 'html.parser')
    war_page = soup.find("div", class_="viewWarPage")
    turf_div = war_page.find('div', style='text-align: center')
    turf = re.search(r'Turf:\s+(\w+\s*\w*\s*\w*)<br\/>',str(turf_div))

    
    return turf.group(1)
                
    
if __name__ == "__main__":
    win32api.SetConsoleCtrlHandler(on_exit,True)
    app=MyGUI()
    app.mainloop()
