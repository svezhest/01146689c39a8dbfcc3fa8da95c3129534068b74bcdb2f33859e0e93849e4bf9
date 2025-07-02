import pandas as pd
import re
from nltk.stem.snowball import SnowballStemmer
import math
import numpy as np
import typing as tp
import json
from catboost import CatBoostClassifier

stemmer = SnowballStemmer("russian")

companies = {
    1: (['derzp', 'derzhava', 'derz', 'держав'], []),
    2: (['мкб', 'cbom'], ['московск кредитн банк', 'credit bank of moscow', 'credit bank']),
    3: (['росдорбанк', 'rdrb', 'рдбанк', 'rosdorbank'], ['российск акционерн коммерческ дорожн банк', 'дорожн банк', 'russian public jointstock commercial roads bank', 'roads bank']),
    4: (['alrosa', 'alrs', 'алрос'], []),
    5: (['авангард', 'avan', 'avangard'], []),
    6: (['prmb', 'primbank'], ['акб примор', 'акб примор', 'банк примор', 'банк примор', 'pjscb primorye', 'pjscb primorye', 'public jointstock commercial bank primorye', 'bank primorye', 'bank primorye']),
    7: (['втб', 'vtbr', 'vtb'], []),
    8: (['irkutskenergo', 'иркутскэнерг', 'irgz', 'иркэнерг'], []),
    9: (['kazanorgsintez', 'казаньоргсинтез', 'kzos'], ['органическ синтез']),
    10: (['lenzoloto', 'lnzl', 'лензолот'], []),
    11: (['rual', 'руса', 'rusal'], ['объединен компан руса']),
    12: (['enpl', 'enpg'], ['эн груп', 'en group', 'en group plc']),
    13: (['белон', 'blng', 'belon'], []),
    14: (['dzrd', 'дзрд'], ['донск завод радиодетал']),
    15: (['левенгук', 'lvhk', 'levenhuk'], []),
    16: (['lpsb', 'лэск', 'lpsbg', 'lesk'], ['липецк энергосбытов компан', 'липецк эск']),
    17: (['mrku'], ['межрегиональн распределительн сетев компан ура', 'мрск ура', 'россет ура', 'rosseti ural']),
    18: (['multisistema', 'мультисистем', 'msst'], []),
    19: (['npof', 'npofizika'], ['научнопроизводствен объединен физик', 'нпо физик', 'нпо физик']),
    20: (['mgnzg', 'mgnz'], ['соликамск магниев завод', 'оа смз', 'оа смз']),
    21: (['инарктр', 'aqua', 'инарктик', 'inarctica'], ['русск аквакультур', 'русск мор']),
    22: (['abraudurso', 'abrd'], ['абра  дюрс', 'абра дюрс']),
    23: (['utar'], []),
    24: (['akrn', 'acron', 'акрон'], []),
    25: (['bane'], []),
    26: (['систем', 'afks'], ['афк систем']),
    27: (['alrosa', 'alnu', 'алрос'], []),
    28: (['aptk'], []),
    29: (['acko'], []),
    30: (['assb'], ['астраханск эсб']),
    31: (['amez'], []),
    32: (['aflt', 'aeroflot', 'аэрофлот'], []),
    33: (['bspb', 'бспб'], ['банк санктпетербург', 'банк петербург', 'спб банк']),
    34: (['usbn'], []),
    35: (['bisv'], []),
    36: (['belu', 'beluga', 'белуг'], []),
    37: (['albk'], []),
    38: (['brzl'], []),
    39: (['vjgz'], []),
    40: (['vlhz'], []),
    41: (['vgsb'], []),
    42: (['ogkb'], []),
    43: (['vsyd'], []),
    44: (['gaza'], ['групп газ', 'групп газ', 'па газ', 'па газ']),
    45: (['газкона', 'газкон', 'gazc'], []),
    46: (['rostovoblgaz', 'rtgz', 'ростовоблгаз'], ['па газпр газораспределен ростовнадон', 'газпр рнд']),
    47: (['sibn'], ['па газпр нефт', 'газпр нефт', 'gazprom neft']),
    48: (['газпр', 'gazprom', 'gazp'], ['па газпр']),
    49: (['gazs', 'gasservice'], ['па газсервис']),
    50: (['газтэк', 'gazt', 'gaztec'], []),
    51: (['gtss', 'геотек', 'gseis'], ['па геотек сейсморазведк']),
    52: (['gtrk', 'globaltruck', 'глобалтрак'], []),
    53: (['nornickel', 'норникел', 'gmkn'], ['па горнометаллургическ компан норильск никел', 'па гмк норильск никел', 'норильск никел']),
    54: (['grnt', 'гит'], ['па городск инновацион технолог', 'па гит', 'городск инновацион технолог']),
    55: (['rlmn', 'роллма', 'rollman'], []),
    56: (['smlt', 'самолет', 'samolet'], ['групп самолет']),
    57: (['лср', 'lsrg'], []),
    58: (['gche', 'черкизов', 'cherkizovo'], []),
    59: (['дагестанэнергосб', 'dasb', 'дагсб'], ['dagestanskaya energosbytovaya']),
    60: (['дэк', 'dvec'], ['дальневосточн энергетическ компан']),
    61: (['fesco', 'fesh', 'двмп'], ['дальневосточн морск пароходств']),
    62: (['dsky', 'детмир'], ['детск мир', 'detsky mir']),
    63: (['gtlc', 'gtl', 'джитиэл'], []),
    64: (['eelt'], ['европейск электротехник', 'yevropyeyskaya elyektrotyekhnika']),
    65: (['zil', 'зил', 'zill'], ['завод имен и а  лихачев', 'завод имен лихачев']),
    66: (['zvezda', 'звезд', 'zvez'], []),
    67: (['ижстал', 'izhstal', 'igst'], ['ижевск металлургическ завод']),
    68: (['investdevelopment', 'idvp', 'инвестдевелопмент'], []),
    69: (['russinvest', 'руссинвест', 'rusi'], ['ик руссинвест', 'руссинвест ик']),
    70: (['ingrad', 'ingr', 'opin', 'инград'], ['инград па', 'па инград']),
    71: (['искч', 'iskj'], ['институт стволов клеток человек']),
    72: (['irao'], ['интер ра', 'inter rao', 'интер ра еэс финанс']),
    73: (['клсб', 'кск', 'klsb'], ['калужск сбытов компан', 'калужск сбыткомп', 'kalujskaya sbytovaya']),
    74: (['kamaz', 'kmaz', 'камаз'], []),
    75: (['kunf', 'кузоцм', 'kuzocm'], []),
    76: (['tgkd', 'quadra', 'квадр'], ['а квадр', 'па квадр']),
    77: (['kmez', 'kvmz'], ['па кмз', 'ковровск мехзд', 'ковровск механическ завод']),
    78: (['кокс', 'koks', 'ksgr'], ['па кокс']),
    79: (['всмпоавсм', 'всмпо', 'всмпоависм', 'vsmpoavisma', 'vsmo'], ['корпорац всмпоависм', 'vsmpoavisma corporation']),
    80: (['kogk', 'korgok'], ['коршуновск гок', 'korshunov mining plant']),
    81: (['kmtz', 'kgiw'], ['косогорск металлургическ завод', 'па кмз']),
    82: (['ksk', 'кск', 'ktsb'], ['костромск сбытов компан', 'kostromskaya sbytovaya kompaniya']),
    83: (['кзмс', 'россет', 'kzms', 'rosset'], ['краснокамск завод металлическ сеток']),
    84: (['красноярскэнергосб', 'krsb', 'krsksbit'], []),
    85: (['ktk', 'ктк', 'kbtk'], ['кузбасск топливн компан', 'па ктк']),
    86: (['kazt', 'куйбазот', 'куйбышевазот', 'kuazot'], []),
    87: (['kgkc', 'кгк', 'kgk'], ['курганск генерирующ компан', 'курганск гк', 'па кгк', 'kurgancskaya generiruyushaya']),
    88: (['мвиде', 'mvideo', 'mvid'], []),
    89: (['магн', 'mgnt', 'magnit'], ['па магн', 'магн па']),
    90: (['магнитк', 'ммк', 'magn'], ['magnitigorskiy metallurgicheskiy', 'магнитогорск металлургическ комбинат']),
    91: (['мегафон', 'mfon', 'megafon'], ['па мегафон', 'мегафон па']),
    92: (['odva'], []),
    93: (['gema'], []),
    94: (['mrkz'], []),
    95: (['mrkp'], []),
    96: (['mrkc'], []),
    97: (['merf'], []),
    98: (['mtkb'], []),
    99: (['mtlr', 'мечел', 'mechel', 'mtlrp'], []),
    100: (['mtss', 'мтс', 'mtc'], []),
    101: (['mrsb'], []),
    102: (['mori'], []),
    103: (['мосбирж', 'moex'], ['московск бирж']),
    104: (['mgts'], []),
    105: (['krot', 'krotp'], []),
    106: (['mstt', 'мостотрест'], []),
    107: (['наукасвяз', 'nsvz'], []),
    108: (['irkt'], []),
    109: (['uwgn'], ['объединен вагон компан']),
    110: (['нефаз', 'nfaz'], ['нефтекамск автозавод']),
    111: (['lkoh', 'лукойл'], []),
    112: (['роснефт', 'rosn', 'rosneft'], []),
    113: (['нижнекамскнефтех', 'nkncp', 'nknc'], []),
    114: (['nkshp', 'нижнекамскшин', 'nksh'], []),
    115: (['nvtk', 'novatek', 'новатэк'], []),
    116: (['нлмк', 'nlmk'], []),
    117: (['nkhp', 'нкхп'], ['новороссийск комбинат хлебопродукт']),
    118: (['нмтп', 'nmtp'], ['новороссийск морск порт', 'новороссийск морск торгов порт']),
    119: (['nompp', 'новошип'], ['новороссийск морск пароходств']),
    120: (['unac'], ['па оак', 'па оак', 'объединен авиастроительн корпорац']),
    121: (['ucss'], ['кредитн систем', 'объединен кредитн систем']),
    122: (['одксатурн', 'сатурн', 'satr'], ['одк сатурн']),
    123: (['orup'], ['ор групп', 'па ор']),
    124: (['paza', 'павлбус'], ['павловск автобус', 'павл автобус']),
    125: (['pmsb', 'пермэнергосб', 'pmsbp'], ['пермск энергосбытов компан']),
    126: (['pikk'], ['пик сз']),
    127: (['полюс', 'plzl'], []),
    128: (['rkke', 'энерг'], ['ркк энерг', 'ркк энерг']),
    129: (['распадск', 'rasp'], ['па распадск']),
    130: (['росбизнесконсалтинг', 'rbcm'], ['гк росбизнесконсалтинг', 'рос бизнес консалтинг']),
    131: (['chgz'], ['рнзападн сибир']),
    132: (['росгосстр', 'rgsc'], ['росгосстр банк', 'банк росгосстр', 'ргс банк']),
    133: (['rost', 'росинтер', 'rosinter'], ['росинтер ресторантс холдинг']),
    134: (['mrkv'], ['россет волг']),
    135: (['kube'], ['россет кубан']),
    136: (['lsng'], ['россет ленэнерг']),
    137: (['msrs'], ['россет московск регион']),
    138: (['mrkk'], ['россет северн кавказ']),
    139: (['mrks'], ['россет сибир']),
    140: (['mrky'], []),
    141: (['rsti'], ['российск сет']),
    142: (['rtkm', 'ростелек'], []),
    143: (['rugr'], []),
    144: (['rolo'], []),
    145: (['rusp'], []),
    146: (['rzsb'], []),
    147: (['krkn', 'krknp'], []),
    148: (['саратовэнерг', 'sare', 'sarep'], []),
    149: (['sfin'], []),
    150: (['сбер', 'sber', 'сбербанк', 'sberbank'], []),
    151: (['svet'], ['светофор групп', 'групп светофор']),
    152: (['chmf', 'северстал'], []),
    153: (['selg', 'селигдар'], []),
    154: (['sibg'], []),
    155: (['mfgs'], []),
    156: (['jnosp', 'jnos'], []),
    157: (['совкомфлот', 'flot'], []),
    158: (['svav', 'sollers', 'северстальавт', 'соллерс'], []),
    159: (['stsb'], []),
    160: (['сургутнефтегаз', 'sngs'], []),
    161: (['krkop'], ['ткз красн котельщик', 'ткз красн котельщик', 'красн котельщик', 'pjsc krasny kotelshchik', 'krasny kotelshchik']),
    162: (['tasb', 'тамбовэнергосб', 'tasbp'], ['тамбовск энергосбытов компан']),
    163: (['tatn', 'tatneft', 'татнефт'], []),
    164: (['таттелек', 'tattelecom', 'ttlk'], []),
    165: (['tgk', 'tgc', 'тгк', 'tgkn'], []),
    166: (['tgk', 'tgc', 'tgka', 'тгк'], []),
    167: (['tgk', 'tgc', 'tgkb', 'тгк'], []),
    168: (['vrsbp', 'vrsb'], ['тнс энерг воронеж']),
    169: (['kbsb', 'kbsbp'], ['тнс энерг кубан']),
    170: (['misb', 'misbp'], ['тнс энерг мар эл']),
    171: (['nnsbp', 'nnsb'], ['тнс энерг нижн новгород', 'тнс энерг нижн новг']),
    172: (['rtsbp', 'rtsb'], ['тнс энерг ростовнадон', 'тнс энерг рост']),
    173: (['yrsbp', 'yrsb'], ['тнс энерг ярославл']),
    174: (['tors', 'трк'], ['томск распределительн компан', 'россет томск']),
    175: (['trnfp', 'transneft', 'транснефт'], []),
    176: (['трансфин', 'transfin', 'trfm'], []),
    177: (['tmk', 'тмк', 'trmk'], ['oao tmk', 'трубн металлургическ компан']),
    178: (['тза', 'tuza'], ['па тза', 'па тза', 'туймазинск завод автобетоновоз', 'не tza  ест американск тикер']),
    179: (['тксм', 'tuch'], ['тучковск ксм']),
    180: (['ukuz'], ['па южн кузбасс', 'па южн кузбасс', 'southern kuzbass coal company', 'южн кузбасс']),
    181: (['арсагер', 'arsa'], ['арсагеран встреча упоминан']),
    182: (['uralkali', 'urka', 'уралкал'], []),
    183: (['urkz'], ['уральск кузниц', 'urals stampings plant']),
    184: (['life', 'pharmsynthez', 'фармсинтез'], ['па фармсинтез']),
    185: (['русгидр', 'hydr', 'rushydro'], ['па русгидр']),
    186: (['fees'], ['россет фск еэс', 'ao fgc ues', 'па россет', 'па фск еэс', 'фск еэс']),
    187: (['фосагр', 'phor', 'phosagro'], []),
    188: (['himcp', 'himprom', 'химпр'], ['па химпр']),
    189: (['wtcm', 'цмт', 'wtc'], ['центр международн торговл', 'world trade center']),
    190: (['trcn', 'трансконтейнер', 'transcontainer'], ['па трансконейнер']),
    191: (['cntl'], ['центральн телеграф', 'central telegraph', 'па центральн телеграф']),
    192: (['чзпснпрофнаст', 'prfn'], ['па чзпснпрофнаст', 'челябинск завод профилирова стальн наст']),
    193: (['чкпз', 'ckpz'], ['oao chelyabinsk forgeandpress plant', 'па челябинск кузнечнопрессов завод']),
    194: (['chmk', 'чмк'], ['chelyabinsk metallurgical plant', 'па чмк', 'челябинск металлургическ комбинат']),
    195: (['чтпз', 'chep'], ['chelyabinsk pipe rolling plant', 'па чтпз', 'челябинск трубопрокатн завод']),
    196: (['электроцинк', 'electrozink', 'eltz'], ['па электроцинк']),
    197: (['elfv', 'enru'], ['энел росс', 'enel russia', 'па энел росс']),
    198: (['unkl', 'unickel', 'южуралникел'], ['комбинат южуралникел', 'па комбинат южуралникел']),
    199: (['unipro', 'юнипр', 'upro'], ['па юнипр']),
    200: (['ятэк', 'yakg', 'yatec'], ['якутск топливноэнергетическ компан', 'па якутск топливноэнергетическ компан']),
    201: (['yken', 'yakutskenergo', 'якутскэнерг'], ['па якутскэнерг']),
    202: (['vzrz'], ['банк возрожден', 'vozrozhdenie bank', 'па банк возрожден']),
    203: (['kuzb', 'kuzbank'], ['банк кузнецк', 'па банк кузнецк']),
    204: (['сегеж', 'segezha', 'sgzh'], ['сегеж групп', 'segezha group']),
    205: (['tnse'], ['тнс энерг', 'tns energo', 'па гк тнс энерг']),
    206: (['diod', 'диод'], ['diod plant of ecological technics and ecomeals', 'па диод', 'завод экологическ техник и экопитан диод']),
    207: (['mobb'], []),
    208: (['nauk'], []),
    209: (['rnft'], []),
    210: (['omzz', 'omzzp'], []),
    211: (['rosb'], []),
    212: (['rgss'], []),
    213: (['kchep', 'kche'], []),
    214: (['magep', 'mage'], []),
    215: (['мосэнерг', 'msng'], ['московскаяэнергетическ компан']),
    216: (['sago', 'самарэнерг'], []),
    217: (['сахалинэнерг', 'slen'], []),
    218: ([], ['etln li', 'эталон груп', 'групп эталон']),
    219: (['fixprice', 'fixp'], ['fix price']),
    220: (['globaltrans', 'глобалтранс'], ['gltr li']),
    221: (['hhru', 'headhunter'], []),
    222: (['hmsg'], []),
    223: (['vkco', 'вк', 'вконтакт'], ['mail li', 'vk group']),
    224: (['mdmg'], ['md medical']),
    225: (['tcsg', 'тинькофф', 'tinkoff'], ['tcs li', 'tcs group']),
    226: (['okey'], []),
    227: ([], ['five li', 'х групп', 'x group']),
    228: (['qiwi'], ['а кив']),
    229: (['lnta', 'lent'], []),
    230: (['ozon'], []),
    231: (['русагр', 'rusagro', 'agro'], []),
    232: (['rtsd'], []),
    233: (['nordgold', 'nord'], []),
    234: (['petropavl', 'петропавловск', 'pogr'], []),
    235: (['polymetal', 'poly', 'полиметалл'], []),
    236: (['yandex', 'яндекс', 'yndx'], []),
    237: (['softline', 'софтлайн', 'sftl', 'noventiq'], []),
    240: (['veon', 'веон'], []),
    241: (['posi'], ['positive tech', 'групп позит', 'гр  позит', 'positive group']),
    251: (['cian', 'циа'], []),
    254: (['wush', 'whoosh', 'вуш'], []),
    255: (['spbe'], ['спб бирж']),
    257: (['globalports', 'глобалпортс', 'glpr'], []),
    267: (['reni'], ['ренессанс страхован']),
    258: (['astr', 'astra', 'астр'], ['гк астр', 'групп астр']),
    261: (['аквакультур', 'aqua', 'инарктик'], ['русск мор', 'русск аквакультур']),
    265: (['ugld', 'югк'], []),
    266: (['abio', 'иартг', 'артг'], ['артг биотех']),
    268: (['игенетик', 'genetico', 'geco'], []),
    269: (['смарттехгрупп', 'carm'], ['па стг']),
    270: (['hnfg', 'хендерсон'], []),
    271: (['svcb', 'sovcombank', 'совкомбанк'], []),
    272: (['eutr'], ['азс трасс', 'азс трасс', 'азс трасс']),
    273: (['delimobil', 'делимоб', 'deli'], ['каршеринг рус', 'па каршеринг русс', 'каршеринг русс  па']),
    274: (['dias', 'diasoft'], [])
}


