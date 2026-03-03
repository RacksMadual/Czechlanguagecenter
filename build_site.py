#!/usr/bin/env python3
"""
Rebuild the Czech study site: study content + embedded interactive games.
Run: python3 build_site.py  → outputs index.html
"""
import os, re, json, markdown

os.chdir('/home/user/Czechlanguagecenter')

# ─── DATA: vocab decks for in-page practice panels ──────────────────────────
DECKS = {
  "vocab": [
    # Core greetings & intro (A2)
    {"cz":"Dobrý den!","en":"Hello / Good day (formal)"},
    {"cz":"Ahoj!","en":"Hi / Bye (informal)"},
    {"cz":"Jak se máte?","en":"How are you? (formal)"},
    {"cz":"Mám se dobře.","en":"I'm fine."},
    {"cz":"Ujde to.","en":"It's okay / manageable (so-so)"},
    {"cz":"Jak se jmenujete?","en":"What is your name? (formal)"},
    {"cz":"Jmenuji se Prince.","en":"My name is Prince."},
    {"cz":"Odkud jste?","en":"Where are you from?"},
    {"cz":"Jsem z Jihoafrické republiky.","en":"I am from South Africa. (JAR)"},
    {"cz":"Bydlím v Praze.","en":"I live in Prague."},
    {"cz":"Pracuju jako účetní.","en":"I work as an accountant."},
    {"cz":"Jsem zasnoubený.","en":"I am engaged."},
    # Family
    {"cz":"manžel","en":"husband"},{"cz":"manželka","en":"wife"},
    {"cz":"snoubenka","en":"fiancée"},{"cz":"snoubenec","en":"fiancé"},
    {"cz":"syn","en":"son"},{"cz":"dcera","en":"daughter"},
    {"cz":"bratr","en":"brother"},{"cz":"sestra","en":"sister"},
    {"cz":"dědeček","en":"grandfather"},{"cz":"babička","en":"grandmother"},
    {"cz":"rodiče","en":"parents"},{"cz":"děti","en":"children"},
    {"cz":"synovec","en":"nephew"},
    # Marital status
    {"cz":"svobodný / svobodná","en":"single (man / woman)"},
    {"cz":"zasnoubený / zasnoubená","en":"engaged (man / woman)"},
    {"cz":"ženatý","en":"married (man)"},
    {"cz":"vdaná","en":"married (woman)"},
    {"cz":"rozvedený / rozvedená","en":"divorced (man / woman)"},
    # Food & drink
    {"cz":"čaj","en":"tea"},{"cz":"káva","en":"coffee"},
    {"cz":"pivo","en":"beer"},{"cz":"voda","en":"water"},
    {"cz":"polévka","en":"soup"},{"cz":"guláš","en":"goulash"},
    {"cz":"řízek","en":"schnitzel"},{"cz":"knedlíky","en":"dumplings"},
    {"cz":"Dám si kávu.","en":"I'll have a coffee. (ordering = akuzativ)"},
    {"cz":"Dám si guláš.","en":"I'll have goulash. (no change — masc. inanim.)"},
    # Health
    {"cz":"Bolí mě hlava.","en":"My head hurts."},
    {"cz":"Bolí mě v krku.","en":"My throat hurts."},
    {"cz":"Bolí mě záda.","en":"My back hurts."},
    {"cz":"Jsem nemocný/á.","en":"I am ill."},
    {"cz":"Mám teplotu.","en":"I have a fever."},
    {"cz":"Mám rýmu.","en":"I have a runny nose."},
    {"cz":"Jsem nastydlý/á.","en":"I have a cold. (= nachlazený/á)"},
    {"cz":"nemocnice","en":"hospital"},{"cz":"lékárna","en":"pharmacy"},
    # Transport
    {"cz":"metro","en":"metro / underground"},{"cz":"tramvaj","en":"tram"},
    {"cz":"vlak","en":"train"},{"cz":"letadlo","en":"airplane"},
    {"cz":"zastávka","en":"stop (bus/tram)"},{"cz":"nádraží","en":"train station"},
    {"cz":"lístek","en":"ticket"},
    # Location
    {"cz":"byt","en":"flat / apartment"},{"cz":"dům","en":"house"},
    {"cz":"kuchyň","en":"kitchen"},{"cz":"koupelna","en":"bathroom"},
    {"cz":"obývací pokoj","en":"living room"},{"cz":"ložnice","en":"bedroom"},
    {"cz":"náměstí","en":"square"},{"cz":"kavárna","en":"café"},
    {"cz":"banka","en":"bank"},{"cz":"pošta","en":"post office"},
    # Seasons/weather
    {"cz":"jaro","en":"spring"},{"cz":"léto","en":"summer"},
    {"cz":"podzim","en":"autumn"},{"cz":"zima","en":"winter"},
    {"cz":"prší","en":"it rains"},{"cz":"sněží","en":"it snows"},
  ],

  # ── Vocabulary from Prince's actual lessons with Petra ──
  "lesson_vocab": [
    {"cz":"ujde to","en":"it's okay / manageable (so-so response to 'Jak se máte?')"},
    {"cz":"pořád","en":"still / always / constantly"},
    {"cz":"bohužel","en":"unfortunately"},
    {"cz":"samozřejmě","en":"of course"},
    {"cz":"přesně!","en":"exactly! / precisely!"},
    {"cz":"opravdu?","en":"really? / truly?"},
    {"cz":"souhlasím","en":"I agree (souhlasit = to agree)"},
    {"cz":"nesouhlasím","en":"I disagree"},
    {"cz":"jsem zmatený/á","en":"I am confused"},
    {"cz":"promiň / promiňte","en":"sorry (informal / formal)"},
    {"cz":"budu se těšit!","en":"I look forward to it!"},
    {"cz":"oblíbený","en":"favourite / beloved"},
    {"cz":"koníček","en":"hobby"},
    {"cz":"volný den","en":"day off"},
    {"cz":"pracovní den","en":"working day / weekday"},
    {"cz":"mám dovolenou","en":"I am on holiday / vacation"},
    {"cz":"sick day","en":"sick day (used in Czech as-is)"},
    {"cz":"home office","en":"working from home (used in Czech as-is)"},
    {"cz":"ostříhaný/á","en":"just got a haircut"},
    {"cz":"soustředit se","en":"to concentrate / focus (= fokusovat)"},
    {"cz":"sdílet monitor","en":"to share screen (= šérovat)"},
    {"cz":"přesný / akurátní","en":"precise / accurate"},
    {"cz":"kooperace / spolupráce","en":"cooperation / collaboration"},
    {"cz":"cena","en":"price"},
    {"cz":"sleva","en":"discount"},
    {"cz":"peníze","en":"money"},
    {"cz":"hezký / krásný","en":"pretty / beautiful"},
    {"cz":"ošklivý","en":"ugly (= to se mi nelíbí)"},
    {"cz":"Jsou doma.","en":"They are at home. (static location)"},
    {"cz":"Jdu domů.","en":"I am going home. (dynamic movement)"},
    {"cz":"Kdy se sejdeme?","en":"When shall we meet?"},
    {"cz":"příště","en":"next time"},
    {"cz":"filmový festival","en":"film festival"},
    {"cz":"výstava","en":"exhibition"},
    {"cz":"divadelní hra","en":"theatre play"},
    {"cz":"koncert","en":"concert"},
    {"cz":"kulturní program","en":"cultural programme"},
    {"cz":"od … do …","en":"from … to … (e.g., od prvního do desátého)"},
    {"cz":"Mám dnes práci.","en":"I have work today. (= Dnes pracuju.)"},
    {"cz":"odpočívat","en":"to rest / relax"},
    {"cz":"vařit","en":"to cook"},
    {"cz":"nakupovat","en":"to shop / go shopping"},
    {"cz":"sportovat","en":"to do sports"},
    {"cz":"vstávat","en":"to get up / wake up"},
    {"cz":"snídat","en":"to eat breakfast"},
    {"cz":"obědvat","en":"to eat lunch"},
    {"cz":"večeřet","en":"to eat dinner"},
    {"cz":"spát","en":"to sleep"},
    {"cz":"pracovní týden","en":"working week (5 days)"},
    {"cz":"víkend","en":"weekend (sobota + neděle)"},
    {"cz":"téma","en":"topic / theme"},
    {"cz":"program","en":"schedule / programme"},
    {"cz":"například","en":"for example (= třeba)"},
    {"cz":"a tak dále","en":"and so on / etc."},
  ],

  # ── Days, dates, ordinal numbers, parts of day ──
  "dates_time": [
    # Days + v/ve rule: v before 1 consonant, ve before 2+ consonants
    {"cz":"v pondělí","en":"on Monday (pondělí = 1st day of week)"},
    {"cz":"v úterý","en":"on Tuesday"},
    {"cz":"ve středu","en":"on Wednesday (ve! — st- = two consonants)"},
    {"cz":"ve čtvrtek","en":"on Thursday (ve! — čt- = two consonants)"},
    {"cz":"v pátek","en":"on Friday (pátek = favourite day!)"},
    {"cz":"v sobotu","en":"on Saturday"},
    {"cz":"v neděli","en":"on Sunday (neděle = do not work)"},
    {"cz":"o víkendu","en":"on the weekend (sobota + neděle)"},
    {"cz":"pracovní den / všední den","en":"weekday / working day"},
    # Parts of day
    {"cz":"ráno","en":"in the morning"},
    {"cz":"dopoledne","en":"before noon / late morning"},
    {"cz":"v poledne","en":"at noon / midday"},
    {"cz":"odpoledne","en":"in the afternoon"},
    {"cz":"večer","en":"in the evening"},
    {"cz":"v noci","en":"at night"},
    # Ordinal date forms (genitive — used for saying dates in Czech)
    {"cz":"prvního (1.)","en":"on the 1st — e.g. prvního března"},
    {"cz":"druhého (2.)","en":"on the 2nd"},
    {"cz":"třetího (3.)","en":"on the 3rd"},
    {"cz":"čtvrtého (4.)","en":"on the 4th"},
    {"cz":"pátého (5.)","en":"on the 5th"},
    {"cz":"šestého (6.)","en":"on the 6th"},
    {"cz":"sedmého (7.)","en":"on the 7th"},
    {"cz":"osmého (8.)","en":"on the 8th"},
    {"cz":"devátého (9.)","en":"on the 9th"},
    {"cz":"desátého (10.)","en":"on the 10th"},
    {"cz":"dvacátého (20.)","en":"on the 20th"},
    {"cz":"dvacátého prvního (21.)","en":"on the 21st"},
    {"cz":"třicátého (30.)","en":"on the 30th"},
    # Months — genitive form (used after ordinal date)
    {"cz":"ledna","en":"of January — prvního ledna = Jan 1st"},
    {"cz":"února","en":"of February"},
    {"cz":"března","en":"of March"},
    {"cz":"dubna","en":"of April"},
    {"cz":"května","en":"of May"},
    {"cz":"června","en":"of June"},
    {"cz":"července","en":"of July"},
    {"cz":"srpna","en":"of August"},
    {"cz":"září","en":"of September"},
    {"cz":"října","en":"of October"},
    {"cz":"listopadu","en":"of November"},
    {"cz":"prosince","en":"of December"},
    # Useful time phrases
    {"cz":"Kolikátého je dnes?","en":"What is today's date?"},
    {"cz":"Dnes je prvního března.","en":"Today is the 1st of March."},
    {"cz":"V kolik hodin?","en":"At what time?"},
    {"cz":"v jednu hodinu","en":"at one o'clock (v jednu — special form)"},
    {"cz":"ve dvě hodiny","en":"at two o'clock (ve! — dv- = two consonants)"},
    {"cz":"v pět hodin","en":"at five o'clock (v pět — p is single consonant)"},
    {"cz":"ve dvanáct hodin","en":"at twelve o'clock (ve! — dv-)"},
  ],

  # ── Verb conjugations from Petra's lessons ──
  "verbs": [
    # být (to be) — complete conjugation
    {"cz":"být → já jsem","en":"to be → I am"},
    {"cz":"být → ty jsi","en":"to be → you are (informal)"},
    {"cz":"být → on/ona/to je","en":"to be → he/she/it is"},
    {"cz":"být → my jsme","en":"to be → we are"},
    {"cz":"být → vy jste","en":"to be → you are (formal/plural)"},
    {"cz":"být → oni/ony jsou","en":"to be → they are"},
    # dělat (to do) — -á type verb
    {"cz":"dělat → já dělám","en":"to do → I do (dělám)"},
    {"cz":"dělat → ty děláš","en":"to do → you do (informal)"},
    {"cz":"dělat → on/ona dělá","en":"to do → he/she does"},
    {"cz":"dělat → my děláme","en":"to do → we do"},
    {"cz":"dělat → vy děláte","en":"to do → you do (formal/plural)"},
    # pracovat / studovat (to work / study) — -uje type verb
    {"cz":"pracovat → já pracuju","en":"to work → I work"},
    {"cz":"pracovat → ty pracuješ","en":"to work → you work"},
    {"cz":"pracovat → on/ona pracuje","en":"to work → he/she works"},
    {"cz":"studovat → já studuju","en":"to study → I study"},
    {"cz":"studovat → on/ona studuje","en":"to study → he/she studies"},
    {"cz":"telefonovat → já telefonuju","en":"to phone → I phone"},
    # bydlet / mluvit (to live / speak) — -í type verb
    {"cz":"bydlet → já bydlím","en":"to live/reside → I live"},
    {"cz":"bydlet → ty bydlíš","en":"to live/reside → you live"},
    {"cz":"mluvit → já mluvím","en":"to speak → I speak"},
    {"cz":"mluvit → ty mluvíš","en":"to speak → you speak"},
    {"cz":"rozumět → já rozumím","en":"to understand → I understand"},
    {"cz":"vidět → já vidím","en":"to see → I see"},
    # Special verbs
    {"cz":"jíst → já jím","en":"to eat → I eat"},
    {"cz":"jíst → ty jíš","en":"to eat → you eat"},
    {"cz":"jíst → on/ona jí","en":"to eat → he/she eats"},
    {"cz":"pít → já piju","en":"to drink → I drink"},
    {"cz":"pít → ty piješ","en":"to drink → you drink"},
    {"cz":"číst → já čtu","en":"to read → I read"},
    {"cz":"číst → ty čteš","en":"to read → you read"},
    {"cz":"jít → já jdu","en":"to go (on foot) → I go"},
    {"cz":"jet → já jedu","en":"to go (by vehicle) → I travel"},
    {"cz":"hledat → já hledám","en":"to look for → I look for"},
    {"cz":"mít → já mám","en":"to have → I have"},
    {"cz":"mít rád/ráda → já mám rád/a","en":"to like → I like (+ accusative)"},
    {"cz":"dát si → já si dám","en":"to have/order → I'll have (ordering food)"},
    {"cz":"dívat se → já se dívám","en":"to watch/look at → I watch"},
    {"cz":"jmenovat se → já se jmenuji","en":"to be named → My name is"},
    {"cz":"vařit → já vařím","en":"to cook → I cook"},
    {"cz":"nakupovat → já nakupuju","en":"to shop → I shop"},
    {"cz":"soustředit se → já se soustředím","en":"to concentrate → I concentrate"},
  ],

  "phrases": [
    {"cz":"Potřebuji se objednat k doktorovi.","en":"I need to make an appointment with the doctor."},
    {"cz":"Bolí mě v krku.","en":"My throat hurts."},
    {"cz":"Necítím se dobře.","en":"I don't feel well."},
    {"cz":"Kde je nejbližší lékárna?","en":"Where is the nearest pharmacy?"},
    {"cz":"Kolik to stojí?","en":"How much does it cost?"},
    {"cz":"Mohu platit kartou?","en":"Can I pay by card?"},
    {"cz":"Platím hotově.","en":"I'm paying cash."},
    {"cz":"Prosím vás, kde je...?","en":"Excuse me, where is...?"},
    {"cz":"Pět minut pěšky.","en":"Five minutes on foot."},
    {"cz":"Tři stanice metrem.","en":"Three stops by metro."},
    {"cz":"Nerozumím.","en":"I don't understand."},
    {"cz":"Mluvíte anglicky?","en":"Do you speak English?"},
    {"cz":"Co si dáte k jídlu?","en":"What will you have to eat? (waiter asks)"},
    {"cz":"Dám si...","en":"I'll have... (ordering food/drink)"},
    {"cz":"Zaplatím.","en":"I'll pay."},
    {"cz":"Zvlášť nebo dohromady?","en":"Separately or together? (splitting the bill)"},
    {"cz":"Jmenuji se Prince.","en":"My name is Prince."},
    {"cz":"Jsem z Jihoafrické republiky.","en":"I am from South Africa."},
    {"cz":"Studuji češtinu.","en":"I study Czech."},
    {"cz":"Chci získat české občanství.","en":"I want to get Czech citizenship."},
    {"cz":"Budu se těšit!","en":"I look forward to it!"},
    {"cz":"Kdy se sejdeme?","en":"When shall we meet?"},
    {"cz":"Promiňte, nerozumím.","en":"Excuse me, I don't understand."},
    {"cz":"Můžete to zopakovat?","en":"Can you repeat that?"},
    {"cz":"Mluvte pomaleji, prosím.","en":"Please speak more slowly."},
  ],

  "b1vocab": [
    {"cz":"přestože","en":"even though / despite the fact that"},
    {"cz":"nicméně","en":"nevertheless / however"},
    {"cz":"vzhledem k tomu","en":"given that / in view of the fact"},
    {"cz":"naproti tomu","en":"on the other hand / in contrast"},
    {"cz":"jinými slovy","en":"in other words"},
    {"cz":"zároveň","en":"at the same time"},
    {"cz":"kromě toho","en":"besides that / in addition"},
    {"cz":"na rozdíl od","en":"unlike / in contrast to"},
    {"cz":"stěžovat si","en":"to complain"},
    {"cz":"obávat se","en":"to fear / be afraid of"},
    {"cz":"souhlasit","en":"to agree"},
    {"cz":"nesouhlasit","en":"to disagree"},
    {"cz":"záležet na","en":"to depend on"},
    {"cz":"přijít o","en":"to lose (something) / miss out on"},
    {"cz":"vzít na vědomí","en":"to take note of"},
    {"cz":"zaměstnání","en":"employment / job"},
    {"cz":"pracovní smlouva","en":"employment contract"},
    {"cz":"výpověď","en":"notice (resignation/dismissal)"},
    {"cz":"životopis","en":"CV / résumé"},
    {"cz":"pohovor","en":"job interview"},
    {"cz":"pojištění","en":"insurance"},
    {"cz":"sociální dávky","en":"social benefits"},
    {"cz":"zdravotní pojišťovna","en":"health insurance company"},
    {"cz":"trvalý pobyt","en":"permanent residence (A2 exam level)"},
    {"cz":"státní občanství","en":"Czech citizenship (B1 exam level)"},
    {"cz":"přihláška","en":"application form"},
    {"cz":"úřad","en":"office / authority / bureau"},
    {"cz":"žadatel","en":"applicant"},
    {"cz":"potvrzení","en":"confirmation / certificate"},
  ],
}

