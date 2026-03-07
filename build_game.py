#!/usr/bin/env python3
"""Build an interactive Czech language game - learn.html"""
import json, os

os.chdir('/home/user/Czechlanguagecenter')

# ── VOCABULARY DECKS ────────────────────────────────────────────────────────
DECKS = [
  {"id":"greetings","name":"Greetings","emoji":"👋","level":"A2","cards":[
    {"cz":"Dobrý den!","en":"Hello / Good day (formal)"},
    {"cz":"Ahoj!","en":"Hi / Bye (informal)"},
    {"cz":"Dobré ráno!","en":"Good morning"},
    {"cz":"Dobrý večer!","en":"Good evening"},
    {"cz":"Na shledanou!","en":"Goodbye (formal)"},
    {"cz":"Čau!","en":"Bye (informal)"},
    {"cz":"Jak se máte?","en":"How are you? (formal)"},
    {"cz":"Jak se máš?","en":"How are you? (informal)"},
    {"cz":"Mám se dobře.","en":"I'm fine."},
    {"cz":"Mám se špatně.","en":"I'm not well."},
    {"cz":"Ujde to.","en":"So-so / Not bad."},
    {"cz":"Jak se jmenujete?","en":"What is your name? (formal)"},
    {"cz":"Jmenuji se...","en":"My name is..."},
    {"cz":"Odkud jste?","en":"Where are you from?"},
    {"cz":"Bydlím v Praze.","en":"I live in Prague."},
    {"cz":"Kolik je Vám let?","en":"How old are you? (formal)"},
    {"cz":"Pracuji jako...","en":"I work as..."},
  ]},
  {"id":"family","name":"Family","emoji":"👨‍👩‍👧","level":"A2","cards":[
    {"cz":"manžel","en":"husband"},
    {"cz":"manželka","en":"wife"},
    {"cz":"tatínek","en":"father / dad"},
    {"cz":"maminka","en":"mother / mum"},
    {"cz":"syn","en":"son"},
    {"cz":"dcera","en":"daughter"},
    {"cz":"bratr","en":"brother"},
    {"cz":"sestra","en":"sister"},
    {"cz":"dědeček","en":"grandfather"},
    {"cz":"babička","en":"grandmother"},
    {"cz":"vnuk","en":"grandson"},
    {"cz":"vnučka","en":"granddaughter"},
    {"cz":"strýc","en":"uncle"},
    {"cz":"teta","en":"aunt"},
    {"cz":"přítel","en":"boyfriend / friend (m)"},
    {"cz":"přítelkyně","en":"girlfriend / friend (f)"},
    {"cz":"rodiče","en":"parents"},
    {"cz":"děti","en":"children"},
    {"cz":"svobodný/á","en":"single"},
    {"cz":"ženatý / vdaná","en":"married (m/f)"},
    {"cz":"rozvedený/á","en":"divorced"},
  ]},
  {"id":"professions","name":"Professions","emoji":"💼","level":"A2","cards":[
    {"cz":"učitel / učitelka","en":"teacher (m/f)"},
    {"cz":"lékař / doktorka","en":"doctor (m/f)"},
    {"cz":"student / studentka","en":"student (m/f)"},
    {"cz":"účetní","en":"accountant"},
    {"cz":"manažer / manažerka","en":"manager (m/f)"},
    {"cz":"politik / politička","en":"politician (m/f)"},
    {"cz":"zpěvák / zpěvačka","en":"singer (m/f)"},
    {"cz":"Pracuji v kanceláři.","en":"I work in an office."},
    {"cz":"Pracuji z domova.","en":"I work from home."},
    {"cz":"Mám hodně práce.","en":"I have a lot of work."},
  ]},
  {"id":"daily","name":"Daily Life","emoji":"🌅","level":"A2","cards":[
    {"cz":"ráno","en":"morning (early)"},
    {"cz":"dopoledne","en":"morning (late)"},
    {"cz":"v poledne","en":"at noon"},
    {"cz":"odpoledne","en":"afternoon"},
    {"cz":"večer","en":"evening"},
    {"cz":"v noci","en":"at night"},
    {"cz":"vstávat","en":"to get up"},
    {"cz":"snídat","en":"to have breakfast"},
    {"cz":"obědvat","en":"to have lunch"},
    {"cz":"večeřet","en":"to have dinner"},
    {"cz":"jít spát","en":"to go to sleep"},
    {"cz":"jít do práce","en":"to go to work"},
    {"cz":"nakupovat","en":"to go shopping"},
    {"cz":"vařit","en":"to cook"},
    {"cz":"číst","en":"to read"},
    {"cz":"snídaně","en":"breakfast"},
    {"cz":"oběd","en":"lunch"},
    {"cz":"večeře","en":"dinner"},
    {"cz":"svačina","en":"snack"},
  ]},
  {"id":"food","name":"Food & Drink","emoji":"🍽️","level":"A2","cards":[
    {"cz":"čaj","en":"tea"},
    {"cz":"káva","en":"coffee"},
    {"cz":"pivo","en":"beer"},
    {"cz":"víno","en":"wine"},
    {"cz":"voda","en":"water"},
    {"cz":"mléko","en":"milk"},
    {"cz":"polévka","en":"soup"},
    {"cz":"guláš","en":"goulash"},
    {"cz":"řízek","en":"schnitzel"},
    {"cz":"kuře","en":"chicken"},
    {"cz":"ryba","en":"fish"},
    {"cz":"knedlíky","en":"dumplings"},
    {"cz":"zelenina","en":"vegetables"},
    {"cz":"ovoce","en":"fruit"},
    {"cz":"zmrzlina","en":"ice cream"},
    {"cz":"dort","en":"cake"},
    {"cz":"chleba","en":"bread"},
    {"cz":"Dám si...","en":"I'll have... (ordering)"},
    {"cz":"Zaplatím.","en":"I'll pay."},
    {"cz":"Jídelní lístek","en":"menu"},
  ]},
  {"id":"health","name":"Health","emoji":"🏥","level":"A2","cards":[
    {"cz":"hlava","en":"head"},
    {"cz":"oči","en":"eyes"},
    {"cz":"ucho","en":"ear"},
    {"cz":"nos","en":"nose"},
    {"cz":"krk","en":"throat / neck"},
    {"cz":"záda","en":"back"},
    {"cz":"ruka","en":"hand / arm"},
    {"cz":"noha","en":"leg / foot"},
    {"cz":"břicho","en":"stomach"},
    {"cz":"srdce","en":"heart"},
    {"cz":"Bolí mě hlava.","en":"My head hurts."},
    {"cz":"Jsem nemocný/á.","en":"I am ill."},
    {"cz":"Mám teplotu.","en":"I have a fever."},
    {"cz":"Mám rýmu.","en":"I have a cold."},
    {"cz":"nemocnice","en":"hospital"},
    {"cz":"lékárna","en":"pharmacy"},
    {"cz":"pohotovost","en":"emergency / urgent care"},
    {"cz":"záchranná služba — 155","en":"ambulance — call 155"},
    {"cz":"policie — 158","en":"police — call 158"},
    {"cz":"evropský záchranný systém — 112","en":"European emergency — 112"},
  ]},
  {"id":"shopping","name":"Shopping","emoji":"🛒","level":"A2","cards":[
    {"cz":"obchod","en":"shop"},
    {"cz":"supermarket","en":"supermarket"},
    {"cz":"pokladna","en":"checkout / cashier"},
    {"cz":"Kolik to stojí?","en":"How much does it cost?"},
    {"cz":"Levný/á/é","en":"cheap"},
    {"cz":"Drahý/á/é","en":"expensive"},
    {"cz":"Platit kartou","en":"to pay by card"},
    {"cz":"Platit hotově","en":"to pay cash"},
    {"cz":"účtenka","en":"receipt"},
    {"cz":"Koruna česká (Kč)","en":"Czech Crown (currency)"},
    {"cz":"Máte...?","en":"Do you have...?"},
    {"cz":"Chtěl/a bych...","en":"I would like..."},
    {"cz":"Mohu platit kartou?","en":"Can I pay by card?"},
  ]},
  {"id":"transport","name":"Transport","emoji":"🚇","level":"A2","cards":[
    {"cz":"metro","en":"metro / underground"},
    {"cz":"tramvaj","en":"tram"},
    {"cz":"autobus","en":"bus"},
    {"cz":"vlak","en":"train"},
    {"cz":"letadlo","en":"airplane"},
    {"cz":"kolo","en":"bicycle"},
    {"cz":"jet metrem","en":"to go by metro"},
    {"cz":"jet autobusem","en":"to go by bus"},
    {"cz":"jet vlakem","en":"to go by train"},
    {"cz":"jít pěšky","en":"to go on foot"},
    {"cz":"zastávka","en":"stop (bus/tram)"},
    {"cz":"nádraží","en":"train station"},
    {"cz":"letiště","en":"airport"},
    {"cz":"lístek","en":"ticket"},
    {"cz":"zpáteční lístek","en":"return ticket"},
    {"cz":"Kde je...?","en":"Where is...?"},
    {"cz":"Musíte jít rovně.","en":"You must go straight."},
    {"cz":"Musíte jít doprava.","en":"You must go right."},
    {"cz":"Musíte jít doleva.","en":"You must go left."},
    {"cz":"Je to blízko.","en":"It is near / close."},
    {"cz":"Je to daleko.","en":"It is far."},
    {"cz":"Nerozumím.","en":"I don't understand."},
    {"cz":"Mluvíte anglicky?","en":"Do you speak English?"},
  ]},
  {"id":"housing","name":"Housing","emoji":"🏠","level":"A2","cards":[
    {"cz":"byt","en":"flat / apartment"},
    {"cz":"dům","en":"house"},
    {"cz":"pokoj","en":"room"},
    {"cz":"kuchyň","en":"kitchen"},
    {"cz":"koupelna","en":"bathroom"},
    {"cz":"obývací pokoj","en":"living room"},
    {"cz":"ložnice","en":"bedroom"},
    {"cz":"záchod / WC","en":"toilet"},
    {"cz":"ulice","en":"street"},
    {"cz":"město","en":"city"},
    {"cz":"pronajímat","en":"to rent"},
    {"cz":"koupit","en":"to buy"},
    {"cz":"velký / malý","en":"big / small"},
    {"cz":"nový / starý","en":"new / old"},
  ]},
  {"id":"city","name":"City Places","emoji":"🏙️","level":"A2","cards":[
    {"cz":"náměstí","en":"square"},
    {"cz":"park","en":"park"},
    {"cz":"most","en":"bridge"},
    {"cz":"řeka","en":"river"},
    {"cz":"banka","en":"bank"},
    {"cz":"pošta","en":"post office"},
    {"cz":"nemocnice","en":"hospital"},
    {"cz":"lékárna","en":"pharmacy"},
    {"cz":"kostel","en":"church"},
    {"cz":"restaurace","en":"restaurant"},
    {"cz":"kavárna","en":"café"},
    {"cz":"hotel","en":"hotel"},
    {"cz":"škola","en":"school"},
    {"cz":"divadlo","en":"theatre"},
    {"cz":"muzeum","en":"museum"},
    {"cz":"kino","en":"cinema"},
  ]},
  {"id":"weather","name":"Weather & Seasons","emoji":"🌤️","level":"A2","cards":[
    {"cz":"jaro","en":"spring"},
    {"cz":"léto","en":"summer"},
    {"cz":"podzim","en":"autumn"},
    {"cz":"zima","en":"winter"},
    {"cz":"teplo / horko","en":"warm / hot"},
    {"cz":"chladno","en":"cool / cold"},
    {"cz":"déšť / prší","en":"rain / it rains"},
    {"cz":"sníh / sněží","en":"snow / it snows"},
    {"cz":"slunce / slunečno","en":"sun / sunny"},
    {"cz":"vítr / větrno","en":"wind / windy"},
    {"cz":"oblačno","en":"cloudy"},
  ]},
  {"id":"phrases","name":"Useful Phrases","emoji":"💬","level":"A2","cards":[
    {"cz":"Potřebuji se objednat k doktorovi.","en":"I need to make an appointment with the doctor."},
    {"cz":"Bolí mě v krku.","en":"My throat hurts."},
    {"cz":"Necítím se dobře.","en":"I don't feel well."},
    {"cz":"Kde je nejbližší lékárna?","en":"Where is the nearest pharmacy?"},
    {"cz":"Prosím vás, kde je...?","en":"Excuse me, where is...?"},
    {"cz":"Tři stanice metrem.","en":"Three stops by metro."},
    {"cz":"Pět minut pěšky.","en":"Five minutes on foot."},
    {"cz":"Zvlášť nebo dohromady?","en":"Separately or together? (bill)"},
    {"cz":"Co si dáte k jídlu?","en":"What will you have to eat? (waiter)"},
    {"cz":"Co si dáte k pití?","en":"What will you have to drink? (waiter)"},
    {"cz":"Jsem tady 9 let.","en":"I've been here 9 years."},
    {"cz":"Studuji češtinu.","en":"I study Czech."},
    {"cz":"Chci získat české občanství.","en":"I want to get Czech citizenship."},
  ]},
]

