#!/usr/bin/python3

import pandas as pd
import numpy as np
from math import floor
from collections import defaultdict

def invert_map(m):
    res={}
    for k, v in m.items():
        res[v]=res.get(v, [])
    for k, v in m.items():
        res[v].append(k)
    return res
 
def get_unique_list(df,name):
    return df[name].unique().tolist()

def get_df_sum(df,name):
    return df.agg({name:'sum'})[name]

def get_df_groupby_sum(df,name_group,name_sum):
    return df.groupby([name_group]).agg({name_sum:'sum'}).to_dict()[name_sum]

def get_df_groupby2_sum(df,name_group1, name_group2,name_sum):
    return df.groupby([name_group1,name_group2]).agg({name_sum:'sum'}).to_dict()[name_sum]

def get_df_groupby_2(df,name1,name2):
    return df.groupby([name1,name2]).count().reset_index(name2).rename(columns={0:'count'}).to_dict()[name2]

def get_list_if(df,name1,name2):
    return list(df.groupby([name1,name2]).count().reset_index(name2).to_dict()[name2].keys())

def remove_if(dic, val):
    d=dic
    d1=dic
    for key, value in list(d.items()):
        if value == val:
#             print(key,value)
             del d1[key]
    return d1
def remove_neg(dic):
    d=dic.copy()
    d1=dic.copy()
    for key, value in list(d.items()):
        if value <= 0:
#             print(key,value)
             del d1[key]
    return d1


def quozienti_interi_migliori_resti(numero_seggi, liste, cifre, quoziente, max_seggi=False, max_seggi_list=[]):
    list_seggi=[]
    list_resti=[]
    list_fraz=[]
    seggi_ass=0
#    print("Da assegnare: ", numero_seggi)
    for l in liste:
        try:
            cifra=cifre[l]
        except KeyError:
            cifra=0
        seggi_lista= floor(cifra/quoziente)
        if(max_seggi):
            try:
                max_seggi_l=max_seggi_list[l]
            except KeyError:
                max_seggi_l=0
        if(max_seggi and max_seggi_l<=seggi_lista):
            resto_lista=0
        else:
            resto_lista= cifra % quoziente
        fraz=cifra/quoziente - seggi_lista
#        print("Quozienti interi: ", seggi_lista, ", ", l)
        list_seggi.append([l,seggi_lista])
        list_resti.append([l,resto_lista])
        list_fraz.append([l,fraz])
        seggi_ass+=seggi_lista
    list_seggi=dict(list_seggi)
    list_resti=dict(list_resti)
    list_fraz=dict(list_fraz)
    seggi_resti=numero_seggi-seggi_ass
    for r in range(1,seggi_resti+1):
        win_resto=max(list_resti,key=list_resti.get)
#        print("Resto ", r, ": ", win_resto)
        list_seggi[win_resto]+=1
        list_resti[win_resto]=0
        #parità di resti?
    return list_seggi, list_resti, list_fraz

def inv_dict(d):
    flipped = defaultdict(dict)
    for key, val in d.items():
        for subkey, subval in val.items():
            flipped[subkey][key] = subval
    return dict(flipped)

def resti_validi(ed_dict, fraz,circ):
    res=False
#    print("Cerco resti")
    for ed_list, ed_val in ed_dict.items():
        try:
            ed_fraz=fraz[ed_list][circ]
        except KeyError:
            ed_fraz=0
#        print(ed_list, ed_val, ed_fraz)
        if(ed_val<0 and ed_fraz > 0):
            return True
#    print("Resti non validi")
    return False

def max_tiebreak(_dict, tb_list):
    max_=max(_dict,key=_dict.get)
    if(tb_list==[]):
        return max_
    else:
        max_= list(sorted(_dict, key=lambda w: (_dict[w], tb_list[w]),reverse=True))[0]
#       print("Parità. Vince: ", max_)
        return max_

def max_tiebreak_minFraz(_dict, fraz_list, liste):
    max_=max(_dict,key=_dict.get)
    if(fraz_list==[]):
        return max_
    else:
