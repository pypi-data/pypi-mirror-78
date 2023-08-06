# %%
# %% [markdown]
# https://rasa.com/docs/rasa/api/custom-nlu-components/
# If you create a custom tokenizer you should implement the methods of rasa.nlu.tokenizers.tokenizer.Tokenizer. The train and process methods are already implemented and you simply need to overwrite the tokenize method. train and process will automatically add a special token __CLS__ to the end of list of tokens, which is needed further down the pipeline.

# %%
import re
import os
from typing import Any, Dict, List, Optional, Text, Union, Type

# %%
from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.nlu.components import Component
from rasa.nlu.featurizers.featurizer import SparseFeaturizer
from rasa.nlu.training_data import Message, TrainingData

from rasa.nlu.constants import TOKENS_NAMES, MESSAGE_ATTRIBUTES
from rasa.constants import DOCS_URL_TRAINING_DATA_NLU
from rasa.nlu.constants import (
    CLS_TOKEN,
    RESPONSE,
    SPARSE_FEATURE_NAMES,
    TEXT,
    TOKENS_NAMES,
    INTENT,
    MESSAGE_ATTRIBUTES,
    ENTITIES,
)

from rasa.nlu.config import RasaNLUModelConfig

import rasa.utils.io as io_utils
from rasa.nlu import utils
import rasa.utils.common as common_utils
from rasa.nlu.model import Metadata

# %%
from pyspace.nlp.preprocessing.normalizer.xnormalizer import xNormalizer

# %%
import copy
import pickle

import numpy as np
import scipy.sparse

import pytz
import datetime

try:
    import stanza
except:
    import_stanza = False
# %%

class EntityNormalization(Component):
    def __init__(self, component_config: Dict[Text, Any] = None,) -> None:
        super(EntityNormalization, self).__init__(component_config)

    def normalize(self, message, entities=[]):
    
        tokens = message.get(TOKENS_NAMES[TEXT])

        entities = sorted(entities, key=lambda e:e['start'])

        for token in tokens:
            
            for e in entities:
                startbool = token.start >= e['start']
                endbool = token.end <= e['end']

                if startbool and endbool:
                    
                    
                    if self.print_example_count != 0:

                        if token.text not in e['value']:
                            print('Token text is not in entity value.')

                            self.print_example_count -= 1

                            print(message.text)
                            print(token.text, token.start, token.end)
                            print(e)
                            print(entities)
                            print()

                    # assert token.text in e['value']
                    token.text = e['entity'] if 'role' not in e else e['entity'] + '-' +e['role']
                    token.lemma = token.text
                    ## TODO
                    ## if e['start'] != token.start:
                    ## ## e['entity].replace('B-', 'I-')

                    # {'entity': 'B-DURATION',
                    # 'start': 0,
                    # 'end': 1,
                    # 'role': 'YEAR',
                    # 'value': '1',
                    # 'extractor': 'DIETClassifierExtended'},
                    pass

        message.set(TOKENS_NAMES[TEXT], tokens)

    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):

        print('  train function')
        self.print_example_count = 5

        for message in training_data.training_examples:
            entities = message.get('norm_ent')
            self.normalize(message, entities)            

    def process(self, message: Message, **kwargs: Any):

        print('  process function')
        self.print_example_count = 0
        entities = message.get(ENTITIES, [])
        entities = [e for e in entities if e['extractor'] in ['DIETClassifierExtended', 'DIETClassifier']]
        self.normalize(message, entities)