# ── CITIZENSHIP QUIZ ─────────────────────────────────────────────────────────
CITIZENSHIP = [
  {"q":"What colours are on the Czech flag?","a":"White, red, and blue","options":["White, red, and blue","Red, white, and green","Blue, yellow, and red","White, blue, and yellow"]},
  {"q":"What is the Czech national anthem called?","a":"Kde domov můj?","options":["Kde domov můj?","Čechy krásné, Čechy mé","Vlajka nad Prahou","Naše vlast"]},
  {"q":"Who wrote the Czech national anthem?","a":"Josef Kajetán Tyl (1834)","options":["Josef Kajetán Tyl (1834)","Bedřich Smetana","Franz Kafka","Václav Havel"]},
  {"q":"Czech State Day (Den české státnosti) is on...","a":"28. září (September 28)","options":["28. října (October 28)","28. září (September 28)","17. listopadu (November 17)","1. ledna (January 1)"]},
  {"q":"The founding of Czechoslovakia is remembered on...","a":"28. října 1918","options":["28. října 1918","17. listopadu 1989","8. května 1945","1. ledna 1993"]},
  {"q":"How many chambers does Czech Parliament have?","a":"Two — Poslanecká sněmovna and Senát","options":["One chamber","Two — Poslanecká sněmovna and Senát","Three chambers","Four chambers"]},
  {"q":"How many members are in the Chamber of Deputies (Poslanecká sněmovna)?","a":"200","options":["81","100","200","300"]},
  {"q":"How many senators are in the Czech Senate?","a":"81","options":["61","71","81","100"]},
  {"q":"How often are senators elected?","a":"Every 6 years (1/3 every 2 years)","options":["Every 4 years","Every 5 years","Every 6 years (1/3 every 2 years)","Every 8 years"]},
  {"q":"The Czech president is elected for how many years?","a":"5 years (max 2 terms)","options":["4 years","5 years (max 2 terms)","6 years","7 years"]},
  {"q":"Who is the current Czech president (since 2023)?","a":"Petr Pavel","options":["Miloš Zeman","Václav Havel","Václav Klaus","Petr Pavel"]},
  {"q":"Who was the first president of Czechoslovakia (1918)?","a":"T.G. Masaryk","options":["Václav Havel","Edvard Beneš","T.G. Masaryk","Antonín Novotný"]},
  {"q":"What is the name of the Czech currency?","a":"Koruna česká (Kč)","options":["Euro (€)","Koruna česká (Kč)","Forint","Zloty"]},
  {"q":"What is the capital city of the Czech Republic?","a":"Praha (Prague)","options":["Brno","Ostrava","Olomouc","Praha (Prague)"]},
  {"q":"What is the largest city in Czech Republic after Prague?","a":"Brno","options":["Plzeň","Ostrava","Brno","Liberec"]},
  {"q":"How many regions (kraje) does the Czech Republic have?","a":"14","options":["10","12","14","16"]},
  {"q":"What is the Czech name for Christmas Eve (December 24)?","a":"Štědrý den","options":["Vánoční den","Štědrý den","Boží hod vánoční","Silvestr"]},
  {"q":"What is Labour Day celebrated in Czech Republic?","a":"1. května (May 1)","options":["1. května (May 1)","1. března (March 1)","8. května (May 8)","5. července (July 5)"]},
  {"q":"Victory Day (end of WWII) is on...","a":"8. května","options":["1. května","8. května","28. října","17. listopadu"]},
  {"q":"The Velvet Revolution (Sametová revoluce) began on...","a":"17. listopadu 1989","options":["28. října 1989","17. listopadu 1989","1. ledna 1990","28. října 1990"]},
  {"q":"When did Czech Republic become independent (separate from Slovakia)?","a":"1. ledna 1993","options":["17. listopadu 1989","28. října 1990","1. ledna 1993","1. května 1994"]},
  {"q":"What river flows through Prague?","a":"Vltava","options":["Labe","Morava","Vltava","Ohře"]},
  {"q":"The highest mountain in Czech Republic is...","a":"Sněžka (1602 m) — Krkonoše","options":["Praděd","Lysá hora","Sněžka (1602 m) — Krkonoše","Říp"]},
  {"q":"What is the Czech emergency number for ambulance?","a":"155","options":["112","150","155","158"]},
  {"q":"What is the Czech police emergency number?","a":"158","options":["112","150","155","158"]},
  {"q":"The pan-European emergency number is...","a":"112","options":["110","111","112","999"]},
  {"q":"Czech Republic joined the European Union in...","a":"2004","options":["1999","2001","2004","2007"]},
  {"q":"Czech Republic joined NATO in...","a":"1999","options":["1993","1999","2004","2007"]},
  {"q":"The patron saint of Bohemia and Moravia is...","a":"Sv. Václav (Saint Wenceslas)","options":["Sv. Jan Nepomucký","Sv. Prokop","Sv. Václav (Saint Wenceslas)","Sv. Cyril"]},
  {"q":"Jan Hus was burned at the stake in...","a":"1415","options":["1348","1415","1620","1848"]},
]

