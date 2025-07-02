from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from telethon import TelegramClient, functions
from datetime import datetime

from keyboards.default import get_menu_keyboard
from loader import dp
from data.config import API_ID, API_HASH
from utils.full_model import predict


shares = {
1: ['$DERZP'],
2: ['$CBOM'],
3: ['$RDRB'],
4: ['$ALRS'],
5: ['$AVAN'],
6: ['$PRMB'],
7: ['$VTBR'],
8: ['$IRGZ'],
9: ['$KZOS'],
10: ['$LNZL'],
11: ['$RUAL'],
12: ['$ENPG'],
13: ['$BLNG'],
14: ['$DZRD'],
15: ['$LVHK'],
16: ['$LPSB'],
17: ['$MRKU'],
18: ['$MSST'],
19: ['$NPOF'],
20: ['$MGNZ'],
21: ['$AQUA'],
22: ['$ABRD'],
23: ['$UTAR'],
24: ['$AKRN'],
25: ['$BANE'],
26: ['$AFKS'],
27: ['$ALNU'],
28: ['$APTK'],
29: ['$ACKO'],
30: ['$ASSB'],
31: ['$AMEZ'],
32: ['$AFLT'],
33: ['$BSPB'],
34: ['$USBN'],
35: ['$BISV'],
36: ['$BELU'],
37: ['$ALBK'],
38: ['$BRZL'],
39: ['$VJGZ'],
40: ['$VLHZ'],
41: ['$VGSB'],
42: ['$OGKB'],
43: ['$VSYD'],
44: ['$GAZA'],
45: ['$GAZC'],
46: ['$RTGZ'],
47: ['$SIBN'],
48: ['$GAZP'],
49: ['$GAZS'],
50: ['$gazt'],
51: ['$GTSS'],
52: ['$GTRK'],
53: ['$GMKN'],
54: ['$GRNT'],
55: ['$RLMN'],
56: ['$SMLT'],
57: ['$LSRG'],
58: ['$GCHE'],
59: ['$DASB'],
60: ['$DVEC'],
61: ['$FESH'],
62: ['$DSKY'],
63: ['$GTLC'],
64: ['$EELT'],
65: ['$ZILL'],
66: ['$ZVEZ'],
67: ['$IGST'],
68: ['$IDVP'],
69: ['$RUSI'],
70: ['$INGR'],
71: ['$ISKJ'],
72: ['$IRAO'],
73: ['$KLSB'],
74: ['$KMAZ'],
75: ['$KUNF'],
76: ['$TGKD'],
77: ['$KMEZ'],
78: ['$KSGR'],
79: ['$VSMO'],
80: ['$KOGK'],
81: ['$KMTZ'],
82: ['$KTSB'],
83: ['$KZMS'],
84: ['$KRSB'],
85: ['$KBTK'],
86: ['$KAZT'],
87: ['$KGKC'],
88: ['$MVID'],
89: ['$MGNT'],
90: ['$MAGN'],
91: ['$MFON'],
92: ['$ODVA'],
93: ['$GEMA'],
94: ['$MRKZ'],
95: ['$MRKP'],
96: ['$MRKC'],
97: ['$MERF'],
98: ['$MTKB'],
99: ['$MTLR'],
100: ['$MTSS'],
101: ['$MRSB'],
102: ['$MORI'],
103: ['$MOEX'],
104: ['$MGTS'],
105: ['$KROT'],
106: ['$mstt'],
107: ['$NSVZ'],
108: ['$IRKT'],
109: ['$UWGN'],
110: ['$NFAZ'],
111: ['$LKOH'],
112: ['$ROSN'],
113: ['$NKNCP'],
114: ['$NKSHP'],
115: ['$NVTK'],
116: ['$NLMK'],
117: ['$NKHP'],
118: ['$nmtp'],
119: ['$nompp'],
120: ['$UNAC'],
121: ['$UCSS'],
122: ['$SATR'],
123: ['$ORUP'],
124: ['$paza'],
125: ['$PMSBP'],
126: ['$PIKK'],
127: ['$PLZL'],
128: ['$RKKE'],
129: ['$RASP'],
130: ['$RBCM'],
131: ['$CHGZ'],
132: ['$RGSC'],
133: ['$ROST'],
134: ['$mrkv'],
135: ['$kube'],
136: ['$lsng'],
137: ['$MSRS'],
138: ['$MRKK'],
139: ['$MRKS'],
140: ['$MRKY'],
141: ['$RSTI'],
142: ['$RTKM'],
143: ['$RUGR'],
144: ['$ROLO'],
145: ['$RUSP'],
146: ['$RZSB'],
147: ['$KRKN'],
148: ['$SAREP'],
149: ['$SFIN'],
150: ['$SBER'],
151: ['$SVET'],
152: ['$CHMF'],
153: ['$SELG'],
154: ['$SIBG'],
155: ['$MFGS'],
156: ['$JNOS'],
157: ['$FLOT'],
158: ['$SVAV'],
159: ['$STSB'],
160: ['$SNGS'],
161: ['$KRKOP'],
162: ['$TASBP'],
163: ['$TATN'],
164: ['$TTLK'],
165: ['$TGKN'],
166: ['$TGKA'],
167: ['$TGKB'],
168: ['$VRSB'],
169: ['$KBSB'],
170: ['$MISB'],
171: ['$NNSB'],
172: ['$RTSB'],
173: ['$YRSB'],
174: ['$TORS'],
175: ['$TRNFP'],
176: ['$TRFM'],
177: ['$TRMK'],
178: ['$TUZA'],
179: ['$TUCH'],
180: ['$UKUZ'],
181: ['$ARSA'],
182: ['$URKA'],
183: ['$URKZ'],
184: ['$LIFE'],
185: ['$HYDR'],
186: ['$FEES'],
187: ['$PHOR'],
188: ['$HIMCP'],
189: ['$WTCM'],
190: ['$TRCN'],
191: ['$CNTL'],
192: ['$PRFN'],
193: ['$CKPZ'],
194: ['$CHMK'],
195: ['$CHEP'],
196: ['$ELTZ'],
197: ['$ENRU'],
198: ['$UNKL'],
199: ['$UPRO'],
200: ['$YAKG'],
201: ['$YKEN'],
202: ['$VZRZ'],
203: ['$KUZB'],
204: ['$SGZH'],
205: ['$TNSE'],
206: ['$DIOD'],
207: ['$MOBB'],
208: ['$NAUK'],
209: ['$RNFT'],
210: ['$OMZZP'],
211: ['$ROSB'],
212: ['$RGSS'],
213: ['$KCHEP'],
214: ['$MAGEP'],
215: ['$MSNG'],
216: ['$SAGO'],
217: ['$SLEN'],
218: ['$ETLN'],
219: ['$FIXP'],
220: ['$GLTR'],
221: ['$HHRU'],
222: ['$HMSG'],
223: ['$MAIL'],
224: ['$MDMG'],
225: ['$TCS'],
226: ['$OKEY'],
227: ['$FIVE'],
228: ['$QIWI'],
229: ['$LNTA'],
230: ['$OZON'],
231: ['$AGRO'],
232: ['$RTSD'],
233: ['$NORD'],
234: ['$POGR'],
235: ['$POLY'],
236: ['$YNDX'],
237: ['$SFTL'],
240: ['$VEON'],
241: ['$POSI'],
251: ['$CIAN'],
254: ['$WUSH'],
255: ['$SPBE'],
257: ['$GLPR'],
267: ['$RENI'],
258: ['$ASTR'],
261: ['$AQUA'],
265: ['$UGLD'],
266: ['$ABIO'],
268: ['$GECO'],
269: ['$CARM'],
270: ['$HNFG'],
271: ['$SVCB'],
272: ['$EUTR'],
273: ['$DELI'],
274: ['$DIAS'],
}

