# LeagueData is not endorsed by Riot Games and does not reflect the views or opinions
# of Riot Games or anyone officially involved in producing or managing Riot Games properties.
# Riot Games and all associated properties are trademarks or registered trademarks of Riot Games, Inc

import requests, pymysql

# INSERIR OS DADOS DA INSTÂNCIA DE BANCO NOS CAMPOS ABAIXO.
con = pymysql.connect(host='', user='', password='')

getversion = "https://ddragon.leagueoflegends.com/api/versions.json"
response = requests.get(getversion)
if response.status_code == 200:
    data = response.json()
    latest_version = data[0]

url = f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/champion.json"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    champions = data['data']
    champion_names = [id for id in champions]
    
    c = con.cursor()
    
    c.execute('''CREATE DATABASE IF NOT EXISTS leaguedatabase;''')
    c.execute('''USE leaguedatabase;''')
    c.execute('''DROP TABLE IF EXISTS champions;''')
    c.execute('''CREATE TABLE champions (
    key_id INT PRIMARY KEY NOT NULL,
    championName varchar(25),
    mainRole varchar(25),
    secondaryRole varchar(25),
    title varchar(75),
    hp int,
    mana int,
    movespeed int,
    armor int,
    magicResistance int,
    attackRange int,
    attackSpeed float
);''')
    print("#! Banco e tabela criados com sucesso. !#\n")
    
    for name in champion_names:        

        placeholder = champions[name]
        roles = placeholder['tags']
        role_1 = roles[0]
        try:
            role_2 = roles[1]
        except IndexError:
            role_2 = ''
        titles = placeholder['title']

        key = placeholder['key']
        key = int(key)

        getstats = placeholder['stats']

        hp = getstats['hp']
        hp = int(hp)

        mana = getstats['mp']
        mana = int(mana)

        ms = getstats['movespeed']
        ms = int(ms)

        armor = getstats['armor']
        armor = int(armor)

        mr = getstats['spellblock']
        mr = int(mr)

        atkrange = getstats['attackrange']
        atkrange = int(atkrange)

        atkspeed = getstats['attackspeed']
        atkspeed = float(atkspeed)

        c.execute(f'''INSERT INTO leaguedatabase.champions VALUES ({key}, '{name}', '{role_1}', '{role_2}', "{titles}", {hp}, {mana}, {ms}, {armor}, {mr}, {atkrange}, {atkspeed});''')
        print(f"#! Campeão {name} adicionado com sucesso. !#\n")
    
    con.commit()
    con.close()
else:
    print(f"Erro ao acessar a API: {response.status_code}")