# ── HTML TEMPLATE ─────────────────────────────────────────────────────────────
data_js = f"""
const DECKS = {json.dumps(DECKS, ensure_ascii=False, indent=2)};
const CITIZENSHIP = {json.dumps(CITIZENSHIP, ensure_ascii=False, indent=2)};
"""

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Czech Language Game — Prince</title>
<style>
:root{
  --bg:#0b0d14;--surface:#14172a;--surface2:#1e2135;--surface3:#252840;
  --accent:#4f8ef7;--accent2:#7c3aed;--green:#22c55e;--red:#ef4444;
  --yellow:#f59e0b;--text:#e2e8f0;--muted:#64748b;--border:#252840;
  --r:14px;
}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;}
button{cursor:pointer;border:none;font-family:inherit;}

/* ── SCREENS ── */
.screen{display:none;min-height:100vh;}
.screen.active{display:flex;flex-direction:column;}

/* ── TOP BAR ── */
#topbar{
  position:fixed;top:0;left:0;right:0;height:56px;
  background:var(--surface);border-bottom:1px solid var(--border);
  display:flex;align-items:center;padding:0 16px;gap:12px;z-index:100;
}
#topbar .logo{font-weight:800;font-size:15px;color:var(--accent);letter-spacing:.04em;}
#xp-pill{background:var(--surface2);padding:4px 12px;border-radius:20px;
  font-size:13px;font-weight:600;color:var(--yellow);}
#hearts-pill{font-size:15px;}
#streak-pill{background:var(--surface2);padding:4px 10px;border-radius:20px;
  font-size:13px;font-weight:600;color:#fb923c;}
.spacer{flex:1;}
#back-btn{background:var(--surface2);color:var(--text);padding:6px 14px;
  border-radius:8px;font-size:13px;display:none;}