CITIZENSHIP_Q = [
  {"q":"What colours are on the Czech flag?","a":"White, red, and blue","opts":["White, red, and blue","Red, white, and green","Blue, yellow, and red","White, blue, and yellow"]},
  {"q":"What is the Czech national anthem called?","a":"Kde domov můj?","opts":["Kde domov můj?","Čechy krásné, Čechy mé","Vlajka nad Prahou","Naše vlast"]},
  {"q":"Who wrote the Czech national anthem?","a":"Josef Kajetán Tyl (1834)","opts":["Josef Kajetán Tyl (1834)","Bedřich Smetana","Franz Kafka","Václav Havel"]},
  {"q":"Czech State Day (Den české státnosti) is on...","a":"28. září (September 28)","opts":["28. října (October 28)","28. září (September 28)","17. listopadu (November 17)","1. ledna (January 1)"]},
  {"q":"The founding of Czechoslovakia is remembered on...","a":"28. října 1918","opts":["28. října 1918","17. listopadu 1989","8. května 1945","1. ledna 1993"]},
  {"q":"How many chambers does Czech Parliament have?","a":"Two (Poslanecká sněmovna + Senát)","opts":["One","Two (Poslanecká sněmovna + Senát)","Three","Four"]},
  {"q":"How many members are in the Chamber of Deputies?","a":"200","opts":["81","100","200","300"]},
  {"q":"How many senators are in the Czech Senate?","a":"81","opts":["61","71","81","100"]},
  {"q":"The Czech president is elected for how many years?","a":"5 years (max 2 terms)","opts":["4 years","5 years (max 2 terms)","6 years","7 years"]},
  {"q":"Who is the current Czech president (since 2023)?","a":"Petr Pavel","opts":["Miloš Zeman","Václav Havel","Václav Klaus","Petr Pavel"]},
  {"q":"Who was the first president of Czechoslovakia?","a":"T.G. Masaryk (1918)","opts":["Václav Havel","Edvard Beneš","T.G. Masaryk (1918)","Antonín Novotný"]},
  {"q":"What is the Czech currency?","a":"Koruna česká (Kč)","opts":["Euro (€)","Koruna česká (Kč)","Forint","Zloty"]},
  {"q":"What is the capital city of Czech Republic?","a":"Praha (Prague)","opts":["Brno","Ostrava","Olomouc","Praha (Prague)"]},
  {"q":"How many regions (kraje) does Czech Republic have?","a":"14","opts":["10","12","14","16"]},
  {"q":"When did Czech Republic become independent from Slovakia?","a":"1. ledna 1993","opts":["17. listopadu 1989","28. října 1990","1. ledna 1993","1. května 1994"]},
  {"q":"What river flows through Prague?","a":"Vltava","opts":["Labe","Morava","Vltava","Ohře"]},
  {"q":"The highest mountain in Czech Republic is...","a":"Sněžka (1602 m)","opts":["Praděd","Lysá hora","Sněžka (1602 m)","Říp"]},
  {"q":"Czech ambulance emergency number?","a":"155","opts":["112","150","155","158"]},
  {"q":"Czech police emergency number?","a":"158","opts":["112","150","155","158"]},
  {"q":"Pan-European emergency number?","a":"112","opts":["110","111","112","999"]},
  {"q":"Czech Republic joined the EU in...","a":"2004","opts":["1999","2001","2004","2007"]},
  {"q":"Czech Republic joined NATO in...","a":"1999","opts":["1993","1999","2004","2007"]},
  {"q":"The Velvet Revolution began on...","a":"17. listopadu 1989","opts":["28. října 1989","17. listopadu 1989","1. ledna 1990","28. října 1990"]},
  {"q":"Jan Hus was burned at the stake in...","a":"1415","opts":["1348","1415","1620","1848"]},
  {"q":"Patron saint of Bohemia and Moravia?","a":"Sv. Václav (Saint Wenceslas)","opts":["Sv. Jan Nepomucký","Sv. Prokop","Sv. Václav (Saint Wenceslas)","Sv. Cyril"]},
  {"q":"The Velvet Divorce (split of Czechoslovakia) was in...","a":"1993","opts":["1989","1991","1993","1995"]},
  {"q":"Victory Day (end of WWII) in Czech Republic is...","a":"8. května","opts":["1. května","8. května","28. října","17. listopadu"]},
  {"q":"Labour Day in Czech Republic is...","a":"1. května (May 1)","opts":["1. března","8. května","1. května (May 1)","28. října"]},
  {"q":"Who leads the Czech government (vláda)?","a":"Prime Minister (Předseda vlády)","opts":["President","Speaker of Parliament","Prime Minister (Předseda vlády)","Senate Chairman"]},
  {"q":"How often are Chamber of Deputies elections held?","a":"Every 4 years","opts":["Every 2 years","Every 4 years","Every 5 years","Every 6 years"]},
]