#        print("Parità")
        list_max={}
        #print(remove_neg(_dict))
        #print(list(_dict.keys()))
        for l in list(_dict.keys()):
            if(_dict[l]>0):
                #print(l,fraz_list[l], _dict[l])
                list_max_key= sorted(fraz_list[l], key=lambda w: (fraz_list[l][w]))[_dict[l]-1]
                list_max[l]=-fraz_list[l][list_max_key]
                #print(l,_dict[l], list_max[l])
 #               print("endif")
#        print("endfor")
#        print("possibili: ",remove_neg(_dict))
        max_= list(sorted(remove_neg(_dict), key=lambda w: (_dict[w], list_max[w]), reverse=True))[0]
        #print(max_)
        return max_

def riassegna_ecc_def_collegio(liste, circoscrizioni, seggi_circ, fraz_circ, seggi_tot, tiebreak_ecc=[], minFraz=False):
    
    seggi_circ_result=seggi_circ
    ###
    def seggi_assegnati():
        for l in liste:
            seggi_l=0
            for circ in circoscrizioni:
                try:
                    seggi_l+=seggi_circ_result[circ][l]
                except KeyError:
                    seggi_l+=0
            try:
                st=seggi_tot[l]
            except KeyError:
                st=0
            if(seggi_l != st):
                return False
        return True
    ###


    fraz_circ_inv=inv_dict(fraz_circ)
    fcinv=fraz_circ_inv.copy()
    while( not seggi_assegnati() ):
        #calcola seggi eccedenti/deficitari
        eccdef = {}
        for l in liste:
            seggi_l=0
            for circ in circoscrizioni:
            #    print(l, circ)
                try:
                    seggi_l+=seggi_circ_result[circ][l]
                except KeyError:
                    seggi_l+=0
            try:
                st=seggi_tot[l]
            except KeyError:
                st=0
            eccdef[l]=seggi_l - st
#       eccdef=remove_if(eccdef,0)
        #prendi max eccedente (TODO: gestire parità
        print(eccdef)
        if not minFraz:
            max_ecc=max_tiebreak(eccdef,tiebreak_ecc)
        else:
            max_ecc=max_tiebreak_minFraz(eccdef, fcinv, liste)
        #print("max eccedente:", max_ecc)
        #print("eccedenti: ", fraz_circ_inv[max_ecc])
        min_max_ecc=min(fraz_circ_inv[max_ecc],key=fraz_circ_inv[max_ecc].get)
        #print("collegio minimo eccedente:", min_max_ecc)
        min_def=min(eccdef, key=eccdef.get)
        #print("min deficitario:", min_def) #gestire parità
        max_min_def=max(fraz_circ_inv[min_def],key=fraz_circ_inv[min_def].get)
        #print("collegio massimo deficitario:", max_min_def)
        seggi_circ_result[max_min_def][min_def]+=1
        seggi_circ_result[min_max_ecc][max_ecc]-=1
        del fraz_circ_inv[max_ecc][min_max_ecc]
        del fraz_circ_inv[min_def][max_min_def]

    return seggi_circ_result



def riassegna_ecc_def(liste, circoscrizioni, seggi_circ, fraz_circ, seggi_tot, tiebreak_ecc=[], minFraz=False):
    
    seggi_circ_result=seggi_circ
    ###
    def seggi_assegnati():
        for l in liste:
            seggi_l=0
            for circ in circoscrizioni:
                try:
                    seggi_l+=seggi_circ_result[circ][l]
                except KeyError:
                    seggi_l+=0
            try:
                st=seggi_tot[l]
            except KeyError:
                st=0
            if(seggi_l != st):
                return False
        return True
    ###


    fraz_circ_inv=inv_dict(fraz_circ)
    fcinv=fraz_circ_inv.copy()
    while( not seggi_assegnati() ):
        #calcola seggi eccedenti/deficitari
        eccdef = {}
        for l in liste:
            seggi_l=0
            for circ in circoscrizioni:
            #    print(l, circ)
                try:
                    seggi_l+=seggi_circ_result[circ][l]
                except KeyError:
                    seggi_l+=0
            try:
                st=seggi_tot[l]
            except KeyError:
                st=0
            eccdef[l]=seggi_l - st
