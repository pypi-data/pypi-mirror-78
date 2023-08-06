# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime
import importlib
import importlib.util
import pymongo
from pymongo import MongoClient
import sys
import em_deep.em_deep as em_deep

importlib.reload(em_deep)

pd.options.display.max_rows = 0


def extract_dates_from_cmms(df_travail,
                            col_event_id, liste_col_equ, state_list,
                            col_date_event_raise, col_date_event_start, col_date_event_end,
                            col_cat_maint, col_type_maint,
                            keep_all_variables=True,
                            col_mdd=None, col_mes=None,
                            col_state_before_event=None, col_state_after_event=None,
                            db_begin_date=None, db_end_date=None):
    """ Fonction rajoutant les 4 dates utiles associées à chaque ligne d'une base GMAO quelconque

    Paramètres obligatoires:

    df_travail : Df contenant la gmao
    col_event-id : col contenant les id des events dans la base
    liste_col_equ : liste des cols permettant d'identifier l'équipements
    col_date_event_start : col contenant les dates de debut des events
    col_date_event_end : col contenant les dates de fin des events
    col_cat-maint:  col contenant les categories de maintenance(préventif, ou correctif)
    col_type-maint: col contenant le type d'action de maintenance (REP, REMP, CTRL)

    Paramètres optionnels

    col_mdd : col contenant les mdd associés a chaque intervention. Si ce paramètre est présent, le mdd associé a
    chaque evenement sera présent dans le df de sortie.
    col_mes : col contenant les dates de MES a l echelle equipement choisie sinon . Si ce paramètre est inexistant
             on traitera la censure, en minorant le TS par :
              - si elle existe, la date présente dans le paramètre db_begin_date
              - sinon prend la date min presente dans la gmao.
    col_state_before-event :  etat observé avant levent
    col_state_after_event :  etat observe apres levenement
    Si ces 2 précedents concepts sont absents les colonnes sont crées automatiquement en supposant que 2 etats,
    et par regle elementaire en fonntion de la colonne "type-maint-event'
    db_begin_date: Date servant la minorer la censure a gauche dans le cas ou il n'y a pas de col_mes présente
    """
    # Rajout des colonnes d'état si elle nexistent pas deja
    print('db_begin_date',db_begin_date)
    print('db end date',db_end_date)
    print('keep all variables', keep_all_variables)
    #    Defintiion des dates limite pour les encadrements des TS

    if db_begin_date is None:  # Dans ce cas on prend le min des dates sur la colonne date_event-start
        date_min = df_travail[col_date_event_raise].min()
    else:
        date_min = db_begin_date

    if db_end_date is None:  # Dans ce cas on prend le min des dates sur la colonne date_event-start
        date_max = df_travail[col_date_event_end].max()
    else:
        date_max = db_begin_date

    date_min = pd.Timestamp(date_min)
    date_max = pd.Timestamp(date_max)
    date_null = pd.Timestamp(2200, 1, 1, 1)
    # print('LA DATE MIN', date_min)
    # print('LA DATE MAX', date_max)

    # Supression des lignes ou le type de maintenance est inconnu

    df_travail = df_travail[df_travail[col_type_maint] != 'nc']

    # Tri préliminaire

    if isinstance(liste_col_equ, str):
        col_tri = [liste_col_equ, col_date_event_raise]
    else:
        col_tri = liste_col_equ + [col_date_event_raise]

    df_travail = df_travail.sort_values(by=col_tri).reset_index()
    # df_travail = df_travail.iloc[0:8]   # Pour le debug
    # print(df_travail)

    # Preparation pour le premier nettoyage de definition des evenements a scanner

    chgt_equ_gauche = df_travail[liste_col_equ] != df_travail[liste_col_equ].shift(1)
    chgt_equ_droite = df_travail[liste_col_equ] != df_travail[liste_col_equ].shift(-1)

    if isinstance(liste_col_equ, list):
        chgt_equ_gauche = chgt_equ_gauche.all(axis=1)
        chgt_equ_droite = chgt_equ_droite.all(axis=1)

    chgt_etat_gauche = df_travail[col_state_before_event] != df_travail[col_state_after_event].shift(1)
    chgt_etat_droite = df_travail[col_state_after_event] != df_travail[col_state_before_event].shift(-1)
    is_ctrl = df_travail[col_type_maint] == 'CTRL'

    #  Supression des lignes de controle inutiles , event detat stationnaires qui ne sont pas sur des frontières de
    #  chgt d equipement ou de changement detat

    indx_useless_ctrl_rows = is_ctrl & ~chgt_equ_gauche & ~chgt_etat_gauche & ~chgt_etat_droite & ~chgt_equ_droite
    df_travail = df_travail[~indx_useless_ctrl_rows]

    # =============================================================================
    # Debut de calcul des dates utiles pour chaque evenements reference
    # ============================================================================

    # Supression des lignes avec des NAT
    df_travail = df_travail.dropna(subset=[col_date_event_start, col_date_event_end, col_date_event_raise])

    # Definition des variables de travail

    output = pd.DataFrame()



    # to force keeping all column to output df
    if keep_all_variables:
        repere_sortie=list(df_travail.columns)
    else:
        if isinstance(liste_col_equ, list):
            repere_sortie = [col_event_id] + liste_col_equ
        else:
            repere_sortie = [col_event_id, liste_col_equ]
    # to ensure compatibility with both V1 and V3
    if 'index' in repere_sortie:
        repere_sortie.remove('index')

    # Comme toujours sur un nouveau groupe devent .. ( ici indx=0 car on est au debut)

    # Creation de la ligne fictive de naissance
    ref_row = df_travail.iloc[[0]].reset_index().drop('index', 1)
    ref_row.loc[0, col_state_after_event] = state_list[0]  # evenement de ref sur la frontière gauche a toujour  ref 0
    ref_row.loc[0, col_date_event_raise] = date_min
    ref_row.loc[0, col_date_event_start] = date_min
    ref_row.loc[0, col_date_event_end] = date_min
    ref_row.loc[0, col_type_maint] = 'fictive MES'

    # init de la ligne de travail
    tmp_row = ref_row[repere_sortie].copy()
    tmp_row.loc[0, 'ref_state'] = state_list[0]  # par defaut sur le premier event dun groupe
    wo_subref = 0  # servira attribuer un unique WO pour les lignes crée relative a un meme

    if col_mes is None:
        col_mes_existante = False
        tmp_row.loc[0, 'date_last_prev'] = date_null
        tmp_row.loc[0, 'date_first_current'] = date_min
    else:
        col_mes_existante = True
        date_mes = ref_row.at[0, col_mes]
        tmp_row.loc[0, 'date_last_prev'] = date_mes
        tmp_row.loc[0, 'date_first_current'] = date_mes

    ta_boucle = int(len(df_travail) / 1)

    # Debut du balayage de la GMAO

    for i in range(0, ta_boucle):
        active_row = df_travail.iloc[[i]].reset_index().drop('index', 1)
        if i % int(ta_boucle / 1) == 0:
            print('pourcentage effectué', int((i / ta_boucle) * 100), '%')

        # test de changement dequipement
        if isinstance(liste_col_equ, list):
            test_chgt_equ = not ((active_row.loc[0][liste_col_equ]).equals(ref_row.loc[0][liste_col_equ]))
        else:
            test_chgt_equ = active_row.at[0, liste_col_equ] != ref_row.at[0, liste_col_equ]

        if test_chgt_equ:
            # print('detection dun changement dequipement')
            # Cloture de levenement precedent avec censure a droite puis enregistrement

            # tmp_row.loc[0, 'date_last_current'] = ref_row.at[0, col_date_event_end]
            tmp_row.loc[0, 'date_last_current'] = date_max
            tmp_row.loc[0, 'date_first_next'] = date_null
            tmp_row.loc[0, 'event_info'] = 'right_censure'
            tmp_row.loc[0, col_cat_maint] = 'hs'
            tmp_row.loc[0, col_type_maint] = 'hs'
            tmp_row.loc[0, 'unique_id'] = str(tmp_row.loc[0, col_event_id]) + '_' + str(wo_subref)
            if col_mdd:
                tmp_row[col_mdd] = 'hs'  # Ajout du mdd de cloture devent

            # print('affichage de temp row avant insertion', tmp_row)

            output = output.append(tmp_row, sort=True)  # ajout de l'event dans la sortie
            wo_subref = 0
            # Initialisation du nouvel event
            ref_row = active_row.copy()  # on recopie la cle equipement
            ref_row.loc[0, col_state_after_event] = state_list[0]  # On crée le ref row en figeant l'état 0
            ref_row.loc[0, col_date_event_raise] = date_min  # On crée le ref row en figeant l'état 0
            ref_row.loc[0, col_date_event_start] = date_min  # On crée le ref row en figeant l'état 0
            ref_row.loc[0, col_date_event_end] = date_min  # On crée le ref row en figeant l'état 0
            ref_row.loc[0, col_type_maint] = 'fictive MES'
            tmp_row = active_row[repere_sortie].copy()  # pour avoir la bonne localisation equ

            # Preparation de la prochaine ligne tmp row
            if col_mes_existante:
                date_mes = ref_row.at[0, col_mes]
                tmp_row.loc[0, 'date_last_prev'] = date_mes
                tmp_row.loc[0, 'date_first_current'] = date_mes
            else:
                tmp_row.loc[0, 'date_last_prev'] = date_null
                tmp_row.loc[0, 'date_first_current'] = date_min

            tmp_row.loc[0, 'ref_state'] = state_list[0]

        # Deroule classique du calcul
        diff_state = state_list.index(active_row.at[0, col_state_before_event]) - state_list.index(
            ref_row.at[0, col_state_after_event])
        # print('affichage du diff state')
        # print(diff_state)
        if diff_state == 0:
            if active_row.at[0, col_type_maint] != 'CTRL':  # levent est censuré puisque coupe par une REMP ou REP

                # Completion puis enregistrement de la ligne (event censuré)

                tmp_row.loc[0, 'date_last_current'] = active_row.at[0, col_date_event_start]
                tmp_row.loc[0, 'date_first_next'] = date_null
                state_before = active_row.at[0, col_state_before_event]
                state_after = active_row.at[0, col_state_after_event]
                tmp_row.loc[0, 'event_info'] = 'transition_' + state_before + '->' + state_after
                tmp_row.loc[0, col_cat_maint] = active_row.at[0, col_cat_maint]
                tmp_row.loc[0, col_type_maint] = active_row.at[0, col_type_maint]
                tmp_row.loc[0, 'unique_id'] = str(tmp_row.loc[0, col_event_id]) + '_' + str(wo_subref)
                wo_subref += 1
                if col_mdd:
                    tmp_row[col_mdd] = active_row.at[0, col_mdd]  # Ajout du mdd de cloture devent
                # print('affichage de temp row avant insertion', tmp_row)
                output = output.append(tmp_row, sort=True)  # ajout de l'event dans la sortie

                # init da la nouvelle ligne temp
                tmp_row = active_row[repere_sortie]
                tmp_row.loc[0, 'date_last_prev'] = active_row.at[0, col_date_event_end]
                tmp_row.loc[0, 'date_first_current'] = active_row.at[0, col_date_event_end]
                tmp_row.loc[0, 'ref_state'] = active_row.at[0, col_state_after_event]
                ref_row = active_row

            # Sinon la ligne active  est une ligne de transfert donc extensoin du TS donc ref_row invariant.

            else:
                tmp_row.loc[0, 'date_last_current'] = active_row.at[0, col_date_event_end]
                ref_row = active_row

        elif diff_state == 1:

            if active_row.at[0, col_type_maint] == 'CTRL':  # Cas d'un changement detat sans defaut

                # Completion de la ligne avant sauvegarde dans la sortie
                tmp_row.loc[0, 'date_last_current'] = ref_row.at[0, col_date_event_end]
                tmp_row.loc[0, 'date_first_next'] = active_row.at[0, col_date_event_start]
                tmp_row.loc[0, col_cat_maint] = active_row.at[0, col_cat_maint]
                tmp_row.loc[0, col_type_maint] = active_row.at[0, col_type_maint]
                state_before = ref_row.at[0, col_state_after_event]
                state_after = active_row.at[0, col_state_before_event]
                tmp_row.loc[0, 'event_info'] = 'transition_' + state_before + '->' + state_after
                tmp_row.loc[0, 'unique_id'] = str(tmp_row.loc[0, col_event_id]) + '_' + str(wo_subref)
                wo_subref += 1
                if col_mdd:
                    tmp_row.loc[0, col_mdd] = 'hs'
                # print('enregistrement de la ligne ref  par CTRL')
                # print(tmp_row)
                output = output.append(tmp_row, sort=True)  # ajout de l'event dans la sortie

                # init da la nouvelle ligne temp
                tmp_row = active_row[repere_sortie].copy()
                tmp_row.loc[0, 'date_last_prev'] = ref_row.at[0, col_date_event_end]
                tmp_row.loc[0, 'date_first_current'] = active_row.at[0, col_date_event_start]
                tmp_row.loc[0, 'ref_state'] = active_row.at[0, col_state_after_event]
                ref_row = active_row
            else:  # avec une rep ou remp avec changement detat

                # Enregistrement de la ligne devent sur letat precedent

                if ref_row.at[0, col_type_maint] == 'fictive MES':  # Pour doha et eviter davoir des TS = 0
                    tmp_row.loc[0, 'date_last_current'] = active_row.at[0, col_date_event_raise]
                else:
                    tmp_row.loc[0, 'date_last_current'] = active_row.at[0, col_date_event_raise]

                tmp_row.loc[0, 'date_first_next'] = active_row.at[0, col_date_event_raise]
                tmp_row.loc[0, col_cat_maint] = 'hs'
                tmp_row.loc[0, col_type_maint] = 'hs'
                state_before = ref_row.at[0, col_state_after_event]
                state_after = active_row.at[0, col_state_before_event]
                tmp_row.loc[0, 'event_info'] = 'transition_' + state_before + '->' + state_after
                tmp_row.loc[0, 'unique_id'] = str(tmp_row.loc[0, col_event_id]) + '_' + str(wo_subref)
                wo_subref += 1
                if col_mdd:
                    # print('active_row mdd3',active_row.at[0, col_mdd])
                    tmp_row.loc[0, col_mdd] = active_row.at[0, col_mdd]  # Ajout du mdd de cloture devent
                # print('enregistrement de la ligne ref  par rep')
                # print(tmp_row)

                output = output.append(tmp_row, sort=True)  # ajout de l'event dans la sortie

                # enregisterment de la ligne relative a letat degrade avant reparation

                tmp_row = active_row[repere_sortie].copy()
                tmp_row.loc[0, 'ref_state'] = active_row.at[0, col_state_before_event]
                tmp_row.loc[0, 'date_last_prev'] = active_row.at[0, col_date_event_raise]
                tmp_row.loc[0, 'date_first_current'] = active_row.at[0, col_date_event_raise]
                tmp_row.loc[0, 'date_last_current'] = active_row.at[0, col_date_event_start]
                tmp_row.loc[0, 'date_first_next'] = date_null
                tmp_row.loc[0, col_cat_maint] = active_row.at[0, col_cat_maint]
                tmp_row.loc[0, col_type_maint] = active_row.at[0, col_type_maint]
                tmp_row.loc[0, 'event_info'] = 'right_censure'
                tmp_row.loc[0, 'unique_id'] = str(tmp_row.loc[0, col_event_id]) + '_' + str(wo_subref)
                wo_subref += 1
                if col_mdd:
                    # print('active_row mdd3',active_row.at[0, col_mdd])
                    tmp_row.loc[0, col_mdd] = active_row.at[0, col_mdd]  # Ajout du mdd de cloture devent
                output = output.append(tmp_row, sort=True)  # ajout de l'event dans la sortie
                # Enregistrement de l event reparation (on pourrait rajouter letat sur lequel on repare par la suite

                tmp_row = active_row[repere_sortie].copy()
                tmp_row.loc[0, 'ref_state'] = active_row.at[
                    0, col_state_before_event]  # On considerera qu'il sagit de letat reparation.
                tmp_row.loc[0, 'ref_state'] = active_row.at[
                    0, col_type_maint]  # pour DOHA (on indifferencie REMP de REP dans ce cas)
                tmp_row.loc[0, 'date_last_prev'] = active_row.at[0, col_date_event_start]
                tmp_row.loc[0, 'date_first_current'] = active_row.at[0, col_date_event_start]
                tmp_row.loc[0, 'date_last_current'] = active_row.at[0, col_date_event_end]
                tmp_row.loc[0, 'date_first_next'] = active_row.at[0, col_date_event_end]
                tmp_row.loc[0, col_cat_maint] = active_row.at[0, col_cat_maint]
                tmp_row.loc[0, col_type_maint] = active_row.at[0, col_type_maint]
                tmp_row.loc[0, 'event_info'] = 'Repair'
                tmp_row.loc[0, 'unique_id'] = str(tmp_row.loc[0, col_event_id]) + '_' + str(wo_subref)
                wo_subref += 1
                if col_mdd:
                    # print('testmdd2',active_row.at[0, col_mdd])
                    tmp_row[col_mdd] = active_row.at[0, col_mdd]  # Ajout du mdd associé a la Repair
                # print('enregistrement de la ligne ref  SUR REP')
                # print(tmp_row)
                output = output.append(tmp_row, sort=True)  # ajout de l'event dans la sortie

                # initialisation de la ligne devent suivante

                tmp_row = active_row[repere_sortie].copy()
                tmp_row.loc[0, 'ref_state'] = active_row.at[0, col_state_after_event]
                tmp_row.loc[0, 'date_last_prev'] = active_row.at[0, col_date_event_end]
                tmp_row.loc[0, 'date_first_current'] = active_row.at[0, col_date_event_end]
                ref_row = active_row
        else:
            print('Saut detat detecte, cas non gere pour l instant')
            sys.exit(0)
    #     print('sortie calculée')
    # Crée un index unique par ligne
    output = output.set_index('unique_id')

    # Rajout deux colonnes specifiques pour DOHA

    output['datetime_start'] = output['date_first_current']
    output['datetime_end'] = output['date_last_current']
    print('resultat final')
    print(output)
    print(output.columns)
    return output