# ─── CSS ─────────────────────────────────────────────────────────────────────
CSS = """
:root {
  --bg:#0f1117;--surface:#1a1d2e;--surface2:#252840;--surface3:#2e3355;
  --accent:#4f8ef7;--accent2:#7c3aed;--green:#22c55e;--red:#ef4444;
  --yellow:#f59e0b;--text:#e2e8f0;--muted:#94a3b8;--border:#2d3154;
  --sidebar-w:280px;
}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--text);display:flex;min-height:100vh;font-size:15px;}

/* SIDEBAR */
#sidebar{width:var(--sidebar-w);min-height:100vh;background:var(--surface);border-right:1px solid var(--border);position:fixed;top:0;left:0;overflow-y:auto;z-index:100;display:flex;flex-direction:column;}
#sidebar-header{padding:18px 20px 14px;border-bottom:1px solid var(--border);}
#sidebar-header h1{font-size:14px;color:var(--accent);font-weight:700;letter-spacing:.05em;text-transform:uppercase;}
#sidebar-header p{font-size:11px;color:var(--muted);margin-top:3px;}
.xp-row{display:flex;align-items:center;gap:6px;margin-top:10px;}
.xp-pill{background:var(--surface2);padding:3px 9px;border-radius:12px;font-size:12px;font-weight:700;color:var(--yellow);}
.streak-pill{background:var(--surface2);padding:3px 9px;border-radius:12px;font-size:12px;font-weight:700;color:#fb923c;}
.xp-bar-wrap{height:4px;background:var(--border);border-radius:4px;margin-top:8px;overflow:hidden;}
.xp-bar-fill{height:100%;background:linear-gradient(90deg,var(--accent),var(--accent2));transition:width .6s;}
#sidebar nav{padding:10px 0;flex:1;}
.nav-section{padding:8px 20px 4px;font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;}
.nav-item{display:block;padding:8px 20px;color:var(--text);text-decoration:none;font-size:13px;border-left:3px solid transparent;transition:all .15s;cursor:pointer;border:none;background:none;width:100%;text-align:left;}
.nav-item:hover{background:var(--surface2);color:var(--accent);}
.nav-item.active{background:var(--surface2);color:var(--accent);border-left-color:var(--accent);}
.badge{display:inline-block;padding:1px 6px;border-radius:10px;font-size:10px;font-weight:600;margin-left:6px;}
.badge-a2{background:#1d4ed830;color:#60a5fa;}
.badge-b1{background:#6d28d930;color:#a78bfa;}
.badge-both{background:#065f4630;color:#6ee7b7;}
#search-bar{width:calc(100% - 40px);margin:10px 20px;padding:7px 12px;background:var(--surface2);border:1px solid var(--border);border-radius:6px;color:var(--text);font-size:12px;}
#search-bar:focus{outline:none;border-color:var(--accent);}
#search-bar::placeholder{color:var(--muted);}

/* MAIN */
#main{margin-left:var(--sidebar-w);flex:1;}
.page{display:none;padding:44px 56px 60px;max-width:900px;}
.page.active{display:block;}

/* CONTENT (rendered markdown) */
.content h1{font-size:22px;color:var(--accent);margin:32px 0 12px;padding-bottom:8px;border-bottom:1px solid var(--border);}
.content h2{font-size:18px;color:#a78bfa;margin:28px 0 10px;}
.content h3{font-size:15px;color:var(--yellow);margin:22px 0 8px;}
.content h4{font-size:13px;color:var(--green);margin:16px 0 6px;text-transform:uppercase;letter-spacing:.05em;}
.content p{line-height:1.7;margin:10px 0;}
.content ul,.content ol{margin:10px 0 10px 24px;}
.content li{line-height:1.7;margin:4px 0;}
.content strong{color:#fbbf24;font-weight:600;}
.content em{color:var(--muted);}
.content code{background:var(--surface2);padding:2px 6px;border-radius:4px;font-family:'Fira Code',monospace;font-size:13px;color:#86efac;}
.content pre{background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:16px;overflow-x:auto;margin:16px 0;}
.content pre code{background:none;padding:0;}
.content blockquote{border-left:3px solid var(--accent2);padding:10px 16px;background:var(--surface2);border-radius:0 8px 8px 0;margin:16px 0;color:var(--muted);}
.content hr{border:none;border-top:1px solid var(--border);margin:28px 0;}
.content a{color:var(--accent);text-decoration:none;}
.content a:hover{text-decoration:underline;}

/* TABLES */
.content table{width:100%;border-collapse:collapse;margin:14px 0;font-size:13.5px;}
.content th{background:var(--surface2);padding:9px 12px;text-align:left;color:var(--accent);font-weight:600;border-bottom:2px solid var(--border);}
.content td{padding:8px 12px;border-bottom:1px solid var(--border);vertical-align:middle;}
.content tr:hover td{background:rgba(79,142,247,.05);}

/* TTS BUTTON (injected into Czech table cells) */
.tts-btn{background:none;border:none;cursor:pointer;font-size:14px;opacity:.55;padding:0 0 0 5px;vertical-align:middle;transition:opacity .15s;}
.tts-btn:hover{opacity:1;}

/* CHECKBOXES */
.content input[type=checkbox]{accent-color:var(--accent);width:14px;height:14px;margin-right:6px;cursor:pointer;}

/* OFFICIAL LINKS BLOCK */
.official-links{background:var(--surface2);border:1px solid var(--border);border-radius:12px;padding:16px 20px;margin:20px 0;}
.official-links h4{color:var(--accent);font-size:13px;font-weight:700;margin-bottom:10px;text-transform:uppercase;letter-spacing:.05em;}
.official-links a{display:flex;align-items:center;gap:8px;padding:8px 12px;background:var(--surface);border-radius:8px;color:var(--text);text-decoration:none;font-size:13px;margin-bottom:6px;border:1px solid var(--border);transition:border-color .15s;}
.official-links a:hover{border-color:var(--accent);color:var(--accent);}
.official-links a span{font-size:11px;color:var(--muted);display:block;margin-top:1px;}

/* PROGRESS BAR */
#progress-bar{position:fixed;top:0;left:var(--sidebar-w);right:0;height:3px;background:var(--border);z-index:200;}
#progress-fill{height:100%;background:linear-gradient(90deg,var(--accent),var(--accent2));width:0;transition:width .1s;}

/* XP TOAST */
.xp-toast{position:fixed;top:14px;right:20px;background:var(--yellow);color:#000;font-weight:800;font-size:13px;padding:5px 14px;border-radius:20px;opacity:0;transform:translateY(-8px);transition:all .25s;pointer-events:none;z-index:500;}
.xp-toast.show{opacity:1;transform:translateY(0);}

/* ─── PRACTICE PANEL ─────────────────────────────────── */
.practice-section{margin-top:40px;border-top:2px solid var(--border);padding-top:24px;}
.practice-header{display:flex;align-items:center;gap:10px;margin-bottom:18px;}
.practice-header h2{font-size:16px;font-weight:800;color:var(--text);}
.practice-header p{font-size:13px;color:var(--muted);}

/* mode tabs */
.mode-tabs{display:flex;gap:8px;margin-bottom:20px;flex-wrap:wrap;}
.mode-tab{padding:8px 16px;border-radius:20px;font-size:13px;font-weight:600;
  background:var(--surface2);border:1px solid var(--border);color:var(--muted);cursor:pointer;transition:all .15s;}
.mode-tab:hover{border-color:var(--accent);color:var(--text);}
.mode-tab.active{background:var(--accent);border-color:var(--accent);color:#fff;}

.game-panel{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:22px;min-height:220px;display:none;}
.game-panel.active{display:block;}

/* shared game UI */
.card-counter{font-size:12px;color:var(--muted);margin-bottom:8px;}
.prog-bar{height:4px;background:var(--surface2);border-radius:4px;margin-bottom:18px;overflow:hidden;}
.prog-fill{height:100%;background:var(--accent);transition:width .3s;}
.gm-q{font-size:17px;font-weight:700;margin-bottom:18px;line-height:1.4;}
.gm-hint{font-size:12px;color:var(--muted);margin-bottom:12px;}
.opts{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:14px;}
.opt{background:var(--surface2);border:2px solid var(--border);border-radius:10px;padding:11px 12px;
  font-size:13px;font-weight:600;color:var(--text);cursor:pointer;text-align:left;line-height:1.4;transition:all .15s;}
.opt:hover:not(:disabled){border-color:var(--accent);}
.opt.correct{background:#22c55e15;border-color:var(--green);color:var(--green);}
.opt.wrong{background:#ef444415;border-color:var(--red);color:var(--red);}
.opt:disabled{cursor:default;}
.feedback{padding:10px 14px;border-radius:8px;font-size:13px;font-weight:600;margin-bottom:12px;display:none;}
.feedback.show{display:flex;align-items:center;gap:8px;}
.feedback.good{background:#22c55e15;color:var(--green);border:1px solid #22c55e30;}
.feedback.bad{background:#ef444415;color:var(--red);border:1px solid #ef444430;}
.gm-next{width:100%;padding:11px;border-radius:10px;font-size:14px;font-weight:700;
  background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;border:none;cursor:pointer;display:none;margin-top:6px;}
.gm-next.show{display:block;}
.hearts{font-size:16px;margin-bottom:10px;}

/* FLASHCARD */
.flip-wrap{perspective:900px;cursor:pointer;margin-bottom:14px;}
.flip-inner{position:relative;width:100%;min-height:160px;transition:transform .4s;transform-style:preserve-3d;}
.flip-wrap.flipped .flip-inner{transform:rotateY(180deg);}
.face{position:absolute;width:100%;min-height:160px;backface-visibility:hidden;
  background:var(--surface2);border:1px solid var(--border);border-radius:14px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;padding:24px;text-align:center;}
.face.back{transform:rotateY(180deg);background:var(--surface3);}
.face .lang{font-size:10px;font-weight:700;color:var(--muted);letter-spacing:.1em;text-transform:uppercase;margin-bottom:10px;}
.face .word{font-size:22px;font-weight:700;line-height:1.3;}
.fc-btns{display:flex;gap:8px;}
.fc-btn{flex:1;padding:10px;border-radius:10px;font-size:13px;font-weight:700;cursor:pointer;border:none;}
.fc-btn.wrong{background:#ef444415;color:var(--red);border:1px solid #ef444430;}
.fc-btn.right{background:#22c55e15;color:var(--green);border:1px solid #22c55e30;}
.fc-btn.next{background:var(--surface2);color:var(--text);border:1px solid var(--border);}
.hear-btn{background:var(--surface2);border:1px solid var(--border);color:var(--accent);
  padding:6px 14px;border-radius:20px;font-size:13px;cursor:pointer;margin-bottom:10px;}
.hear-btn:hover{background:var(--surface3);}
.flip-hint{font-size:12px;color:var(--muted);text-align:center;margin-bottom:8px;}

/* MATCH */
.match-grid{display:grid;grid-template-columns:1fr 1fr;gap:7px;}
.mtile{background:var(--surface2);border:2px solid var(--border);border-radius:9px;
  padding:10px 9px;font-size:12.5px;font-weight:600;text-align:center;cursor:pointer;
  transition:all .2s;min-height:46px;display:flex;align-items:center;justify-content:center;line-height:1.3;}
.mtile:hover{border-color:var(--accent);}
.mtile.sel{border-color:var(--accent);background:rgba(79,142,247,.1);}
.mtile.matched{background:#22c55e10;border-color:var(--green);color:var(--green);cursor:default;}
.mtile.shake{animation:shake .3s;}
@keyframes shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-5px)}75%{transform:translateX(5px)}}
.match-info{font-size:12px;color:var(--muted);margin-bottom:10px;}

/* LISTEN */
.listen-center{text-align:center;margin-bottom:20px;}
.big-play{background:linear-gradient(135deg,var(--accent),var(--accent2));border:none;
  border-radius:50%;width:72px;height:72px;font-size:26px;cursor:pointer;
  display:inline-flex;align-items:center;justify-content:center;transition:transform .15s;}
.big-play:hover{transform:scale(1.08);}
.big-play.pulse{animation:pulse 1.1s ease-out infinite;}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(79,142,247,.5);}70%{box-shadow:0 0 0 18px rgba(79,142,247,0);}100%{box-shadow:0 0 0 0 rgba(79,142,247,0);}}

/* RESULT banner */
.result-banner{background:var(--surface2);border:1px solid var(--border);border-radius:12px;padding:18px 22px;margin-top:14px;text-align:center;display:none;}
.result-banner.show{display:block;}
.result-banner .emoji{font-size:36px;margin-bottom:8px;}
.result-banner .score{font-size:20px;font-weight:800;margin-bottom:4px;}
.result-banner .sub{font-size:13px;color:var(--muted);margin-bottom:14px;}
.play-again{background:var(--accent);color:#fff;border:none;padding:10px 24px;border-radius:20px;font-size:13px;font-weight:700;cursor:pointer;}

/* MOBILE */
#menu-toggle{display:none;position:fixed;top:10px;left:10px;z-index:300;background:var(--surface);border:1px solid var(--border);color:var(--text);padding:7px 12px;border-radius:7px;cursor:pointer;font-size:17px;}
@media(max-width:768px){
  #menu-toggle{display:block;}
  #sidebar{transform:translateX(-100%);transition:transform .2s;}
  #sidebar.open{transform:translateX(0);}
  #main{margin-left:0;}
  .page{padding:56px 18px 40px;}
  #progress-bar{left:0;}
  .opts{grid-template-columns:1fr;}
  .match-grid{grid-template-columns:1fr 1fr;}
}
"""

