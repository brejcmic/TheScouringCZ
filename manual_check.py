"""
    Základní překlad souborů do češtiny
"""
# čtení csv souborů
import pandas
import csv
import shutil

# klíčové slovo pro ukončení editace
END_KEYWORD = "END"

def manual_check(filename:str):
    """
        Smyčka kontroly.

    Returns
    -------
        None
    """

    print("####################### Kontrola souboru {0} #######################".format(filename))

    # Načtení CSV v UTF-16 LE
    endf = pandas.read_csv(filepath_or_buffer="simple_translation/en/{0}".format(filename),
                           usecols=[0, 1],
                           names=['key', 'descr'],
                           header=None,
                           encoding="utf-16-le")

    try:
        csdf = pandas.read_csv(filepath_or_buffer="simple_translation/cs/{0}".format(filename),
                               usecols=[0, 1],
                               names=['key', 'descr'],
                               header=None,
                               encoding="utf-16-le")
    except FileNotFoundError:
        print("Není k dispozici překlad souboru simple_translation/cs/{0}".format(filename))
        exit(1)

    try:
        csdfref = pandas.read_csv(filepath_or_buffer="manual_checked/cs/{0}".format(filename),
                                  usecols=[0, 1],
                                  names=['key', 'descr'],
                                  header=None,
                                  encoding="utf-16-le")
    except FileNotFoundError:
        print("Není k dispozici zkontrolovaný souboru manual_checked/cs/{0}".format(filename))
        csdfref = pandas.DataFrame(data={'key': ['no_data'], 'descr': ['Nejsou data']})



    # příprava výsledku
    translation = []

    # smyčka kontroly
    csdf = csdf.reset_index()
    for index, row in csdf.iterrows():

        # test zda nebyl klíč již přeložen
        checked_meaning = csdfref.loc[csdfref['key'] == row['key']]
        if checked_meaning['key'].empty:
            en_meaning = endf.loc[endf['key'] == row['key'], 'descr'].values[0]
            cs_meaning = row['descr']

            print("### {0} ###".format(row['key']))
            print("Původní popis: {0}".format(en_meaning))
            print("Nový popis: {0}".format(cs_meaning))

            lines = []
            change = True
            print(f"Potvrď popis, pro nezměněný ENTER, jinak popis ukončit zápisem '{END_KEYWORD}':")
            while change:
                response = input()
                change = (response != "" or lines) and response != END_KEYWORD

                if change:
                    lines.append(response)

            if not lines:
                descr = cs_meaning
            else:
                descr = "\n".join(lines)

            translation.append(descr)
            print("------------------------------------")
            print("Nový popis:\n{0}".format(descr))
            print("====================================")
        else:
            translation.append('{0}'.format(checked_meaning['descr'].values[0]))

    # zápis překladu
    csdf['descr_checked'] = translation

    csdf_out = csdf[['key', 'descr_checked']]
    csdf_out.to_csv("manual_checked/cs/{0}".format(filename),
                     encoding="utf-16-le",
                     header=None,
                     index=False,
                     quoting=csv.QUOTE_MINIMAL)


shutil.copy(src="simple_translation/en/devlog.csv",dst="manual_checked/cs/devlog.csv")
shutil.copy(src="simple_translation/en/heroes.csv",dst="manual_checked/cs/heroes.csv")
manual_check("assets.csv")
manual_check("game.csv")
manual_check("tips.csv")
manual_check("tutorial.csv")
manual_check("ui.csv")