def compute_sj_from_dates(cmms_df, backend_db,
                          col_date_last_prev, col_date_first_current, col_date_last_current, col_date_first_next,
                          col_id, col_event_info, col_datetime_start, col_datetime_end,
                          col_ref_state, service_duration_proportion=1,
                          col_equ_cmms=None, type_unit='elem', unit='defaut', cycle_name=None,
                          min_time=0, db_cycles_name=None):  # user param
    """Fonctions rajoutant dans une gmao quelconque déjà munie des 4 dates, Les TS min et max associé à chaque ligne
     soit dans une unité elementaire soit dans une unite particulière en utilisant un df de serie temporelle.

    Paramètres obligatoires:

        gmao_df : Df contenant la gmao
        type_unite : Type dunite choisie, 'elem' ou autre' (par defaut en 'elem')
        unite : Unite choisie, pour les unites elementaires (a : année,j : jour, m, mois, min : minutes, defaut: en
        jour min heure)
        capteurs_df : Df contenant les series temporelles de sollicitation

     Paramètres optionnels : (car obligatoires seulement dans le cas d'unité non elementaires)

        capteurs_df : df contenant les sollicitations des equipements
        col_equ_gmao : Colonne contenant les identifiant dequipement dans gmao_df
                       (cette col doit etre à la meme echelle que celle ayant servie a generer les 4 dates)
        col_equ_capteurs : Colonne contenant les id d'equipement dans capteurs_df"
        col_time : col dans capteurs_df contenant les instants de sollicitations
        ref_event_state : evenement de ref choisi pour calcules les TS, (defini de le fichier de paramétrage
                          utile uniquement pour des unites non elementaires)
        min_time : temps minimal entre deux evenements de ref   (utile uniquement pour des unites non elementaires
    """
    # Verifiation sur lidentifiant de connection au backend

    print('backend db',backend_db)
    print('nom source ST', db_cycles_name)
    # Levent de ref sera l unite mise en paramètre , par exemple : Opening

    ref_event_state = unit

    # Les valeurs inconnues correspondent aux dates 2200-1-1
    date_null = pd.Timestamp(2200, 1, 1, 1)
    delta_max = np.datetime64('NaT') - np.datetime64('NaT')

    # Lecture de la gmao augmentée des 4 dates dencadrement
    df_travail = cmms_df.copy()

    # Creation de la colonne censure

    df_travail['inf_censor'] = (df_travail[col_date_last_prev] == date_null) | \
                               (df_travail[col_date_first_next] == date_null)

    # nouveau systeme : ensure=True si la largeur de l intervalle dencadrement est non nulle.
    df_travail['censor'] = (df_travail[col_date_last_current] - df_travail[col_date_first_current] !=
                            df_travail[col_date_first_next] - df_travail[col_date_last_prev])

    if type_unit == 'elem':  # Dasn ce cas calcul direct
        print('unite elementaire', unit)

        if cycle_name is None:
            cycle_name = unite
        TS_min = 'NC_min_' + cycle_name
        TS_max = 'NC_max_' + cycle_name

        df_travail[TS_min] = df_travail[col_date_last_current] - df_travail[col_date_first_current]
        df_travail[TS_max] = df_travail[col_date_first_next] - df_travail[col_date_last_prev]

        # Correction dans les cas censure on met NAT
        df_travail[TS_max] = np.where(df_travail['inf_censor'], delta_max, df_travail[TS_max])

        # Suppression des valeurs negative ou nulles

        null_value = pd.isna(df_travail[TS_min]) & pd.isna(df_travail[TS_max])
        df_travail = df_travail[~null_value]
        negative_value = df_travail[TS_min] < datetime.timedelta(0)
        df_travail = df_travail[~negative_value]
        # reset des index pour test

        print('convesrion des unites')

        # Conversion dans l'unite choisie

        if unit != 'defaut':
            df_travail[TS_min] = df_travail[TS_min].apply(lambda x: x.total_seconds())
            df_travail[TS_max] = df_travail[TS_max].apply(lambda x: x.total_seconds())
            if unit == 'sec':
                df_travail[TS_min] = df_travail[TS_min] / 1
                df_travail[TS_max] = df_travail[TS_max] / 1
            elif unit == 'min':
                df_travail[TS_min] = df_travail[TS_min] / 60
                df_travail[TS_max] = df_travail[TS_max] / 60
            elif unit == 'h':
                df_travail[TS_min] = df_travail[TS_min] / 3600
                df_travail[TS_max] = df_travail[TS_max] / 3600
            elif unit == 'j':
                df_travail[TS_min] = df_travail[TS_min] / (3600 * 24)
                df_travail[TS_max] = df_travail[TS_max] / (3600 * 24)
            elif unit == 'a':
                df_travail[TS_min] = df_travail[TS_min] / (3600 * 24 * 365)
                df_travail[TS_max] = df_travail[TS_max] / (3600 * 24 * 365)
            else:
                raise ValueError(' erreur : unit {0} is not recognized'.format(unit))

        # Prise en compte du coeff pondere par la durée de mise en service

        df_travail[TS_min] = np.where(df_travail['ref_state'] != -1, df_travail[TS_min] * (service_duration_proportion),
                                      df_travail[TS_min])
        df_travail[TS_max] = np.where(df_travail['ref_state'] != -1, df_travail[TS_max] * (service_duration_proportion),
                                      df_travail[TS_max])

    else:  # choix dune unité alternative necessitant une ST
        print('cas des unites specifique pas encore code, necessite une ST')
        # Verification de la presence de données obligatoires

        # if capteurs_df is None: #Remplacer par un test dexistance de db_capteur_name dans la base mongo
        #    raise ValueError('erreur : un db capteurs est requis pour calculer les TS dans une unité non elementaoire')

        if ref_event_state is None:
            raise ValueError('erreur : Levenement de reference n a pas ete definit dans le parametrage : la conversion'
                             'en une unite non elementaire est donc impossible')

        # importation des meta donnees, il faudra une requete mongo pour ca

        if isinstance(col_equ_cmms, list):
            equ_lvl = len(col_equ_cmms)
        else:
            equ_lvl = 1

        if backend_db == "unused":
            print('error :sensor_data ds name has not been set')
            sys.exit()

        meta_dict = list(backend_db['app_meta'].find({}))[0]['sources'][db_cycles_name]
        # Recupdes noms de colonnes

        # col_equ_capteurs= col_equ_cmms
        liste_col_equ = ["level-" + str(i) for i in range(1, equ_lvl + 1)]

        col_equ_capteurs = em_deep.th_get_var(meta_dict, ["system", liste_col_equ], one_var_as_list=True)
        col_event_start = em_deep.th_get_var(meta_dict, 'event_start')
        col_event_end = em_deep.th_get_var(meta_dict, 'event_end')
        col_duration = em_deep.th_get_var(meta_dict, 'event_duration')
        col_ref_event = em_deep.th_get_var(meta_dict, 'event_ref')

        # Modif  temporaire pour DOHA  pour que ca marche avec la V2

        col_equ_capteurs = ['STATION_ID', 'SIDE', 'DEVICE NO']
        col_event_start = ['datetime_start']
        col_event_end = ['datetime_end']
        col_duration = ['duration']
        col_ref_event = ['event']

        print('liste des colonnes equipements', col_equ_capteurs)
        if cycle_name is None:
            cycle_name = "_".join(unite)
        TS_min = 'NC_min_' + cycle_name
        TS_max = 'NC_max_' + cycle_name

        # Preparation

        mongo_db_capteurs = backend_db[db_cycles_name]
        # init de la sortie
        df_travail = cmms_df.sort_values(by=col_equ_cmms).reset_index()
        df_travail[TS_min] = 0
        df_travail[TS_max] = 0
        df_travail['censor'] = (df_travail[col_date_last_prev] == date_null) | \
                               (df_travail[col_date_first_next] == date_null)

        # prepa de la boucle

        ta_boucle = int(len(df_travail) / 1)
        ref_row = df_travail.iloc[[0]].reset_index().drop('index', 1)
        list_equ_actif = list(ref_row[col_equ_capteurs].iloc[0])  # extract de la loc equ a chercher dans capteurs_df
        # print('test liste equ actif',list_equ_actif)
        # Importation initiale

        # Creation du filtre mongo :

        filter_value = [str(x) for x in list_equ_actif]  # conversion pour eviter bug encoding

        if not (isinstance(filter_value, list)):
            filter_value = [filter_value]

        dico_filtre = dict(zip(col_equ_capteurs, filter_value))
        capteurs_tmp = pd.DataFrame(list(mongo_db_capteurs.find(dico_filtre)))
        print(dico_filtre)
        print(capteurs_tmp)

        # Balayage de la Gamo pour mise a jour successive

        for i in range(0, ta_boucle):
            # print('traitement ligne ', i, ' sur ',ta_boucle )
            active_row = df_travail.iloc[[i]].reset_index().drop('index', 1)
            # print('active_row', active_row)
            #
            if isinstance(col_equ_cmms, list):
                test_chgt_equ = not (active_row.loc[0][col_equ_cmms]).equals((ref_row.loc[0][col_equ_cmms]))
            else:
                test_chgt_equ = active_row.at[0, col_equ_cmms] != ref_row.at[0, col_equ_cmms]

            # Mise a jour du plc de reference
            if test_chgt_equ:
                # Remise a jour du plc correspondant
                ref_row = active_row
                list_equ_actif = list(
                    ref_row[col_equ_capteurs].iloc[0])  # extract de la loc equ a chercher dans capteurs_df
                filter_value = [str(x) for x in list_equ_actif]  # conversion pour eviter bug encoding
                dico_filtre = dict(zip(col_equ_capteurs, filter_value))
                capteurs_tmp = pd.DataFrame(list(mongo_db_capteurs.find(dico_filtre)))
                # print(dico_filtre)
                # print(capteurs_tmp)
            # Calcule du temps de sejour

            if len(capteurs_tmp) != 0:
                # TS min
                date_min = active_row[col_date_first_current][0]
                date_max = active_row[col_date_last_current][0]
                # print( 'les deux dates',date_min,date_max)
                # print('capteur init')
                # print(capteurs_tmp)
                row_to_keep_min = capteurs_tmp[col_event_start[0]] >= date_min
                row_to_keep_max = capteurs_tmp[col_event_end[0]] <= date_max

                df_temp = capteurs_tmp.loc[row_to_keep_min & row_to_keep_max]
                # print('capteur filtre par dates')
                # print(df_temp)
                df_temp = df_temp[df_temp[col_ref_event].isin(unit)]

                tmp_min = df_temp[
                              col_duration] < min_time  # car le duration et mintime sont donnés par nature en secondes
                df_temp = df_temp[~tmp_min]
                # print('temps de sejour min trouve',len(df_temp))
                df_travail[TS_min].iloc[i] = len(df_temp)

                # TS max

                date_min = active_row[col_date_last_prev][0]
                date_max = active_row[col_date_first_next][0]

                if (date_min == date_null) or (date_max == date_null):
                    row_to_keep_min = True
                    df_travail[TS_max].iloc[i] = np.nan
                else:
                    row_to_keep_min = capteurs_tmp[col_event_start[0]] >= date_min
                    row_to_keep_max = capteurs_tmp[col_event_end[0]] <= date_max
                    df_temp = capteurs_tmp.loc[row_to_keep_min & row_to_keep_max]

                    df_temp = df_temp[df_temp[col_ref_event].isin(unit)]
                    tmp_min = df_temp[
                                  col_duration] < min_time  # car le duration et mintime sont donnés par nature en secondes
                    df_temp = df_temp[~tmp_min]
                    df_travail[TS_max].iloc[i] = len(df_temp)
                    # print('temps de sejour max trouve', len(df_temp))
            else:
                df_travail[TS_min].iloc[i] = np.nan
                df_travail[TS_max].iloc[i] = np.nan

        # Supression des valeurs negative ou nulles

        null_value = pd.isna(df_travail[TS_min]) & pd.isna(df_travail[TS_max])
        # df_travail = df_travail[~null_value]
        negative_value = df_travail[TS_min] < 0
        df_travail = df_travail[~negative_value]
        # reset des index pour test
        df_travail = df_travail.reset_index().drop('index', 1).set_index('unique_id')

    # print('resultat final')
    # print(df_travail)
    # print(df_travail.info())
    return df_travail