# ─── GAME JAVASCRIPT ─────────────────────────────────────────────────────────
# Each practice panel has a unique ID (pane prefix). The JS engine is generic.
GAME_JS = r"""
// ── STATE ──
let XP=+localStorage.getItem('xp')||0,STREAK=+localStorage.getItem('streak')||0;
let sessionXP=0,hearts=3,activePanel=null;
const LEVELS=[{n:'Beginner',x:0},{n:'Elementary A1',x:100},{n:'A2 Student',x:300},{n:'B1 Learner',x:700},{n:'B1 Speaker',x:1500}];

function updateXPBar(){
  let lv=0;for(let i=0;i<LEVELS.length;i++)if(XP>=LEVELS[i].x)lv=i;
  const nx=LEVELS[lv+1];
  const pct=nx?Math.min(100,((XP-LEVELS[lv].x)/(nx.x-LEVELS[lv].x))*100):100;
  document.querySelectorAll('.xp-bar-fill').forEach(b=>b.style.width=pct+'%');
  document.querySelectorAll('.xp-val').forEach(b=>b.textContent=XP);
  document.querySelectorAll('.streak-val').forEach(b=>b.textContent=STREAK);
}
updateXPBar();

function addXP(n,pid){
  XP+=n;sessionXP+=n;localStorage.setItem('xp',XP);updateXPBar();
  const t=document.getElementById('xp-toast');if(!t)return;
  t.textContent='+'+n+' XP 🌟';t.classList.add('show');setTimeout(()=>t.classList.remove('show'),1100);
}
function speak(txt){if(!window.speechSynthesis)return;const u=new SpeechSynthesisUtterance(txt);u.lang='cs-CZ';u.rate=0.85;speechSynthesis.cancel();speechSynthesis.speak(u);}
function shuffle(a){return[...a].sort(()=>Math.random()-.5);}
function $i(id){return document.getElementById(id);}

// ── TABS ──
function showTab(panelId,mode){
  const wrap=$i(panelId);if(!wrap)return;
  wrap.querySelectorAll('.mode-tab').forEach(t=>t.classList.toggle('active',t.dataset.mode===mode));
  wrap.querySelectorAll('.game-panel').forEach(p=>p.classList.toggle('active',p.dataset.mode===mode));
  activePanel={panelId,mode};
  if(mode==='flashcard')initFlashcard(panelId);
  else if(mode==='quiz')initQuiz(panelId);
  else if(mode==='match')initMatch(panelId);
  else if(mode==='listen')initListen(panelId);
  else if(mode==='citizenship')initCitizenship(panelId);
}

// ── FLASHCARD ──
const fcState={};
function initFlashcard(pid){
  const raw=JSON.parse($i(pid).dataset.cards);
  const st=fcState[pid]={cards:shuffle(raw).slice(0,14),idx:0,correct:0,flipped:false,sessionXP:0};
  hearts=3;renderFC(pid);
}
function renderFC(pid){
  const st=fcState[pid],card=st.cards[st.idx],total=st.cards.length;
  const p=$i(pid+'-fc');
  p.querySelector('.card-counter').textContent=`Card ${st.idx+1} of ${total}`;
  p.querySelector('.prog-fill').style.width=((st.idx/total)*100)+'%';
  p.querySelector('.fc-cz').textContent=card.cz;
  p.querySelector('.fc-en').textContent=card.en;
  const fw=p.querySelector('.flip-wrap');fw.classList.remove('flipped');st.flipped=false;
  p.querySelector('.flip-hint').style.display='';
  p.querySelector('.fc-btns').style.display='none';
  p.querySelector('.fc-next').style.display='flex';
  p.querySelector('.result-banner').classList.remove('show');
}
function flipFC(pid){
  const st=fcState[pid],p=$i(pid+'-fc');
  const fw=p.querySelector('.flip-wrap');fw.classList.toggle('flipped');
  st.flipped=fw.classList.contains('flipped');
  if(st.flipped){p.querySelector('.flip-hint').style.display='none';p.querySelector('.fc-btns').style.display='flex';p.querySelector('.fc-next').style.display='none';speak(st.cards[st.idx].cz);}
}
function fcAnswer(pid,correct){
  const st=fcState[pid];
  if(correct){addXP(8,pid);st.correct++;st.sessionXP+=8;}
  st.idx++;
  if(st.idx>=st.cards.length){fcShowResult(pid);return;}
  renderFC(pid);
}
function fcNext(pid){const st=fcState[pid];st.idx++;if(st.idx>=st.cards.length){fcShowResult(pid);return;}renderFC(pid);}
function fcShowResult(pid){
  const st=fcState[pid],p=$i(pid+'-fc');
  const pct=Math.round((st.correct/st.cards.length)*100);
  const em=pct>=80?'🏆':pct>=60?'🎉':'💪';
  p.querySelector('.result-banner').classList.add('show');
  p.querySelector('.res-emoji').textContent=em;
  p.querySelector('.res-score').textContent=st.correct+'/'+st.cards.length+' correct ('+pct+'%)';
  p.querySelector('.res-sub').textContent='+'+(pct>=60?'Earned '+st.sessionXP+' XP!':'Keep practising!')
  STREAK++;localStorage.setItem('streak',STREAK);updateXPBar();
}

// ── QUIZ ──
const qzState={};
function initQuiz(pid){
  const raw=JSON.parse($i(pid).dataset.cards);
  const st=qzState[pid]={cards:shuffle(raw).slice(0,12).map(c=>{
    const ask=Math.random()>.5;
    const q=ask?c.cz:c.en,a=ask?c.en:c.cz,lang=ask?'Czech':'English';
    const dist=shuffle(raw.filter(x=>x!==c)).slice(0,3).map(x=>ask?x.en:x.cz);
    return{q,a,opts:shuffle([a,...dist]),lang,cz:c.cz};
  }),idx:0,correct:0,sessionXP:0};
  hearts=3;renderQuiz(pid);
}
function renderQuiz(pid){
  const st=qzState[pid],card=st.cards[st.idx],total=st.cards.length,p=$i(pid+'-quiz');
  p.querySelector('.card-counter').textContent=`Q ${st.idx+1} / ${total}`;
  p.querySelector('.prog-fill').style.width=((st.idx/total)*100)+'%';
  p.querySelector('.hearts').textContent='❤️'.repeat(hearts)+'🖤'.repeat(Math.max(0,3-hearts));
  p.querySelector('.gm-hint').textContent='Translate from '+card.lang+':';
  p.querySelector('.gm-q').textContent=card.q;
  const og=p.querySelector('.opts');og.innerHTML='';
  card.opts.forEach(o=>{const b=document.createElement('button');b.className='opt';b.textContent=o;b.onclick=()=>checkQuiz(pid,o,b);og.appendChild(b);});
  p.querySelector('.feedback').className='feedback';
  p.querySelector('.gm-next').className='gm-next';
  p.querySelector('.result-banner').classList.remove('show');
}
function checkQuiz(pid,chosen,btn){
  const st=qzState[pid],card=st.cards[st.idx],p=$i(pid+'-quiz');
  p.querySelectorAll('.opt').forEach(b=>{b.disabled=true;if(b.textContent===card.a)b.classList.add('correct');});
  const fb=p.querySelector('.feedback');
  if(chosen===card.a){btn.classList.add('correct');fb.className='feedback show good';fb.innerHTML='✅ Correct!';addXP(10,pid);st.correct++;st.sessionXP+=10;speak(card.cz);}
  else{btn.classList.add('wrong');fb.className='feedback show bad';fb.innerHTML='❌ Answer: <strong>'+card.a+'</strong>';hearts=Math.max(0,hearts-1);p.querySelector('.hearts').textContent='❤️'.repeat(hearts)+'🖤'.repeat(3-hearts);}
  p.querySelector('.gm-next').className='gm-next show';
}
function quizNext(pid){
  const st=qzState[pid];st.idx++;
  if(st.idx>=st.cards.length||hearts===0){quizShowResult(pid);return;}
  renderQuiz(pid);
}
function quizShowResult(pid){
  const st=qzState[pid],p=$i(pid+'-quiz');
  const pct=Math.round((st.correct/st.cards.length)*100);
  p.querySelector('.result-banner').classList.add('show');
  p.querySelector('.res-emoji').textContent=pct>=80?'🏆':pct>=60?'🎉':'💪';
  p.querySelector('.res-score').textContent=st.correct+'/'+st.cards.length+' ('+pct+'%)';
  p.querySelector('.res-sub').textContent='Earned '+st.sessionXP+' XP!';
  STREAK++;localStorage.setItem('streak',STREAK);updateXPBar();
}

// ── MATCH ──
const mState={};
function initMatch(pid){
  const raw=JSON.parse($i(pid).dataset.cards);
  const pairs=shuffle(raw).slice(0,7);
  const st=mState[pid]={pairs,sel:null,found:0,total:pairs.length,timer:null,secs:0,sessionXP:0};
  const left=shuffle(pairs.map((c,i)=>({t:c.cz,id:i,type:'cz'})));
  const right=shuffle(pairs.map((c,i)=>({t:c.en,id:i,type:'en'})));
  const tiles=[];for(let i=0;i<left.length;i++){tiles.push(left[i]);tiles.push(right[i]);}
  const p=$i(pid+'-match');
  p.querySelector('.match-info').textContent='⏱ 0s · Match 0 / '+pairs.length;
  const g=p.querySelector('.match-grid');g.innerHTML='';
  tiles.forEach((t,idx)=>{
    const d=document.createElement('div');d.className='mtile';d.textContent=t.t;
    d.dataset.id=t.id;d.dataset.type=t.type;d.dataset.idx=idx;
    d.onclick=()=>matchClick(pid,d);g.appendChild(d);
  });
  clearInterval(st.timer);st.secs=0;
  st.timer=setInterval(()=>{st.secs++;p.querySelector('.match-info').textContent='⏱ '+st.secs+'s · Found '+st.found+' / '+st.total;},1000);
  p.querySelector('.result-banner').classList.remove('show');
}
function matchClick(pid,tile){
  const st=mState[pid];if(tile.classList.contains('matched'))return;
  if(st.sel===tile){tile.classList.remove('sel');st.sel=null;return;}
  if(!st.sel){tile.classList.add('sel');st.sel=tile;return;}
  const a=st.sel,b=tile;
  if(a.dataset.id===b.dataset.id&&a.dataset.type!==b.dataset.type){
    a.classList.remove('sel');a.classList.add('matched');b.classList.add('matched');st.sel=null;st.found++;addXP(12,pid);st.sessionXP+=12;
    speak(a.dataset.type==='cz'?a.textContent:b.textContent);
    const p=$i(pid+'-match');p.querySelector('.match-info').textContent='⏱ '+st.secs+'s · Found '+st.found+' / '+st.total;
    if(st.found===st.total){clearInterval(st.timer);setTimeout(()=>matchShowResult(pid),500);}
  } else {
    a.classList.add('shake');b.classList.add('shake');setTimeout(()=>{a.classList.remove('shake','sel');b.classList.remove('shake');},400);st.sel=null;hearts=Math.max(0,hearts-1);
  }
}
function matchShowResult(pid){
  const st=mState[pid],p=$i(pid+'-match');
  p.querySelector('.result-banner').classList.add('show');
  p.querySelector('.res-emoji').textContent='🏆';
  p.querySelector('.res-score').textContent='All matched in '+st.secs+' seconds!';
  p.querySelector('.res-sub').textContent='Earned '+st.sessionXP+' XP!';
  STREAK++;localStorage.setItem('streak',STREAK);updateXPBar();
}

// ── LISTEN ──
const liState={};
function initListen(pid){
  const raw=JSON.parse($i(pid).dataset.cards);
  const st=liState[pid]={cards:shuffle(raw).slice(0,10),idx:0,correct:0,sessionXP:0};
  hearts=3;renderListen(pid);
}
function renderListen(pid){
  const st=liState[pid],card=st.cards[st.idx],total=st.cards.length,p=$i(pid+'-listen');
  p.querySelector('.card-counter').textContent='Round '+( st.idx+1)+' / '+total;
  p.querySelector('.prog-fill').style.width=((st.idx/total)*100)+'%';
  p.querySelector('.hearts').textContent='❤️'.repeat(hearts)+'🖤'.repeat(Math.max(0,3-hearts));
  const og=p.querySelector('.opts');og.innerHTML='';
  const raw=JSON.parse($i(pid).dataset.cards);
  const dist=shuffle(raw.filter(c=>c!==card)).slice(0,3).map(c=>c.en);
  shuffle([card.en,...dist]).forEach(o=>{const b=document.createElement('button');b.className='opt';b.textContent=o;b.onclick=()=>checkListen(pid,o,b,card);og.appendChild(b);});
  p.querySelector('.feedback').className='feedback';
  p.querySelector('.gm-next').className='gm-next';
  p.querySelector('.result-banner').classList.remove('show');
  setTimeout(()=>speak(card.cz),350);
}
function checkListen(pid,chosen,btn,card){
  const st=liState[pid],p=$i(pid+'-listen');
  p.querySelectorAll('.opt').forEach(b=>{b.disabled=true;if(b.textContent===card.en)b.classList.add('correct');});
  const fb=p.querySelector('.feedback');
  if(chosen===card.en){btn.classList.add('correct');fb.className='feedback show good';fb.innerHTML='✅ '+card.cz;addXP(10,pid);st.correct++;st.sessionXP+=10;}
  else{btn.classList.add('wrong');fb.className='feedback show bad';fb.innerHTML='❌ It was: <strong>'+card.en+'</strong>';hearts=Math.max(0,hearts-1);p.querySelector('.hearts').textContent='❤️'.repeat(hearts)+'🖤'.repeat(3-hearts);}
  p.querySelector('.gm-next').className='gm-next show';
}
function listenNext(pid){const st=liState[pid];st.idx++;if(st.idx>=st.cards.length||hearts===0){listenShowResult(pid);return;}renderListen(pid);}
function listenShowResult(pid){
  const st=liState[pid],p=$i(pid+'-listen');
  const pct=Math.round((st.correct/st.cards.length)*100);
  p.querySelector('.result-banner').classList.add('show');
  p.querySelector('.res-emoji').textContent=pct>=70?'🎧 ':' 📻';
  p.querySelector('.res-score').textContent=st.correct+'/'+st.cards.length+' ('+pct+'%)';
  p.querySelector('.res-sub').textContent='Earned '+st.sessionXP+' XP!';
  STREAK++;localStorage.setItem('streak',STREAK);updateXPBar();
}

// ── CITIZENSHIP QUIZ ──
const czState={};
function initCitizenship(pid){
  const raw=JSON.parse($i(pid).dataset.citizenship);
  const st=czState[pid]={cards:shuffle(raw).slice(0,15),idx:0,correct:0,sessionXP:0};
  hearts=3;renderCZ(pid);
}
function renderCZ(pid){
  const st=czState[pid],card=st.cards[st.idx],total=st.cards.length,p=$i(pid+'-citizenship');
  p.querySelector('.card-counter').textContent='Q '+(st.idx+1)+' / '+total;
  p.querySelector('.prog-fill').style.width=((st.idx/total)*100)+'%';
  p.querySelector('.hearts').textContent='❤️'.repeat(hearts)+'🖤'.repeat(Math.max(0,3-hearts));
  p.querySelector('.gm-q').textContent=card.q;
  const og=p.querySelector('.opts');og.innerHTML='';
  card.opts.forEach(o=>{const b=document.createElement('button');b.className='opt';b.textContent=o;b.onclick=()=>checkCZ(pid,o,b);og.appendChild(b);});
  p.querySelector('.feedback').className='feedback';
  p.querySelector('.gm-next').className='gm-next';
  p.querySelector('.result-banner').classList.remove('show');
}
function checkCZ(pid,chosen,btn){
  const st=czState[pid],card=st.cards[st.idx],p=$i(pid+'-citizenship');
  p.querySelectorAll('.opt').forEach(b=>{b.disabled=true;if(b.textContent===card.a)b.classList.add('correct');});
  const fb=p.querySelector('.feedback');
  if(chosen===card.a){btn.classList.add('correct');fb.className='feedback show good';fb.textContent='✅ Correct!';addXP(10,pid);st.correct++;st.sessionXP+=10;}
  else{btn.classList.add('wrong');fb.className='feedback show bad';fb.innerHTML='❌ Correct: <strong>'+card.a+'</strong>';hearts=Math.max(0,hearts-1);p.querySelector('.hearts').textContent='❤️'.repeat(hearts)+'🖤'.repeat(3-hearts);}
  p.querySelector('.gm-next').className='gm-next show';
}
function czNext(pid){const st=czState[pid];st.idx++;if(st.idx>=st.cards.length||hearts===0){czShowResult(pid);return;}renderCZ(pid);}
function czShowResult(pid){
  const st=czState[pid],p=$i(pid+'-citizenship');
  const pct=Math.round((st.correct/st.cards.length)*100);
  p.querySelector('.result-banner').classList.add('show');
  p.querySelector('.res-emoji').textContent=pct>=80?'🏆':pct>=60?'🎉':'📚';
  p.querySelector('.res-score').textContent=st.correct+'/'+st.cards.length+' ('+pct+'%)';
  p.querySelector('.res-sub').textContent=pct>=60?'Pass rate! Earned '+st.sessionXP+' XP':'Keep studying — you need 60% to pass';
  STREAK++;localStorage.setItem('streak',STREAK);updateXPBar();
}

// ── PAGE NAVIGATION ──
const pages=document.querySelectorAll('.page');
const navItems=document.querySelectorAll('.nav-item');
function showPage(id){
  pages.forEach(p=>p.classList.remove('active'));
  navItems.forEach(n=>n.classList.remove('active'));
  const page=document.getElementById(id);
  const nav=document.querySelector('[data-page="'+id+'"]');
  if(page)page.classList.add('active');if(nav)nav.classList.add('active');
  window.scrollTo(0,0);localStorage.setItem('lastPage',id);
  document.getElementById('sidebar').classList.remove('open');
  updateProgress();
}
function updateProgress(){
  const el=document.scrollingElement;
  const pct=(el.scrollTop/(el.scrollHeight-el.clientHeight))*100||0;
  document.getElementById('progress-fill').style.width=pct+'%';
}
document.addEventListener('scroll',updateProgress);
document.getElementById('search-bar').addEventListener('input',function(){
  const q=this.value.toLowerCase();
  document.querySelectorAll('.nav-item').forEach(i=>i.style.display=i.textContent.toLowerCase().includes(q)?'':'none');
});
document.getElementById('menu-toggle').onclick=()=>document.getElementById('sidebar').classList.toggle('open');
const last=localStorage.getItem('lastPage')||'page-0';showPage(last);

// persist checkboxes
document.querySelectorAll('input[type=checkbox]').forEach(cb=>{
  const key='cb_'+cb.parentElement.textContent.trim().substring(0,40);
  cb.checked=localStorage.getItem(key)==='1';
  cb.addEventListener('change',()=>localStorage.setItem(key,cb.checked?'1':'0'));
});
"""