#back-btn.show{display:block;}

/* ── DASHBOARD ── */
#dash{padding:72px 20px 24px;max-width:700px;margin:0 auto;width:100%;}
#dash h1{font-size:22px;font-weight:800;margin-bottom:4px;}
#dash p.sub{color:var(--muted);font-size:14px;margin-bottom:24px;}
.xp-bar-wrap{background:var(--surface2);border-radius:20px;height:10px;margin-bottom:24px;overflow:hidden;}
.xp-bar-fill{height:100%;background:linear-gradient(90deg,var(--accent),var(--accent2));border-radius:20px;transition:width .6s;}
.level-row{display:flex;justify-content:space-between;font-size:12px;color:var(--muted);margin-bottom:24px;}

.section-title{font-size:12px;font-weight:700;color:var(--muted);letter-spacing:.1em;
  text-transform:uppercase;margin-bottom:12px;}
.deck-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(155px,1fr));gap:12px;margin-bottom:28px;}
.deck-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);
  padding:16px 14px;cursor:pointer;transition:all .15s;position:relative;}
.deck-card:hover{border-color:var(--accent);transform:translateY(-2px);}
.deck-card .emoji{font-size:28px;margin-bottom:8px;}
.deck-card .name{font-weight:700;font-size:14px;}
.deck-card .count{font-size:12px;color:var(--muted);margin-top:2px;}
.deck-card .stars{position:absolute;top:10px;right:12px;font-size:13px;}
.level-badge{display:inline-block;padding:2px 8px;border-radius:10px;font-size:10px;
  font-weight:700;margin-top:6px;}