#       eccdef=remove_if(eccdef,0)
        #prendi max eccedente (TODO: gestire parità
        #print(eccdef)
        if not minFraz:
            max_ecc=max_tiebreak(eccdef,tiebreak_ecc)
        else:
            max_ecc=max_tiebreak_minFraz(eccdef, fcinv, liste)
#        print("max eccedente:", max_ecc)
#        print("eccedenti: ", fraz_circ_inv[max_ecc])
        min_max_ecc=min(fraz_circ_inv[max_ecc],key=fraz_circ_inv[max_ecc].get)
#        print("min eccedente:", min_max_ecc)
        
        if(resti_validi(eccdef, fraz_circ_inv, min_max_ecc)):
            seggi_circ_result[min_max_ecc][max_ecc]-=1
            def_list=[]

            for ed_list, ed_val in eccdef.items():
                 if(ed_val < 0):
#                     print("Deficitario possibile", ed_list)
                     try:
                         def_list.append([ed_list,fraz_circ[min_max_ecc][ed_list]])
                     except KeyError:
                         pass
            def_list=dict(def_list)
#            print("deficitari in ", min_max_ecc, ":", def_list)
            max_def=max(def_list,key=def_list.get)
#            print("seggio assegnato a ", max_def)
            seggi_circ_result[min_max_ecc][max_def]+=1

            del fraz_circ[min_max_ecc][max_def]
            del fraz_circ_inv[max_def][min_max_ecc]
        del fraz_circ_inv[max_ecc][min_max_ecc]

    return seggi_circ_result