# ─── HELPERS ─────────────────────────────────────────────────────────────────
CZECH_CHARS = re.compile(r'[áéíóúůěščžřďťňýÁÉÍÓÚŮĚŠČŽŘĎŤŇÝ]')

def add_tts_to_tables(html):
    """Add 🔊 TTS buttons to first <td> of rows that contain Czech chars."""
    def replace_td(m):
        inner = m.group(1)
        if CZECH_CHARS.search(inner) and '<' not in inner:
            safe = inner.replace("'", "\\'")
            return f'<td>{inner} <button class="tts-btn" onclick="speak(\'{safe}\')" title="Hear Czech">🔊</button></td>'
        return m.group(0)
    return re.sub(r'<td>((?:(?!</td>).)+)</td>', replace_td, html)

def fix_links(html):
    """Convert bare URLs into proper anchor tags."""
    url_map = {
        'https://cestina-pro-cizince.cz/obcanstvi/wp-content/uploads/2023/12/zkobc-modelova-varianta_2024.pdf':
            '📄 Download Sample B1 Exam (PDF)',
        'https://cestina-pro-cizince.cz/obcanstvi/en/zkouska-z-ceskeho-jazyka/ke-stazeni-jazyk/':
            '📥 All Language Exam Downloads',
        'https://cestina-pro-cizince.cz/obcanstvi/en/zkouska-z-ceskeho-jazyka/priprava-na-zkousku/modelova-varianta-zkousky-z-ceskeho-jazyka/':
            '🧪 Sample B1 Test Page',
        'https://cestina-pro-cizince.cz/obcanstvi/en/zkouska-z-ceskeho-jazyka/':
            '🌐 B1 Language Exam Info',
        'https://cestina-pro-cizince.cz/obcanstvi/en/databanka-uloh/':
            '📋 All 300 Exam Questions (free!)',
        'https://cestina-pro-cizince.cz/obcanstvi/en/interaktivni-modelovy-test/':
            '🧪 Free Interactive Practice Test',
        'https://obcanstvi.cestina-pro-cizince.cz/index.php?p=ke-stazeni-2&hl=en_US':
            '📥 All Life & Institutions Downloads',
        'https://cestina-pro-cizince.cz/obcanstvi/en/':
            '🌐 cestina-pro-cizince.cz — Official Exam Site',
    }
    for url, label in url_map.items():
        html = html.replace(url, f'<a href="{url}" target="_blank" rel="noopener">{label}</a>')
    return html