class EntityManager(Component):

    defaults = {
        "priority_config": {},
    }

    def __init__(
        self,
        component_config: Dict[Text, Any] = None,
    ) -> None:
        super(EntityManager, self).__init__(component_config)
        
        self.priority_config = self.component_config["priority_config"]
        self.priority_config = { float(k):v for k,v in self.priority_config.items()}
        self.priority_config = [self.priority_config[i].split('___',1) for i in sorted (self.priority_config.keys())]

        print()
        print('Entity Priority List')
        print(self.priority_config)
        print()
        # tempcount = 6
        # for i in range(len(self.priority_config)//tempcount +1):
        #     print(self.priority_config[ i*tempcount: (i+1)*tempcount ])
        pass
        # self.mcmmapper = MCMEntityMapper()
        
    def process(self, message: Message, **kwargs: Any) -> None:
        """Process an incoming message."""

        if not self.priority_config:
            return

        intent = message.get(INTENT)['name']
        entities = message.get("entities", [])
        entities_updated = copy.deepcopy(entities)
        priority_config = copy.deepcopy(self.priority_config)
        
        ############################################################################
        ############################################################################
        ############################################################################
        ## update priority config for predicted intents

        if intent == 'foreign_currency_tr':
            te1 = ['DIETClassifierExtended', 'B-amount'] 
            te2 = ['DIETClassifierExtended', 'I-amount'] 
            if te1 in priority_config and te2 in priority_config:
                tempindex1 = max(priority_config.index(te1), priority_config.index(te2))

                
                teXlist = [['DucklingHTTPExtractor', 'amount-of-money'], ['DucklingHTTPExtractor', 'time'], ['DucklingHTTPExtractor', 'duration'] ]
                for teX in teXlist:
                    if teX in priority_config:
                        tempindexX = priority_config.index(teX)
                        if tempindex1 > tempindexX:
                            priority_config.remove(teX)
                            priority_config.insert(tempindex1, teX)

            else:
                pass
        
        ############################################################################
        ############################################################################
        ############################################################################

        def merge_entity_func(temp):

            if len(temp) == 1:
                return temp
                # merged_model_entities.append(temp[0])
            else:
                if all([ temp[i+1]['start'] - temp[i]['end'] <= 1 for i in range(len(temp)-1)]):
                    temp_value = message.text[temp[0]['start']:temp[-1]['end']]
                    temp_value_norm = xNormalizer.tr_normalize(temp_value).lower()
                    # if all( [xNormalizer.tr_normalize(tt['value']) in xNormalizer.tr_normalize(temp_value) for tt in temp]):
                    # if all([tt['value'] in temp_value for tt in temp]):
                    if all( [xNormalizer.tr_normalize(tt['value']).lower() in temp_value_norm for tt in temp]):
                        temp_copy = copy.deepcopy(temp)

                        temp[0]['value'] = temp_value
                        temp[0]['end'] = temp[-1]['end']
                        temp[0]['raw'] = temp_copy

                        return [temp[0]]
                        # merged_model_entities.append(temp[0])
                    else:
                        print()
                        print('Model entities are consecutive but not match with message. They are not merged.')
                        print(temp_value)
                        print(model_entities)
                        print(temp)
                        return temp
                        # merged_model_entities.extend(temp)

                else:
                    print()
                    print('Model entities are not consecutive. They are not merged.')
                    print(model_entities)
                    print(temp)
                    return temp
                    # merged_model_entities.extend(temp)


        ############################################################################
        ############################################################################
        ############################################################################
        ## DIET split entities - v0

        if False:
            other_entities = [e for e in entities_updated if e['extractor'] not in ['DIETClassifierExtended', 'DIETClassifier']]
            model_entities = [e for e in entities_updated if e['extractor'] in ['DIETClassifierExtended', 'DIETClassifier']]
            model_entities = sorted(model_entities, key=lambda x: x['start'])

            splitted_model_entities = []
            for e in model_entities:
                if e['entity'].startswith('B-'):
                    if e['entity'] == 'B-currency':
                        e['value'].split()

            entities_updated = splitted_model_entities + other_entities


        ############################################################################
        ############################################################################
        ############################################################################
        ## DIET merge entities - v1

        other_entities = [e for e in entities_updated if e['extractor'] not in ['DIETClassifierExtended', 'DIETClassifier']]
        model_entities = [e for e in entities_updated if e['extractor'] in ['DIETClassifierExtended', 'DIETClassifier']]
        model_entities = sorted(model_entities, key=lambda x: x['start'])

        merged_model_entities = []
        model_entities.append({'entity':'dummy', 'value':'dummy',})
        temp = []
        for e in model_entities:
            if temp == []:
                temp.append(e)
            else:
                if e['entity'].startswith('I-'):
                    temp.append(e)
                else:
                    merged_model_entities.extend(merge_entity_func(temp))        
                    temp = []
                    temp.append(e)


        entities_updated = merged_model_entities + other_entities

        ############################################################################
        ############################################################################
        ############################################################################
        ## DIET merge entities - v2

        other_entities = [e for e in entities_updated if e['extractor'] not in ['DIETClassifierExtended', 'DIETClassifier']]
        model_entities = [e for e in entities_updated if e['extractor'] in ['DIETClassifierExtended', 'DIETClassifier']]
        model_entities = sorted(model_entities, key=lambda x: x['start'])

        merged_model_entities = []
        model_entities.append({'entity':'dummy', 'value':'dummy',})
        temp = []
        for e in model_entities:
            if temp == []:
                temp.append(e)
            else:
                # if temp[-1]['entity'] in ['B-AMOUNT-OF-MONEY','I-AMOUNT-OF-MONEY', 'B-amount', 'I-amount'] and e['entity'] in ['B-currency']:
                if temp[-1]['entity'] in ['B-AMOUNT-OF-MONEY', 'B-amount',] and e['entity'] in ['B-currency']:
                    if 'role' in temp[-1] or 'role' in e:
                        try:
                            assert temp[-1]['role'] == e['role']
                            # merge B-AMOUNT-OF-MONEY/from and B-currency/from, and to-to pair.
                            temp.append(e)
                        except:
                            # do not merge B-AMOUNT-OF-MONEY/from and B-currency/to
                            merged_model_entities.extend(merge_entity_func(temp))        
                            temp = []
                            temp.append(e)
                    else:
                        # merge B-AMOUNT-OF-MONEY and B-currency
                        temp.append(e)
                else:
                    merged_model_entities.extend(merge_entity_func(temp))        
                    temp = []
                    temp.append(e)


        entities_updated = merged_model_entities + other_entities

        ############################################################################
        ############################################################################
        ############################################################################
        ## RegexEntityExtractor merge entities

        entities_updated = sorted(entities_updated, key=lambda x: x['start'])
        merged_entities_updated = []
        
        entities_updated.append({'entity':'dummy', 'value':'dummy',})
        
        temp = []
        for e in entities_updated:
            if temp == []:
                temp.append(e)
            else:
                if temp[-1]['entity'] in ['account'] and temp[-1]['extractor'] in ['RegexEntityExtractor'] and e['entity'] in ['account'] and e['extractor'] in ['RegexEntityExtractor']:
                    temp.append(e)
                elif temp[-1]['entity'] in ['<num>'] and temp[-1]['extractor'] in ['RasaSpacyTokenizer'] and e['entity'] in ['B-currency'] and e['extractor'] in ['DIETClassifierExtended', 'DIETClassifier']:
                    temp.append(e)
                else:
                    merged_entities_updated.extend(merge_entity_func(temp))        
                    temp = []
                    temp.append(e)


        entities_updated = merged_entities_updated
        ############################################################################
        ############################################################################
        ############################################################################
        ## SORT WITH PRIORITY
        ## KEEP AT LAST IF NOT IN PRIORITY

        temp = []
        tempothers = []
        tempdict = {}
        
        for eidx, entity in enumerate(entities_updated):
            tempdict[eidx] = False

        for priority_i in priority_config:
            for eidx, entity in enumerate(entities_updated):

                if [entity['extractor'], entity['entity']] == priority_i:
                    temp.append(entity)
                    tempdict[eidx] = True
                    
        for eidx, entity in enumerate(entities_updated):
            if not tempdict[eidx]:
                temp.append(entity)
                
        entities_updated = temp
        temp = []

        ############################################################################
        ############################################################################
        ############################################################################
        ## IF THERE ARE MORE THAN ONE MATCH FOR A TOKEN, SELECT THE FIRST ONE IN PRIORITY 
        ## AFTER FIRST ONE, KEEP IN OTHERS

        temp = []
        tempspan = []
        tempdict = {}
        
        for entity in entities_updated:
            ## NOTE if 22,25 in tempdict, and an entity with 16,28 comes, 16,28 stays
            overlapidx = -1
            if entity['start'] in tempdict:
                overlapidx = entity['start']
            elif entity['end']-1 in tempdict:
                overlapidx = entity['end']-1

            if overlapidx == -1:
                entity['others'] = []
                temp.append(entity)
                for idx in list(range(entity['start'],entity['end'])):
                    tempdict[idx] = entity
            else:
                tempdict[overlapidx]['others'].append(entity)

        # for entity in entities_updated:
        #     if not (entity['start'] in tempspan or entity['end'] in tempspan):
        #         temp.append(entity)
        #         tempspan.append(entity['start'])
        #         tempspan.append(entity['end'])

        entities_updated = temp
        temp = []

        ############################################################################
        ############################################################################
        ############################################################################

        # entities_updated = self.mcmmapper.process({'intent':message.get("intent", [])['name'], 'entities': entities_updated})
        message.set("entities", entities_updated, add_to_output=True)