def rosatellum_camera(numero_seggi, file_risultati, file_seggi_circoscrizioni, file_seggi_collegi, sbarramento_lista=0.03, sbarramento_coal=0.1, sbarramento_lista_coal=0.01, delim=',', nome_lista="LISTA", nome_coal="COALIZIONE", nome_voti="VOTI_LISTA",nome_circ="CIRCOSCRIZIONE", nome_coll="COLLEGIOPLURINOMINALE", nome_minl="TIPO"):
    df = pd.read_csv(file_risultati, delimiter=delim)
    liste = get_unique_list(df,nome_lista)
    coalizioni = get_unique_list(df,nome_coal)
    cifra_elett_naz = get_df_groupby_sum(df,nome_lista,nome_voti)
    totale_voti_validi = get_df_sum(df,nome_voti)
    list_coal=get_df_groupby_2(df, nome_lista,nome_coal)
    
    coal_list=invert_map(list_coal)
    cifra_elett_naz_coal = get_df_groupby_sum(df,nome_coal,nome_voti)

    lista_minoranze=get_list_if(df,nome_lista,nome_minl)
    
    def lista_non_ammessa_cifra_coalizione(l):
        return cifra_elett_naz[l]/totale_voti_validi < sbarramento_lista_coal and l not in lista_minoranze

    #rimuove dalle coalizioni liste sotto lo sbarramento 1%
    for lista in liste:
        if lista_non_ammessa_cifra_coalizione(lista):
            cifra_elett_naz_coal[list_coal[lista]] -= cifra_elett_naz[lista]

    cifra_elett_circ_coal = get_df_groupby2_sum(df,nome_circ,nome_coal,nome_voti)
    cifra_elett_circ_list = get_df_groupby2_sum(df,nome_circ,nome_lista,nome_voti)


    def lista_ammessa_riparto(l):
        return (cifra_elett_naz[l]/totale_voti_validi > sbarramento_lista or l in lista_minoranze)
 
    def coalizione_ammessa(c):
        return cifra_elett_naz_coal[c]/totale_voti_validi > sbarramento_coal
    #coalizioni e liste singole ammesse:
    admitted_coal=[]
    admitted_list=[]
    adm_list_coal={}
    for lista in liste:
        if lista_ammessa_riparto(lista):
            if coalizione_ammessa(list_coal[lista]):
                if list_coal[lista] not in admitted_coal:
                    admitted_coal.append(list_coal[lista])
            else:
                admitted_list.append(lista)
    admitted_lc=admitted_list+ admitted_coal
    cifre_lc   ={**cifra_elett_naz,**cifra_elett_naz_coal}

    #determina quoziente elettorale nazionale
    quoz_elett_naz=0
    for lc in admitted_lc:
        quoz_elett_naz+=cifre_lc[lc]
    quoz_elett_naz=floor(quoz_elett_naz/numero_seggi)

    #ripartisci seggi nazionali (coalizioni e liste singole)
    seggi_lc, resti_lc, fraz_lc = quozienti_interi_migliori_resti(numero_seggi, admitted_lc, cifre_lc, quoz_elett_naz)
    #ripartisci seggi nazionali coalizioni tra le liste
    seggi_liste_naz={}
    for l in admitted_list:
        seggi_liste_naz[l]= seggi_lc[l]
    for c in admitted_coal:
        adm_list_coal[c]=[]
        quoz_naz_coal=0
        for l in coal_list[c]:
            if lista_ammessa_riparto(l):
                quoz_naz_coal+=cifra_elett_naz[l]
                adm_list_coal[c].append(l)
                
        quoz_naz_coal=floor(quoz_naz_coal/seggi_lc[c])
        seggi_coal,resti_coal,fraz_coal=quozienti_interi_migliori_resti(seggi_lc[c],adm_list_coal[c],cifra_elett_naz,quoz_naz_coal)
        seggi_liste_naz = {**seggi_liste_naz, **seggi_coal}
    #print(seggi_liste_naz) 


    circ_seggi = pd.read_csv(file_seggi_circoscrizioni, delimiter=delim, index_col=0,squeeze=True).to_dict()

    
    circoscrizioni = get_unique_list(df,nome_circ)
    #ripartizione circoscrizioni
    cifra_elett_list_circ = {}
    for circ in circoscrizioni:
        cifra_elett_list_circ[circ]={}
        for l in liste:
            try:
                _cifra=cifra_elett_circ_list[circ,l]
            except KeyError:
                _cifra=0
            cifra_elett_list_circ[circ][l]=_cifra

    cifre_lc_circ={}
    fraz_lc_circ={}
    seggi_lc_circ={}
    for circ in circoscrizioni:
        quoz_elett_circ=0
        for l in admitted_list:
            quoz_elett_circ += cifra_elett_circ_list[circ,l]
        for c in admitted_coal:
            quoz_elett_circ += cifra_elett_circ_coal[circ,c]
        quoz_elett_circ = floor(quoz_elett_circ / circ_seggi[circ])
 
        cifra_elett_circ_lc={**cifra_elett_circ_list,**cifra_elett_circ_coal}
        cifre_lc_circ[circ]={}
        for lc in admitted_lc:
            cifre_lc_circ[circ][lc]=cifra_elett_circ_lc[circ,lc]

        seggi_lc_circ[circ], resti_lc_circ, fraz_lc_circ[circ] = quozienti_interi_migliori_resti(circ_seggi[circ], admitted_lc, cifre_lc_circ[circ], quoz_elett_circ, max_seggi=True, max_seggi_list=seggi_lc)
    
    seggi_lc_circ=riassegna_ecc_def(admitted_lc, circoscrizioni, seggi_lc_circ,fraz_lc_circ,seggi_lc,tiebreak_ecc=cifre_lc)

    seggi_liste_circ={}
    for circ in circoscrizioni:
        seggi_liste_circ[circ]={}
        for l in admitted_list:
            seggi_liste_circ[circ][l]=seggi_lc_circ[circ][l]
    for c in admitted_coal:
        seggi_coal_circ={}
        fraz_coal_circ={}
        for circ in circoscrizioni:
            if(seggi_lc_circ[circ][c]>0):
                quoz_circ_coal=cifra_elett_circ_coal[circ,c]/seggi_lc_circ[circ][c]
                seggi_coal_circ[circ], resti_coal_circ, fraz_coal_circ[circ] = quozienti_interi_migliori_resti(seggi_lc_circ[circ][c], adm_list_coal[c], cifra_elett_list_circ[circ], quoz_circ_coal)
            else:
                seggi_coal_circ[circ]={}

        seggi_coal_circ = riassegna_ecc_def(adm_list_coal[c], circoscrizioni, seggi_coal_circ, fraz_coal_circ,seggi_liste_naz,tiebreak_ecc=cifra_elett_naz)
        for circ in circoscrizioni:
            seggi_liste_circ[circ]={**seggi_liste_circ[circ],**seggi_coal_circ[circ]}
    
    #print(seggi_liste_circ)

    ###divisione in collegi
    #print("Divisione in collegi")
    collegi = get_unique_list(df,nome_coll)
    coll_seggi = pd.read_csv(file_seggi_collegi, delimiter=delim, index_col=0,squeeze=True).to_dict()
    cifra_elett_coll_coal = get_df_groupby2_sum(df,nome_coll,nome_coal,nome_voti)
    cifra_elett_coll_list = get_df_groupby2_sum(df,nome_coll,nome_lista,nome_voti)
    
    collegi_circ_inv= get_df_groupby_2(df,nome_coll,nome_circ)
    collegi_circ = invert_map(collegi_circ_inv)
    