def make_practice_panel(panel_id, cards_key, include_citizenship=False):
    """Generate an embedded practice panel with game modes."""
    cards_json = json.dumps(DECKS[cards_key], ensure_ascii=False)
    cz_json = json.dumps(CITIZENSHIP_Q, ensure_ascii=False) if include_citizenship else '[]'
    tabs_html = ''
    panels_html = ''

    modes = [
        ('flashcard', '🃏 Flashcards'),
        ('quiz',      '🧠 Quiz'),
        ('match',     '🎯 Match'),
        ('listen',    '🎧 Listen'),
    ]
    if include_citizenship:
        modes.append(('citizenship', '🏛️ Citizenship Test'))

    for mode, label in modes:
        tabs_html += f'<button class="mode-tab" data-mode="{mode}" onclick="showTab(\'{panel_id}\',\'{mode}\')">{label}</button>\n'

    # --- FLASHCARD PANEL ---
    panels_html += f'''<div class="game-panel" data-mode="flashcard" id="{panel_id}-fc">
  <div class="card-counter">Card 1 of …</div>
  <div class="prog-bar"><div class="prog-fill" style="width:0%"></div></div>
  <div class="flip-wrap" onclick="flipFC('{panel_id}')">
    <div class="flip-inner">
      <div class="face front"><div class="lang">Czech 🇨🇿 — tap to flip</div><div class="word fc-cz"></div></div>
      <div class="face back"><div class="lang">English 🇬🇧</div><div class="word fc-en"></div></div>
    </div>
  </div>
  <p class="flip-hint">👆 Tap the card to reveal the translation</p>
  <button class="hear-btn" onclick="speak(fcState['{panel_id}']?.cards[fcState['{panel_id}']?.idx]?.cz)">🔊 Hear Czech</button>
  <div class="fc-btns" style="display:none">
    <button class="fc-btn wrong" onclick="fcAnswer('{panel_id}',false)">✗ Still learning</button>
    <button class="fc-btn right" onclick="fcAnswer('{panel_id}',true)">✓ Got it!</button>
  </div>
  <div class="fc-btn next" id="{panel_id}-fc-next" style="display:flex"><button class="fc-btn next" onclick="fcNext('{panel_id}')">Next →</button></div>
  <div class="result-banner">
    <div class="emoji res-emoji"></div><div class="score res-score"></div>
    <div class="sub res-sub"></div>
    <button class="play-again" onclick="initFlashcard('{panel_id}')">Play again</button>
  </div>
</div>'''

    # --- QUIZ PANEL ---
    panels_html += f'''<div class="game-panel" data-mode="quiz" id="{panel_id}-quiz">
  <div class="card-counter"></div>
  <div class="prog-bar"><div class="prog-fill" style="width:0%"></div></div>
  <div class="hearts">❤️❤️❤️</div>
  <div class="gm-hint"></div>
  <div class="gm-q"></div>
  <div class="opts"></div>
  <div class="feedback"></div>
  <button class="gm-next" onclick="quizNext('{panel_id}')">Continue →</button>
  <div class="result-banner">
    <div class="emoji res-emoji"></div><div class="score res-score"></div>
    <div class="sub res-sub"></div>
    <button class="play-again" onclick="initQuiz('{panel_id}')">Play again</button>
  </div>
</div>'''

    # --- MATCH PANEL ---
    panels_html += f'''<div class="game-panel" data-mode="match" id="{panel_id}-match">
  <div class="match-info">⏱ 0s · Match 0 / 7</div>
  <div class="match-grid"></div>
  <div class="result-banner">
    <div class="emoji res-emoji"></div><div class="score res-score"></div>
    <div class="sub res-sub"></div>
    <button class="play-again" onclick="initMatch('{panel_id}')">Play again</button>
  </div>
</div>'''

    # --- LISTEN PANEL ---
    panels_html += f'''<div class="game-panel" data-mode="listen" id="{panel_id}-listen">
  <div class="card-counter"></div>
  <div class="prog-bar"><div class="prog-fill" style="width:0%"></div></div>
  <div class="hearts">❤️❤️❤️</div>
  <div class="listen-center">
    <button class="big-play" onclick="speak(liState['{panel_id}']?.cards[liState['{panel_id}']?.idx]?.cz)">🔊</button>
    <p style="font-size:12px;color:var(--muted);margin-top:6px;">Tap to hear again</p>
  </div>
  <div class="opts"></div>
  <div class="feedback"></div>
  <button class="gm-next" onclick="listenNext('{panel_id}')">Continue →</button>
  <div class="result-banner">
    <div class="emoji res-emoji"></div><div class="score res-score"></div>
    <div class="sub res-sub"></div>
    <button class="play-again" onclick="initListen('{panel_id}')">Play again</button>
  </div>
</div>'''

    # --- CITIZENSHIP PANEL ---
    if include_citizenship:
        panels_html += f'''<div class="game-panel" data-mode="citizenship" id="{panel_id}-citizenship">
  <div class="card-counter"></div>
  <div class="prog-bar"><div class="prog-fill" style="width:0%"></div></div>
  <div class="hearts">❤️❤️❤️</div>
  <div class="gm-q"></div>
  <div class="opts"></div>
  <div class="feedback"></div>
  <button class="gm-next" onclick="czNext('{panel_id}')">Continue →</button>
  <div class="result-banner">
    <div class="emoji res-emoji"></div><div class="score res-score"></div>
    <div class="sub res-sub"></div>
    <button class="play-again" onclick="initCitizenship('{panel_id}')">Play again</button>
  </div>
</div>'''

    first_mode = modes[0][0]
    return f'''
<div class="practice-section" id="{panel_id}" data-cards='{cards_json}' data-citizenship='{cz_json}'>
  <div class="practice-header">
    <div>
      <h2>🎮 Practice This Module</h2>
      <p>Choose a game mode to practise what you just studied</p>
    </div>
  </div>
  <div class="mode-tabs">{tabs_html}</div>
  {panels_html}
</div>
<script>showTab('{panel_id}','{first_mode}');</script>
'''