def extract_transitions(events_df,
                        event_start_specs,
                        event_end_specs):
    """
    Search events in dataframe caracterized by starting and ending properties.

    :param events_df: Data frame with a datetime index.
    :type events_df: pd.DataFrame
    :param event_start_specs: column/value pairs defining the starting event to lookup in the dataframe. 
    :type event_start_specs: dict
    :param event_end_specs: column/value pairs defining the ending event to lookup in the dataframe. 
    :type event_end_specs: dict

    :return: A dataframe containing each events found with starting date, ending date.
    :rtype: pd.DataFrame
    """

    # Extract starting transitions
    events_start_query = " and ".join(['`{}`.str.contains("{}")'.format(k, v) for
                                       k, v in event_start_specs.items()])
    events_start_df = events_df.query(events_start_query)

    # Extract ending transitions
    events_end_query = " and ".join(['`{}`.str.contains("{}")'.format(k, v) for
                                     k, v in event_end_specs.items()])
    events_end_df = events_df.query(events_end_query)

    # Merge starting and ending transitions
    events_seq_df = pd.concat([events_start_df, events_end_df],
                              axis=0) \
        .sort_index() \
        .reset_index() \
        .rename(columns={events_df.index.name: "datetime"})

    events_var = list(events_seq_df.columns)

    # Shift transitions
    events_seq_shift_df = events_seq_df.shift(-1)

    # Rename columns appropriately
    events_seq_df.rename(columns={v: v + '_start' for v in events_var},
                         inplace=True)
    events_seq_shift_df.rename(columns={v: v + '_end' for v in events_var},
                               inplace=True)

    # Put starting and ending transitions on the same row
    trans_tmp_df = pd.concat([events_seq_df, events_seq_shift_df],
                             axis=1)

    # Keep the correct transitions
    trans_start_query = " and ".join(['`{}_start`.str.contains("{}")'.format(k, v) for
                                      k, v in event_start_specs.items()])

    trans_end_query = " and ".join(['`{}_end`.str.contains("{}")'.format(k, v) for
                                    k, v in event_end_specs.items()])

    trans_query = " and ".join([trans_start_query, trans_end_query])

    trans_df = trans_tmp_df.query(trans_query)

    # Extract the final data
    return trans_df[["datetime_start", "datetime_end"]]