class WordScore:
    def __init__(self, super_negative_count: float, negative_count: float, neutral_count: float, positive_count: float, super_positive_count: float):
        self.super_negative_count = super_negative_count
        self.negative_count = negative_count
        self.neutral_count = neutral_count
        self.positive_count = positive_count
        self.super_positive_count = super_positive_count

        # not to return
        self.total_positive_count = self.super_positive_count + self.positive_count
        self.total_negative_count = self.super_negative_count + self.negative_count
        self.total_count = self.total_positive_count + self.total_negative_count

        _total_count = max(self.total_count, 1)

        self.positive_proportion = self.total_positive_count / _total_count
        self.negative_proportion = self.total_negative_count / _total_count

        # not to return
        self.simple_score = -1 * self.total_negative_count + self.total_positive_count
        self.score = -1 * self.super_negative_count + -0.1 * self.negative_count + \
            0.1 * self.positive_count + self.super_positive_count
        self.score_extreme_only = -1 * self.super_negative_count + self.super_positive_count

        self.simple_score_relative = self.simple_score / \
            max(self.total_negative_count + self.total_positive_count, 1)
        self.score_relative = self.score / _total_count
        self.score_extreme_only_relative = self.score_extreme_only / _total_count

        self.meaningful_proportion = (
            self.super_positive_count + self.total_negative_count) / max(self.positive_count + self.neutral_count, 1)
        self.extreme_proporion = (self.super_positive_count + self.super_negative_count) / max(
            self.positive_count + self.neutral_count + self.negative_count, 1)

        self.certanty = (self.positive_proportion if self.score > 0 else (
            self.negative_proportion if self.score < 0 else 0)) * max(1, self.extreme_proporion * 10) * math.log(_total_count)

    def get_array(self) -> list[float]:
        return [self.super_negative_count,
                self.negative_count,
                self.neutral_count,
                self.positive_count,
                self.super_positive_count,
                # self.total_positive_count,
                # self.total_negative_count,
                # self.total_count,
                self.positive_proportion,
                self.negative_proportion,
                # self.simple_score,
                # self.score,
                # self.score_extreme_only,
                self.simple_score_relative,
                self.score_relative,
                self.score_extreme_only_relative,

                self.meaningful_proportion,
                self.extreme_proporion,

                self.certanty]