def make_official_links_block():
    return '''
<div class="official-links">
  <h4>🔗 Official Exam Resources</h4>
  <div style="font-size:11px;color:var(--muted);margin-bottom:10px;padding:6px 12px;background:rgba(79,142,247,.07);border-radius:6px;">
    ⚠️ <strong style="color:var(--yellow);">Citizenship exam = B1 level.</strong>
    A2 is for permanent residence (trvalý pobyt) — a separate, earlier exam.
  </div>

  <div style="font-size:11px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.07em;margin:8px 0 6px;">Language Exam (B1)</div>
  <a href="https://cestina-pro-cizince.cz/obcanstvi/en/zkouska-z-ceskeho-jazyka/" target="_blank" rel="noopener">
    🌐 B1 Language Exam — Info Page
    <span>Reading 50min · Listening 30min · Writing 60min · Speaking 15min · Fee CZK 3,700</span>
  </a>
  <a href="https://cestina-pro-cizince.cz/obcanstvi/wp-content/uploads/2023/12/zkobc-modelova-varianta_2024.pdf" target="_blank" rel="noopener">
    📄 Download Sample B1 Exam (PDF) — 2024 edition
    <span>Official model test from ÚJOP Charles University — includes answer key</span>
  </a>
  <a href="https://cestina-pro-cizince.cz/obcanstvi/en/zkouska-z-ceskeho-jazyka/priprava-na-zkousku/modelova-varianta-zkousky-z-ceskeho-jazyka/" target="_blank" rel="noopener">
    🧪 Sample Test Page (+ listening MP3)
    <span>Download page for the official B1 model exam including audio file</span>
  </a>
  <a href="https://cestina-pro-cizince.cz/obcanstvi/en/zkouska-z-ceskeho-jazyka/ke-stazeni-jazyk/" target="_blank" rel="noopener">
    📥 All Language Exam Downloads
    <span>Sample exam PDF, listening MP3, information for candidates, exam rules</span>
  </a>

  <div style="font-size:11px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.07em;margin:14px 0 6px;">Life &amp; Institutions Exam</div>
  <a href="https://cestina-pro-cizince.cz/obcanstvi/en/databanka-uloh/" target="_blank" rel="noopener">
    📋 All 300 Exam Questions (free!)
    <span>Full question database — all possible exam questions are published here in advance</span>
  </a>
  <a href="https://cestina-pro-cizince.cz/obcanstvi/en/interaktivni-modelovy-test/" target="_blank" rel="noopener">
    🧪 Free Interactive Practice Test
    <span>Simulate the real 30-question citizenship knowledge exam online</span>
  </a>
  <a href="https://obcanstvi.cestina-pro-cizince.cz/index.php?p=ke-stazeni-2&hl=en_US" target="_blank" rel="noopener">
    📥 All Life &amp; Institutions Downloads
    <span>Sample exam, question database PDF, monolingual dictionary, candidate info</span>
  </a>
</div>
'''

