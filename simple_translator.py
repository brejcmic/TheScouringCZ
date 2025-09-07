"""
    Základní překlad souborů do češtiny
"""

# čtení csv souborů
import pandas
import csv
# překladač
from googletrans import Translator
# asynchronní operace
import asyncio

# přepínač pro windows
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def simple_translator(filename:str):
    """
        Smyčka překladu.

    Returns
    -------
        None
    """
    # Výzva
    print("####### Překlad souboru {0} #######".format(filename))


    # Načtení CSV v UTF-16 LE
    endf = pandas.read_csv(filepath_or_buffer="simple_translation/en/{0}".format(filename),
                           usecols=[0, 1],
                           names=['key', 'descr'],
                           header=None,
                           encoding="utf-16-le")

    try:
        csdf = pandas.read_csv(filepath_or_buffer="manual_checked/cs/{0}".format(filename),
                               usecols=[0, 1],
                               names=['key', 'descr'],
                               header=None,
                               encoding="utf-16-le")
    except FileNotFoundError:
        csdf = pandas.DataFrame(data={'key': ['no_data'], 'descr': ['Nejsou data']})

    # Inicializace překladače
    translator = Translator()
    translation = []

    # smyčka překladu
    endf = endf.reset_index()
    for index, row in endf.iterrows():

        # test zda nebyl klíč již přeložen
        checked_meaning = csdf.loc[csdf['key'] == row['key']]
        if checked_meaning['key'].any():
            cs_meaning = checked_meaning['descr'].values[0]
        else:
            cs_transl = await translator.translate(text=row['descr'], src="en", dest='cs')
            cs_meaning = cs_transl.text

        translation.append('{0}'.format(cs_meaning))

        print("Zpracovan radek {0}".format(index))

    # zápis překladu
    endf['descr_cs'] = translation

    csdf_out = endf[['key', 'descr_cs']]
    csdf_out.to_csv("simple_translation/cs/{0}".format(filename),
                     encoding="utf-16-le",
                     header=None,
                     index=False,
                     quoting=csv.QUOTE_MINIMAL)


asyncio.run(simple_translator("assets.csv"))
asyncio.run(simple_translator("devlog.csv"))
asyncio.run(simple_translator("game.csv"))
asyncio.run(simple_translator("tips.csv"))
asyncio.run(simple_translator("tutorial.csv"))
asyncio.run(simple_translator("ui.csv"))
