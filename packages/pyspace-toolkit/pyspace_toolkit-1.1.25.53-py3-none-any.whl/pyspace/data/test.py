import pandas as pd

def test_maxi(config={}, data=None, intent_filter_for_entities=False):

    if str(type(data)) != str(type(None)):
        assert isinstance(data, pd.DataFrame)
        assert 'Text' in list(data.columns)
        assert 'Intent' in list(data.columns)
    else:
        
        data = []

        # transfer_money_tr
        data.append( ('Simgeye 50 tl yolla', 'transfer_money_tr', {'_AMOUNT_TRANSFER_MONEY_TR_': ['50 tl'], '_TO_ACCOUNT_TRANSFER_MONEY_TR_': ['Simgeye']}) )
        data.append( ('levent hesabimdan simgeye 100 tl at', 'transfer_money_tr', {'_AMOUNT_TRANSFER_MONEY_TR_': ['100 tl'], '_TO_ACCOUNT_TRANSFER_MONEY_TR_': ['simgeye'], '_FROM_ACCOUNT_TRANSFER_MONEY_TR_': ['levent']}) )
        data.append( ('levent hesabimdan onura bin lira gonder', 'transfer_money_tr', {'_AMOUNT_TRANSFER_MONEY_TR_': ['bin lira'], '_TO_ACCOUNT_TRANSFER_MONEY_TR_': ['onur'], '_FROM_ACCOUNT_TRANSFER_MONEY_TR_': ['levent']}) )
        data.append( ('finansbank hesabima 200 tl gonder', 'transfer_money_tr', {'_TO_ACCOUNT_TRANSFER_MONEY_TR_': ['finansbank'], '_AMOUNT_TRANSFER_MONEY_TR_': ['200 tl']}) )
        data.append( ('simgeye vadesiz hesabımdan 100 tl para aktar', 'transfer_money_tr', {'_AMOUNT_TRANSFER_MONEY_TR_': ['100 tl'], '_TO_ACCOUNT_TRANSFER_MONEY_TR_': ['simgeye'], '_FROM_ACCOUNT_TRANSFER_MONEY_TR_': ['vadesiz']}) )
        data.append( ('simgeye ve oguzhana para gonder', 'transfer_money_tr', {'_TO_ACCOUNT_TRANSFER_MONEY_TR_': ['simgeye', 'oguzhana']}) )
        data.append( ('simgeye 100 tl para gonder', 'transfer_money_tr', {'_AMOUNT_TRANSFER_MONEY_TR_': ['100 tl'], '_TO_ACCOUNT_TRANSFER_MONEY_TR_': ['simgeye']}) )
        data.append( ('Levent hesabimdan simge ulusoya 100 tl para gonder', 'transfer_money_tr', {'_AMOUNT_TRANSFER_MONEY_TR_': ['100 tl'], '_TO_ACCOUNT_TRANSFER_MONEY_TR_': ['simge ulusoya'], '_FROM_ACCOUNT_TRANSFER_MONEY_TR_': ['Levent']}) )
        data.append( ('hesabimdan 200 tl gonder', 'transfer_money_tr', {'_AMOUNT_TRANSFER_MONEY_TR_': ['200 tl'], '_FROM_ACCOUNT_TRANSFER_MONEY_TR_': ['hesabimdan']}) )
        data.append( ('levent subesinden kira odemesi yap', 'transfer_money_tr', {'_FROM_ACCOUNT_TRANSFER_MONEY_TR_': ['levent'], '_TRXTYPE_TRANSFER_MONEY_TR_': ['kira']}) )
        data.append( ('maaslar yatinca kira odemesini yap', 'transfer_money_tr', {'_TRXTYPE_TRANSFER_MONEY_TR_': ['kira']}) )
        data.append( ('1.490 lira bucadaki hesabimdan', 'transfer_money_tr', {'_AMOUNT_TRANSFER_MONEY_TR_': ['1.490 lira'], '_FROM_ACCOUNT_TRANSFER_MONEY_TR_': ['bucadaki']}) )
        data.append( ('250 lira 678902 numarali hesabimdan Murat\'in Levent Subesi aktarmak istiyorum', 'transfer_money_tr', {'_TO_ACCOUNT_TRANSFER_MONEY_TR_': ["Murat'in", 'Levent'], '_FROM_ACCOUNT_TRANSFER_MONEY_TR_': ['678902'], '_AMOUNT_TRANSFER_MONEY_TR_': ['250 lira'],}) )
        data.append( ('1.200 dolar göndereceğim', 'transfer_money_tr', {'_AMOUNT_TRANSFER_MONEY_TR_': ['1200 dolar']}) )


        # bill_payment_tr
        data.append( ('fatura odemek istiyorum', 'bill_payment_tr', {}) )
        data.append( ('internet fatura', 'bill_payment_tr', {'_CATEGORY_TR_': ['internet']}) )
        data.append( ('internet faturasi', 'bill_payment_tr', {'_CATEGORY_TR_': ['internet']}) )
        data.append( ('internet faturası', 'bill_payment_tr', {'_CATEGORY_TR_': ['internet']}) )
        data.append( ('internet tv', 'bill_payment_tr', {'_CATEGORY_TR_': ['internet','tv']}) )
        data.append( ('fatura iz su', 'bill_payment_tr', {'_CATEGORY_TR_': ['su']}) )
        data.append( ('igdas', 'bill_payment_tr', {'_TARGET_TR_': ['igdas']}) )
        data.append( ('kredi kartimdan iski su faturami odemek istiyorum', 'bill_payment_tr', {'_ACCOUNT_TR_': ['kredi kartimdan'], '_TARGET_TR_': ['iski'], '_CATEGORY_TR_': ['su']}) )
        data.append( ('hesaptan fatura ödeme yapmak istiyorum ne yapmam gerekiyor', 'bill_payment_tr', {'_ACCOUNT_TR_': ['hesaptan']}) )
        data.append( ('Kredi kartimdan faturami odemek istiyorum', 'bill_payment_tr', {'_ACCOUNT_TR_': ['Kredi kartimdan']}) )
        data.append( ('istanbul şubesindeki hesabımdan elektrik faturamı ödemek istiyorum', 'bill_payment_tr', {'_ACCOUNT_TR_': ['istanbul'], '_CATEGORY_TR_': ['elektrik']}) )
        data.append( ('Afyonkarahisar Belediyesi', 'bill_payment_tr', {'_TARGET_TR_': ['Afyonkarahisar Belediyesi']}) )
        data.append( ('Agdaş faturamı ödemek istiyorum', 'bill_payment_tr', {'_TARGET_TR_': ['Agdaş']}) )
        data.append( ('AKSA Malatya doğalgaz faturamı ödemek istiyorum', 'bill_payment_tr', {'_TARGET_TR_': ['AKSA Malatya'], '_CATEGORY_TR_': ['doğalgaz']}) )
        data.append( ('2M Enerji elektrik faturamı ödemek istiyorum', 'bill_payment_tr', {'_TARGET_TR_': ['2M'], '_CATEGORY_TR_': ['Enerji elektrik']}) )
        data.append( ('beşiktaş şubesinden hesabımdan telefon faturamı ödemek istiyorum', 'bill_payment_tr', {'_ACCOUNT_TR_': ['beşiktaş'], '_CATEGORY_TR_': ['telefon']}) )
        data.append( ('cep faturami nasil yatiririm', 'bill_payment_tr', {'_CATEGORY_TR_': ['cep']}) )
        data.append( ('cep telefonu faturamı öde', 'bill_payment_tr', {'_CATEGORY_TR_': ['cep telefonu']}) )
        
        # history_tr
        data.append( ('gecen ayki migros harcmalarimi gosterir misin', 'history_tr', {'_DATE_SVP_': ['gecen ayki'], '_DATE_': [{'startDate': '2020-07-01T00:00:00Z', 'endDate': '2020-08-01T00:00:00Z', 'type': 'DURATION', 'period': 'P1M', 'tokens': 'gecen ayki'}], '_TARGET_SVP_': ['migros']}) )
        data.append( ('son harcamalarim', 'history_tr', {'_DATE_SVP_': ['son'], '_DATE_': [{'startDate': '2020-07-25T01:28:27Z', 'endDate': '2020-08-25T01:28:27Z', 'type': 'DURATION', 'period': 'P3M', 'tokens': 'DEFAULT GENERATED'}]}) )
        data.append( ('migros ve boyner harcamalarim neler', 'history_tr', {'_DATE_': [{'startDate': '2020-05-25T01:28:27Z', 'endDate': '2020-08-25T01:28:27Z', 'type': 'DURATION', 'period': 'P3M', 'tokens': 'DEFAULT GENERATED'}], '_MODIFIER_SVP_': ['harcamalarim'], '_MOD_TR_': [{'value': 'SPEND'}], '_TARGET_SVP_': ['migros ve boyner']}) )
        data.append( ('ağustos ayında hesabımdan ne kadar çekim yaptım', 'history_tr', {'_DATE_SVP_': ['ağustos ayında'], '_DATE_': [{'startDate': '2020-08-01T00:00:00Z', 'endDate': '2020-08-27T11:39:14.562Z', 'type': 'DURATION', 'period': 'P1M', 'tokens': 'ağustos ayında'}], '_ACCOUNT_SVP_': ['hesabımdan']}) )

        data.append( ('01.01.2018\'de Pizza Pizza\'da ne kadar harcadim?', 'history_tr', {'_DATE_SVP_': ["01.01.2018'de"], '_DATE_': [{'startDate': '2018-01-01T00:00:00Z', 'endDate': '2018-01-01T23:59:59Z', 'type': 'DURATION', 'period': 'P1D', 'tokens': "01.01.2018'de"}], '_TARGET_SVP_': ["Pizza Pizza'da"]}) )
        data.append( ('Gecen ay boyner\'de en fazla ne kadar harcadim?', 'history_tr', {'_DATE_SVP_': ['Gecen ay'], '_DATE_': [{'startDate': '2020-07-01T00:00:00Z', 'endDate': '2020-08-01T00:00:00Z', 'type': 'DURATION', 'period': 'P1M', 'tokens': 'Gecen ay'}], '_MODIFIER_SVP_': ['en fazla'], '_MOD_TR_': [{'value': 'MAX'}], '_TARGET_SVP_': ["boyner'de"]}) )
        data.append( ('Gecen ay boyner\'de en az ne kadar harcadim?', 'history_tr', {'_DATE_SVP_': ['Gecen ay'], '_DATE_': [{'startDate': '2020-07-01T00:00:00Z', 'endDate': '2020-08-01T00:00:00Z', 'type': 'DURATION', 'period': 'P1M', 'tokens': 'Gecen ay'}], '_MODIFIER_SVP_': ['en az'], '_MOD_TR_': [{'value': 'MIN'}], '_TARGET_SVP_': ["boyner'de"]}) )
        data.append( ('3 ay once boyner\'de en fazla ne kadar harcadim?', 'history_tr', {'_DATE_SVP_': ['3 ay once'], '_DATE_': [{'startDate': '2020-05-01T00:00:00Z', 'endDate': '2020-06-01T00:00:00Z', 'type': 'DURATION', 'period': 'P1M', 'tokens': '3 ay once'}], '_MODIFIER_SVP_': ['en fazla'], '_MOD_TR_': [{'value': 'MAX'}], '_TARGET_SVP_': ["boyner'de"]}) )
        data.append( ('boyner harcama gecmisim neler', 'history_tr', {'_DATE_': [{'startDate': '2020-05-25T01:28:27Z', 'endDate': '2020-08-25T01:28:27Z', 'type': 'DURATION', 'period': 'P3M', 'tokens': 'DEFAULT GENERATED'}], '_TARGET_SVP_': ['boyner']}) )

        data.append( ('Ortalama gida harcamam ne kadar', 'history_tr', {'_DATE_': [{'startDate': '2020-05-25T01:51:12Z', 'endDate': '2020-08-25T01:51:12Z', 'type': 'DURATION', 'period': 'P3M', 'tokens': 'DEFAULT GENERATED'}], '_MODIFIER_SVP_': ['Ortalama'], '_MOD_TR_': [{'value': 'AVG'}], '_TARGET_SVP_': ['gida']}) )
        data.append( ('En dusuk gida harcamam ne kadar', 'history_tr', {'_DATE_': [{'startDate': '2020-05-25T01:28:27Z', 'endDate': '2020-08-25T01:28:27Z', 'type': 'DURATION', 'period': 'P3M', 'tokens': 'DEFAULT GENERATED'}], '_MODIFIER_SVP_': ['En dusuk'], '_MOD_TR_': [{'value': 'MIN'}], '_TARGET_SVP_': ['gida']}) )
        data.append( ('kredi kartimdan son 1 ayda gida harcamalarim ne kadar tuttu', 'history_tr', {'_DATE_SVP_': ['son 1 ayda'], '_DATE_': [{'startDate': '2020-07-25T01:28:27Z', 'endDate': '2020-08-25T01:28:27Z', 'type': 'DURATION', 'period': 'P1M', 'tokens': 'son 1 ayda'}], '_ACCOUNT_SVP_': ['kredi kartimdan'], '_TARGET_SVP_': ['gida']}) )
        data.append( ('kredi kartimdan son 1 yilda gida harcamalarim ne kadar tuttu', 'history_tr', {'_DATE_SVP_': ['son 1 yilda'], '_DATE_': [{'startDate': '2019-08-25T01:28:27Z', 'endDate': '2020-08-25T01:28:27Z', 'type': 'DURATION', 'period': 'P1Y', 'tokens': 'son 1 yilda'}], '_ACCOUNT_SVP_': ['kredi kartimdan'], '_TARGET_SVP_': ['gida']}) )
        data.append( ('kadikoyde son 3 ayda yaptigim kahve harcamalarim neler', 'history_tr', {'_DATE_SVP_': ['son 3 ayda'], '_DATE_': [{'startDate': '2020-05-25T01:28:27Z', 'endDate': '2020-08-25T01:28:27Z', 'type': 'DURATION', 'period': 'P3M', 'tokens': 'son 3 ayda'}], '_MODIFIER_SVP_': ['harcamalarim'], '_MOD_TR_': [{'value': 'SPEND'}], '_TARGET_SVP_': ['kahve']}) )
        data.append( ('10 20 Nisan tarihleri arası hesabımdan ne kadar çekim yaptım?', 'history_tr', {'_DATE_SVP_': ['10 20 Nisan tarihleri arası'], '_DATE_': [{'startDate': '2020-04-10T00:00:00Z', 'endDate': '2020-04-20T23:59:59Z', 'type': 'DURATION', 'period': 'P10D', 'tokens': '10 20 Nisan tarihleri arası'}], '_ACCOUNT_SVP_': ['hesabımdan']}) )
        data.append( ('ekimde bauhaus\'a ne kadar harcamışım', 'history_tr', {'_DATE_SVP_': ['ekimde'], '_DATE_': [{'startDate': '2019-10-01T00:00:00Z', 'endDate': '2019-10-31T23:59:59Z', 'type': 'DURATION', 'period': 'P1M', 'tokens': 'ekimde'}], '_MODIFIER_SVP_': ['harcamışım'], '_MOD_TR_': [{'value': 'SPEND'}], '_TARGET_SVP_': ["bauhaus'a"]}) )
        data.append( ('1 0cak 2018 kredi kartı kullanım dökümü?', 'history_tr', {'_DATE_SVP_': ['1 0cak 2018'], '_DATE_': [{'startDate': '2018-01-01T00:00:00Z', 'endDate': '2018-01-02T00:00:00Z', 'type': 'DURATION', 'period': 'P1D', 'tokens': '1 0cak 2018'}], '_ACCOUNT_SVP_': ['kredi kartı']}) )
        data.append( ('ekimde bauhaus\'a ne kadar harcamışım', 'history_tr', {'_DATE_SVP_': ['ekimde'], '_DATE_': [{'startDate': '2019-10-01T00:00:00Z', 'endDate': '2019-10-31T23:59:59Z', 'type': 'DURATION', 'period': 'P1M', 'tokens': 'ekimde'}], '_MODIFIER_SVP_': ['harcamışım'], '_MOD_TR_': [{'value': 'SPEND'}], '_TARGET_SVP_': ["bauhaus\'a"]}) )
        data.append( ('En fazla hangi kategoride harcıyorum', 'history_tr', {'_DATE_': [{'startDate': '2020-05-25T13:00:03Z', 'endDate': '2020-08-25T13:00:03Z', 'type': 'DURATION', 'period': 'P3M', 'tokens': 'DEFAULT GENERATED'}], '_MODIFIER_SVP_': ['En fazla'], '_MOD_TR_': [{'value': 'MAX'}]}) )

        # txnlist_tr
        data.append( ('en cok nelere para harcamisim', 'txnlist_tr', {'_DATE_': [{'startDate': '2020-05-25T01:51:12Z', 'endDate': '2020-08-25T01:51:12Z', 'type': 'DURATION', 'period': 'P3M', 'tokens': 'DEFAULT GENERATED'}], '_MODIFIER_SVP_': ['en cok', 'harcamisim'], '_MOD_TR_': [{'value': 'MAX'}, {'value': 'SPEND'}]}) )
        data.append( ('son dokuz aya ait kredi kartımdan yapilan işlemleri gösterebilir misin', 'txnlist_tr', {'_DATE_SVP_': ['son dokuz aya'], '_DATE_': [{'startDate': '2019-11-25T01:28:27Z', 'endDate': '2020-08-25T01:28:27Z', 'type': 'DURATION', 'period': 'P9M', 'tokens': 'son dokuz aya'}], '_MODIFIER_SVP_': ['işlemleri'], '_ACCOUNT_SVP_': ['kredi kartımdan']}) )

        data.append( ('Son 6 ayki gida alisverisim neler', 'txnlist_tr', {'_DATE_SVP_': ['Son 6 ayki'], '_DATE_': [{'startDate': '2020-02-25T01:28:27Z', 'endDate': '2020-08-25T01:28:27Z', 'type': 'DURATION', 'period': 'P6M', 'tokens': 'Son 6 ayki'}], '_MODIFIER_SVP_': ['alisverisim'], '_MOD_TR_': [{'value': 'MAX'}], '_TARGET_SVP_': ['gida']}) )
        data.append( ('Son 6 ay , en fazla gida alisveris', 'txnlist_tr', {'_DATE_SVP_': ['Son 6 ay'], '_DATE_': [{'startDate': '2020-02-25T01:28:27Z', 'endDate': '2020-08-25T01:28:27Z', 'type': 'DURATION', 'period': 'P6M', 'tokens': 'Son 6 ay'}], '_MODIFIER_SVP_': ['en fazla', 'alisveris'], '_MOD_TR_': [{'value': 'MAX'}, {'value': 'SPEND'}]}) )
        data.append( ('3 ay once boyner\'de 1000 lira uzeri 5 harcamam neler', 'txnlist_tr', {'_DATE_SVP_': ['3 ay once'], '_DATE_': [{'startDate': '2020-05-01T00:00:00Z', 'endDate': '2020-06-01T00:00:00Z', 'type': 'DURATION', 'period': 'P1M', 'tokens': '3 ay once'}], '_MODIFIER_SVP_': ['harcamam'], '_MOD_TR_': [{'value': 'SPEND'}], '_TARGET_SVP_': ["boyner'de"], '_MONEY_MIN_SVP_': ['1000 lira'], '_COUNT_SVP_': ['5'], '_COUNT_': [{'value':5}]}) )
        data.append( ('1 şubat ile 1 kasım arasında yaptığım en yüksek üç anadolu jet harcamamı listele', 'txnlist_tr', {'_DATE_SVP_': ['1 şubat ile 1 kasım arasında'], '_DATE_': [{'startDate': '2020-02-01T00:00:00Z', 'endDate': '2020-08-27T11:39:29.340Z', 'type': 'DURATION', 'period': 'P274D', 'tokens': '1 şubat ile 1 kasım arasında'}], '_MODIFIER_SVP_': ['en yüksek', 'harcamamı'], '_MOD_TR_': [{'value': 'MAX'}, {'value': 'SPEND'}], '_TARGET_SVP_': ['anadolu jet'], '_COUNT_SVP_': ['üç']}) )
        data.append( ('1 ayda en çok yeme içmeye para vermişimdir heralde, doğru mudur', 'txnlist_tr', {'_DATE_SVP_': ['1 ayda'], '_DATE_': [{'startDate': '2020-07-25T01:28:27Z', 'endDate': '2020-08-25T01:28:27Z', 'type': 'DURATION', 'period': 'P1M', 'tokens': '1 ayda'}], '_MODIFIER_SVP_': ['en çok'], '_MOD_TR_': [{'value': 'MAX'}], '_TARGET_SVP_': ['yeme içmeye']}) )
        data.append( ('2 ay once en pahalı harcamam ne üzerine oldu?', 'txnlist_tr', {'_DATE_SVP_': ['2 ay once'], '_DATE_': [{'startDate': '2020-06-01T00:00:00Z', 'endDate': '2020-07-01T00:00:00Z', 'type': 'DURATION', 'period': 'P1M', 'tokens': '2 ay once'}], '_MODIFIER_SVP_': ['en pahalı', 'harcamam'], '_MOD_TR_': [{'value': 'MAX'}, {'value': 'SPEND'}]}) )
        data.append( ('1 ay boyunca Vestel\'den yaptığım alışverişlerin listesi', 'txnlist_tr', {'_DATE_SVP_': ['1 ay boyunca'], '_DATE_': [{'startDate': '2020-07-25T01:28:27Z', 'endDate': '2020-08-25T01:28:27Z', 'type': 'DURATION', 'period': 'P1M', 'tokens': '1 ay boyunca'}], '_MODIFIER_SVP_': ['alışverişlerin'], '_MOD_TR_': [{'value': 'SPEND'}], '_TARGET_SVP_': ["Vestel'den"]}) )
        data.append( ('119 28 hesabımdan çekilen para nedir', 'txnlist_tr', {'_DATE_': [{'startDate': '2020-05-25T13:00:03Z', 'endDate': '2020-08-25T13:00:03Z', 'type': 'DURATION', 'period': 'P3M', 'tokens': 'DEFAULT GENERATED'}], '_MODIFIER_SVP_': ['çekilen'], '_ACCOUNT_SVP_': ['hesabımdan']}) )
        data.append( ('200 tl\'yi aşmayan kredi karti harcamalarını göster', 'txnlist_tr', {'_DATE_': [{'startDate': '2020-05-25T13:00:03Z', 'endDate': '2020-08-25T13:00:03Z', 'type': 'DURATION', 'period': 'P3M', 'tokens': 'DEFAULT GENERATED'}], '_MODIFIER_SVP_': ['harcamalarını'], '_MOD_TR_': [{'value': 'SPEND'}], '_ACCOUNT_SVP_': ['kredi karti'], '_MONEY_MAX_SVP_': ['200']}) )
        data.append( ('4553 ile sonlanan kredi kartımdan son ay çekilen bireysel emeklilik ücreti nedir?', 'txnlist_tr', {'_DATE_SVP_': ['son ay'], '_DATE_': [{'startDate': '2020-07-25T13:00:03Z', 'endDate': '2020-08-25T13:00:03Z', 'type': 'DURATION', 'period': 'P1M', 'tokens': 'son ay'}], '_ACCOUNT_SVP_': ['4553 ile sonlanan'], '_TARGET_SVP_': ['bireysel emeklilik']}) )
        data.append( ('1 ay önce ençok harcama yaptığım 5 işlem nedir?', 'txnlist_tr', {'_DATE_SVP_': ['1 ay önce'], '_DATE_': [{'startDate': '2020-07-01T00:00:00Z', 'endDate': '2020-08-01T00:00:00Z', 'type': 'DURATION', 'period': 'P1M', 'tokens': '1 ay önce'}], '_MODIFIER_SVP_': ['ençok', 'işlem'], '_MOD_TR_': [{'value': 'MAX'}], '_COUNT_SVP_': ['5'], '_COUNT_': [5]}) )
        data.append( ('350 liradan az ilk dört alışverişimi getir', 'txnlist_tr', {'_DATE_': [{'startDate': '2020-05-25T13:00:03Z', 'endDate': '2020-08-25T13:00:03Z', 'type': 'DURATION', 'period': 'P3M', 'tokens': 'DEFAULT GENERATED'}], '_MODIFIER_SVP_': ['ilk', 'alışverişimi'], '_MOD_TR_': [{'value': 'SPEND'}], '_MONEY_MAX_SVP_': ['350'], '_COUNT_SVP_': ['dört']}) )
        data.append( ('bu ay yaptığım son dört harcamayı göster', 'txnlist_tr', {'_DATE_SVP_': ['bu ay'], '_DATE_': [{'startDate': '2020-08-01T00:00:00Z', 'endDate': '2020-08-25T13:00:03Z', 'type': 'DURATION', 'period': 'P1M', 'tokens': 'bu ay'}], '_MODIFIER_SVP_': ['son', 'harcamayı'], '_MOD_TR_': [{'value': 'SPEND'}], '_COUNT_SVP_': ['dört']}) )
        data.append( ('1 ay içerisinde House Cafe\'de kaç kere harcama yaptım?', 'txnlist_tr', {'_DATE_SVP_': ['1 ay içerisinde'], '_DATE_': [{'startDate': '2020-07-25T13:00:03Z', 'endDate': '2020-08-25T13:00:03Z', 'type': 'DURATION', 'period': 'P1M', 'tokens': '1 ay içerisinde'}], '_TARGET_SVP_': ["House Cafe\'de"]}) )
        data.append( ('1 Ocak ve 1 Şubat arasında bitki ve bahçeye harcadığım en yüksek miktar', 'txnlist_tr', {'_DATE_SVP_': ['1 Ocak ve 1 Şubat arasında'], '_DATE_': [{'startDate': '2020-01-01T00:00:00Z', 'endDate': '2020-02-01T00:00:00Z', 'type': 'DURATION', 'period': 'P1M', 'tokens': '1 Ocak ve 1 Şubat arasında'}], '_MODIFIER_SVP_': ['en yüksek'], '_MOD_TR_': [{'value': 'MAX'}], '_TARGET_SVP_': ['bitki ve bahçeye']}) )
        data.append( ('eylül ayında İzmir\'de 50 lira üzeri yaptığım harcamaları göster', 'txnlist_tr', {'_DATE_SVP_': ['eylül ayında'], '_DATE_': [{'startDate': '2019-09-01T00:00:00Z', 'endDate': '2019-09-30T23:59:59Z', 'type': 'DURATION', 'period': 'P1M', 'tokens': 'eylül ayında'}], '_MODIFIER_SVP_': ['harcamaları'], '_MOD_TR_': [{'value': 'SPEND'}], '_LOCATION_SVP_': ["İzmir\'de"], '_MONEY_MIN_SVP_': ['50']}) )
        data.append( ('bana gelen havale', 'txnlist_tr', {'_DATE_': [{'startDate': '2020-05-25T13:00:03Z', 'endDate': '2020-08-25T13:00:03Z', 'type': 'DURATION', 'period': 'P3M', 'tokens': 'DEFAULT GENERATED'}], '_MODIFIER_SVP_': ['gelen'], '_TARGET_SVP_': ['havale']}) )
        data.append( ('2 ay once en pahalı harcamam ne üzerine oldu?', 'txnlist_tr', {'_DATE_SVP_': ['2 ay once'], '_DATE_': [{'startDate': '2020-06-01T00:00:00Z', 'endDate': '2020-07-01T00:00:00Z', 'type': 'DURATION', 'period': 'P1M', 'tokens': '2 ay once'}], '_MODIFIER_SVP_': ['en pahalı', 'harcamam'], '_MOD_TR_': [{'value': 'MAX'}, {'value': 'SPEND'}]}) )
        data.append( ('100 tl altı seyahat harcamalarımı gösterir misin?', 'txnlist_tr', {'_DATE_': [{'startDate': '2020-05-25T13:00:03Z', 'endDate': '2020-08-25T13:00:03Z', 'type': 'DURATION', 'period': 'P3M', 'tokens': 'DEFAULT GENERATED'}], '_TARGET_SVP_': ['seyahat'], '_MONEY_MAX_SVP_': ['100']}) )
        data.append( ('100 lira ve üzeri yaptığım alışverişleri listele', 'txnlist_tr', {'_DATE_': [{'startDate': '2020-05-25T13:00:03Z', 'endDate': '2020-08-25T13:00:03Z', 'type': 'DURATION', 'period': 'P3M', 'tokens': 'DEFAULT GENERATED'}], '_MONEY_MIN_SVP_': ['100']}) )
        data.append( ('1 ayda en çok yeme içmeye para vermişimdir heralde, doğru mudur?', 'txnlist_tr', {'_DATE_SVP_': ['1 ayda'], '_DATE_': [{'startDate': '2020-07-25T13:00:03Z', 'endDate': '2020-08-25T13:00:03Z', 'type': 'DURATION', 'period': 'P1M', 'tokens': '1 ayda'}], '_MODIFIER_SVP_': ['en çok'], '_MOD_TR_': [{'value': 'MAX'}], '_TARGET_SVP_': ['yeme içmeye']}) )
        data.append( ('100 liranın üzerinde doğa sporlarına para harcamış mıyım?', 'txnlist_tr', {'_DATE_': [{'startDate': '2020-05-25T13:00:03Z', 'endDate': '2020-08-25T13:00:03Z', 'type': 'DURATION', 'period': 'P3M', 'tokens': 'DEFAULT GENERATED'}], '_TARGET_SVP_': ['doğa sporlarına'], '_MONEY_MIN_SVP_': ['100']}) )
        
        # foreign_currency_tr
        data.append( ('100 dolarimi bozdurmak istiyorum', 'foreign_currency_tr', {'_TARGET_AMOUNT_TR_': ['100 dolarimi'], '_SELL_TR_': ['bozdurmak']}) )
        data.append( ('100 dolar almak istiyorum', 'foreign_currency_tr', {'_TARGET_AMOUNT_TR_': ['100 dolar'], '_BUY_TR_': ['almak']}) )
        data.append( ('100 liralik dolar al', 'foreign_currency_tr', {'_REF_AMOUNT_TR_': ['100 liralik'], '_TARGET_AMOUNT_TR_': ['dolar'], '_BUY_TR_': ['al']}) )
        data.append( ('bir dolar kaç lira', 'foreign_currency_tr', {'_TARGET_AMOUNT_TR_': ['bir dolar'], '_REF_AMOUNT_TR_': ['lira']}) )
        data.append( ('iki dolar kaç lira', 'foreign_currency_tr', {'_TARGET_AMOUNT_TR_': ['iki dolar'], '_REF_AMOUNT_TR_': ['lira']}) )
        data.append( ('on dolarlık tl alicam', 'foreign_currency_tr', {'_TARGET_AMOUNT_TR_': ['tl'], '_REF_AMOUNT_TR_': ['on dolarlık'], '_BUY_TR_': ['alicam']}) )
        data.append( ('100 liralik dolar al', 'foreign_currency_tr', {'_REF_AMOUNT_TR_': ['100 liralik'], '_TARGET_AMOUNT_TR_': ['dolar'], '_BUY_TR_': ['al']}) )
        data.append( ('100 DKK al', 'foreign_currency_tr', {'_TARGET_AMOUNT_TR_': ['100 DKK'], '_BUY_TR_': ['al']}) )
        data.append( ('100 lira degerinde dolar al', 'foreign_currency_tr', {'_REF_AMOUNT_TR_': ['100 lira'], '_TARGET_AMOUNT_TR_': ['dolar'], '_BUY_TR_': ['al']}) )
        data.append( ('100 tllik euro bozdur', 'foreign_currency_tr', {'_REF_AMOUNT_TR_': ['100 tllik'], '_TARGET_AMOUNT_TR_': ['euro'], '_SELL_TR_': ['bozdur']}) )
        data.append( ('altmış isveç kronu satabilir misin maxi', 'foreign_currency_tr', {'_TARGET_AMOUNT_TR_': ['altmış isveç kronu'], '_SELL_TR_': ['satabilir']}) )
        data.append( ('amerikan dolari islemleri yapicam', 'foreign_currency_tr', {'_TARGET_AMOUNT_TR_': ['amerikan dolari']}) )
        data.append( ('dolar al 4000 liralık', 'foreign_currency_tr', {'_REF_AMOUNT_TR_': ['4000 liralık'], '_TARGET_AMOUNT_TR_': ['dolar'], '_BUY_TR_': ['al']}) )
        data.append( ('dolar gunluk kur bilgileri', 'foreign_currency_tr', {'_TARGET_AMOUNT_TR_': ['dolar']}) )
        data.append( ('hesabimdaki 3000 lirami dolarya yatir', 'foreign_currency_tr', {'_REF_AMOUNT_TR_':['3000 lirami'], '_TARGET_AMOUNT_TR_': ['dolarya'], '_BUY_TR_': ['yatir']}) )
        data.append( ('maxi şu anda doların fiyatı kaç', 'foreign_currency_tr', {'_TARGET_AMOUNT_TR_': ['doların']}) )
        data.append( ('paramı pounda çevir', 'foreign_currency_tr', {'_TARGET_AMOUNT_TR_': ['pounda'], '_BUY_TR_': ['çevir']}) )
        data.append( ('10 dolar tl cinsinden ne kadar', 'foreign_currency_tr', {'_REF_AMOUNT_TR_': ['10 dolar'], '_TARGET_AMOUNT_TR_': ['tl']}) )
        data.append( ('150dolar bozmak istiyorum', 'foreign_currency_tr', {'_TARGET_AMOUNT_TR_': ['150dolar'], '_SELL_TR_': ['bozmak']}) )
        data.append( ('20 dolarlık tl alsana', 'foreign_currency_tr', {'_REF_AMOUNT_TR_': ['20 dolarlık'],'_TARGET_AMOUNT_TR_': ['tl'], '_BUY_TR_': ['alsana']}) )
        data.append( ('20 dolarlık tl satsana', 'foreign_currency_tr', {'_REF_AMOUNT_TR_': ['20 dolarlık'],'_TARGET_AMOUNT_TR_': ['tl'], '_SELL_TR_': ['satsana']}) )
        data.append( ('200 tl lik usd bozdurmak istiyorum', 'foreign_currency_tr', {'_REF_AMOUNT_TR_': ['200 tl'], '_TARGET_AMOUNT_TR_': ['usd'], '_SELL_TR_': ['bozdurmak']}) )
        data.append( ('550 tl\'yi dolar hesabıma yatırır mısın', 'foreign_currency_tr', {'_TARGET_AMOUNT_TR_': ['dolar'], '_REF_AMOUNT_TR_': ["550 tl'yi"], '_BUY_TR_': ['yatırır']}) )
        data.append( ('bin liramı euro\'ya çevir', 'foreign_currency_tr', {'_REF_AMOUNT_TR_': ['bin liramı'], '_TARGET_AMOUNT_TR_': ["euro\'ya"], '_BUY_TR_': ['çevir']}) )
        data.append( ('hesabimdaki 3000 lirami dolarya yatir', 'foreign_currency_tr', {'_REF_AMOUNT_TR_': ['3000 lirami'], '_TARGET_AMOUNT_TR_': ['dolarya'], '_BUY_TR_': ['yatir']}) )
        data.append( ('hesabımdaki bin lirayla isviçre frangı almak istiyorum', 'foreign_currency_tr', {'_REF_AMOUNT_TR_': ['bin lirayla'], '_TARGET_AMOUNT_TR_': ['isviçre frangı'], '_BUY_TR_': ['almak']}) )
        data.append( ('usd al dört bin liralik', 'foreign_currency_tr', {'_REF_AMOUNT_TR_':['dört bin liralik'], '_TARGET_AMOUNT_TR_': ['usd',], '_BUY_TR_': ['al']}) )
        data.append( ('üç yüz türk lirasını sterlin\'e çevir', 'foreign_currency_tr', {'_REF_AMOUNT_TR_':["üç yüz türk lirasını"],'_TARGET_AMOUNT_TR_': ["sterlin\'e"], '_BUY_TR_': ['çevir']}) )
        data.append( ('10 dolarlık tl saticam', 'foreign_currency_tr', {'_REF_AMOUNT_TR_':['10 dolarlık'], '_TARGET_AMOUNT_TR_': ['tl'], '_SELL_TR_': ['saticam']}) )
        data.append( ('yüz lira degerinde dolar al', 'foreign_currency_tr', {'_TARGET_AMOUNT_TR_':['dolar'], '_REF_AMOUNT_TR_': ['yüz lira'], '_BUY_TR_': ['al']}) )
        
        # term_deposit_calculation_tr
        data.append( ('1000 liraya 1 yil faiz', 'term_deposit_calculation_tr', {'_TYPE_': ['liraya'], '_AMOUNT_': ['1000'], '_DATE_YEAR_': ['1']}) )
        data.append( ('1000 liraya 6 ay vade', 'term_deposit_calculation_tr', {'_TYPE_': ['liraya'], '_AMOUNT_': ['1000'], '_DATE_MONTH_': ['6']}) )
        data.append( ('1000 liraya 1 ay icin ne kadar gelir elde ederim', 'term_deposit_calculation_tr', {'_AMOUNT_': ['1000'], '_TYPE_': ['liraya'], '_DATE_MONTH_': ['1']}) )
        data.append( ('1 yıl 10 ay 30 gün vadeli faiz hesapla', 'term_deposit_calculation_tr', {'_DATE_MONTH_': ['10'], '_DATE_YEAR_': ['1'], '_DATE_DAY_': ['30']}) )
        data.append( ('1 yıl 10 ay 30 gün otuz bin tl vadeli faiz hesapla', 'term_deposit_calculation_tr', {'_TYPE_': ['tl'], '_AMOUNT_': ['otuz bin'], '_DATE_MONTH_': ['10'], '_DATE_YEAR_': ['1'], '_DATE_DAY_': ['30']}) )
        data.append( ('1 ayda yirmi bin lira ne kadar faiz kazanirim' , 'term_deposit_calculation_tr', {'_TYPE_': ['lira'], '_AMOUNT_': ['yirmi bin'], '_DATE_YEAR_': ['1']}) )
        data.append( ('1 ayda 20000 lira ne kadar faiz kazanirim' , 'term_deposit_calculation_tr', {'_TYPE_': ['lira'], '_AMOUNT_': ['20000'], '_DATE_MONTH_': ['1']}) )
        data.append( ('20000 lira 1 ayda ne kadar faiz kazanirim' , 'term_deposit_calculation_tr', {'_TYPE_': ['lira'], '_AMOUNT_': ['20000'], '_DATE_MONTH_': ['1']}) )
        data.append( ('20000 liraya 1 ayda ne kadar faiz kazanirim' , 'term_deposit_calculation_tr', {'_TYPE_': ['liraya'], '_AMOUNT_': ['20000'], '_DATE_MONTH_': ['1']}) )
        data.append( ('yirmi bin turk lirasina 1 ayda ne kadar faiz kazanirim' , 'term_deposit_calculation_tr', {'_TYPE_': ['turk lirasina'], '_AMOUNT_': ['yirmi bin'], '_DATE_MONTH_': ['1']}) )
        data.append( ('yirmi bin 1 ayda ne kadar faiz kazanirim' , 'term_deposit_calculation_tr', {'_AMOUNT_': ['yirmi bin'], '_DATE_MONTH_': ['1']}) )
        data.append( ('1 milyon tl param var vadeli hesap bir ayda ne getirir', 'term_deposit_calculation_tr', {'_TYPE_': ['tl'], '_AMOUNT_': ['1000000'], '_DATE_MONTH_': ['bir']}) )
        data.append( ('10 bin eur yatırsam yılda kazanırım', 'term_deposit_calculation_tr', {'_AMOUNT_': ['10 bin'], '_TYPE_': ['eur'], '_DATE_YEAR_': ['yılda']}) )
        data.append( ('10bin sterlin yatırsam ayda kazanırım', 'term_deposit_calculation_tr', {'_TYPE_': ['sterlin'], '_AMOUNT_': ['10bin'], '_DATE_MONTH_': ['ayda']}) )
        data.append( ('100 tl ye ne kadar faiz veriyorsunuz günlük', 'term_deposit_calculation_tr', {'_TYPE_': ['tl'], '_AMOUNT_': ['100'], '_DATE_DAY_':['günlük']}) )
        data.append( ('100.000 uzeri vadeli hesapta nekadar faiz uygulaniyor', 'term_deposit_calculation_tr', {'_AMOUNT_': ['100.000']}) )
        data.append( ('5000 usd 32 gün', 'term_deposit_calculation_tr', {'_AMOUNT_': ['5000'], '_TYPE_': ['usd'], '_DATE_DAY_': ['32']}) )
        data.append( ('bi milyon aylık getirisi', 'term_deposit_calculation_tr', {'_AMOUNT_': ['bi milyon'], '_DATE_MONTH_': ['aylık'],}) )
        data.append( ('bi trilyon ayık getiri', 'term_deposit_calculation_tr', {'_AMOUNT_': ['bi trilyon'], '_DATE_MONTH_': ['aylık'],}) )
        data.append( ('kırk bin tele yatırsam ne kadar faiz alabillirim', 'term_deposit_calculation_tr', {'_TYPE_': ['tele'], '_AMOUNT_': ['kırk bin']}) )
        data.append( ('10 bin eur ile ayda kazanırım', 'term_deposit_calculation_tr', {'_AMOUNT_': ['10 bin'], '_TYPE_': ['eur'], '_DATE_MONTH_': ['ayda']}) )
        data.append( ('10.000 tl ye kaç tl faiz veriliyor', 'term_deposit_calculation_tr', {'_AMOUNT_': ['10.000'], '_TYPE_': ['tl']}) )
        data.append( ('1000 liranın 28 gündeki getirisi nedir', 'term_deposit_calculation_tr', {'_TYPE_': ['liranın'], '_AMOUNT_': ['1000'], '_DATE_DAY_': ['28']}) )
        data.append( ('47580 tlnin 32 günlük faizi ne kadardır', 'term_deposit_calculation_tr', {'_TYPE_': ['tlnin'], '_AMOUNT_': ['47580'], '_DATE_DAY_': ['32']}) )
        data.append( ('50.000 TL \'ye ne faiz veriyorsunuz', 'term_deposit_calculation_tr', {'_TYPE_': ['TL'], '_AMOUNT_': ['50.000']}) )
        data.append( ('peki 30 bin tl ye 12 ne kadar', 'term_deposit_calculation_tr', {'_TYPE_': ['tl'], '_AMOUNT_': ['30 bin']}) )
        data.append( ('vadeli tl faiz oranlarınız nedir', 'term_deposit_calculation_tr', {'_TYPE_': ['tl'],}) )
        data.append( ('vadeli usd', 'term_deposit_calculation_tr', {'_TYPE_': ['usd']}) )
        data.append( ('100 bın tl 31 gunde alacagım faız tutarı nedır', 'term_deposit_calculation_tr', {'_TYPE_': ['tl'], '_AMOUNT_': ['100 bın'], '_DATE_DAY_': ['31']}) )
        data.append( ('250bin 32gun faizi', 'term_deposit_calculation_tr', {'_AMOUNT_': ['250bin'], '_DATE_DAY_': ['32gun']}) )
        data.append( ('beş bin lira için otuz iki gün vadeli mevduat faiz', 'term_deposit_calculation_tr', {'_TYPE_': ['lira'], '_AMOUNT_': ['beş bin'], '_DATE_DAY_': ['otuz iki']}) )
        data.append( ('tamam yirmi sekiz günlük olursa ne kadar faiz gelir', 'term_deposit_calculation_tr', {'_DATE_DAY_': ['yirmi sekiz']}) )
        data.append( ('10 bin eur ile ayda kazanırım', 'term_deposit_calculation_tr', {'_TYPE_': ['eur'], '_AMOUNT_': ['10 bin'], '_DATE_MONTH_': ['ayda']}) )
        data.append( ('5000 bin doların aylık faizi ne dir', 'term_deposit_calculation_tr', {'_TYPE_': ['doların'], '_AMOUNT_': ['5000 bin'], '_DATE_MONTH_': ['aylık']}) )
        data.append( ('1 senelik 6500 tl vadelli faiz ne kadardir', 'term_deposit_calculation_tr', {'_TYPE_': ['tl'], '_AMOUNT_': ['6500'], '_DATE_YEAR_': ['1']}) )
        data.append( ('100 bin lira yatırsam yıllık kazancım', 'term_deposit_calculation_tr', {'_TYPE_': ['lira'], '_AMOUNT_': ['100 bin'], '_DATE_YEAR_': ['yıllık']}) )
        data.append( ('1000 liranin 1 senede ki getirisi nedir', 'term_deposit_calculation_tr', {'_TYPE_': ['liranin'], '_AMOUNT_': ['1000'], '_DATE_YEAR_': ['1']}) )
        data.append( ('50 000 tl senelik nekadar faiz veriliyorr', 'term_deposit_calculation_tr', {'_TYPE_': ['tl'], '_AMOUNT_': ['50 000'], '_DATE_YEAR_': ['senelik']}) )
        data.append( ('faiz yıllık getiri', 'term_deposit_calculation_tr', {'_DATE_YEAR_': ['yıllık']}) )
        data.append( ('bana faiz hesapla', 'term_deposit_calculation_tr', {}) )
        data.append( ('bana mevduat getiri hesaplamasi yap', 'term_deposit_calculation_tr', {}) )
        
        # loan_application_tr
        data.append( ('1000 lira 4 ay krediye ne kadar faiz olur', 'loan_application_tr', {'_CURRENCY_': ['lira'], '_AMOUNT_': ['1000'], '_DATE_MONTH_': ['4']}) )
        data.append( ('50.000 lira kredi cekmek istiyorum, 12 ay vadeli olsun', 'loan_application_tr', {'_CURRENCY_': ['lira'], '_AMOUNT_': ['50000'], '_DATE_MONTH_': ['12']}) )
        data.append( ('10000 tl kredi cekmek istiyorum 12 ay icin', 'loan_application_tr', {'_CURRENCY_': ['tl'], '_AMOUNT_': ['10000'], '_DATE_MONTH_': ['12']}) )
        data.append( ('360 gun 20000 lira kredi' , 'loan_application_tr', {'_CURRENCY_': ['lira'], '_AMOUNT_': ['20000'], '_DATE_DAY_': ['360']}) )
        data.append( ('bin ne kadar faiz kazanirim' , 'loan_application_tr', {'_AMOUNT_': ['bin']}) )
        data.append( ('10.000 lira şirket için kıredi çekeceğim' , 'loan_application_tr', {'_CURRENCY_': ['lira'], '_AMOUNT_': ['10000'], '_CREDIT_TYPE_': ['şirket']}) )
        data.append( ('10 bin bireysel kredi cekebilirmiyim', 'loan_application_tr', {'_AMOUNT_': ['10 bin'], '_CREDIT_TYPE_': ['bireysel']}) )
        data.append( ('10 bin ihtiyac kiredisine ne kadar ödeme yaparim', 'loan_application_tr', {'_AMOUNT_': ['10 bin'], '_CREDIT_TYPE_': ['ihtiyac']}) )
        data.append( ('10 bin tele ihtiyac bireysel ihtiyac kredisi almak istiyom', 'loan_application_tr', {'_CURRENCY_': ['tele'], '_AMOUNT_': ['10 bin'], '_CREDIT_TYPE_': ['ihtiyac bireysel ihtiyac']}) )
        data.append( ('10.000 lira ticari kredi ver', 'loan_application_tr', {'_CURRENCY_': ['lira'], '_AMOUNT_': ['10000'], '_CREDIT_TYPE_': ['ticari']}) )
        data.append( ('10000 TL işyeri kredisi verebilir misiniz', 'loan_application_tr', {'_CURRENCY_': ['TL'], '_AMOUNT_': ['10000'], '_CREDIT_TYPE_': ['işyeri']}) )
        data.append( ('20bin alışveriş kredisi', 'loan_application_tr', {'_AMOUNT_': ['20bin'], '_CREDIT_TYPE_': ['alışveriş']}) )
        data.append( ('40.bintl 3 yıl ticari kredi çeksem faizim be olur', 'loan_application_tr', {'_AMOUNT_': ['40.bintl'], '_CREDIT_TYPE_': ['ticari'], '_DATE_YEAR_': ['3']}) )
        data.append( ('aninda ticari kirediden 1000 cekmek istiyorum', 'loan_application_tr', {'_AMOUNT_': ['1000'], '_CREDIT_TYPE_': ['ticari']}) )
        data.append( ('anında ticari krefi', 'loan_application_tr', {'_CREDIT_TYPE_': ['ticari']}) )
        data.append( ('anında ticari kırediye nasıl başvurulur', 'loan_application_tr', {'_CREDIT_TYPE_': ['ticari']}) )
        data.append( ('arac kredisi basvurusu', 'loan_application_tr', {'_CREDIT_TYPE_': ['arac']}) )
        data.append( ('atk', 'loan_application_tr', {'_CREDIT_TYPE_': ['atk']}) )
        data.append( ('atk almak istiyorum', 'loan_application_tr', {'_CREDIT_TYPE_': ['atk']}) )
        data.append( ('atkk', 'loan_application_tr', {'_CREDIT_TYPE_': ['atkk']}) )
        data.append( ('bana ne kadar bireysel kredi cikar', 'loan_application_tr', {'_CREDIT_TYPE_': ['bireysel']}) )
        data.append( ('bana konut kredısı cıkar mo', 'loan_application_tr', {'_CREDIT_TYPE_': ['konut']}))
        data.append( ('bayram kredisi muracaat son gun', 'loan_application_tr', {'_CREDIT_TYPE_': ['bayram']}) )
        data.append( ('bir yıllık vadeli ticari kredi lazım', 'loan_application_tr', {'_CREDIT_TYPE_': ['ticari'], '_DATE_YEAR_': ['bir']}) )
        data.append( ('esnaf ticari kiredi basvuru', 'loan_application_tr', {'_CREDIT_TYPE_': ['esnaf ticari']}) )
        data.append( ('hizli ticari kredi', 'loan_application_tr', {'_CREDIT_TYPE_': ['ticari']}) )
        data.append( ('ihtiyaç', 'loan_application_tr', {'_CREDIT_TYPE_': ['ihtiyaç']}) )
        data.append( ('ihtiyaç kredisi yirmi bin TL hesaplar mısın', 'loan_application_tr', {'_CREDIT_TYPE_': ['ihtiyaç'], '_AMOUNT_': ['yirmi bin'], '_CURRENCY_': ['TL']}) )
        data.append( ('işyeri krdisi kulanmAk istiyorum', 'loan_application_tr', {'_CREDIT_TYPE_': ['işyeri']}) )
        data.append( ('işyeri kiresisi cekmek istiuorum', 'loan_application_tr', {'_CREDIT_TYPE_': ['işyeri']}) )
        data.append( ('Tasit kredisi hakkında bilgi alacaktım', 'loan_application_tr', {'_CREDIT_TYPE_': ['tasit']}))
        data.append( ('taşıt kedisi bas vuruşu yapcam', 'loan_application_tr', {'_CREDIT_TYPE_': ['taşıt']}) )
        data.append( ('şirket kıradisi çekebiliri', 'loan_application_tr', {'_CREDIT_TYPE_': ['şirket']}) )
        data.append( ('10.000 lira 36 ay vadeli kredi çekmek istiyorum', 'loan_application_tr', {'_CURRENCY_': ['lira'], '_AMOUNT_': ['10.000'], '_DATE_MONTH_': ['36']}) )
        data.append( ('10000 tl yi 24 ay taksit yapsak', 'loan_application_tr', {'_CURRENCY_': ['tl'], '_AMOUNT_': ['10000'], '_DATE_MONTH_': ['24']}) )
        data.append( ('100000 120 ay kredi', 'loan_application_tr', {'_AMOUNT_': ['100000'], '_DATE_MONTH_': ['120']}) )
        data.append( ('160 ay veda olursa aylik kredi odemem nasil olur', 'loan_application_tr', {'_DATE_MONTH_': ['160']}) )
        data.append( ('18 bin kredı cekcek nekadar faıı var taksıtler kac kac 15 aylık 12 aylık 18 aylık', 'loan_application_tr', {'_AMOUNT_': ['18 bin'], '_DATE_MONTH_': ['15', '12', '18']}) )
        data.append( ('2 ay 2000 euro kıredi', 'loan_application_tr', {'_CURRENCY_': ['EUR'], '_AMOUNT_': ['2000'], '_DATE_MONTH_': ['2']}) )
        data.append( ('22000 tl ihtiyat kredisi düşünüyorum 24 ay ödeme ile', 'loan_application_tr', {'_CURRENCY_': ['tl'], '_AMOUNT_': ['22000'], '_CREDIT_TYPE_': ['ihtiyat'], '_DATE_MONTH_': ['24']}) )
        data.append( ('on iki ay yirmi dört bin lira kredi', 'loan_application_tr', {'_CURRENCY_': ['lira'], '_AMOUNT_': ['yirmi dört bin'], '_DATE_MONTH_': ['on iki']}) )
        data.append( ('20bin 4 yıl kredi başrusu', 'loan_application_tr', {'_AMOUNT_': ['20bin'], '_DATE_YEAR_': ['4']}) )
        data.append( ('bir yil icinde odeyecegim bireysel kredi', 'loan_application_tr', {'_CREDIT_TYPE_': ['bireysel'], '_DATE_YEAR_': ['bir']}) )
        data.append( ('500000 tl kredi alırsam 1825 günde kaç tl faiz ödüyorum', 'loan_application_tr', {'_CURRENCY_': ['tl'], '_AMOUNT_': ['500000'], '_DATE_DAY_': ['1825']}) )
        data.append( ('10 bin kobi kiredisi cekebilirmiyim', 'loan_application_tr', {'_AMOUNT_': ['10 bin'], '_CREDIT_TYPE_': ['kobi']}) )
        data.append( ('10.000 tl 48 ay ticari kredi ver', 'loan_application_tr', {'_CURRENCY_': ['tl'], '_AMOUNT_': ['10.000'], '_DATE_MONTH_': ['48']}) )
        data.append( ('35000 5 yıl ticari kredi talebi', 'loan_application_tr', {'_AMOUNT_': ['35000'], '_CREDIT_TYPE_': ['ticari'], '_DATE_YEAR_': ['5']}) )
        data.append( ('acil 23bin kredi lazim', 'loan_application_tr', {'_AMOUNT_': ['23bin']}) )
        data.append( ('altı ay yetmiş sekiz bin lira kredi', 'loan_application_tr', {'_CURRENCY_': ['lira'], '_AMOUNT_': ['yetmiş sekiz bin'], '_DATE_MONTH_': ['altı']}) )
        data.append( ('on iki ay sekiz bin sekiz yüz seksen lira kredi', 'loan_application_tr', {'_CURRENCY_': ['lira'], '_AMOUNT_': ['sekiz bin sekiz yüz seksen'], '_DATE_MONTH_': ['on iki']}) )
        data.append( ('şipşak 10bin kredi', 'loan_application_tr', {'_AMOUNT_': ['10bin']}) )
        data.append( ('10 bin tele ihtiyac kıredisi almak istiyom', 'loan_application_tr', {'_CURRENCY_': ['tele'], '_AMOUNT_': ['10 bin'], '_CREDIT_TYPE_': ['ihtiyac']}) )
        data.append( ('2 ay 2000 euro kredi', 'loan_application_tr', {'_CURRENCY_': ['EUR'], '_AMOUNT_': ['2000'], '_DATE_MONTH_': ['2']}) )
        data.append( ('20000 tl kredi almak istiyorum', 'loan_application_tr', {'_CURRENCY_': ['tl'], '_AMOUNT_': ['20000']}) )
        data.append( ('600000 TL kredi cekecegim 36 ay vade ile', 'loan_application_tr', {'_CURRENCY_': ['TL'], '_AMOUNT_': ['600000'], '_DATE_MONTH_': ['36']}) )
        data.append( ('bana kredi hesapla', 'loan_application_tr', {}) )
        data.append( ('kredi basvurusunu istiyorum', 'loan_application_tr', {}) )


        # spendadvice_tr
        data.append( ('bu ay kac liralik benzin alabilirim', 'spendadvice_tr', {'_TARGET_SVP_': ['benzin']}) )
        data.append( ('bu ay benzine en fazla ne kadar harcayabilirim', 'spendadvice_tr', {'_TARGET_SVP_': ['benzine']}) )
        data.append( ('bu ay benzine 1000 lira harcayabilirim', 'spendadvice_tr', {'_AMOUNT_TR_': ['1000 lira'], '_TARGET_SVP_': ['benzine'], '_MONEY_': [{'tokens': '1000 lira', 'numbers': [{'value': 1000, 'tokens': '1000'}], 'value': 1000, 'currency': 'lira', 'svp_tokens': '1000 lira'}]}) )
        data.append( ('1000tl harcayabilir miyim', 'spendadvice_tr', {'_AMOUNT_TR_': ['1000tl'], '_MONEY_': [{'tokens': '1000tl', 'numbers': [{'value': 1000, 'tokens': '1000'}], 'value': 1000, 'currency': 'lira', 'svp_tokens': '1000tl'}]}) )
        data.append( ('1300tl sınav ücreti ödemem bu ay ki harcamalarımı nasıl etkiler ?', 'spendadvice_tr', {'_AMOUNT_TR_': ['1300tl'], '_TARGET_SVP_': ['sınav'], '_MONEY_': [{'tokens': '1300tl', 'numbers': [{'value': 1300, 'tokens': '1300'}], 'value': 1300, 'currency': 'lira', 'svp_tokens': '1300tl'}]}) )
        data.append( ('250₺’lik züccaciye alisverisimi kredi kartindan ödeyebilirmiyim ?', 'spendadvice_tr', { '_AMOUNT_TR_': ['250₺'], '_TARGET_SVP_': ['züccaciye'], '_MONEY_': [{'tokens': '250₺', 'numbers': [{'value': 250, 'tokens': '250'}], 'value': 250, 'currency': 'lira', 'svp_tokens': '250₺'}]}) )
        data.append( ('50 liralık benzin alabilir miyim?', 'spendadvice_tr', {'_AMOUNT_TR_': ['50 liralık'], '_TARGET_SVP_': ['benzin'], '_MONEY_': [{'tokens': '50 liralık', 'numbers': [{'value': '50', 'tokens': '50'}], 'value': '50', 'currency': 'liralık', 'svp_tokens': '50 liralık'}]}) )
        data.append( ('acil DIGDIGDIG lira lazım var mı ?', 'spendadvice_tr', {'_AMOUNT_TR_': ['DIGDIGDIG lira'], '_MONEY_': [{'tokens': 'DIGDIGDIG lira', 'numbers': [{'value': 'DIGDIGDIG', 'tokens': 'DIGDIGDIG'}], 'value': 'DIGDIGDIG', 'currency': 'lira', 'svp_tokens': 'DIGDIGDIG lira'}]}) )
        data.append( ('altı yüz lira harcayabilir miyim', 'spendadvice_tr', {'_AMOUNT_TR_': ['altı yüz lira'], '_MONEY_': [{'tokens': 'altı yüz lira', 'numbers': [{'value': 600, 'tokens': '600'}], 'value': 600, 'currency': 'lira', 'svp_tokens': 'altı yüz lira'}]}) )
        data.append( ('arkadaşlarla kahvaltıya gideceğim . DIGDIGDIG tl yeter mi ?', 'spendadvice_tr', {'_AMOUNT_TR_': ['DIGDIGDIG tl'], '_TARGET_SVP_': ['kahvaltıya'], '_MONEY_': [{'tokens': 'DIGDIGDIG tl', 'numbers': [{'value': 'DIGDIGDIG', 'tokens': 'DIGDIGDIG'}], 'value': 'DIGDIGDIG', 'currency': 'tl', 'svp_tokens': 'DIGDIGDIG tl'}]}) )
        data.append( ('aylık bilançoya göre takım elbiseye 800tl ayırabiliyor muyum ?', 'spendadvice_tr', {'_AMOUNT_TR_': ['800tl'], '_TARGET_SVP_': ['takım elbiseye'], '_MONEY_': [{'tokens': '800tl', 'numbers': [{'value': 800, 'tokens': '800'}], 'value': 800, 'currency': 'lira', 'svp_tokens': '800tl'}]}) )
        data.append( ('DIG liraya pokemon almam hakkında ne düşünüyorsun', 'spendadvice_tr', {'_AMOUNT_TR_': ['DIG liraya'], '_TARGET_SVP_': ['pokemon'], '_MONEY_': [{'tokens': 'DIG liraya', 'numbers': [{'value': 'DIG', 'tokens': 'DIG'}], 'value': 'DIG', 'currency': 'liraya', 'svp_tokens': 'DIG liraya'}]}) )
        data.append( ('DIG.DIGDIGDIG liralık mobilya satın alabilir miyim ?', 'spendadvice_tr', { '_AMOUNT_TR_': ['DIG.DIGDIGDIG liralık'], '_TARGET_SVP_': ['mobilya'], '_MONEY_': [{'tokens': 'DIG.DIGDIGDIG liralık', 'numbers': [{'value': 'DIG.DIGDIGDIG', 'tokens': 'DIG.DIGDIGDIG'}], 'value': 'DIG.DIGDIGDIG', 'currency': 'liralık', 'svp_tokens': 'DIG.DIGDIGDIG liralık'}]}) )
        data.append( ('harcamak için DIGDIG liram var mı ?', 'spendadvice_tr', {'_AMOUNT_TR_': ['DIGDIG liram'], '_MONEY_': [{'tokens': 'DIGDIG liram', 'numbers': [{'value': 'DIGDIG', 'tokens': 'DIGDIG'}], 'value': 'DIGDIG', 'currency': 'liram', 'svp_tokens': 'DIGDIG liram'}]}) )
        data.append( ('itunes\'a DIGDIG tl harcama yapabilecek bütçem var mı ?', 'spendadvice_tr', {'_AMOUNT_TR_': ['DIGDIG tl'], '_TARGET_SVP_': ["itunes'a"], '_MONEY_': [{'tokens': 'DIGDIG tl', 'numbers': [{'value': 'DIGDIG', 'tokens': 'DIGDIG'}], 'value': 'DIGDIG', 'currency': 'tl', 'svp_tokens': 'DIGDIG tl'}]}) )
        data.append( ('kredi kartimdan DIGDIGDIG tl lik bot alabilirmiyim', 'spendadvice_tr', {'_AMOUNT_TR_': ['DIGDIGDIG tl'], '_TARGET_SVP_': ['bot'], '_MONEY_': [{'tokens': 'DIGDIGDIG tl', 'numbers': [{'value': 'DIGDIGDIG', 'tokens': 'DIGDIGDIG'}], 'value': 'DIGDIGDIG', 'currency': 'tl', 'svp_tokens': 'DIGDIGDIG tl'}]}) )
        data.append( ('kredi kartim harcama limitim doldu fakat ben DIGDIGDIG tl\'lik benzin almak istiyorum mümkün mü ?', 'spendadvice_tr', {'_AMOUNT_TR_': ["DIGDIGDIG tl'lik"], '_TARGET_SVP_': ['benzin'], '_MONEY_': [{'tokens': "DIGDIGDIG tl'lik", 'numbers': [{'value': 'DIGDIGDIG', 'tokens': 'DIGDIGDIG'}], 'value': 'DIGDIGDIG', 'currency': "tl'lik", 'svp_tokens': "DIGDIGDIG tl'lik"}]}) )
        data.append( ('market ten DIGDIGDIG tl lik erzak alışverişi yapabilir miyim ?', 'spendadvice_tr', {'_AMOUNT_TR_': ['DIGDIGDIG tl'], '_TARGET_SVP_': ['market', 'erzak alışverişi'], '_MONEY_': [{'tokens': 'DIGDIGDIG tl', 'numbers': [{'value': 'DIGDIGDIG', 'tokens': 'DIGDIGDIG'}], 'value': 'DIGDIGDIG', 'currency': 'tl', 'svp_tokens': 'DIGDIGDIG tl'}]}) )
        data.append( ('taksitle DIGDIGDIG liralık bir çanta alışverişi bütçem var mı ?', 'spendadvice_tr', {'_AMOUNT_TR_': ['DIGDIGDIG liralık'], '_TARGET_SVP_': ['çanta alışverişi'], '_MONEY_': [{'tokens': 'DIGDIGDIG liralık', 'numbers': [{'value': 'DIGDIGDIG', 'tokens': 'DIGDIGDIG'}], 'value': 'DIGDIGDIG', 'currency': 'liralık', 'svp_tokens': 'DIGDIGDIG liralık'}]}) )
        data.append( ('yaz tatilinde DIGDIGDIGDIG liralık bir tatil yapabilir miyim ?', 'spendadvice_tr', {'_AMOUNT_TR_': ['DIGDIGDIGDIG liralık'], '_TARGET_SVP_': ['tatil'], '_MONEY_': [{'tokens': 'DIGDIGDIGDIG liralık', 'numbers': [{'value': 'DIGDIGDIGDIG', 'tokens': 'DIGDIGDIGDIG'}], 'value': 'DIGDIGDIGDIG', 'currency': 'liralık', 'svp_tokens': 'DIGDIGDIGDIG liralık'}]}) )
        data.append( ('1300tl sınav ücreti ödemem bu ay ki harcamalarımı nasıl etkiler ?', 'spendadvice_tr', {'_AMOUNT_TR_': ['1300tl'], '_TARGET_SVP_': ['sınav'], '_MONEY_': [{'tokens': '1300tl', 'numbers': [{'value': 1300, 'tokens': '1300'}], 'value': 1300, 'currency': 'lira', 'svp_tokens': '1300tl'}]}) )
        data.append( ('akşam etkinliği yaparsam ne kadarlık harcama yaparım ?', 'spendadvice_tr', {'_TARGET_SVP_': ['etkinliği']}) )
        data.append( ('amazon haramalarım ne kadar olabilir ?', 'spendadvice_tr', {'_TARGET_SVP_': ['amazon']}) )
        data.append( ('ankaragücü kombinesi DIGDIGDIGDIG tl . benim bütçem var mı ?', 'spendadvice_tr', {'_AMOUNT_TR_': ['DIGDIGDIGDIG tl'], '_TARGET_SVP_': ['ankaragücü kombinesi'], '_MONEY_': [{'tokens': 'DIGDIGDIGDIG tl', 'numbers': [{'value': 'DIGDIGDIGDIG', 'tokens': 'DIGDIGDIGDIG'}], 'value': 'DIGDIGDIGDIG', 'currency': 'tl', 'svp_tokens': 'DIGDIGDIGDIG tl'}]}) )
        data.append( ('araba almayı karşılayabilir miyim ?', 'spendadvice_tr', {'_TARGET_SVP_': ['araba']}) )
        data.append( ('arabama ne kadarlık benzin alabilirim ?', 'spendadvice_tr', {'_TARGET_SVP_': ['benzin']}) )
        data.append( ('arkadaşlarla kahvaltıya gideceğim . DIGDIGDIG tl yeter mi ?', 'spendadvice_tr', {'_AMOUNT_TR_': ['DIGDIGDIG tl'], '_TARGET_SVP_': ['kahvaltıya'], '_MONEY_': [{'tokens': 'DIGDIGDIG tl', 'numbers': [{'value': 'DIGDIGDIG', 'tokens': 'DIGDIGDIG'}], 'value': 'DIGDIGDIG', 'currency': 'tl', 'svp_tokens': 'DIGDIGDIG tl'}]}) )
        data.append( ('arkadaşıma hediye almak için ne kadar bütçem var ?', 'spendadvice_tr', {'_TARGET_SVP_': ['hediye']}) )
        data.append( ('atasun optiğe verebileceğim tutar ne olur ?', 'spendadvice_tr', {'_TARGET_SVP_': ['atasun optiğe']}) )
        data.append( ('avrupa tatili düşünüyorum . bir haftalık , her şey dahil ne kadar harcayabiliriz ?', 'spendadvice_tr', {'_TARGET_SVP_': ['tatili']}) )
        data.append( ('aynı kirayı vermeye devam edebilir miyim ?', 'spendadvice_tr', {'_TARGET_SVP_': ['kirayı']}) )
        data.append( ('bilekliğe DIGDIGDIG lira verebilir miyim ?', 'spendadvice_tr', {'_AMOUNT_TR_': ['DIGDIGDIG lira'], '_TARGET_SVP_': ['bilekliğe'], '_MONEY_': [{'tokens': 'DIGDIGDIG lira', 'numbers': [{'value': 'DIGDIGDIG', 'tokens': 'DIGDIGDIG'}], 'value': 'DIGDIGDIG', 'currency': 'lira', 'svp_tokens': 'DIGDIGDIG lira'}]}) )
        data.append( ('bu akşam konferans sonrası lüks bir restoranta gideceğim . ne kadar harcayabilirim ?', 'spendadvice_tr', {'_TARGET_SVP_': ['restoranta']}) )
        data.append( ('bu ay gsm operatörüm için ne kadar harcayabilirim ?', 'spendadvice_tr', {'_TARGET_SVP_': ['gsm']}) )
        data.append( ('evleneceğim , mobilyalar için ne kadar ayırabilirim ?', 'spendadvice_tr', {'_TARGET_SVP_': ['mobilyalar']}) )
        data.append( ('hafta sonu gezmek için yeterli bütçem var mıdır ?', 'spendadvice_tr', {'_TARGET_SVP_': ['gezmek']}) )
        data.append( ('hafta sonu kaçamak yapabilmem için ne kadar harcarım', 'spendadvice_tr', {'_TARGET_SVP_': ['kaçamak']}) )
        data.append( ('lc waikiki de en fazla ne kadar harcayabilirim .', 'spendadvice_tr', {'_TARGET_SVP_': ['lc waikiki']}) )
        data.append( ('opet\'te nekadarlik benzin alabilirim', 'spendadvice_tr', {'_TARGET_SVP_': ["opet'te", 'benzin']}) )
        data.append( ('oğlumu özel okula yazdırabilir miyim ?', 'spendadvice_tr', {'_TARGET_SVP_': ['özel okula']}) )


        # campaign_tr
        data.append( ('boyner kampanyalari neler', 'campaign_tr', {'_TARGET_TR_': ['boyner']}) )
        data.append( ('katildigim shell kampanyalari neler', 'campaign_tr', {'_JOINED_TR_': ['katildigim'], '_TARGET_TR_': ['shell']}) )
        data.append( ('is bankali calısan icin kampanyalari listele', 'campaign_tr', {'_STAFF_TR_': ['is bankali calısan']}) )
        data.append( ('başvurduğum kampanya', 'campaign_tr', {'_JOINED_TR_': ['başvurduğum']}) )
        data.append( ('daha önce katıldığım kampanyalar', 'campaign_tr', {'_JOINED_TR_': ['katıldığım']}) )
        data.append( ('kampanya katıldıklarım', 'campaign_tr', {'_JOINED_TR_': ['katıldıklarım']}) )
        data.append( ('katıldığım kampanyaları sırala', 'campaign_tr', {'_JOINED_TR_': ['katıldığım']}) )
        data.append( ('calısan kampanyalari goster', 'campaign_tr', {'_STAFF_TR_': ['calısan']}) )
        data.append( ('iş ailem kampanyaları listele', 'campaign_tr', {'_STAFF_TR_': ['iş ailem']}) )
        data.append( ('mensup kampamya', 'campaign_tr', {'_STAFF_TR_': ['mensup']}) )
        data.append( ('üye kanpaya', 'campaign_tr', {'_STAFF_TR_': ['üye']}) )
        data.append( ('akaryakıt kampanyaları', 'campaign_tr', {'_TARGET_TR_': ['akaryakıt']}) )
        data.append( ('aktif cinemaximum kampanyalari', 'campaign_tr', {'_TARGET_TR_': ['cinemaximum']}) )
        data.append( ('aktif hobi kampanyalari', 'campaign_tr', {'_TARGET_TR_': ['hobi']}) )
        data.append( ('atasun optik kampanyasını göster', 'campaign_tr', {'_TARGET_TR_': ['atasun optik']}) )
        data.append( ('benzin kampanyaları', 'campaign_tr', {'_TARGET_TR_': ['benzin']}) )
        data.append( ('boyner kampanyaları', 'campaign_tr', {'_TARGET_TR_': ['boyner']}) )
        data.append( ('eğitim kampanyaları', 'campaign_tr', {'_TARGET_TR_': ['eğitim']}) )
        data.append( ('hd iskender kampanyasına katılmak istiyorum', 'campaign_tr', {'_TARGET_TR_': ['hd iskender']}) )
        data.append( ('uçak kampanha', 'campaign_tr', {'_TARGET_TR_': ['uçak']}) )

        # account_tr
        data.append( ('hesabimda kac apra var', 'account_tr', {}) )
        data.append( ('degistir vadesiz hesabim', 'account_tr', {'_TYPE_': ['vadesiz']}) )
        data.append( ('vadesiz ve maas hesabimda kac para var', 'account_tr', {'_TYPE_': ['vadesiz', 'maas']}) )

        data.append( ('Ek hesap limitim ne kadardır ?', 'account_tr', {'_TYPE_': ['Ek hesap']}) )
        data.append( ('4534 ile biten kartımın bakiyesi', 'account_tr', {'_TYPE_': ['4534 ile biten kartımın']}) )
        
        data.append( ('acibadem tl hesabim', 'account_tr', {'_TYPE_': ['tl', 'acibadem']}) )
        data.append( ('Acıbadem şubesindeki dolar bakiyemi öğrenmek istiyorum', 'account_tr', {'_TYPE_': ['dolar', 'Acıbadem']}) )
        data.append( ('Akatlar şubesindeki vadeli hesabımda kaç euro var?', 'account_tr', {'_TYPE_': ['vadeli', 'euro', 'Akatlar']}) )
        data.append( ('Altin bakiyem nedir?', 'account_tr', {'_TYPE_': ['Altin']}) )
        data.append( ('Bahçelievler izmir şubesinde ne kadar dövizim var', 'account_tr', {'_TYPE_': ['dövizim', 'Bahçelievler izmir']}) )
        data.append( ('Dolar aldım nerde', 'account_tr', {'_TYPE_': ['Dolar']}) )
        data.append( ('döviz hesaplarım altın hesaplarım', 'account_tr', {'_TYPE_': ['döviz', 'altın']}) )
        data.append( ('ek heap borcum', 'account_tr', {'_TYPE_': ['ek heap']}) )
        data.append( ('Ek hesap limitim ne kadardır ?', 'account_tr', {'_TYPE_': ['Ek hesap']}) )
        data.append( ('Göztepe şubesindeki altın hesaplarımda kaç gr var', 'account_tr', {'_TYPE_': ['altın', 'Göztepe']}) )
        data.append( ('iban numaram', 'account_tr', {'_TYPE_': ['iban']}) )
        data.append( ('kaç liram var', 'account_tr', {'_TYPE_': ['liram']}) )
        data.append( ('KMH BORCU', 'account_tr', {'_TYPE_': ['KMH']}) )
        data.append( ('pound hesabımı getir', 'account_tr', {'_TYPE_': ['pound']}) )
        data.append( ('vadeli hesabimda ne kadar var', 'account_tr', {'_TYPE_': ['vadeli']}) )
        data.append( ('yatırım fonlarım ne durumda', 'account_tr', {'_TYPE_': ['yatırım']}) )
        data.append( ('maxi kredi kartım kaç para olduğunu', 'credit_card_tr', {'_TYPE_': ['maxi kredi kartım']}) )
        data.append( ('aidatsız kartımın limiti nedir', 'credit_card_tr', {'_TYPE_': ['aidatsız kartımın']}) )
        data.append( ('avro kartlarımı listele', 'credit_card_tr', {'_TYPE_': ['avro']}) )
        data.append( ('Bu ay kredi kartı borcum var mı?', 'credit_card_tr', {}) )
        data.append( ('euro kartim', 'credit_card_tr', {'_TYPE_': ['euro']}) )
        data.append( ('iş bankası ek kartımın güncel bakiyesi ne kadar?', 'credit_card_tr', {'_TYPE_': ['ek kartımın']}) )
        data.append( ('kart limitim nedir?', 'credit_card_tr', {}) )
        data.append( ('kartımın son ödeme tarihi', 'credit_card_tr', {}) )
        data.append( ('maximiles business limitimi göster', 'credit_card_tr', {'_TYPE_': ['maximiles business']}) )
        data.append( ('mercedescard borcum', 'credit_card_tr', {'_TYPE_': ['mercedescard']}) )
        data.append( ('visa yurtdışı kredi kartımın limiti kaldı mı', 'credit_card_tr', {'_TYPE_': ['visa yurtdışı']}) )

        # credit_card_tr
        data.append( ('kredi kartimda ne kadar limit var', 'credit_card_tr', {}) )
        data.append( ('kredi karti borcum ne kadar', 'credit_card_tr', {}) )

        # credit_card_payment_tr
        data.append( ('kart odemesi yapicam', 'credit_card_payment_tr', {}) )
        data.append( ('kart borcumu öde', 'credit_card_payment_tr', {}) )
        data.append( ('toplam kart borcumu öde', 'credit_card_payment_tr', {'_PAYMENT_TYPE_TR_': ['toplam']}) )
        data.append( ('kredı kartı borcumu öde', 'credit_card_payment_tr', {}) )
        data.append( ('kredi kartı borcumu öde', 'credit_card_payment_tr', {}) )
        data.append( ('200 tl maximiles kredi kartı borcumu öde', 'credit_card_payment_tr', {'_CARD_TYPE_TR_': ['maximiles'], '_AMOUNT_TR_': ['200 tl']}) )
        data.append( ('maximiles kredi kartımin asgari borcunu öde', 'credit_card_payment_tr', {'_CARD_TYPE_TR_': ['maximiles'], '_PAYMENT_TYPE_TR_': ['asgari']}) )
        data.append( ('10 lira öder misin', 'credit_card_payment_tr', {'_AMOUNT_TR_': ['10 lira']}) )
        data.append( ('100 tl yatır', 'credit_card_payment_tr', {'_AMOUNT_TR_': ['100 tl']}) )
        data.append( ('100 tl yatırırmısın', 'credit_card_payment_tr', {'_AMOUNT_TR_': ['100 tl']}) )
        data.append( ('altı yüz elli tl ödeyebilir misin', 'credit_card_payment_tr', {'_AMOUNT_TR_': ['altı yüz elli tl']}) )
        data.append( ('Banka kartımdaki 620 tl parayı kredi kartına aktarmak istiyorum', 'credit_card_payment_tr', {'_AMOUNT_TR_': ['620 tl']}) )
        data.append( ('elli TL kredi kartıma atacağım', 'credit_card_payment_tr', {'_AMOUNT_TR_': ['elli TL']}) )
        data.append( ('kartimin 600 tl borcunu odemek istiyorum', 'credit_card_payment_tr', {'_CARD_TYPE_TR_': ['kart'], '_AMOUNT_TR_': ['600 tl']}) )
        data.append( ('kredi kartı borcumu vadesiz hesabımdaki 10000 tl ile ödemek istiyorum', 'credit_card_payment_tr', {'_AMOUNT_TR_': ['10000 tl']}) )
        data.append( ('1234 ile biten kartımın borcunu öde', 'credit_card_payment_tr', {'_CARD_TYPE_TR_': ['1234']}) )
        data.append( ('5235\'le biten kartımın borcunu öde', 'credit_card_payment_tr', {'_CARD_TYPE_TR_': ['5235\'le biten kartımın']}) )
        data.append( ('35le biten kartın borcumu ödemek istiyorum', 'credit_card_payment_tr', {'_CARD_TYPE_TR_': ['35le']}) )
        data.append( ('7852le baslayan kartin borcumu ödemek istiyorum', 'credit_card_payment_tr', {'_CARD_TYPE_TR_': ['7852le']}) )
        data.append( ('Bankamatik kartımdan maksimum gol yüz elli TL aktarmak istiyorum', 'credit_card_payment_tr', {'_CARD_TYPE_TR_': ['maksimum gol'], '_AMOUNT_TR_': ['yüz elli TL']}) )
        data.append( ('ek hesabımdan maximiles kartın borcunun asgarisini ödeyebilir miyim', 'credit_card_payment_tr', {'_CARD_TYPE_TR_': ['maximiles'], '_PAYMENT_TYPE_TR_': ['asgarisini']}) )
        data.append( ('gold kart borç ödemesi', 'credit_card_payment_tr', {'_CARD_TYPE_TR_': ['gold']}) )
        data.append( ('maksimilesselect kartına 300 tl yatır', 'credit_card_payment_tr', {'_CARD_TYPE_TR_': ['maksimilesselect'], '_AMOUNT_TR_': ['300 tl']}) )
        data.append( ('maximil kartına borç ödemesi', 'credit_card_payment_tr', {'_CARD_TYPE_TR_': ['maximil']}) )
        data.append( ('privia borcumu öde', 'credit_card_payment_tr', {'_CARD_TYPE_TR_': ['privia']}) )
        data.append( ('vadesiz hesabımdaki tüm parayı maximiles select kredi kartıma aktarmak istiyorum', 'credit_card_payment_tr', {'_CARD_TYPE_TR_': ['maximiles select'], '_PAYMENT_TYPE_TR_': ['tüm']}) )
        data.append( ('asgari odememi yap', 'credit_card_payment_tr', {'_PAYMENT_TYPE_TR_': ['asgari']}) )
        data.append( ('asgari tutari ode', 'credit_card_payment_tr', {'_PAYMENT_TYPE_TR_': ['asgari']}) )
        data.append( ('Banka kartimdaki parayi kredi kartina aktararak askeri borcu ödemek istiyorum', 'credit_card_payment_tr', {'_PAYMENT_TYPE_TR_': ['askeri']}) )
        data.append( ('donem sonu borcumu ode', 'credit_card_payment_tr', {'_PAYMENT_TYPE_TR_': ['donem sonu']}) )
        data.append( ('hesap ozeti odemesini ode', 'credit_card_payment_tr', {'_PAYMENT_TYPE_TR_': ['hesap ozeti']}) )
        data.append( ('kredi karti borcumun en az ödemesi ne kadarsa o kadar öde', 'credit_card_payment_tr', {'_PAYMENT_TYPE_TR_': ['en az']}) )
        data.append( ('kredi kartimin ekstre borcunu nasil odeyebilirim', 'credit_card_payment_tr', {'_PAYMENT_TYPE_TR_': ['ekstre']}) )
        data.append( ('maaş hesabimdan kiredi karti borcumun minimumunu ode', 'credit_card_payment_tr', {'_PAYMENT_TYPE_TR_': ['minimumunu']}) )
        data.append( ('maaş hesabimdan kredi karti borcumun tamamini ode', 'credit_card_payment_tr', {'_PAYMENT_TYPE_TR_': ['tamamini']}) )
        data.append( ('merkezi bankamatik kartımdaki parayı kredi kartı toplam borcuna aktarmak istiyorum', 'credit_card_payment_tr', {'_PAYMENT_TYPE_TR_': ['toplam']}) )
        data.append( ('minimum borç ödeme', 'credit_card_payment_tr', {'_PAYMENT_TYPE_TR_': ['minimum']}) )
        data.append( ('privia kartımın hesap özetini yatır', 'credit_card_payment_tr', {'_CARD_TYPE_TR_': ['privia'], '_PAYMENT_TYPE_TR_': ['hesap özetini']}) )

        # cash_advance_tr
        data.append( ('maximum kartımdan 3 ay vadeli 10 bin tl taksitli vadesiz hesabıma nakit avans cekmek istiyorum', 'cash_advance_tr', {'_CARD_TYPE_TR_': ['maximum kartımdan'], '_AMOUNT_TR_': ['10 bin tl'], '_INSTALLMENT_TR_': ['3 ay']}) )
        data.append( ('maximiles kredi kartimdan 200 tl avans cekmek istiyorum', 'cash_advance_tr', {'_CARD_TYPE_TR_': ['maximiles'], '_AMOUNT_TR_': ['200 tl']}) )
        data.append( ('maximiles kredi kartimdan 10 taksitle 2000 tl avans cekmek istiyorum', 'cash_advance_tr', {'_CARD_TYPE_TR_': ['maximiles'], '_AMOUNT_TR_': ['2000 tl'], '_INSTALLMENT_TR_': ['10']}) )
        data.append( ('100 lira ihtiyacım var', 'cash_advance_tr', {'_AMOUNT_TR_': ['100 lira']}) )
        data.append( ('1000 tl 7 ay vadeli nakit avans', 'cash_advance_tr', {'_AMOUNT_TR_': ['1000 tl'], '_INSTALLMENT_TR_': ['7 ay']}) )
        data.append( ('4500 nakit ceksem faiz ne kadar öderim karta', 'cash_advance_tr', {'_AMOUNT_TR_': ['4500']}) )
        data.append( ('50 tl borç', 'cash_advance_tr', {'_AMOUNT_TR_': ['50 tl']}) )
        data.append( ('acil 10.000 tl nakit lazım nasıl halledebilirim', 'cash_advance_tr', {'_AMOUNT_TR_': ['10.000 tl']}) )
        data.append( ('altı bin dört yüz elli lira taksitli nakit avans çekmek istiyorum', 'cash_advance_tr', {'_AMOUNT_TR_': ['altı bin dört yüz elli lira']}) )
        data.append( ('altı bin seksen tl altı taksitle avans çekebilirmiyim', 'cash_advance_tr', {'_INSTALLMENT_TR_': ['altı']}) )
        data.append( ('Ben kredi kartındaki 1550 tl yi diğer hesabıma aktarmak istiyorum', 'cash_advance_tr', {'_AMOUNT_TR_': ['1550 tl']}) )
        data.append( ('iki yüz on TL çekmek istiyorum', 'cash_advance_tr', {'_AMOUNT_TR_': ['iki yüz on TL']}) )
        data.append( ('kredi kartım\'dan 240 çek', 'cash_advance_tr', {'_AMOUNT_TR_': ['240']}) )
        data.append( ('Nakitavans 900 lira', 'cash_advance_tr', {'_AMOUNT_TR_': ['900 lira']}) )
        data.append( ('taksitli avansı kaç kaç ödeyeceğim 1800 tl 9 ay', 'cash_advance_tr', {'_AMOUNT_TR_': ['1800 tl'], '_INSTALLMENT_TR_': ['9 ay']}) )
        data.append( ('vazgeçtim sekiz yüz tl çekicem', 'cash_advance_tr', {'_AMOUNT_TR_': ['sekiz yüz tl']}) )
        data.append( ('gold kart limitten taksitli para çekme', 'cash_advance_tr', {'_CARD_TYPE_TR_': ['gold']}) )
        data.append( ('gold kredi kartindan taksitle para cekcem', 'cash_advance_tr', {'_CARD_TYPE_TR_': ['gold']}) )
        data.append( ('işte üniversiteli kredi kartimdan avans para alma', 'cash_advance_tr', {'_CARD_TYPE_TR_': ['işte üniversiteli']}) )
        data.append( ('maksi bana maximiles select karttan taksitli nakit avans ver', 'cash_advance_tr', {'_CARD_TYPE_TR_': ['maximiles select']}) )
        data.append( ('maksimil selek limitten taksitli nakit avans kullanmalıyım', 'cash_advance_tr', {'_CARD_TYPE_TR_': ['maksimil selek']}) )
        data.append( ('miles kredi kartindan limitten para cekme', 'cash_advance_tr', {'_CARD_TYPE_TR_': ['miles']}) )
        data.append( ('platinium kredi kartindan borc alma', 'cash_advance_tr', {'_CARD_TYPE_TR_': ['platinium']}) )
        data.append( ('tema kredi kartindan limitten para alma', 'cash_advance_tr', {'_CARD_TYPE_TR_': ['tema']}) )
        data.append( ('10 ay vadeli taksitli nakit avans kullanmak istiyorum', 'cash_advance_tr', {'_INSTALLMENT_TR_': ['10 ay']}) )
        data.append( ('10 taksitli nakit avans kullanmak istiyorum', 'cash_advance_tr', {'_INSTALLMENT_TR_': ['10']}) )
        data.append( ('1100 tl 10 ay vadeli nakit avans', 'cash_advance_tr', {'_AMOUNT_TR_': ['1100 tl'], '_INSTALLMENT_TR_': ['10 ay']}) )
        data.append( ('1260 tl sekiz taksitle avans çekebilir miyim', 'cash_advance_tr', {'_AMOUNT_TR_': ['1260 tl'], '_INSTALLMENT_TR_': ['sekiz']}) )
        data.append( ('1500 tl nakit çekersem taksitler ne kadar olur 12 aylık ve faiz ne olur', 'cash_advance_tr', {'_AMOUNT_TR_': ['1500 tl'], '_INSTALLMENT_TR_': ['12 aylık']}) )
        data.append( ('bin iki yüz lira on sekiz taksitle nakit avans çekebilirmiyim', 'cash_advance_tr', {'_AMOUNT_TR_': ['bin iki yüz lira'], '_INSTALLMENT_TR_': ['on sekiz']}) )
        data.append( ('vazgeçtim 10 taksit yap', 'cash_advance_tr', {'_INSTALLMENT_TR_': ['10']}) )
        data.append( ('yedi ay vadeli nakit avans kullanmak istiyorum', 'cash_advance_tr', {'_INSTALLMENT_TR_': ['yedi ay']}) )



        # inform
        data.append( ('elli iki lira', 'inform', {}) )
        data.append( ('500 tl', 'inform', {}) )
        data.append( ('100 usd', 'inform', {}) )
        data.append( ('5000 tl', 'inform', {}) )
        data.append( ('1 aylik', 'inform', {}) )
        data.append( ('elli bin tl', 'inform', {}) )


        # avantages_of_maximiles_tr
        data.append( ('maximiles uçuş kartının avantajları nelerdir', 'avantages_of_maximiles_tr', {}) )

        # online_shopping_tr
        data.append( ('Neden alışveriş yapamıyorum', 'online_shopping_tr', {}) )
        data.append( ('kartımın e-ticaretini açmak istiyorum', 'online_shopping_tr', {}) )

        # transfer_info_tr
        data.append( ('eft gidis bilgi', 'transfer_info_tr', {}) )
        

        # bad_comment_tr
        data.append( ('sıktır gıt', 'bad_comment_tr', {}) )
        data.append( ('bi ...... yarmadı', 'bad_comment_tr', {}) )
        data.append( ('salak deli', 'bad_comment_tr', {}) )
        data.append( ('gerizekalı', 'bad_comment_tr', {}) )

        # oos
        data.append( ('bu saate aranmaz ayıp olur', 'oos', {}) )
        data.append( ('Off', 'oos', {}) )

        data = pd.DataFrame(data, columns=['Text', 'Intent', 'gold_mcm'])

    if intent_filter_for_entities == False:
        pass
    else:
        if intent_filter_for_entities == True:
            # 'inform' is also removed because desired entities changes from intent to intent among target intents.
            intent_filter_for_entities = ['account_tr', 'bill_payment_tr', 'campaign_tr', 'cash_advance_tr', 'credit_card_payment_tr', 'credit_card_tr', 'foreign_currency_tr', 'history_tr', 'loan_application_tr', 'spendadvice_tr', 'term_deposit_calculation_tr', 'transfer_money_tr', 'txnlist_tr', ]
        elif isinstance(intent_filter_for_entities, list):
            pass
        else:
            print(intent_filter_for_entities)
            assert 1==0
        data = data[data['Intent'].isin(intent_filter_for_entities)]

    if 'rasa' in config:

        import pyspace
        import importlib
        from pyspace.rasa.components.update import MCMEntityMapper
        importlib.reload(pyspace.rasa.components.update)
        from pyspace.rasa.components.update import MCMEntityMapper
        mcmmapper = MCMEntityMapper()

        ###############################################
        data['temp'] = data['Text'].apply(lambda x: config['rasa'](x))
        data['rasa_intent'] = data['temp'].apply(lambda x: x['intent']['name'])
        data['rasa_entities'] = data['temp'].apply(lambda x: x['entities'])
        data['rasa_mcm'] = data['temp'].apply(lambda x: mcmmapper.process({'intent':x['intent']['name'], 'entities': x['entities']}))
        data = data.drop(columns=['temp'])

    if 'finie' in config:

        def fix_finie_intent(x):
            if x in ['spendadvice']:
                return 'spendadvice_tr'
            else:
                return x
        def fix_finie_entity(x):
            temp = x
            x = x['finie_mcm']

            unnecessary_fields = ['remaining_slots',
            '_RECALCULATION_',
            '_SPENDABLE_', '_ACCOUNT_NAME_NORM_', '_ACCOUNT_NORM_', '_ACCOUNT_NORM_TEMP_',
            '_ACCOUNT_SM_', '_CATEGORY_MATCH_',
            '_TOP_MERCHANT_', '_MERCHANT_MATCH_', 
            '_MERCHANT_', '_TARGET_TYPE_']
            for field in unnecessary_fields:
                if field in x:
                    del x[field]
                
            [x.pop(k) for k in list(x.keys()) if x[k] == []]
            if temp['finie_intent'] == 'spendadvice_tr':
                x.pop('_DATE_')
            return x

        data['temp'] = data['Text'].apply(lambda x: config['finie'](x))
        data['finie_intent'] = data['temp'].apply(lambda x: x['response']['type'])
        data['finie_intent'] = data['finie_intent'].apply(lambda x: fix_finie_intent(x))
        data['finie_mcm'] = data['temp'].apply(lambda x: x['slots'] if 'slots' in x else x)
        data['finie_mcm'] = data.apply(lambda x: fix_finie_entity(x),axis=1)
        data = data.drop(columns=['temp'])

    if 'duckling' in config:
        data['duckling_entities'] = data['Text'].apply(lambda x: config['duckling'](x))

    print(f'Data count : {data.shape[0]}')
    if 'rasa_intent' in data:
        temp = data[data['Intent']!=data['rasa_intent']].shape[0]
        print(f'Rasa error : {temp}, ({round(100*(data.shape[0]-temp)/data.shape[0],2)} %)')
    if 'finie_intent' in data:
        temp = data[data['Intent']!=data['finie_intent']].shape[0]
        print(f'Finie error : {temp}, ({round(100*(data.shape[0]-temp)/data.shape[0],2)} %)')

    return data