# ─── SIDEBAR + PAGE DEFINITIONS ──────────────────────────────────────────────
MODULES = [
    ("README.md",                    "Overview & Guide",                   "page-0"),
    ("01_grammar_reference.md",      "01 · Grammar Reference (A2)",        "page-1"),
    ("02_vocabulary_by_topic.md",    "02 · Vocabulary by Topic",           "page-2"),
    ("03_citizenship_knowledge.md",  "03 · Citizenship Exam Topics",       "page-3"),
    ("04_exam_practice.md",          "04 · A2 Exam Practice",              "page-4"),
    ("05_useful_phrases.md",         "05 · Useful Phrases",                "page-5"),
    ("06_B1_grammar_bridge.md",      "06 · B1 Grammar Bridge",             "page-6"),
    ("07_B1_vocabulary_expansion.md","07 · B1 Vocabulary",                 "page-7"),
    ("08_B1_exam_practice.md",       "08 · B1 Exam Practice",              "page-8"),
    ("09_study_roadmap.md",          "09 · Study Roadmap",                 "page-9"),
]

def md_to_html(text):
    text = re.sub(r'- \[ \] ', '- <input type="checkbox"> ', text)
    text = re.sub(r'- \[x\] ', '- <input type="checkbox" checked> ', text)
    return markdown.markdown(text, extensions=['tables','fenced_code','nl2br'])

def build():
    nav_html = ''
    pages_html = ''

    nav_html += '<div class="nav-section">Start here</div>\n'

    for i, (fname, label, pid) in enumerate(MODULES):
        # badges
        if any(x in fname for x in ['B1','b1']):
            badge = '<span class="badge badge-b1">B1</span>'
        elif fname in ('03_citizenship_knowledge.md','09_study_roadmap.md'):
            badge = '<span class="badge badge-both">Both</span>'
        elif fname == 'README.md':
            badge = ''
        else:
            badge = '<span class="badge badge-a2">A2</span>'

        if i == 5:  nav_html += '<div class="nav-section">B1 Level</div>\n'
        elif i == 3: nav_html += '<div class="nav-section">Exam Prep</div>\n'
        elif i == 1: nav_html += '<div class="nav-section">A2 Materials</div>\n'

        nav_html += f'<button class="nav-item" data-page="{pid}" onclick="showPage(\'{pid}\')">{label}{badge}</button>\n'

        # read + render markdown
        try:
            raw = open(fname, encoding='utf-8').read()
        except FileNotFoundError:
            raw = f'# {label}\n\nFile not found.'
        content = md_to_html(raw)

        # post-process
        content = add_tts_to_tables(content)
        content = fix_links(content)

        # per-page extras
        extras = ''
        if fname == 'README.md':
            extras = make_official_links_block()
        elif fname == '01_grammar_reference.md':
            extras = make_practice_panel('pane-verbs', 'verbs')
        elif fname == '02_vocabulary_by_topic.md':
            extras = make_practice_panel('pane-vocab', 'vocab')
        elif fname == '03_citizenship_knowledge.md':
            extras = make_official_links_block()
            extras += make_practice_panel('pane-cz', 'vocab', include_citizenship=True)
        elif fname == '04_exam_practice.md':
            extras = make_practice_panel('pane-lesson', 'lesson_vocab')
        elif fname == '05_useful_phrases.md':
            extras = make_practice_panel('pane-phrases', 'phrases')
        elif fname == '06_B1_grammar_bridge.md':
            extras = make_practice_panel('pane-dates', 'dates_time')
        elif fname == '07_B1_vocabulary_expansion.md':
            extras = make_practice_panel('pane-b1vocab', 'b1vocab')

        pages_html += f'<div class="page" id="{pid}"><div class="content">{content}</div>{extras}</div>\n'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Czech Study — Prince</title>
<style>{CSS}</style>
</head>
<body>
<button id="menu-toggle">☰</button>
<div id="progress-bar"><div id="progress-fill"></div></div>
<div id="xp-toast" class="xp-toast"></div>

<aside id="sidebar">
  <div id="sidebar-header">
    <h1>Czech Study 🇨🇿</h1>
    <p>A2 → B1 · Citizenship Exam</p>
    <div class="xp-row">
      <span class="xp-pill">⭐ <span class="xp-val">0</span> XP</span>
      <span class="streak-pill">🔥 <span class="streak-val">0</span></span>
    </div>
    <div class="xp-bar-wrap"><div class="xp-bar-fill" style="width:0%"></div></div>
  </div>
  <input type="text" id="search-bar" placeholder="Search modules…">
  <nav>
    {nav_html}
  </nav>
</aside>

<main id="main">
{pages_html}
</main>

<script>{GAME_JS}</script>
</body>
</html>"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'index.html written ({os.path.getsize("index.html")//1024} KB)')

if __name__ == '__main__':
    build()