.badge-a2{background:#1d4ed820;color:#60a5fa;border:1px solid #1d4ed850;}
.badge-b1{background:#6d28d920;color:#a78bfa;border:1px solid #6d28d950;}

.cta-btn{background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;
  border:none;padding:14px 28px;border-radius:12px;font-size:15px;font-weight:700;
  cursor:pointer;width:100%;margin-bottom:12px;transition:opacity .15s;}
.cta-btn:hover{opacity:.9;}
.cta-btn.secondary{background:var(--surface2);color:var(--text);}

/* ── DECK MENU ── */
#deck-menu{padding:72px 20px 24px;max-width:480px;margin:0 auto;width:100%;}
#deck-menu h2{font-size:20px;font-weight:800;margin-bottom:6px;}
#deck-menu p.sub{color:var(--muted);font-size:14px;margin-bottom:24px;}
.mode-list{display:flex;flex-direction:column;gap:10px;}
.mode-btn{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);
  padding:16px 18px;text-align:left;transition:all .15s;color:var(--text);}
.mode-btn:hover{border-color:var(--accent);}
.mode-btn .m-title{font-weight:700;font-size:15px;display:flex;align-items:center;gap:8px;}
.mode-btn .m-desc{font-size:13px;color:var(--muted);margin-top:3px;}

/* ── FLASHCARD ── */
#flashcard-screen{padding:72px 20px 24px;max-width:480px;margin:0 auto;width:100%;align-items:center;}
.card-counter{font-size:13px;color:var(--muted);margin-bottom:12px;text-align:center;}
.progress-thin{width:100%;height:4px;background:var(--surface2);border-radius:4px;margin-bottom:24px;overflow:hidden;}
.progress-thin-fill{height:100%;background:var(--accent);transition:width .3s;}
.flip-card{width:100%;max-width:420px;perspective:1000px;cursor:pointer;margin-bottom:20px;}
.flip-inner{position:relative;width:100%;min-height:200px;transition:transform .45s;
  transform-style:preserve-3d;}
.flip-card.flipped .flip-inner{transform:rotateY(180deg);}
.face{position:absolute;width:100%;min-height:200px;backface-visibility:hidden;
  background:var(--surface);border:1px solid var(--border);border-radius:20px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  padding:28px 24px;text-align:center;}
.face.back{transform:rotateY(180deg);background:var(--surface2);}
.face .lang-tag{font-size:11px;font-weight:700;color:var(--muted);letter-spacing:.1em;
  text-transform:uppercase;margin-bottom:12px;}
.face .word{font-size:26px;font-weight:700;line-height:1.3;}
.face .note{font-size:13px;color:var(--muted);margin-top:8px;}
.audio-btn{background:var(--surface2);border:1px solid var(--border);color:var(--accent);
  padding:8px 16px;border-radius:20px;font-size:14px;margin-bottom:16px;}
.audio-btn:hover{background:var(--surface3);}
.fc-actions{display:flex;gap:10px;width:100%;max-width:420px;}
.fc-btn{flex:1;padding:12px;border-radius:12px;font-size:14px;font-weight:700;}
.fc-btn.wrong{background:#ef444420;color:var(--red);border:1px solid #ef444440;}
.fc-btn.right{background:#22c55e20;color:var(--green);border:1px solid #22c55e40;}
.fc-btn.next{background:var(--surface2);color:var(--text);border:1px solid var(--border);}
.flip-hint{font-size:12px;color:var(--muted);text-align:center;margin-top:12px;}

/* ── QUIZ ── */
#quiz-screen{padding:72px 20px 24px;max-width:480px;margin:0 auto;width:100%;}
.quiz-prompt{font-size:14px;color:var(--muted);margin-bottom:8px;}
.quiz-question{font-size:20px;font-weight:700;margin-bottom:24px;line-height:1.4;}
.options-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:20px;}
.opt-btn{background:var(--surface);border:2px solid var(--border);border-radius:12px;
  padding:14px 12px;font-size:14px;font-weight:600;text-align:left;
  color:var(--text);transition:all .15s;line-height:1.4;}
.opt-btn:hover:not(:disabled){border-color:var(--accent);}
.opt-btn.correct{background:#22c55e20;border-color:var(--green);color:var(--green);}
.opt-btn.wrong{background:#ef444420;border-color:var(--red);color:var(--red);}
.opt-btn:disabled{cursor:default;}
.feedback-bar{padding:14px 18px;border-radius:12px;font-size:14px;font-weight:700;
  margin-bottom:16px;display:none;}
.feedback-bar.show{display:flex;align-items:center;gap:10px;}
.feedback-bar.good{background:#22c55e20;color:var(--green);border:1px solid #22c55e40;}
.feedback-bar.bad{background:#ef444420;color:var(--red);border:1px solid #ef444440;}
.next-btn{width:100%;padding:14px;border-radius:12px;font-size:15px;font-weight:700;
  background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;display:none;}
.next-btn.show{display:block;}

/* ── MATCHING GAME ── */
#match-screen{padding:72px 20px 24px;max-width:520px;margin:0 auto;width:100%;}
#match-screen h3{font-size:15px;font-weight:700;margin-bottom:6px;}
#match-screen p.sub{font-size:13px;color:var(--muted);margin-bottom:20px;}
.match-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;}
.match-tile{background:var(--surface);border:2px solid var(--border);border-radius:10px;
  padding:12px 10px;font-size:13px;font-weight:600;text-align:center;
  cursor:pointer;transition:all .2s;min-height:52px;display:flex;align-items:center;justify-content:center;line-height:1.3;}
.match-tile:hover{border-color:var(--accent);}
.match-tile.selected{border-color:var(--accent);background:rgba(79,142,247,.12);}
.match-tile.matched{background:#22c55e15;border-color:var(--green);color:var(--green);cursor:default;}
.match-tile.wrong-flash{border-color:var(--red);background:#ef444420;animation:shake .3s;}
@keyframes shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-6px)}75%{transform:translateX(6px)}}
.match-score{font-size:13px;color:var(--muted);margin-bottom:12px;}

/* ── LISTEN ── */
#listen-screen{padding:72px 20px 24px;max-width:480px;margin:0 auto;width:100%;}
.listen-prompt{text-align:center;margin-bottom:24px;}
.listen-prompt p{color:var(--muted);font-size:14px;margin-bottom:16px;}
.big-audio-btn{background:linear-gradient(135deg,var(--accent),var(--accent2));
  border:none;border-radius:50%;width:88px;height:88px;font-size:32px;
  display:inline-flex;align-items:center;justify-content:center;
  cursor:pointer;transition:transform .15s;box-shadow:0 0 0 0 rgba(79,142,247,.4);}
.big-audio-btn:hover{transform:scale(1.08);}
.big-audio-btn.playing{animation:pulse-ring 1.2s ease-out infinite;}
@keyframes pulse-ring{
  0%{box-shadow:0 0 0 0 rgba(79,142,247,.5);}
  70%{box-shadow:0 0 0 20px rgba(79,142,247,0);}
  100%{box-shadow:0 0 0 0 rgba(79,142,247,0);}
}
.listen-hint{font-size:12px;color:var(--muted);margin-top:8px;}

/* ── RESULTS ── */
#result-screen{padding:80px 20px 24px;max-width:420px;margin:0 auto;width:100%;align-items:center;justify-content:center;}
.result-emoji{font-size:64px;margin-bottom:12px;text-align:center;}
.result-title{font-size:24px;font-weight:800;margin-bottom:8px;text-align:center;}
.result-sub{font-size:15px;color:var(--muted);margin-bottom:28px;text-align:center;}
.result-stats{display:flex;gap:16px;margin-bottom:32px;width:100%;justify-content:center;}
.stat-box{background:var(--surface2);border-radius:12px;padding:14px 20px;text-align:center;flex:1;}
.stat-box .val{font-size:28px;font-weight:800;}
.stat-box .lbl{font-size:12px;color:var(--muted);margin-top:2px;}

/* ── XP POPUP ── */
.xp-popup{position:fixed;top:60px;right:16px;background:var(--yellow);color:#000;
  font-weight:800;font-size:14px;padding:6px 14px;border-radius:20px;
  opacity:0;transform:translateY(-10px);transition:all .3s;pointer-events:none;z-index:200;}
.xp-popup.show{opacity:1;transform:translateY(0);}

/* ── RESPONSIVE ── */
@media(max-width:400px){
  .options-grid{grid-template-columns:1fr;}
  .face .word{font-size:20px;}
}
</style>
</head>
<body>

<!-- TOP BAR -->
<div id="topbar">
  <span class="logo">🇨🇿 Czech Game</span>
  <span id="xp-pill">⭐ <span id="xp-val">0</span> XP</span>
  <span id="hearts-pill">❤️❤️❤️</span>
  <span id="streak-pill">🔥 <span id="streak-val">0</span></span>
  <span class="spacer"></span>
  <button id="back-btn" onclick="goHome()">← Home</button>
</div>
<div class="xp-popup" id="xp-popup">+10 XP</div>

<!-- ══════════════ DASHBOARD ══════════════ -->
<div class="screen active" id="home-screen">
  <div id="dash">
    <h1>Czech Learning Game 🇨🇿</h1>
    <p class="sub">Inspired by Duolingo · Flashcards · Quiz · Match · Listen</p>
    <div class="xp-bar-wrap"><div class="xp-bar-fill" id="xp-bar" style="width:0%"></div></div>
    <div class="level-row"><span id="level-label">Level: Beginner</span><span id="xp-to-next">100 XP to next level</span></div>

    <button class="cta-btn" onclick="startCitizenship()">🏛️ Citizenship Exam Practice (30 Q)</button>

    <p class="section-title" style="margin-top:8px;">Vocabulary Decks</p>
    <div class="deck-grid" id="deck-grid"></div>
  </div>
</div>

<!-- ══════════════ DECK MENU ══════════════ -->
<div class="screen" id="deck-screen">
  <div id="deck-menu">
    <h2 id="deck-menu-title"></h2>
    <p class="sub" id="deck-menu-sub"></p>
    <div class="mode-list">
      <button class="mode-btn" onclick="startFlashcards()">
        <div class="m-title">🃏 Flashcards</div>
        <div class="m-desc">Flip cards, hear Czech pronunciation, mark known/unknown</div>
      </button>
      <button class="mode-btn" onclick="startQuiz()">
        <div class="m-title">🧠 Multiple Choice Quiz</div>
        <div class="m-desc">4 options, instant feedback, earn XP, lose hearts on mistakes</div>
      </button>
      <button class="mode-btn" onclick="startMatch()">
        <div class="m-title">🎯 Match the Pairs</div>
        <div class="m-desc">Click Czech then English to match — beat your best time!</div>
      </button>
      <button class="mode-btn" onclick="startListen()">
        <div class="m-title">🎧 Listen & Choose</div>
        <div class="m-desc">Hear Czech spoken, pick the correct English translation</div>
      </button>
    </div>
  </div>
</div>

<!-- ══════════════ FLASHCARD ══════════════ -->
<div class="screen" id="flashcard-screen">
  <div style="max-width:480px;margin:0 auto;width:100%;padding:72px 20px 24px;">
    <div class="card-counter" id="fc-counter">Card 1 of 10</div>
    <div class="progress-thin"><div class="progress-thin-fill" id="fc-progress"></div></div>
    <div class="flip-card" id="flip-card" onclick="flipCard()">
      <div class="flip-inner">
        <div class="face front">
          <div class="lang-tag">Czech 🇨🇿</div>
          <div class="word" id="fc-cz"></div>
        </div>
        <div class="face back">
          <div class="lang-tag">English 🇬🇧</div>
          <div class="word" id="fc-en"></div>
        </div>
      </div>
    </div>
    <p class="flip-hint" id="flip-hint">👆 Tap card to flip</p>
    <button class="audio-btn" onclick="speakCzech()">🔊 Hear Czech</button>
    <div class="fc-actions" id="fc-actions" style="display:none;">
      <button class="fc-btn wrong" onclick="fcAnswer(false)">✗ Still learning</button>
      <button class="fc-btn right" onclick="fcAnswer(true)">✓ Got it!</button>
    </div>
    <div class="fc-actions" id="fc-next-row" style="display:flex;margin-top:10px;">
      <button class="fc-btn next" onclick="fcNext()">Next →</button>
    </div>
  </div>
</div>

<!-- ══════════════ QUIZ ══════════════ -->
<div class="screen" id="quiz-screen">
  <div style="max-width:480px;margin:0 auto;width:100%;padding:72px 20px 24px;">
    <div class="progress-thin"><div class="progress-thin-fill" id="quiz-progress"></div></div>
    <div class="card-counter" id="quiz-counter">Question 1 of 10</div>
    <div class="quiz-prompt" id="quiz-prompt"></div>
    <div class="quiz-question" id="quiz-question"></div>
    <div class="options-grid" id="options-grid"></div>
    <div class="feedback-bar" id="feedback-bar"></div>
    <button class="next-btn" id="quiz-next-btn" onclick="quizNext()">Continue →</button>
  </div>
</div>

<!-- ══════════════ MATCHING ══════════════ -->
<div class="screen" id="match-screen">
  <div style="max-width:520px;margin:0 auto;width:100%;padding:72px 20px 24px;">
    <h3>Match the Pairs 🎯</h3>
    <p class="sub">Tap a Czech word, then its English translation</p>
    <div class="match-score">⏱ <span id="match-timer">0</span>s &nbsp;·&nbsp; ✅ <span id="match-found">0</span>/<span id="match-total">0</span></div>
    <div class="match-grid" id="match-grid"></div>
  </div>
</div>

<!-- ══════════════ LISTEN ══════════════ -->
<div class="screen" id="listen-screen">
  <div style="max-width:480px;margin:0 auto;width:100%;padding:72px 20px 24px;">
    <div class="progress-thin"><div class="progress-thin-fill" id="listen-progress"></div></div>
    <div class="card-counter" id="listen-counter">Round 1 of 10</div>
    <div class="listen-prompt">
      <p>Listen to the Czech word/phrase, then choose the correct translation.</p>
      <button class="big-audio-btn" id="big-audio-btn" onclick="playListenAudio()">🔊</button>
      <div class="listen-hint">Tap to hear again</div>
    </div>
    <div class="options-grid" id="listen-options"></div>
    <div class="feedback-bar" id="listen-feedback"></div>
    <button class="next-btn" id="listen-next-btn" onclick="listenNext()">Continue →</button>
  </div>
</div>

<!-- ══════════════ RESULT ══════════════ -->
<div class="screen" id="result-screen">
  <div class="result-emoji" id="res-emoji"></div>
  <div class="result-title" id="res-title"></div>
  <div class="result-sub" id="res-sub"></div>
  <div class="result-stats">
    <div class="stat-box"><div class="val" id="res-score"></div><div class="lbl">Score</div></div>
    <div class="stat-box"><div class="val" id="res-xp"></div><div class="lbl">XP earned</div></div>
    <div class="stat-box"><div class="val" id="res-streak"></div><div class="lbl">Streak</div></div>
  </div>
  <button class="cta-btn" onclick="goHome()">Back to Home</button>
  <button class="cta-btn secondary" style="margin-top:10px;" onclick="playAgain()">Play Again</button>
</div>

<script>
""" + "const DECKS=" + json.dumps(DECKS, ensure_ascii=False) + ";\nconst CITIZENSHIP=" + json.dumps(CITIZENSHIP, ensure_ascii=False) + ";\n" + r"""
// ── STATE ──────────────────────────────────────────────────────────────────
let xp = +localStorage.getItem('xp')||0;
let streak = +localStorage.getItem('streak')||0;
let hearts = 3;
let deckProgress = JSON.parse(localStorage.getItem('deckProgress')||'{}');

// current session
let currentDeck = null;
let currentMode = null;
let sessionCards = [];
let sessionIdx = 0;
let sessionCorrect = 0;
let sessionXP = 0;
let matchTimer = null;
let matchSeconds = 0;
let matchSelected = null;
let matchFound = 0;
let fcFlipped = false;

// ── HELPERS ────────────────────────────────────────────────────────────────
function shuffle(arr){ return [...arr].sort(()=>Math.random()-.5); }
function $(id){ return document.getElementById(id); }

function showScreen(id){
  document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));
  $(id).classList.add('active');
  $('back-btn').classList.toggle('show', id!=='home-screen');
}

function goHome(){ showScreen('home-screen'); renderDash(); clearMatchTimer(); }
function playAgain(){ if(currentMode==='citizenship') startCitizenship(); else if(currentDeck) pickMode(currentDeck); }

function renderDash(){
  // XP bar
  const LEVELS=[{name:'Beginner',xp:0},{name:'Elementary A1',xp:100},{name:'A2 Student',xp:300},{name:'B1 Learner',xp:700},{name:'B1 Speaker',xp:1500},{name:'B2 Fluent',xp:3000}];
  let lvl=0; for(let i=0;i<LEVELS.length;i++) if(xp>=LEVELS[i].xp) lvl=i;
  const next=LEVELS[lvl+1];
  const lvlXP=LEVELS[lvl].xp;
  const nextXP=next?next.xp:lvlXP+500;
  const pct=Math.min(100,((xp-lvlXP)/(nextXP-lvlXP))*100);
  $('xp-bar').style.width=pct+'%';
  $('level-label').textContent='Level: '+LEVELS[lvl].name;
  $('xp-to-next').textContent=next?(nextXP-xp)+' XP to '+next.name:'Max level!';
  updateTopBar();
  // deck grid
  const grid=$('deck-grid'); grid.innerHTML='';
  DECKS.forEach(d=>{
    const prog=deckProgress[d.id]||0;
    const stars=prog>=80?'⭐⭐⭐':prog>=50?'⭐⭐':prog>0?'⭐':'';
    const div=document.createElement('div');
    div.className='deck-card';
    div.innerHTML=`<div class="stars">${stars}</div>
      <div class="emoji">${d.emoji}</div>
      <div class="name">${d.name}</div>
      <div class="count">${d.cards.length} cards</div>
      <span class="level-badge badge-${d.level.toLowerCase()}">${d.level}</span>`;
    div.onclick=()=>pickMode(d);
    grid.appendChild(div);
  });
}

function updateTopBar(){
  $('xp-val').textContent=xp;
  $('streak-val').textContent=streak;
  $('hearts-pill').textContent='❤️'.repeat(hearts)+'🖤'.repeat(Math.max(0,3-hearts));
}

function addXP(n){
  xp+=n; sessionXP+=n; localStorage.setItem('xp',xp);
  const p=$('xp-popup'); p.textContent='+'+n+' XP';
  p.classList.add('show'); setTimeout(()=>p.classList.remove('show'),1200);
  updateTopBar();
}

function loseHeart(){
  hearts=Math.max(0,hearts-1); updateTopBar();
}

function speak(text, lang='cs-CZ'){
  if(!window.speechSynthesis) return;
  const u=new SpeechSynthesisUtterance(text);
  u.lang=lang; u.rate=0.85;
  speechSynthesis.cancel();
  speechSynthesis.speak(u);
}

// ── DECK MENU ─────────────────────────────────────────────────────────────
function pickMode(deck){
  currentDeck=deck;
  $('deck-menu-title').textContent=deck.emoji+' '+deck.name;
  $('deck-menu-sub').textContent=deck.cards.length+' cards · '+deck.level+' Level';
  showScreen('deck-screen');
}

// ── FLASHCARDS ────────────────────────────────────────────────────────────
function startFlashcards(){
  currentMode='flashcard';
  sessionCards=shuffle(currentDeck.cards).slice(0,15);
  sessionIdx=0; sessionCorrect=0; sessionXP=0;
  showScreen('flashcard-screen');
  renderFlashcard();
}

function renderFlashcard(){
  const card=sessionCards[sessionIdx];
  const total=sessionCards.length;
  $('fc-counter').textContent=`Card ${sessionIdx+1} of ${total}`;
  $('fc-progress').style.width=((sessionIdx/total)*100)+'%';
  $('fc-cz').textContent=card.cz;
  $('fc-en').textContent=card.en;
  const fc=$('flip-card');
  fc.classList.remove('flipped'); fcFlipped=false;
  $('flip-hint').style.display='';
  $('fc-actions').style.display='none';
  $('fc-next-row').style.display='flex';
}

function flipCard(){
  const fc=$('flip-card');
  fc.classList.toggle('flipped');
  fcFlipped=fc.classList.contains('flipped');
  if(fcFlipped){
    $('flip-hint').style.display='none';
    $('fc-actions').style.display='flex';
    $('fc-next-row').style.display='none';
    speak(sessionCards[sessionIdx].cz);
  }
}

function speakCzech(){ speak(sessionCards[sessionIdx].cz); }

function fcAnswer(correct){
  if(correct){ addXP(8); sessionCorrect++; }
  fcNext();
}
function fcNext(){
  sessionIdx++;
  if(sessionIdx>=sessionCards.length){ showResult(); return; }
  renderFlashcard();
}

// ── QUIZ ──────────────────────────────────────────────────────────────────
function startQuiz(isCitizenship){
  currentMode= isCitizenship ? 'citizenship' : 'quiz';
  hearts=3; updateTopBar();
  if(isCitizenship){
    sessionCards=shuffle(CITIZENSHIP).slice(0,15);
  } else {
    // build MCQ from vocab deck — ask EN for CZ or CZ for EN
    const allCards=[...currentDeck.cards];
    sessionCards=shuffle(allCards).slice(0,12).map(card=>{
      const askCz=Math.random()>.5;
      const question=askCz?card.cz:card.en;
      const answer=askCz?card.en:card.cz;
      const lang=askCz?'Czech':'English';
      // distractors from same deck
      const distractors=shuffle(allCards.filter(c=>c!==card)).slice(0,3)
        .map(c=>askCz?c.en:c.cz);
      const options=shuffle([answer,...distractors]);
      return {question,answer,options,lang,cz:card.cz};
    });
  }
  sessionIdx=0; sessionCorrect=0; sessionXP=0;
  showScreen('quiz-screen');
  renderQuiz();
}

function renderQuiz(){
  const card=sessionCards[sessionIdx];
  const total=sessionCards.length;
  $('quiz-counter').textContent=`Question ${sessionIdx+1} of ${total}`;
  $('quiz-progress').style.width=((sessionIdx/total)*100)+'%';

  if(currentMode==='citizenship'){
    $('quiz-prompt').textContent='🏛️ Czech Citizenship Trivia';
    $('quiz-question').textContent=card.q;
  } else {
    $('quiz-prompt').textContent=`Translate from ${card.lang}:`;
    $('quiz-question').textContent=card.question;
  }

  const grid=$('options-grid'); grid.innerHTML='';
  const opts=currentMode==='citizenship'?card.options:card.options;
  opts.forEach(opt=>{
    const btn=document.createElement('button');
    btn.className='opt-btn'; btn.textContent=opt;
    btn.onclick=()=>checkQuiz(opt, btn);
    grid.appendChild(btn);
  });

  const fb=$('feedback-bar'); fb.className='feedback-bar'; fb.style.display='none';
  $('quiz-next-btn').className='next-btn';
}

function checkQuiz(chosen, btn){
  const card=sessionCards[sessionIdx];
  const correct=currentMode==='citizenship'?card.a:card.answer;
  document.querySelectorAll('.opt-btn').forEach(b=>{
    b.disabled=true;
    if(b.textContent===correct) b.classList.add('correct');
  });
  const fb=$('feedback-bar');
  if(chosen===correct){
    btn.classList.add('correct');
    fb.className='feedback-bar show good';
    fb.innerHTML='✅ Correct! '+( currentMode!=='citizenship' && card.cz? '<em>'+card.cz+'</em>':'' );
    addXP(10); sessionCorrect++;
    if(currentMode!=='citizenship') speak(card.cz);
  } else {
    btn.classList.add('wrong');
    fb.className='feedback-bar show bad';
    fb.innerHTML='❌ Correct answer: <strong>'+correct+'</strong>';
    loseHeart();
  }
  fb.style.display='flex';
  $('quiz-next-btn').className='next-btn show';
}

function quizNext(){
  sessionIdx++;
  if(sessionIdx>=sessionCards.length || hearts===0){ showResult(); return; }
  renderQuiz();
}

// ── MATCHING ──────────────────────────────────────────────────────────────
function startMatch(){
  currentMode='match';
  sessionXP=0;
  const pairs=shuffle(currentDeck.cards).slice(0,7);
  matchFound=0; matchSelected=null;

  // build tile list: 7 cz + 7 en, shuffled into 2 column grid
  const czTiles=pairs.map((c,i)=>({text:c.cz,pairId:i,type:'cz'}));
  const enTiles=pairs.map((c,i)=>({text:c.en,pairId:i,type:'en'}));
  const leftCol=shuffle(czTiles);
  const rightCol=shuffle(enTiles);
  const tiles=[]; // interleave for 2-col grid
  for(let i=0;i<leftCol.length;i++){ tiles.push(leftCol[i]); tiles.push(rightCol[i]); }

  const grid=$('match-grid'); grid.innerHTML='';
  $('match-found').textContent=0; $('match-total').textContent=pairs.length;

  tiles.forEach((t,idx)=>{
    const div=document.createElement('div');
    div.className='match-tile';
    div.textContent=t.text;
    div.dataset.pairId=t.pairId;
    div.dataset.type=t.type;
    div.dataset.idx=idx;
    div.onclick=()=>matchClick(div);
    grid.appendChild(div);
  });

  // start timer
  clearMatchTimer();
  matchSeconds=0; $('match-timer').textContent=0;
  matchTimer=setInterval(()=>{ matchSeconds++; $('match-timer').textContent=matchSeconds; },1000);

  showScreen('match-screen');
}

function matchClick(tile){
  if(tile.classList.contains('matched')) return;
  if(matchSelected===tile){ tile.classList.remove('selected'); matchSelected=null; return; }

  if(!matchSelected){
    tile.classList.add('selected'); matchSelected=tile; return;
  }

  // check pair
  const a=matchSelected, b=tile;
  if(a.dataset.pairId===b.dataset.pairId && a.dataset.type!==b.dataset.type){
    // correct!
    a.classList.remove('selected'); a.classList.add('matched');
    b.classList.add('matched');
    matchSelected=null; matchFound++;
    $('match-found').textContent=matchFound;
    addXP(12);
    speak(a.dataset.type==='cz'?a.textContent:b.textContent);
    if(matchFound===+$('match-total').textContent){ matchComplete(); }
  } else {
    // wrong
    a.classList.add('wrong-flash'); b.classList.add('wrong-flash');
    setTimeout(()=>{ a.classList.remove('wrong-flash','selected'); b.classList.remove('wrong-flash'); }, 400);
    matchSelected=null; loseHeart();
  }
}

function matchComplete(){
  clearMatchTimer();
  sessionCorrect=matchFound; sessionCards={length:matchFound};
  setTimeout(showResult, 600);
}

function clearMatchTimer(){ clearInterval(matchTimer); }

// ── LISTEN ────────────────────────────────────────────────────────────────
function startListen(){
  currentMode='listen';
  const allCards=[...currentDeck.cards];
  sessionCards=shuffle(allCards).slice(0,10);
  sessionIdx=0; sessionCorrect=0; sessionXP=0;
  hearts=3; updateTopBar();
  showScreen('listen-screen');
  renderListen();
}

function renderListen(){
  const card=sessionCards[sessionIdx];
  const total=sessionCards.length;
  $('listen-counter').textContent=`Round ${sessionIdx+1} of ${total}`;
  $('listen-progress').style.width=((sessionIdx/total)*100)+'%';

  const btn=$('big-audio-btn');
  btn.classList.remove('playing');

  // distractors
  const allCards=currentDeck.cards;
  const distractors=shuffle(allCards.filter(c=>c!==card)).slice(0,3).map(c=>c.en);
  const options=shuffle([card.en,...distractors]);

  const grid=$('listen-options'); grid.innerHTML='';
  options.forEach(opt=>{
    const b=document.createElement('button');
    b.className='opt-btn'; b.textContent=opt;
    b.onclick=()=>checkListen(opt,b,card);
    grid.appendChild(b);
  });

  $('listen-feedback').className='feedback-bar';
  $('listen-next-btn').className='next-btn';

  // auto-play
  setTimeout(()=>speak(card.cz), 400);
}

function playListenAudio(){
  const card=sessionCards[sessionIdx];
  const btn=$('big-audio-btn');
  btn.classList.add('playing');
  speak(card.cz);
  setTimeout(()=>btn.classList.remove('playing'),1500);
}

function checkListen(chosen, btn, card){
  document.querySelectorAll('#listen-options .opt-btn').forEach(b=>{
    b.disabled=true;
    if(b.textContent===card.en) b.classList.add('correct');
  });
  const fb=$('listen-feedback');
  if(chosen===card.en){
    btn.classList.add('correct');
    fb.className='feedback-bar show good';
    fb.innerHTML='✅ Correct! <em>'+card.cz+'</em>';
    addXP(10); sessionCorrect++;
  } else {
    btn.classList.add('wrong');
    fb.className='feedback-bar show bad';
    fb.innerHTML='❌ It was: <strong>'+card.en+'</strong>';
    loseHeart();
  }
  fb.style.display='flex';
  $('listen-next-btn').className='next-btn show';
}

function listenNext(){
  sessionIdx++;
  if(sessionIdx>=sessionCards.length || hearts===0){ showResult(); return; }
  renderListen();
}

// ── CITIZENSHIP ────────────────────────────────────────────────────────────
function startCitizenship(){
  currentDeck=null; currentMode='citizenship';
  startQuiz(true);
}

// ── RESULTS ────────────────────────────────────────────────────────────────
function showResult(){
  clearMatchTimer();
  const total=sessionCards.length||1;
  const pct=Math.round((sessionCorrect/total)*100);

  // update streak & deck progress
  streak++;
  localStorage.setItem('streak',streak);
  if(currentDeck){
    deckProgress[currentDeck.id]=Math.max(deckProgress[currentDeck.id]||0, pct);
    localStorage.setItem('deckProgress',JSON.stringify(deckProgress));
  }

  const emoji=pct>=80?'🏆':pct>=60?'🎉':pct>=40?'💪':'📚';
  const title=pct>=80?'Outstanding!':pct>=60?'Great job!':pct>=40?'Keep going!':'Keep practising!';

  $('res-emoji').textContent=emoji;
  $('res-title').textContent=title;
  $('res-sub').textContent=sessionCorrect+' / '+total+' correct ('+pct+'%)';
  $('res-score').textContent=pct+'%';
  $('res-xp').textContent=sessionXP;
  $('res-streak').textContent=streak+'🔥';

  showScreen('result-screen');
  updateTopBar();
}

// ── INIT ───────────────────────────────────────────────────────────────────
renderDash();

// check TTS
if(!window.speechSynthesis){
  document.querySelectorAll('.audio-btn,.big-audio-btn').forEach(b=>{
    b.title='Text-to-speech not supported in this browser';
    b.style.opacity='.4';
  });
}
</script>
</body>
</html>
"""

with open('learn.html','w',encoding='utf-8') as f:
    f.write(HTML)

print(f"Done! learn.html ({os.path.getsize('learn.html')//1024} KB)")