#   print(collegi_circ)
    
    seggi_liste_coll = {}
    for circ in circoscrizioni:
            #print("Seggi totali: ", seggi_liste_circ[circ])
            cifre_lc_coll={}
            fraz_lc_coll={}
            seggi_lc_coll={}
            for coll in collegi_circ[circ]:
                cifre_lc_coll[coll]={}
                quoz_elett_coll=0
                for l in liste: 
                    #determina il quoziente elettorale di collegio dividendo la somma delle cifre elettorali 
                    #di collegio di *tutte le liste* per il numero dei seggi da attribuire nel collegio stesso
                    try:
                        quoz_elett_coll += cifra_elett_coll_list[coll,l]
                        cifre_lc_coll[coll][l]=cifra_elett_coll_list[coll,l]
                    except KeyError:
                        quoz_elett_coll +=0
                        cifre_lc_coll[coll][l]=0
                quoz_elett_coll = floor(quoz_elett_coll / coll_seggi[coll])
 
                #cifra_elett_coll_lc={**cifra_elett_coll_list,**cifra_elett_coll_coal}

                seggi_lc_coll[coll], resti_lc_coll, fraz_lc_coll[coll] = quozienti_interi_migliori_resti(coll_seggi[coll], liste, cifre_lc_coll[coll], quoz_elett_coll, max_seggi=True, max_seggi_list=seggi_liste_circ[circ])
#               print(coll, seggi_lc_coll[coll])
#                     def riassegna_ecc_def(liste, circoscrizioni,     seggi_circ,   fraz_circ,    seggi_tot):
            seggi_lc_coll=riassegna_ecc_def_collegio(liste, collegi_circ[circ], seggi_lc_coll,fraz_lc_coll,seggi_liste_circ[circ],minFraz=True) 
            
            for coll in collegi_circ[circ]:
                seggi_liste_coll[coll] = remove_if(seggi_lc_coll[coll],0)
#   print(seggi_collegi_liste)
    return seggi_liste_naz, seggi_liste_circ, seggi_liste_coll 

seggi_naz, seggi_circ, seggi_coll =  rosatellum_camera(245,"camera-20180304_new.csv","seggi_circ_camera","seggi_coll_camera")

import yaml
print(yaml.dump(seggi_naz))
print(yaml.dump(seggi_circ))
print(yaml.dump(seggi_coll))