grades = {0 : "Сильный негатив",
          1 : "Сильный негатив",
          2 : "Негатив",
          3 : "Нейтрально",
          4 : "Позитив",
          5 : "Сильный позитив",}


@dp.message(lambda message: message.text == "👤 Проанализировать каналы 👤")
async def analyze_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f'✍️ Введите ссылки на каналы, которые хотите проанализировать (каналы должны быть публичными):')

@dp.message(lambda message: message.text == "ℹ️ Помощь ℹ️")
async def help_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f'ℹ️ Список доступных команд ℹ️\n\n/start - Запустить бота\n/help - Вывести список доступных команд\n/analyze - Проанализировать каналы\n/get - Список компаний', reply_markup=(await get_menu_keyboard()))


@dp.message(lambda message: message.text == "📋 Список компаний 📋")
async def help_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"📋 Список компаний, по которым нам удалось проанализировать настроения за сегодняшний день: (фича в разработке)", reply_markup=(await get_menu_keyboard()))


@dp.message(lambda message: ("t.me" in message.text) or ("@" in message.text))
async def analyze_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f'🔄 Анализируем каналы...')
    
    channels = message.text.strip().split()
    
    client = TelegramClient('parser', API_ID, API_HASH)
    await client.start()
    
    date_today = datetime(datetime.now().year, datetime.now().month, datetime.now().day - 2, datetime.now().hour, datetime.now().minute, datetime.now().second, datetime.now().microsecond, datetime.now().tzinfo)
    
    res_string = "📌 Результат анализа:\n\n"
    
    for ch in channels:
        if ("t.me" in ch) or ("@" in ch):
            await client(functions.channels.JoinChannelRequest(channel=ch))
            try:
                async for mess in client.iter_messages((ch), offset_date=date_today, reverse=True):
                    res = predict(mess.text)
                    if res:
                        grade = grades[res[0][1]]
                        share = shares[res[0][0]][0]
                        
                        if not (share in res_string):
                            res_string += f"{share}: {grade}\n"
            except Exception:
                pass
    
    if res_string == "📌 Результат анализа:\n\n":
        await message.answer("Ошибка во время анализа. Попробуйте ещё раз.")
        return
    await message.answer(res_string)
    