def apply_filter_from_dict(df, filter_dict):
    """   This function apply a filter_dict to the dataframe given as input
    1) It assume that each key of the dict is a col name
    2 )each column filter has 2 type of filter :
    - a list of value (even for one unique value it souhld be given as a list ex: { "OT_ID : ["456123"]}
    - an interval filter represented as a dict with pandas recognized keyword ex  {DATE_CREATION : {lte: 2012-02-25,  gte: 2028-06-02}}"""

    # Split interval filter , and values filter
    if bool(filter_dict):
        value_filter = {key: value for key, value in filter_dict.items() if isinstance(value, list)}
        interval_filter = {key: value for key, value in filter_dict.items() if isinstance(value, dict)}

        # Apply filter on values
        if bool(value_filter) :
            MASK = pd.DataFrame(
                {col_name: df[col_name].isin(value_filter[col_name]) for col_name in value_filter.keys()}).all(axis=1)
            df = df[MASK]

        #Apply on intervals
        if bool(interval_filter) :
            MASK2 = pd.DataFrame(
                {col_name: df[col_name].between(interval_filter[col_name]['gte'],
                                                interval_filter[col_name]['lte'] ,
                                                inclusive=True)
                           for col_name in interval_filter .keys()}).all(axis=1)
            df = df[MASK2]

    return df