FEAUTURES_LEN = 13


def transform_word(word):
    return stemmer.stem(''.join(ch for ch in word.lower() if ch.isalpha()))


def get_text_word_metrics(text: str, word_scores: dict[str, list[float]]) -> list[float]:
    metrics = []

    sentence_word_scores = [word_scores[word]
                            for word in text.split() if word in word_scores]
    if len(sentence_word_scores) == 0:
        sentence_word_scores.append([0] * FEAUTURES_LEN)

    for idx in range(FEAUTURES_LEN):
        for aggr_fn in (min, max, sum, np.mean):
            metrics.append(
                aggr_fn(np.array([word_score[idx] for word_score in sentence_word_scores])))

    return metrics


def make_features(text, word_scores):
    return [get_text_word_metrics(' '.join(filter(lambda w: True if w in word_scores else False, (transform_word(word) for word in filter(lambda w: len(w) > 0, re.split('[?!.,:; \n\t]', text))))), word_scores)]


def make_features_splitted(splitted, word_scores):
    return [get_text_word_metrics(' '.join(filter(lambda w: True if w in word_scores else False, (transform_word(word) for word in splitted))), word_scores)]


def predict(text: str) -> list[tuple[int, int]]:
    splitted = [transform_word(word)
                for word in filter(lambda word: len(word) > 0, re.split('[?!.,:; \n\t]', text))]

    mentioned_companies = []

    for company in companies:
        found = False
        for single_word_mention in companies[company][0]:
            if single_word_mention in splitted:
                mentioned_companies.append(company)
                found = True
                break
        if not found:
            for compound_mention in companies[company][1]:
                if compound_mention in ' '.join(splitted):
                    mentioned_companies.append(company)
                    found = True
                    break

    with open('utils/word_scores_full.json') as f:
        word_scores = json.loads(f.read())
        model = CatBoostClassifier()
        model.load_model('utils/model')

        y = model.predict(make_features_splitted(splitted, word_scores))
        return list(set((company_id, y[0][0]) for company_id in mentioned_companies))
    