class MCMEntityMapper(Component):

    def process(self, message: Message, **kwargs: Any) -> None:

        def generate_entity(etype, evalue_list):

            if etype in ['history_tr_DATE_SVP_', 'txnlist_tr_DATE_SVP_']:
                output = []
                for evalue in evalue_list:
                    temp = xNormalizer.tr_normalize(evalue).lower()

                    
                    if 'son' in temp:
                        date_type = 'until_now'
                    elif 'gecen' in temp:
                        date_type = 'one_before'
                    elif 'once' in temp:
                        date_type = 'n_before'
                    else:
                        date_type = 'until_now'

                    if 'ay' in temp:
                        date_dim = 'M'
                    elif 'gun' in temp:
                        date_dim = 'D'
                    elif 'yil' in temp:
                        date_dim = 'Y'
                    else:
                        date_dim = 'M'

                    date_dur = 'unknown'
                    for t in temp:
                        try:
                            date_dur = int(t)
                            break
                        except:
                            pass

                    if date_dur == 'unknown':
                        date_dur = 3

                        
                    datetime.datetime.strptime('2018', '%Y')# m d Y   H M S   
                    datetime.date.today() - datetime.timedelta(days=1)

                    if date_type == 'until_now':
                        end_date = datetime.datetime.now(tz=pytz.timezone("Europe/Istanbul"))
                        r = {'Y':0, 'M':0, 'D':0}
                        r[date_dim] = date_dur

                        # TODO TODO
                        if end_date.day - r['D'] < 1:
                            r['D'] = 0


                        start_date = end_date.replace(year=end_date.year - r['Y'],month=end_date.month - r['M'], day=end_date.day - r['D'])
                        
                        end_date = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
                        start_date = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
                        duration = f'P{date_dur}{date_dim}'
                        
                        output.append( {
                                'startDate': start_date, 
                                'endDate': end_date, 
                                'type': 'DURATION', 
                                'period': duration, 
                                'tokens': evalue})
                        
                    elif date_type == 'one_before':
                        today = datetime.datetime.now(tz=pytz.timezone("Europe/Istanbul"))
                        if date_dim == 'Y':
                            end_date = datetime.datetime(year=today.year,month=1,day=1)
                            start_date = datetime.datetime(year=today.year-date_dur,month=1,day=1)
                        elif date_dim == 'M':
                            end_date = datetime.datetime(year=today.year,month=today.month,day=1)
                            start_date = datetime.datetime(year=today.year,month=today.month-date_dur,day=1)
                        elif date_dim == 'D':
                            end_date = datetime.datetime(year=today.year,month=today.month,day=today.day)
                            start_date = datetime.datetime(year=today.year,month=today.month,day=today.day-date_dur)
                            
                        end_date = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
                        start_date = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
                        duration = f'P{date_dur}{date_dim}'
                        
                        
                        output.append( {
                                'startDate': start_date, 
                                'endDate': end_date, 
                                'type': 'DURATION', 
                                'period': duration, 
                                'tokens': evalue})   
                    elif date_type == 'n_before':
                        today = datetime.datetime.now(tz=pytz.timezone("Europe/Istanbul"))
                        if date_dim == 'Y':
                            end_date = datetime.datetime(year=today.year-date_dur+1,month=1,day=1)
                            start_date = datetime.datetime(year=today.year-date_dur,month=1,day=1)
                        elif date_dim == 'M':
                            end_date = datetime.datetime(year=today.year,month=today.month-date_dur+1,day=1)
                            start_date = datetime.datetime(year=today.year,month=today.month-date_dur,day=1)
                        elif date_dim == 'D':
                            end_date = datetime.datetime(year=today.year,month=today.month,day=today.day-date_dur+1)
                            start_date = datetime.datetime(year=today.year,month=today.month,day=today.day-date_dur)
                            
                        end_date = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
                        start_date = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
                        duration = f'P{date_dur}{date_dim}'
                        
                        
                        output.append( {
                                'startDate': start_date, 
                                'endDate': end_date, 
                                'type': 'DURATION', 
                                'period': duration, 
                                'tokens': evalue})

                return output

            elif etype in ['history_tr_MODIFIER_SVP__MOD_TR_', 'txnlist_tr_MODIFIER_SVP__MOD_TR_']:
                output = []

                for evalue in evalue_list:
                    temp = xNormalizer.tr_normalize(evalue).lower()

                    if temp in ['en fazla', 'en cok', 'encok', 'en yuksek','en pahali']:
                        output.append({'value': 'MAX'})
                    elif temp in ['en az', 'en dusuk', 'en ucuz']:
                        output.append({'value': 'MIN'})
                    elif temp == 'ortalama':
                        output.append({'value': 'AVG'})
                    elif 'harca' in temp or 'alisveris' in temp:
                        output.append({'value': 'SPEND'})
                
                return output
                    
            else:
                return {
                            'slot': etype,
                            'raw_value': evalue_list,
                            'visual': f"{evalue_list}",
                            'speakable': f"{evalue_list}",
                        }

        def backup_condition(e):

            ## TODO Check suffixes of B-HESAP-X entity for from account. 
            if e['entity'] == 'B-HESAP-X':
                return e['value'] in ['hesabimda', 'hesabımda','hesabimdan', 'hesabımdan', 'hesabimdaki', 'hesabımdaki', 'hesapta', 'hesaptan', 'hesaptaki', ]
            else:
                return False
        ner_intents = [
            'account_tr',
            'credit_card_tr',
            'cash_advance_tr',
            'credit_card_payment_tr',
            'foreign_currency_tr',
            'transfer_money_tr',

            'loan_application_tr',
            'term_deposit_calculation_tr',

            'bill_payment_tr',

            'history_tr',
            'txnlist_tr',

            'spendadvice_tr',
            'campaign_tr',

            'inform',
            ]

        intent = message.get(INTENT)
        entities = message.get(ENTITIES, [])

        if intent not in ner_intents or intent == 'inform':
            pass
        elif intent == 'account_tr':
            
            ############################
            ## MCM EXPECTED ENTITIES
            ############################
            val = ['_TYPE_', ]

            ############################
            ## OUTPUT CONTROL BOOLEANS
            ############################
            checks ={'_TYPE_':False, }

            
            ############################
            ## OUTPUT VARIABLE
            ############################
            output = {'_TYPE_':[], }
            
            ############################
            ## MAIN ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'DucklingHTTPExtractor':
                    pass
                elif e['extractor'] in  ['DIETClassifierExtended', 'DIETClassifier']:
                    if e['entity'] == 'B-account':
                        output['_TYPE_'].append(e['value'])
                        checks['_TYPE_'] = True
                    elif e['entity'] == 'B-sube':
                        output['_TYPE_'].append(e['value'])
                        checks['_TYPE_'] = True
                    elif e['entity'] == 'B-currency':
                        output['_TYPE_'].append(e['value'])
                        checks['_TYPE_'] = True


            ############################
            ## BACKUP ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'RegexEntityExtractor':
                    if not checks['_TYPE_'] and e['entity'] == 'account':
                        output['_TYPE_'].append(e['value'])
                    
                elif e['extractor'] in  ['DIETClassifierExtended', 'DIETClassifier']:
                    if not checks['_TYPE_'] and e['entity'] == 'B-HESAP-X': # and backup_condition(e) # Not needed in this intent.
                        output['_TYPE_'].append(e['value'])

            
            [output.pop(k) for k in list(output.keys()) if output[k] == []]
            entities = output
            # entities = [generate_entity(k, output[k]) for k in output if output[k] != []]
            
        elif intent == 'credit_card_tr':
            
            
            ############################
            ## MCM EXPECTED ENTITIES
            ############################
            val = ['_TYPE_', ]

            ############################
            ## OUTPUT CONTROL BOOLEANS
            ############################
            checks ={'_TYPE_':False, }

            
            ############################
            ## OUTPUT VARIABLE
            ############################
            output = {'_TYPE_':[], }
            
            ############################
            ## MAIN ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'DucklingHTTPExtractor':
                    pass
                elif e['extractor'] in  ['DIETClassifierExtended', 'DIETClassifier']:
                    if e['entity'] in ['B-account', 'B-cardtype', 'B-CARDTYPE']:
                        
                        if re.match('kredi kart', xNormalizer.tr_normalize(e['value']).lower()):
                            continue

                        output['_TYPE_'].append(e['value'])
                        checks['_TYPE_'] = True
                    elif e['entity'] in ['B-currency']:
                        output['_TYPE_'].append(e['value'])
                        checks['_TYPE_'] = True

            ############################
            ## BACKUP ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'RegexEntityExtractor':
                    if not checks['_TYPE_'] and e['entity'] == 'account':
                        
                        if re.match('kredi kart', xNormalizer.tr_normalize(e['value']).lower()):
                            continue

                        output['_TYPE_'].append(e['value'])
                        
                elif e['extractor'] ==  'RasaSpacyTokenizer':
                    pass
                
                elif e['extractor'] in  ['DIETClassifierExtended', 'DIETClassifier']:
                    pass

            
            [output.pop(k) for k in list(output.keys()) if output[k] == []]
            entities = output
            # entities = [generate_entity(k, output[k]) for k in output if output[k] != []]
            
        elif intent == 'cash_advance_tr':
            
            
            ############################
            ## MCM EXPECTED ENTITIES
            ############################
            val = ['_CARD_TYPE_TR_', '_AMOUNT_TR_','_INSTALLMENT_TR_']

            ############################
            ## OUTPUT CONTROL BOOLEANS
            ############################
            checks ={'_CARD_TYPE_TR_':False, '_AMOUNT_TR_':False,'_INSTALLMENT_TR_':False}

            
            ############################
            ## OUTPUT VARIABLE
            ############################
            output = {'_CARD_TYPE_TR_':[], '_AMOUNT_TR_':[], '_INSTALLMENT_TR_':[] }
            
            ############################
            ## MAIN ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'DucklingHTTPExtractor':
                    
                    if e['entity'] == 'amount-of-money':
                        output['_AMOUNT_TR_'].append(e['text'])
                        checks['_AMOUNT_TR_'] = True

                elif e['extractor'] in  ['DIETClassifierExtended', 'DIETClassifier']:
                    # 'B-account' # kredi karti, vadesiz
                    if e['entity'] in ['B-cardtype', 'B-CARDTYPE']:
                        
                        if re.match('kredi kart', xNormalizer.tr_normalize(e['value']).lower()):
                            continue
                        output['_CARD_TYPE_TR_'].append(e['value'])
                        checks['_CARD_TYPE_TR_'] = True
                    elif e['entity'] in ['B-DATE-DURATION']:
                        tempinstallment = e['value']
                        tempinstallment = re.sub('taksit.*?($|\s)', '', tempinstallment).strip()
                        output['_INSTALLMENT_TR_'].append(tempinstallment)

                    elif e['entity'] in ['B-amount', 'B-AMOUNT-OF-MONEY']:
                        output['_AMOUNT_TR_'].append(e['value'])
                        checks['_AMOUNT_TR_'] = True

            ############################
            ## BACKUP ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'RegexEntityExtractor':                    
                    if not checks['_CARD_TYPE_TR_'] and e['entity'] == 'account':
                        
                        if re.match('kredi kart', xNormalizer.tr_normalize(e['value']).lower()):
                            continue
                        output['_CARD_TYPE_TR_'].append(e['value'])
                        
                elif e['extractor'] ==  'RasaSpacyTokenizer':
                    pass
                
                elif e['extractor'] in  ['DIETClassifierExtended', 'DIETClassifier']:
                    pass

            
            [output.pop(k) for k in list(output.keys()) if output[k] == []]
            entities = output
            # entities = [generate_entity(k, output[k]) for k in output if output[k] != []]
            
        elif intent == 'credit_card_payment_tr':
           
            ############################
            ## MCM EXPECTED ENTITIES
            ############################
            val = ['_CARD_TYPE_TR_', '_AMOUNT_TR_', '_PAYMENT_TYPE_TR_']

            ############################
            ## OUTPUT CONTROL BOOLEANS
            ############################
            checks ={'_CARD_TYPE_TR_':False, '_AMOUNT_TR_':False}

            
            ############################
            ## OUTPUT VARIABLE
            ############################
            output = {'_CARD_TYPE_TR_':[], '_AMOUNT_TR_':[], '_PAYMENT_TYPE_TR_':[] }
            
            ############################
            ## MAIN ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'DucklingHTTPExtractor':
                    
                    if e['entity'] == 'amount-of-money':
                        output['_AMOUNT_TR_'].append(e['text'])
                        checks['_AMOUNT_TR_'] = True

                elif e['extractor'] in  ['DIETClassifierExtended', 'DIETClassifier']:
                    if e['entity'] in ['B-account', 'B-cardtype', 'B-CARDTYPE']:

                        if re.match('kredi kart', xNormalizer.tr_normalize(e['value']).lower()):
                            continue
                        output['_CARD_TYPE_TR_'].append(e['value'])
                        checks['_CARD_TYPE_TR_'] = True

                    elif e['entity'] in ['B-TEXT-AMOUNT']:
                        output['_PAYMENT_TYPE_TR_'].append(e['value'])

            ############################
            ## BACKUP ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'RegexEntityExtractor':                    
                    if not checks['_CARD_TYPE_TR_'] and e['entity'] == 'account':
                        
                        if re.match('kredi kart', xNormalizer.tr_normalize(e['value']).lower()):
                            continue
                        output['_CARD_TYPE_TR_'].append(e['value'])
                        
                elif e['extractor'] ==  'RasaSpacyTokenizer':
                    pass
                
                elif e['extractor'] in  ['DIETClassifierExtended', 'DIETClassifier']:
                    pass

            
            [output.pop(k) for k in list(output.keys()) if output[k] == []]
            entities = output
            # entities = [generate_entity(k, output[k]) for k in output if output[k] != []]
                      
        elif intent == 'foreign_currency_tr':
            
            ############################
            ## MCM EXPECTED ENTITIES
            ############################
            
            val = ['_TARGET_AMOUNT_TR_', '_REF_AMOUNT_TR_', 
            '_BUY_TR_', '_SELL_TR_']

            
            ############################
            ## OUTPUT CONTROL BOOLEANS
            ############################
            checks ={'_TARGET_AMOUNT_TR_':False, '_REF_AMOUNT_TR_':False, }

            
            ############################
            ## OUTPUT VARIABLE
            ############################
            output = {'_TARGET_AMOUNT_TR_':[], '_REF_AMOUNT_TR_':[],
            '_BUY_TR_':[], '_SELL_TR_':[]}
            
            ############################
            ## MAIN ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'DucklingHTTPExtractor':
                    if e['entity'] == 'amount-of-money':
                        # TODO Duckling losts to / from information.
                        output['_TARGET_AMOUNT_TR_'].append(e['text'])
                        checks['_TARGET_AMOUNT_TR_'] = True
                elif e['extractor'] in ['DIETClassifierExtended', 'DIETClassifier']:

                    if 'role' in e and e['role'] == 'to':
                        output['_TARGET_AMOUNT_TR_'].append(e['value'])
                        checks['_TARGET_AMOUNT_TR_'] = True

                    elif 'role' in e and e['role'] == 'from':
                        output['_REF_AMOUNT_TR_'].append(e['value'])
                        checks['_REF_AMOUNT_TR_'] = True

                    elif e['entity'] in ['B-amount']:
                        
                        # try:
                        #     assert e['raw'][-1]['entity'] == 'B-currency'
                        #     assert len(e['raw']) == 2
                        #     assert re.findall(r'(tl|lira|dolar|usd|euro|eur|yüro|avro|\$|€|pound|sterlin|gbp)', e['raw'][0]['raw'][-1]['value'])
                        #     output['_REF_AMOUNT_TR_'].append(e['raw'][0]['value'])
                        #     output['_TARGET_AMOUNT_TR_'].append(e['raw'][-1]['value'])
                        # except:
                        #     output['_TARGET_AMOUNT_TR_'].append(e['value'])

                        output['_TARGET_AMOUNT_TR_'].append(e['value'])
                        checks['_TARGET_AMOUNT_TR_'] = True

                    elif e['entity'] in ['B-BUY-X', 'B-EXCHANGE-X', 'B-SEND-X']:
                        # TODO B-EXCHANGE-X and B-SEND-X can also belong to B-SELL-X.
                        # TODO TODO
                        output['_BUY_TR_'].append(e['value'])
                        
                    elif e['entity'] in ['B-SELL-X']: 
                        output['_SELL_TR_'].append(e['value'])

            ############################
            ## BACKUP ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'RegexEntityExtractor':
                    pass
                elif e['extractor'] ==  'RasaSpacyTokenizer':
                    if not checks['_TARGET_AMOUNT_TR_'] and e['entity'] == '<num>':
                        output['_TARGET_AMOUNT_TR_'].append(e['value'])

                elif e['extractor'] in  ['DIETClassifierExtended', 'DIETClassifier']:
                    pass
            
            # UPDATE REF AND TARGET FOR MCM
            if output['_BUY_TR_'] == []:
                if output['_REF_AMOUNT_TR_'] != []:
                    temppostprocessing = output['_TARGET_AMOUNT_TR_']
                    output['_TARGET_AMOUNT_TR_'] = output['_REF_AMOUNT_TR_']
                    output['_REF_AMOUNT_TR_'] = temppostprocessing

            

            [output.pop(k) for k in list(output.keys()) if output[k] == []]
            entities = output
            # entities = [generate_entity(k, output[k]) for k in output if output[k] != []]
            
        elif intent == 'transfer_money_tr':

            ############################
            ## MCM EXPECTED ENTITIES
            ############################
            val = ['_AMOUNT_TRANSFER_MONEY_TR_', 
            '_TO_ACCOUNT_TRANSFER_MONEY_TR_', 
            '_FROM_ACCOUNT_TRANSFER_MONEY_TR_', 
            '_TRXTYPE_TRANSFER_MONEY_TR_']
            
            ############################
            ## OUTPUT CONTROL BOOLEANS
            ############################
            checks ={'_AMOUNT_TRANSFER_MONEY_TR_':False, 
            '_TO_ACCOUNT_TRANSFER_MONEY_TR_':False, 
            '_FROM_ACCOUNT_TRANSFER_MONEY_TR_':False, }

            
            ############################
            ## OUTPUT VARIABLE
            ############################
            output = {'_AMOUNT_TRANSFER_MONEY_TR_':[], 
            '_TO_ACCOUNT_TRANSFER_MONEY_TR_':[], 
            '_FROM_ACCOUNT_TRANSFER_MONEY_TR_':[], 
            '_TRXTYPE_TRANSFER_MONEY_TR_':[]}
            
            ############################
            ## MAIN ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'DucklingHTTPExtractor':
                    if e['entity'] == 'amount-of-money':                        
                        output['_AMOUNT_TRANSFER_MONEY_TR_'].append(e['text'])
                        checks['_AMOUNT_TRANSFER_MONEY_TR_'] = True

                elif e['extractor'] in  ['DIETClassifierExtended', 'DIETClassifier']:
                    if e['entity'] == 'B-per':
                        # TODO No need to check 'to' / 'from'. It must be a 'to'.
                        output['_TO_ACCOUNT_TRANSFER_MONEY_TR_'].append(e['value'])
                        checks['_TO_ACCOUNT_TRANSFER_MONEY_TR_'] = True

                    elif 'role' in e and e['role'] == 'to':
                        output['_TO_ACCOUNT_TRANSFER_MONEY_TR_'].append(e['value'])
                        checks['_TO_ACCOUNT_TRANSFER_MONEY_TR_'] = True

                    elif 'role' in e and e['role'] == 'from':
                        output['_FROM_ACCOUNT_TRANSFER_MONEY_TR_'].append(e['value'])
                        checks['_FROM_ACCOUNT_TRANSFER_MONEY_TR_'] = True

                    elif e['entity'] == 'B-txtype':
                        output['_TRXTYPE_TRANSFER_MONEY_TR_'].append(e['value'])

                    elif e['entity'] == 'B-bank':
                        output['_TO_ACCOUNT_TRANSFER_MONEY_TR_'].append(e['value'])
                        checks['_TO_ACCOUNT_TRANSFER_MONEY_TR_'] = True


            ############################
            ## BACKUP ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'RegexEntityExtractor':
                    if not checks['_TO_ACCOUNT_TRANSFER_MONEY_TR_'] and e['entity'] in ['B-female-name', 'B-male-name', 'B-last-name']:
                        output['_TO_ACCOUNT_TRANSFER_MONEY_TR_'].append(e['value'])

                elif e['extractor'] ==  'RasaSpacyTokenizer':
                    if not checks['_AMOUNT_TRANSFER_MONEY_TR_'] and e['entity'] == '<num>':
                        output['_AMOUNT_TRANSFER_MONEY_TR_'].append(e['value'])

                elif e['extractor'] in  ['DIETClassifierExtended', 'DIETClassifier']:
                    ## TODO Check suffixes of B-HESAP-X entity for from account. 
                    if not checks['_FROM_ACCOUNT_TRANSFER_MONEY_TR_'] and e['entity'] == 'B-HESAP-X' and backup_condition(e):
                        output['_FROM_ACCOUNT_TRANSFER_MONEY_TR_'].append(e['value'])
            
            [output.pop(k) for k in list(output.keys()) if output[k] == []]
            entities = output
            # entities = [generate_entity(k, output[k]) for k in output if output[k] != []]
            
        elif intent == 'loan_application_tr':
            
               
            ############################
            ## MCM EXPECTED ENTITIES
            ############################
            val = ['_CURRENCY_', '_AMOUNT_', 
            '_CREDIT_TYPE_',
            '_DATE_MONTH_', '_DATE_YEAR_','_DATE_DAY_']

            ############################
            ## OUTPUT CONTROL BOOLEANS
            ############################
            checks ={'_AMOUNT_':False}

            
            ############################
            ## OUTPUT VARIABLE
            ############################
            output = {'_CURRENCY_':[], '_AMOUNT_':[], 
            '_CREDIT_TYPE_':[],
            '_DATE_MONTH_':[], '_DATE_YEAR_':[],'_DATE_DAY_':[] }
            
            ############################
            ## MAIN ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'DucklingHTTPExtractor':
                    
                    if e['entity'] == 'amount-of-money':
                        tempcurrency = e['additional_info']['unit']
                        tempcurrency = 'lira' if tempcurrency == 'TRY' else tempcurrency
                        output['_CURRENCY_'].append(tempcurrency)
                        output['_AMOUNT_'].append(str(e['additional_info']['value']))
                        checks['_AMOUNT_'] = True

                elif e['extractor'] in  ['DIETClassifierExtended', 'DIETClassifier']:
                    if e['entity'] in ['B-DURATION']:
                        if 'role' in e:
                            if e['role'] in ['YEAR']:
                                output['_DATE_YEAR_'].append(e['value'])
                            elif e['role'] in ['MONTH']:
                                output['_DATE_MONTH_'].append(e['value'])
                            elif e['role'] in ['DAY']:
                                output['_DATE_DAY_'].append(e['value'])
                        else:
                            print(e)
                            print('B-DURATION does not have role.')
                    elif e['entity'] in ['B-AMOUNT-OF-MONEY']:
                        try:
                            tempcurrencybool = e['raw'][-1]['entity'] == 'B-currency'
                            assert tempcurrencybool
                            assert len(e['raw']) == 2
                            output['_AMOUNT_'].append(e['raw'][0]['value'])
                            output['_CURRENCY_'].append(e['raw'][-1]['value'])
                        except:
                            output['_AMOUNT_'].append(e['value'])
                        checks['_AMOUNT_'] = True
                    elif e['entity'] in ['B-CREDITTYPE']:
                        output['_CREDIT_TYPE_'].append(e['value'])


            ############################
            ## BACKUP ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'RegexEntityExtractor':                    
                    pass
                        
                elif e['extractor'] ==  'RasaSpacyTokenizer':
                    pass
                
                elif e['extractor'] in  ['DIETClassifierExtended', 'DIETClassifier']:
                    pass

            
            [output.pop(k) for k in list(output.keys()) if output[k] == []]
            entities = output
            # entities = [generate_entity(k, output[k]) for k in output if output[k] != []]

        elif intent == 'term_deposit_calculation_tr':

            ############################
            ## MCM EXPECTED ENTITIES
            ############################
            val = ['_TYPE_', '_AMOUNT_', 
            '_DATE_MONTH_', '_DATE_YEAR_','_DATE_DAY_']

            ############################
            ## OUTPUT CONTROL BOOLEANS
            ############################
            checks ={'_AMOUNT_':False, '_TYPE_':False}

            
            ############################
            ## OUTPUT VARIABLE
            ############################
            output = {'_TYPE_':[], '_AMOUNT_':[], 
            '_DATE_MONTH_':[], '_DATE_YEAR_':[],'_DATE_DAY_':[] }
            
            ############################
            ## MAIN ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'DucklingHTTPExtractor':
                    
                    if e['entity'] == 'amount-of-money':
                        
                        tempcurrency = e['additional_info']['unit']
                        tempcurrency = 'lira' if tempcurrency == 'TRY' else tempcurrency
                        output['_TYPE_'].append(tempcurrency)
                        output['_AMOUNT_'].append(str(e['additional_info']['value']))
                        checks['_AMOUNT_'] = True

                elif e['extractor'] in  ['DIETClassifierExtended', 'DIETClassifier']:
                    if e['entity'] in ['B-AMOUNT-OF-MONEY']:
                        
                        try:
                            tempcurrencybool = e['raw'][-1]['entity'] == 'B-currency'
                            assert tempcurrencybool
                            assert len(e['raw']) == 2
                            output['_AMOUNT_'].append(e['raw'][0]['value'])
                            output['_TYPE_'].append(e['raw'][-1]['value'])
                        except:
                            output['_AMOUNT_'].append(e['value'])
                        checks['_AMOUNT_'] = True

                        
                    elif e['entity'] in ['B-DURATION']:
                        if e['role'] in ['YEAR']:
                            output['_DATE_YEAR_'].append(e['value'])
                        elif e['role'] in ['MONTH']:
                            output['_DATE_MONTH_'].append(e['value'])
                        elif e['role'] in ['DAY']:
                            output['_DATE_DAY_'].append(e['value'])

                    elif e['entity'] in ['B-currency']:
                        output['_TYPE_'].append(e['value'])

            ############################
            ## BACKUP ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'RegexEntityExtractor':                    
                    pass
                        
                elif e['extractor'] ==  'RasaSpacyTokenizer':
                    pass
                
                elif e['extractor'] in  ['DIETClassifierExtended', 'DIETClassifier']:
                    pass

            
            [output.pop(k) for k in list(output.keys()) if output[k] == []]
            entities = output
            # entities = [generate_entity(k, output[k]) for k in output if output[k] != []]
            
        elif intent == 'bill_payment_tr':

            
            ############################
            ## MCM EXPECTED ENTITIES
            ############################
            val = ['_ACCOUNT_TR_', '_TARGET_TR_', '_CATEGORY_TR_']

            ############################
            ## OUTPUT CONTROL BOOLEANS
            ############################
            checks ={'_ACCOUNT_TR_':False, '_TARGET_TR_':False, '_CATEGORY_TR_':False, }

            
            ############################
            ## OUTPUT VARIABLE
            ############################
            output = {'_ACCOUNT_TR_':[], '_TARGET_TR_':[], '_CATEGORY_TR_':[] }
            
            ############################
            ## MAIN ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'DucklingHTTPExtractor':
                    pass
                
                elif e['extractor'] in  ['DIETClassifierExtended', 'DIETClassifier']:
                    if e['entity'] == 'B-account':
                        # TODO No need to check 'to' / 'from'. It must be a 'from'.
                        output['_ACCOUNT_TR_'].append(e['value'])
                        checks['_ACCOUNT_TR_'] = True
                    elif e['entity'] == 'B-bill-agency':
                        output['_TARGET_TR_'].append(e['value'])
                        checks['_TARGET_TR_'] = True
                    elif e['entity'] == 'B-bill-type':
                        output['_CATEGORY_TR_'].append(e['value'])
                        checks['_CATEGORY_TR_'] = True

            ############################
            ## BACKUP ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'RegexEntityExtractor':
                    if not checks['_TARGET_TR_'] and e['entity'] in ['B-billing-agencies']:
                        output['_TARGET_TR_'].append(e['value'])

                elif e['extractor'] ==  'RasaSpacyTokenizer':
                    pass
                
                elif e['extractor'] in  ['DIETClassifierExtended', 'DIETClassifier']:
                    ## TODO Check suffixes of B-HESAP-X entity for from account. 
                    if not checks['_ACCOUNT_TR_'] and e['entity'] == 'B-HESAP-X' and backup_condition(e):
                        output['_ACCOUNT_TR_'].append(e['value'])

            [output.pop(k) for k in list(output.keys()) if output[k] == []]
            entities = output
            # entities = [generate_entity(k, output[k]) for k in output if output[k] != []]
            
        elif intent == 'history_tr':
                       
            ############################
            ## MCM EXPECTED ENTITIES
            ############################
            # '_DATE_START_', '_DATE_END_', '_MOD_ORDER_', 
            val = ['_ACCOUNT_SVP_', '_DATE_SVP_', '_DATE_', 
            '_MODIFIER_SVP_', '_MOD_TR_', '_TARGET_SVP_',]
            
            ############################
            ## OUTPUT CONTROL BOOLEANS
            ############################
            checks ={'_AMOUNT_':False}

            
            ############################
            ## OUTPUT VARIABLE
            ############################
            output = {'_DATE_SVP_':[], '_DATE_':[], 
            '_MOD_ORDER_':[], '_MODIFIER_SVP_':[], '_MOD_TR_':[],
            '_ACCOUNT_SVP_':[],'_TARGET_SVP_':[] }
            
            ############################
            ## MAIN ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'DucklingHTTPExtractor':
                    
                    if e['entity'] == 'amount-of-money':
                        pass

                elif e['extractor'] in  ['DIETClassifierExtended', 'DIETClassifier']:
                    if e['entity'] in ['B-target_svp']:
                        output['_TARGET_SVP_'].append(e['value'])
                    elif e['entity'] in ['B-date_svp']:
                        output['_DATE_SVP_'].append(e['value'])
                    elif e['entity'] in ['B-modifier_svp']:
                        output['_MODIFIER_SVP_'].append(e['value'])
                    elif e['entity'] in ['B-account_svp']:
                        output['_ACCOUNT_SVP_'].append(e['value'])

                        


            ############################
            ## BACKUP ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'RegexEntityExtractor':                    
                    pass
                        
                elif e['extractor'] ==  'RasaSpacyTokenizer':
                    pass
                
                elif e['extractor'] in  ['DIETClassifierExtended', 'DIETClassifier']:
                    pass

            if output['_DATE_SVP_'] != []:
                output['_DATE_'] = generate_entity(f'{intent}_DATE_SVP_', output['_DATE_SVP_']) 
            else:
                output['_DATE_'] = generate_entity(f'{intent}_DATE_SVP_', ['son 3 ay'])
                output['_DATE_'][0]['tokens'] = 'DEFAULT GENERATED'
            if output['_MODIFIER_SVP_'] != []:
                output['_MOD_TR_'] = generate_entity(f'{intent}_MODIFIER_SVP__MOD_TR_', output['_MODIFIER_SVP_']) 
            
            
            [output.pop(k) for k in list(output.keys()) if output[k] == []]
            entities = output

        elif intent == 'txnlist_tr':
            
            
            ############################
            ## MCM EXPECTED ENTITIES
            ############################
            # '_DATE_START_', '_DATE_END_', '_MOD_ORDER_', 
            
            val = ['_ACCOUNT_SVP_', '_DATE_SVP_', '_DATE_', 
            '_LOCATION_SVP_',  
            '_MONEY_MAX_SVP_', '_MONEY_MIN_SVP_', '_COUNT_SVP_', 
            '_MODIFIER_SVP_', '_MOD_TR_','_TARGET_SVP_',
            ]
            
            ############################
            ## OUTPUT CONTROL BOOLEANS
            ############################
            checks ={}

            
            ############################
            ## OUTPUT VARIABLE
            ############################
            output = {'_DATE_SVP_':[], '_DATE_':[], 
            '_MOD_ORDER_':[], '_MODIFIER_SVP_':[], '_MOD_TR_':[],
            '_ACCOUNT_SVP_':[],'_TARGET_SVP_':[],
            '_LOCATION_SVP_':[],
            '_MONEY_MAX_SVP_':[], '_MONEY_MIN_SVP_':[], 
            '_COUNT_SVP_':[], '_COUNT_':[] }
            
            ############################
            ## MAIN ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'DucklingHTTPExtractor':
                    
                    if e['entity'] == 'amount-of-money':
                        pass

                elif e['extractor'] in  ['DIETClassifierExtended', 'DIETClassifier']:
                    if e['entity'] in ['B-target_svp']:
                        output['_TARGET_SVP_'].append(e['value'])
                    elif e['entity'] in ['B-date_svp']:
                        output['_DATE_SVP_'].append(e['value'])
                    elif e['entity'] in ['B-modifier_svp']:
                        output['_MODIFIER_SVP_'].append(e['value'])
                    elif e['entity'] in ['B-account_svp']:
                        output['_ACCOUNT_SVP_'].append(e['value'])
                    elif e['entity'] in ['B-count_svp']:
                        output['_COUNT_SVP_'].append(e['value'])
                        try:
                            output['_COUNT_'].append(int(e['value']))
                        except:
                            pass
                    elif e['entity'] in ['B-money_min_svp']:
                        output['_MONEY_MIN_SVP_'].append(e['value'])
                    elif e['entity'] in ['B-money_max_svp']:
                        output['_MONEY_MAX_SVP_'].append(e['value'])
                    elif e['entity'] in ['B-location_svp']:
                        output['_LOCATION_SVP_'].append(e['value'])

                        


            ############################
            ## BACKUP ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'RegexEntityExtractor':                    
                    pass
                        
                elif e['extractor'] ==  'RasaSpacyTokenizer':
                    pass
                
                elif e['extractor'] in  ['DIETClassifierExtended', 'DIETClassifier']:
                    pass

            if output['_DATE_SVP_'] != []:
                output['_DATE_'] = generate_entity(f'{intent}_DATE_SVP_', output['_DATE_SVP_'])
            else:
                output['_DATE_'] = generate_entity(f'{intent}_DATE_SVP_', ['son 3 ay'])
                output['_DATE_'][0]['tokens'] = 'DEFAULT GENERATED'
                
            if output['_MODIFIER_SVP_'] != []:
                output['_MOD_TR_'] = generate_entity(f'{intent}_MODIFIER_SVP__MOD_TR_', output['_MODIFIER_SVP_']) 
            
            
            [output.pop(k) for k in list(output.keys()) if output[k] == []]
            entities = output

        elif intent == 'spendadvice_tr':
            
            ############################
            ## MCM EXPECTED ENTITIES
            ############################
            # '_DATE_START_', '_DATE_END_', '_MOD_ORDER_', 
            val = ['_TARGET_SVP_','_MONEY_', '_AMOUNT_TR_']
            
            ############################
            ## OUTPUT CONTROL BOOLEANS
            ############################
            checks ={}

            
            ############################
            ## OUTPUT VARIABLE
            ############################
            output = {'_TARGET_SVP_':[], '_MONEY_':[], '_AMOUNT_TR_':[] }
            
            ############################
            ## MAIN ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'DucklingHTTPExtractor':
                    
                    if e['entity'] == 'amount-of-money':
                        
                        tempcurrency = e['additional_info']['unit']
                        tempcurrency = 'lira' if tempcurrency == 'TRY' else tempcurrency

                        output['_AMOUNT_TR_'].append(e['text'])
                        output['_MONEY_'].append({
                            'tokens': e['text'], 
                            'numbers': [{'value': e['value'], 'tokens': str(e['value'])}], 
                            'value': e['value'], 
                            'currency': tempcurrency, 
                            'svp_tokens': e['text']})

                elif e['extractor'] in  ['DIETClassifierExtended', 'DIETClassifier']:
                    if e['entity'] in ['B-SPENDING-CATEGORY']:
                        output['_TARGET_SVP_'].append(e['value'])
                    elif e['entity'] in ['B-AMOUNT-OF-MONEY']:
                        
                        try:
                            tempcurrencybool = e['raw'][-1]['entity'] == 'B-currency'
                            assert tempcurrencybool
                            assert len(e['raw']) == 2
                            
                            tempall = e['value']
                            tempamount = e['raw'][0]['value']
                            tempcurrency = e['raw'][-1]['value']
                        except:
                            tempall = e['value']
                            tempamount = e['value']
                            tempcurrency = e['value']

                        output['_AMOUNT_TR_'].append(tempall)
                        output['_MONEY_'].append({
                            'tokens': tempall, 
                            'numbers': [{'value': tempamount, 'tokens': str(tempamount)}], 
                            'value': tempamount, 
                            'currency': tempcurrency, 
                            'svp_tokens': tempall})

                        # output['_MONEY_'].append({
                        #     'tokens': e['value'], 
                        #     'numbers': [{'value': e['value'], 'tokens': str(e['value'])}], 
                        #     'value': e['value'], 
                        #     'currency': e['value'], 
                        #     'svp_tokens': e['value']})


                        


            ############################
            ## BACKUP ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'RegexEntityExtractor':                    
                    pass
                        
                elif e['extractor'] ==  'RasaSpacyTokenizer':
                    pass
                
                elif e['extractor'] in  ['DIETClassifierExtended', 'DIETClassifier']:
                    pass

            
            [output.pop(k) for k in list(output.keys()) if output[k] == []]
            entities = output

        elif intent == 'campaign_tr':

            ############################
            ## MCM EXPECTED ENTITIES
            ############################
            # '_DATE_START_', '_DATE_END_', '_MOD_ORDER_', 
            val = ['_JOINED_TR_','_TARGET_TR_','_STAFF_TR_']
            
            ############################
            ## OUTPUT CONTROL BOOLEANS
            ############################
            checks ={}

            
            ############################
            ## OUTPUT VARIABLE
            ############################
            output = {'_JOINED_TR_':[], '_TARGET_TR_':[], '_STAFF_TR_':[] }
            
            ############################
            ## MAIN ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'DucklingHTTPExtractor':
                    
                    if e['entity'] == 'amount-of-money':
                        pass

                elif e['extractor'] in  ['DIETClassifierExtended', 'DIETClassifier']:
                    if e['entity'] in ['B-JOIN-X']:
                        output['_JOINED_TR_'].append(e['value'])
                    elif e['entity'] in ['B-SPENDING-CATEGORY']:
                        output['_TARGET_TR_'].append(e['value'])
                    elif e['entity'] in ['B-STAFF-X']:
                        output['_STAFF_TR_'].append(e['value'])
            ############################
            ## BACKUP ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'RegexEntityExtractor':                    
                    pass
                        
                elif e['extractor'] ==  'RasaSpacyTokenizer':
                    pass
                
                elif e['extractor'] in  ['DIETClassifierExtended', 'DIETClassifier']:
                    pass

            
            [output.pop(k) for k in list(output.keys()) if output[k] == []]
            entities = output

        else:
            print(f"This intent is not handled : {intent}")

        message.set("entities", entities, add_to_output=True)
        # return entities