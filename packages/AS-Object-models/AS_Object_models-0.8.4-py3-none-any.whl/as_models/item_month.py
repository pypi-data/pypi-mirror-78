from .sales_inv_utils import SalesInvBase
from datetime import datetime
from dateutil.relativedelta import relativedelta
import jmespath

from .item_month_notes import ItemMonthNotes, MonthNotesCollection
from .item_month_supply import ItemMonthSupply, MonthSupplyCollection
from .inventory_active_items import InventoryActiveItems
from .supplier import Supplier
from .reserve_summary import ReserveSummary
from .pub_sub import publish_message,UPDATE_MONTH_INVENTORY
from . import GetInstance

class ItemMonthSummary(SalesInvBase):
    ext_fields = ['year', 'item_type', 'inventory_summary','soft_delete', 'parent_path','path']
    COLLECTION_NAME = 'application_data'
    valid_item_types = ['Vase']

    def __init__(self, fsClient, **kwargs):
        self.soft_delete = kwargs.get('soft_delete',False)
        self.year = kwargs.get('year',None)
        self.item_type = kwargs.get('item_type',None)
        self.inventory_summary = kwargs.get('inventory_summary',{})

        super(ItemMonthSummary,self).__init__(fsClient,**kwargs)

    def base_path(self):
        return ItemMonthSummary.__basePath(self._fsClient)

    @classmethod
    def basePath(cls):
        return ItemMonthSummary.__basePath(ItemMonthSummary.get_client())

    @classmethod
    def __basePath(cls,inClient):
        return ItemMonthSummary.COLLECTION_NAME+'/'+inClient.company+'/Sales_Inventory/Converted/ItemMonthSummary'

    @classmethod
    def getInstance(cls,fsDocument):
        ref,snap = ItemMonthSummary.getDocuments(fsDocument)
        docDict = snap.to_dict() if snap.exists else {}
        docDict['fs_docSnap'] = snap
        docDict['fs_docRef'] = ref
        return ItemMonthSummary(ItemMonthSummary.get_firestore_client(),**docDict)

    @classmethod
    def getInstanceByYearType(cls, year, itemType):
        docId = cls.CreateId(year,itemType)
        docPath = cls.basePath()+"/"+docId
        return cls.getInstance(cls.get_firestore_client().document(docPath))

    @classmethod
    def CreateId(cls, year, itemType):
        return str(year)+"_"+itemType

    @property
    def id(self):
        return ItemMonthSummary.CreateId(self.year,self.item_type)

    @classmethod
    def _PublishYearsMonths(cls, startMonth=None):
        years = [(datetime.now().year-1)+x for x in range(6)]
        months = [str(x+1).zfill(2) for x in range(12)]
        if startMonth is None:
            startMonth = str(years[0])+"_"+months[0]
        return years, months, startMonth

    @classmethod
    def PublishRefreshLists(cls, itemType, startMonth=None,doPublish=True):
        years, months, startMonth = cls._PublishYearsMonths(startMonth)

        ia_items = InventoryActiveItems.get_all(itemType)
        publish_lists = []
        for key in ia_items.keys():
            ia_item = ia_items[key]
            publish_lists.append(cls._getItemNamePublishList(itemType,ia_item.name,years,months,startMonth))

        for pl in publish_lists:
            if doPublish:
                strGrowMonths = ":".join(pl['grow_months'])
                pubList = {"item_name":pl['item_name'],'item_type':pl['item_type'],'grow_months':strGrowMonths}
                publish_message(UPDATE_MONTH_INVENTORY,'Start Processing Refresh',pubList)

        return publish_lists
    
    @classmethod
    def PublishRefreshListsName(cls, itemType, itemName, startMonth=None, doPublish=True):
        years, months, startMonth = cls._PublishYearsMonths(startMonth)
        nameRefreshList = cls._getItemNamePublishList(itemType, itemName, years, months, startMonth)
        if doPublish:
            strGrowMonths = ":".join(nameRefreshList['grow_months'])
            pubList = {"item_name":nameRefreshList['item_name'],'item_type':nameRefreshList['item_type'],'grow_months':strGrowMonths}
            publish_message(UPDATE_MONTH_INVENTORY,'Start Processing Name Refresh',pubList)
        return nameRefreshList

    @classmethod
    def _getItemNamePublishList(cls, itemType, itemName, years, months, startMonth):
        cleanName = ItemMonth.CleanItemName(itemName)
        itemList = {"item_type": itemType,"item_name": cleanName, "grow_months": []}
        for year in years:
            for month in months:
                growMonth = str(year)+"_"+month
                if cls.yearMonthGreaterEq(growMonth,startMonth):
                    itemList['grow_months'].append(growMonth)
        itemList['grow_months'].sort()
        itemList['grow_months'].reverse()
        return itemList

    @classmethod
    def yearMonthGreaterEq(cls, currYearMonth, compYearMonth):
        return int(currYearMonth.replace("_","")) >= int(compYearMonth.replace("_",""))
    
    @classmethod
    def PopProcessPublishStr(cls,publishInfo,doPublish=True):
        if publishInfo is None or publishInfo == {}:
            return None
        
        if publishInfo.get('grow_months',None) is None:
            return None
        elif publishInfo['grow_months'] == '':
            return None

        if publishInfo.get('item_type', None) is None:
            return None
        
        if publishInfo.get('item_name',None) is None:
            return None

        publishInfo['grow_months'] = publishInfo['grow_months'].split(":")
        return cls.PopProcessPublish(publishInfo,doPublish)

    @classmethod
    def PopProcessPublish(cls,publishInfo,doPublish=True):
        if len(publishInfo['grow_months']) == 0:
            return None

        gms = publishInfo['grow_months']
        itemType = publishInfo['item_type']
        itemName = publishInfo['item_name']
        growMonth = gms.pop()

        ims = ItemMonthSummary.getInstanceByYearType(growMonth.split("_")[0],itemType)
        try:
            im = ItemMonth.getItemMonthInstance(growMonth,itemType,itemName)
        except Exception:
            print("Not able to pull Item Month ({}) for item: {} - {}".format(growMonth,itemType,itemName))
            return None

        im._refreshInventoryLevels()
        ims.add_summary(im)
        if doPublish:
            strGms = ":".join(gms)
            newPubInfo = {'item_type':itemType,'item_name':itemName,'grow_months':strGms}
            publish_message(UPDATE_MONTH_INVENTORY,'Process Inventory Refresh',newPubInfo)

        return im.dict_summary()

    @classmethod
    def UpdateItemMonthSummary(self, itemMonth):
        ims = ItemMonthSummary.getInstanceByYearType(itemMonth.year,itemMonth.item_type)
        ims.add_summary(itemMonth)

    def add_summary(self, itemMonth):
        month = itemMonth.grow_month.split("_")[1]
        pubData = itemMonth.dict_summary()
        if self.exists:
            self._documentRef.update({'inventory_summary.'+month+'.'+itemMonth.item_name: pubData})
        else:
            month_summary = self.inventory_summary.get(month,{})
            month_summary[itemMonth.item_name] = pubData
            self.inventory_summary[month] = month_summary
            self.update_ndb()

    def get_summary(self, cleanName, month):
        month_summary = self.inventory_summary.get(month,{})
        return month_summary.get(cleanName,None)
    
    def _getMonths(self, startMonth, endMonth="12"):
        return [str(x+int(startMonth)).zfill(2) for x in range(13-int(startMonth)) if (x+int(startMonth)) <= int(endMonth)]

    def summary_info(self, startMonth="01", endMonth="12"):
        if int(startMonth) == 1 and int(endMonth) == 12:
            return jmespath.search("*.[*][][]",self.inventory_summary)
        else:
            mos = self._getMonths(startMonth,endMonth)
            return jmespath.search("*.[*][][]",{k : v for (k,v) in self.inventory_summary.items() if k in mos})


class ItemMonthCollection(SalesInvBase):
    ext_fields = ['items','item_type','grow_month','soft_delete','parent_path','path']
    COLLECTION_NAME = 'application_data'
    collection = {}

    IWS = "Supply"
    IWN = "Notes"

    def __init__(self,fsClient, **kwargs):
        self.soft_delete = kwargs.get('soft_delete',False)
        self._items = kwargs.get('items',None)
        self.item_type = kwargs.get('item_type','')
        self.grow_month = kwargs.get('grow_month','')
        self._in_growMonthParent = kwargs.get('_growMonthParent',None)
        self._loaded_items = {}

        super(ItemMonthCollection,self).__init__(fsClient, **kwargs)
    
    def post_create_activities(self):
        self.load_collections()
        self.load_items()
        self.load_item_months()

    def load_collections(self):
        self._notes_collection = MonthNotesCollection.getOrCreateInstance(self._fsClient.document(self.notes_path),self._in_growMonthParent)
        self._supply_collection = MonthSupplyCollection.getOrCreateInstance(self._fsClient.document(self.supply_path),self._in_growMonthParent)
        self._month_reserves = ItemMonthReserves.getOrCreateMonthReserve(self._in_growMonthParent)

    def load_items(self):
        if self._items is None:
            ia_items = InventoryActiveItems.get_all(self.item_type)
            self._items = {}
            for key in ia_items.keys():
                ia_item = ia_items[key]
                cleanName = ItemMonth.CleanItemName(ia_item.name)
                self._items[cleanName] = ia_item.get_dict()
    
    def load_item_months(self):
        item_names = self.items.keys()
        for item_name in item_names:
            inPath = ItemMonth.GetPath(self._growMonthParent,self.item_type,item_name)
            ItemMonthCollection.GetOrCreateItemMonth(inPath,self,item_name)
    
    @classmethod
    def GetOrCreateItemMonth(cls, imPath, itemMonthCollection, item_name):
            fsDocument = ItemMonth.get_firestore_client().document(imPath)
            ref,snap = ItemMonth.getDocuments(fsDocument)
            item_dict = snap.to_dict() if snap.exists else {}
            item_dict['fs_docSnap'] = snap
            item_dict['fs_docRef'] = ref
            item_dict['_itemCollection'] = itemMonthCollection
            item_dict['_notesCollection'] = itemMonthCollection._notes_collection
            item_dict['_supplyCollection'] = itemMonthCollection._supply_collection
            item_dict['_growMonthParent'] = itemMonthCollection._growMonthParent
            if not snap.exists:
                item_dict['name'] = item_name
                item_dict['grow_month'] = itemMonthCollection.grow_month
                item_dict['item_type'] = itemMonthCollection.item_type
                item_dict['item'] = itemMonthCollection.items[item_name]
            im = ItemMonth(itemMonthCollection._fsClient,**item_dict)
            itemMonthCollection._loaded_items[item_name] = im
            if not im.exists:
                im.update_ndb()
    
    def refresh_loaded_items(self):
        for item_name in list(self._loaded_items.keys()):
            im = self._loaded_items[item_name]
            im._refreshInventoryLevels()
        
        return jmespath.search('*',self._loaded_items)

    
    @property
    def items(self):
        if self._items is None:
            ia_items = InventoryActiveItems.get_all(self.item_type)
            self._items = {}
            for key in ia_items.keys():
                ia_item = ia_items[key]
                cleanName = ItemMonth.CleanItemName(ia_item.name)
                self._items[cleanName] = ia_item.get_dict()
        return self._items

    def update_month_reserves(self):
        self._month_reserves = ItemMonthReserves.getOrCreateMonthReserve(self._growMonthParent)
        self._month_reserves.load_reserves()

    def base_path(self):
        return self.parent_path+'/Items'

    @property
    def id(self):
        return self.item_type

    @property
    def notes_path(self):
        return self._growMonthParent.path+'/'+self.IWN+'/'+self.item_type
    
    @property
    def supply_path(self):
        return self._growMonthParent.path+'/'+self.IWS+'/'+self.item_type
    
    @property
    def month_reserve_path(self):
        return self._growMonthParent.path+'/MonthReserves/reserves'

    @classmethod
    def _get_active_items(cls,item_type):
        return InventoryActiveItems.get_all(item_type)

    @classmethod
    def getInstance(cls,docRef,itemType, gwParent):
        key = str(itemType)+'_'+str(gwParent.id)
        imc = ItemMonthCollection.collection.get(key,None)
        if imc is None:
            ref,snap = ItemMonthCollection.getDocuments(docRef)
            docDict = snap.to_dict() if snap.exists else {}
            docDict['fs_docSnap'] = snap
            docDict['fs_docRef'] = ref
            docDict['item_type'] = itemType
            docDict['_growMonthParent'] = gwParent
            imc = ItemMonthCollection(ItemMonthCollection.get_firestore_client(),**docDict)
        return imc

    @classmethod
    def getOrCreateInstance(cls,item_type,gwParent):
        key = str(item_type)+'_'+str(gwParent.id)
        imc = ItemMonthCollection.collection.get(key,None)
        if imc is None:
            imc = cls.getInstance(gwParent._fsClient.document(gwParent.path+'/Items/'+item_type),item_type, gwParent)
            if not imc.exists:
                imc.item_type = item_type
                imc.grow_month = gwParent.id
                #iwc.update_ndb(True)
                imc.post_create_activities()
            ItemMonthCollection.collection[key] = imc
        return imc

    @property
    def _growMonthParent(self):
        if self._in_growMonthParent is None:
            gwParDoc = self.get_firestore_client().document(self.parent_path)
            self._in_growMonthParent = GetInstance("GrowMonth",gwParDoc)
        return self._in_growMonthParent

    def create_itemmonth_entry(self, item, gwPar):
        ''' Input is going to be recipe item '''
        cleanName = ItemMonth.CleanItemName(item.name)
        iw = self._loaded_items.get(cleanName,None)
        if iw is None:
            item_dict = {}
            itemObj = self._get_sb_instance_by_path(item.path)
            item_dict['item'] = {'name':itemObj.name,'id':itemObj.id,'path':itemObj.path}
            item_dict['name'] = itemObj.name
            item_dict['item_type'] = self.item_type
            item_dict['grow_month'] = self.grow_month
            item_dict['actual'] = None
            item_dict['inventory_set'] = False
            item_dict['color_groupings'] = {}
            item_dict['_growMonthParent'] = gwPar
            item_dict['_itemCollection'] = self
            item_dict['_notesCollection'] = self._notes_collection
            item_dict['_supplyCollection'] = self._supply_collection
            iw = ItemMonth(self._fsClient,**item_dict)
            iw.update_ndb()
        return iw

    def get_itemmonth(self,itemName):
        cleanName = ItemMonth.CleanItemName(itemName)
        return self._loaded_items.get(cleanName,None)

    def get_supply(self):
        return self._supply_collection

    def get_notes(self):
        return self._notes_collection

    def update_ndb(self, doCreate=False):
        if self.items is None:
            self.items = {}

        item_names = self._loaded_items.keys()
        for item_name in item_names:
            self.items[item_name] = self._loaded_items[item_name].get_dict()

        super(ItemMonthCollection,self).update_ndb(doCreate)

class ItemMonthReserves(SalesInvBase):
    """ Hey keeping the summary for just this month """
     
    ext_fields = ['week_summaries','month_summary','grow_month','soft_delete','parent_path','path']
    COLLECTION_NAME = 'application_data'

    def __init__(self, fsClient, **kwargs):
        self.item_types = ['Vase']
        self.soft_delete = kwargs.get('soft_delete',False)
        self.week_summaries = kwargs.get('week_summaries',{})
        self.month_summary = kwargs.get('month_summary',{})
        self._grow_month = kwargs.get('grow_month',None)
        self._in_growMonthParent = kwargs.get('_growMonthParent',None)
        super(ItemMonthReserves, self).__init__(fsClient, **kwargs)

    def base_path(self):
        return self.parent_path+'/MonthReserves'

    @classmethod
    def getInstance(cls,fsDocument,gmParent):
        ref,snap = ItemMonthReserves.getDocuments(fsDocument)
        docDict = snap.to_dict() if snap.exists else {}
        docDict['fs_docSnap'] = snap
        docDict['fs_docRef'] = ref
        docDict['_growMonthParent'] = gmParent
        return ItemMonthReserves(ItemMonthReserves.get_firestore_client(),**docDict)

    @classmethod
    def getOrCreateMonthReserve(cls, gmParent, load_doc=True):
        imr = cls.getInstance(gmParent._fsClient.document(gmParent.path+'/MonthReserves/reserves'), gmParent)
        if not imr.exists and load_doc:
            imr.load_reserves()
        return imr

    def load_reserves(self):
        self.week_summaries = {}
        self.load_week_reserves()

        self.month_summary = {}
        self.load_month_reserves()
        self.update_ndb()

    def load_month_reserves(self):
        gws = self._growMonthParent.grow_weeks
        for itemType in self.item_types:
            #typeSummary = self.month_summary.get(itemType,{})
            typeSummary = {}
            for gw in gws:
                weekSummary = self._load_growweek_reserves(itemType,gw,'total')
                for key in weekSummary.keys():
                    amt = weekSummary[key]
                    monthTotal = typeSummary.get(key,0)
                    monthTotal = monthTotal + amt
                    if key != '':
                        typeSummary[key] = monthTotal
            self.month_summary[itemType] = typeSummary

    def load_week_reserves(self):
        gws = self._growMonthParent.grow_weeks
        for itemType in self.item_types:
            typeSummary = self.week_summaries.get(itemType,{})
            for gw in gws:
                item_week_summ = self._load_growweek_reserves(itemType,gw)
                for itemName in item_week_summ.keys():
                    nameList = typeSummary.get(itemName,[])
                    reserves = item_week_summ[itemName]
                    for reserve in reserves:
                        reserve['finish_week'] = gw
                        nameList.append(reserve)
                    if itemName != '':
                        typeSummary[itemName] = nameList
            self.week_summaries[itemType] = typeSummary
    
    def _load_growweek_reserves(self,item_type, growWeekId,summType='by_item'):
        rs = ReserveSummary.getReserveSummary(growWeekId)
        summ = rs.getReserveItemAmts(item_type)
        return summ.get(summType,{})
    
    @property
    def grow_month(self):
        return self._growMonthParent.id

    @property
    def _growMonthParent(self):
        if self._in_growMonthParent is None:
            gwParDoc = self.get_firestore_client().document(self.parent_path)
            self._in_growMonthParent = GetInstance("GrowMonth",gwParDoc)
        return self._in_growMonthParent
        

class ItemMonth(SalesInvBase):
    """ This is the class represents all plants that are available during a specific week """

    ext_fields = ['item','name','item_name','reserve_total','item_type','grow_month','actual',
                  'inventory_add','calc_actual','prev_actual','inventory_set','color_groupings',
                  'soft_delete','parent_path','path']

    COLLECTION_NAME = 'application_data'
    _imr_collection = {}
    
    def __init__(self, fsClient, **kwargs):
        self.soft_delete = kwargs.get('soft_delete',False)
        #self.name = kwargs.get('name','')
        self.item_type = kwargs.get('item_type',None)
        self._collection_parent = kwargs.get('_itemCollection',None)
        self._notesCollection = kwargs.get('_notesCollection',None)
        self._supplyCollection = kwargs.get('_supplyCollection',None)
        self.item = kwargs.get('item',{}) 
        self.grow_month = kwargs.get('grow_month','')
        self.reserve_total = kwargs.get('reserve_total',0)
        self.actual = kwargs.get('actual',None)
        self.inventory_add = kwargs.get('inventory_add',0)
        self.calc_actual = kwargs.get('calc_actual',None)
        self.prev_actual = kwargs.get('prev_actual',None)
        self._inventory_set = kwargs.get('inventory_set',False)
        self.previous_inventory = kwargs.get('previous_inventory',0)
        self.next_inventory = kwargs.get("next_inventory",0)
        self._previous_month_path = kwargs.get('previous_month_path',None)
        self._next_month_path = kwargs.get('next_month_path',None)
        self.color_groupings = kwargs.get('color_groupings','')
        self._in_growMonthParent = kwargs.get('_growMonthParent',None)
        if kwargs.get('fs_docRef',None) is None:
            path = self._growMonthParent.path+'/Items/'+self.item_type+"_"+self.item_name
            kwargs['fs_docRef'] = fsClient.document(path)

        self._supplies = None
        self._notes = None
        super(ItemMonth, self).__init__(fsClient, **kwargs)
        
    
    def base_path(self):
        return ItemMonth.GetPath(self._growMonthParent,self.item_type,self.item_name)
    
    @classmethod
    def GetPath(cls,growMonth, itemType, itemName):
        return ItemMonth.GetPathStr(growMonth.path,itemType,itemName)
    
    @classmethod
    def GetPathStr(cls,growMonthPath, itemType, itemName):
        return growMonthPath+'/Items/'+itemType+"_"+ItemMonth.CleanItemName(itemName)

    @property
    def previous_month_path(self):
        if self._previous_month_path is None:
            prevMonth = self._format_month_date(self.prev_month_date)
            self._previous_month_path = self.path.replace(self.grow_month,prevMonth)
        return self._previous_month_path

    @property
    def next_month_path(self):
        if self._next_month_path is None:
            nextMonth = self._format_month_date(self.next_month_date)
            self._next_month_path = self.path.replace(self.grow_month,nextMonth)
        return self._next_month_path

    @property
    def year(self):
        return self.grow_month.split("_")[0]

    @classmethod
    def RefreshInventoryLevels(cls, growMonthId, itemType, itemName):
        im = ItemMonth.getItemMonthInstance(growMonthId,itemType,itemName)
        return im._refreshInventoryLevels()

    def _refreshInventoryLevels(self,repull=True):
        new_calc_actual = 0
        total = self.reserve_total
        if repull:
            total = self._getReservesTotal()

        doSave = False
        if self.reserve_total != total:
            self.reserve_total = total
            doSave = True

        if self.inventory_set:
            if self.actual is None:
                self.actual = 0
            new_calc_actual = self.actual - self.reserve_total
            if new_calc_actual != self.calc_actual:
                doSave = True
        else:
            pmActual = self.prev_actual
            if repull:
                pmActual = self._getPrevMonthActual()

            if pmActual is not None:
                self.prev_actual = pmActual
                new_calc_actual = self.prev_actual - self.reserve_total
                if self.prev_actual != pmActual:
                    doSave = True
            else:
                if pmActual is None:
                    # Being here means that there is no inventory set
                    #   and no previous inventory to use... so subtract
                    #   the reserve_total from zero
                    new_calc_actual = 0 - self.reserve_total
                    doSave = True

        new_calc_actual = new_calc_actual + self.inventory_add
        if new_calc_actual != self.calc_actual:
            self.calc_actual = new_calc_actual
            doSave = True
        
        if doSave or not self.exists:
            self.update_ndb()
        
        return {'inventory': self.calc_actual, 'reserves': self.reserve_total, 'updated': doSave}
 
    @property
    def _growMonthParent(self):
        if self._in_growMonthParent is None:
            gwParDoc = self.get_firestore_client().document(self.parent_path.replace('/Items',''))
            self._in_growMonthParent = GetInstance("GrowMonth",gwParDoc)
        return self._in_growMonthParent
        
    def _getReservesTotal(self):
        imr = None #ItemMonth._imr_collection.get(self.grow_month,None)
        if imr is None:
            imr = ItemMonthReserves.getOrCreateMonthReserve(self._growMonthParent)
            imr.load_month_reserves()
        ItemMonth._imr_collection[self.grow_month] = imr
        return imr.month_summary.get(self.item_type,{}).get(self.item_name,0)

    def _getPrevMonthActual(self):
        pm = ItemMonth.getItemMonthInstanceByPath(self.previous_month_path)
        if pm.exists:
            return pm.calc_actual
        return None

    @property
    def month_date(self):
        return datetime.strptime(self.grow_month,"%Y_%m")

    @property
    def next_month_date(self):
        return self.month_date+relativedelta(months=1)
    
    @property
    def prev_month_date(self):
        return self.month_date+relativedelta(months=-1)

    def _format_month_date(self,monthDate):
        return monthDate.strftime("%Y_%m")

    def add_inventory(self, added_inventory):
        self.inventory_add = added_inventory
        results = self._refreshInventoryLevels(repull=False)
        return results

    @property
    def inventory_set(self):
        return self._inventory_set
    
    def set_actual(self, inventory_amt):
        self._inventory_set = True
        if inventory_amt != self.actual:
            self.actual = inventory_amt
            
        results = self._refreshInventoryLevels(repull=False)
        if not results['updated']:
            self.update_ndb()
    
    def unset_actual(self):
        self._inventory_set = False
        results = self._refreshInventoryLevels(repull=False)
        if not results['updated']:
            self.update_ndb()

    @property
    def item_name(self):
        return ItemMonth.CleanItemName(self.item.get('name','NoItemName'))
    
    @property
    def name(self):
        return self.item.get('name',"No Item Name")

    @property
    def get_lookup_entry(self):
        return {'key': self.item_name, 'value': self.item.get('name','NoItemName')}
    
    @property
    def item_id(self):
        return self.item.get('id',"NoItemId")

    @property
    def item_path(self):
        return self.item.get('path',"NoItemPath")

    #@property
    #def _growMonthParent(self):
    #    if self._in_growMonthParent is None:
    #        gwParDoc = self.get_firestore_client().document(self.parent_path)
    #        self._in_growMonthParent = GetInstance("GrowMonth",gwParDoc)
    #    return self._in_growMonthParent

    @classmethod
    def getItemMonthInstance(cls, growMonthId, itemType, itemName):
        clt = ItemMonth.get_client()
        item = InventoryActiveItems.GetItemByName(itemType,itemName)
        if item is None:
            raise Exception("Item of type {}, with name {}, Not Found.".format(itemType,itemName))
        item = item.get_dict()
        gmPath = ItemMonth.COLLECTION_NAME+'/'+clt.company+'/Sales_Inventory/Converted/GrowMonth/'+growMonthId
        #imPath = gmPath+'/Items/'+itemType+"_"+ItemMonth.CleanItemName(item.get('name','NoNameGiven'))  
        imPath = ItemMonth.GetPathStr(gmPath,itemType,item.get('name','NoNameGiven'))
        imDoc = ItemMonth.get_firestore_client().document(imPath)
        return ItemMonth.getInstanceItem(imDoc,growMonthId, itemType, item)
    
    @classmethod
    def getItemMonthInstanceByPath(cls,inPath):
        fsDocument = ItemMonth.get_firestore_client().document(inPath)
        ref,snap = ItemMonth.getDocuments(fsDocument)
        docDict = snap.to_dict() if snap.exists else {}
        docDict['fs_docSnap'] = snap
        docDict['fs_docRef'] = ref
        return ItemMonth(ItemMonth.get_firestore_client(),**docDict)

    @classmethod
    def getInstanceItem(cls,fsDocument,growMonthId, itemType, item):
        ref,snap = ItemMonth.getDocuments(fsDocument)
        docDict = snap.to_dict() if snap.exists else {}
        docDict['fs_docSnap'] = snap
        docDict['fs_docRef'] = ref
        docDict['grow_month'] = growMonthId
        docDict['item_type'] = itemType
        docDict['item'] = item
        return ItemMonth(ItemMonth.get_firestore_client(),**docDict)

    @classmethod
    def getInstance(cls,fsDocument):
        ref,snap = ItemMonth.getDocuments(fsDocument)
        docDict = snap.to_dict() if snap.exists else {}
        docDict['fs_docSnap'] = snap
        docDict['fs_docRef'] = ref
        return ItemMonth(ItemMonth.get_firestore_client(),**docDict)

    @classmethod
    def CleanItemName(cls,inName):
        return inName.replace("'","").replace('"','').replace(' ','').replace(".","").replace('&',"")

    @property
    def notes(self):
        if self._notes is None:
            notes = self._notesCollection.getNotesByItemName(self.item_name)
            self._notes = notes
        return self._notes

    @property
    def notes_dict(self):
        return [note.get_dict() for note in self.notes]

    @property
    def supply(self):
        if self._supplies is None:
            supplies = self._supplyCollection.getSupplyByItemName(self.item_name)
            self._supplies = supplies
        return self._supplies

    def create_note(self, note):
        return self._notesCollection.create_note(self.item_name, note)

    def delete_note(self, note_id):
        return self._notesCollection.delete_note(note_id)
        
    def create_supply(self,supplier_id, inForecast, confirmation_num):
        return self._supplyCollection.create_supply(self.item_name,supplier_id,inForecast,confirmation_num)

    def get_itemmonth_dict(self):
        d = {'name': self.item['name'],
             'grow_month': self._growMonthParent.get_growweek_dict(),
             'actual': self.actual,
             'inventory_set': self.inventory_set,
             'color_groupings': self.color_groupings,
             '_id':self.id}

        return d

    def update_groupings(self, grouping, reset=False):
        """
        TODO
        """
        total_qnt = 0
        vals = False
        for key in grouping.keys():
            vals = True
            qnt = grouping[key]
            total_qnt = total_qnt + int(qnt)

        if vals or reset:
            self.actual = total_qnt

        self.grouping = grouping
        self.update_ndb()
        return True


    def update_color_grouping(self, color_grouping, reset=False):
        """
        The color grouping object should be a dict where the keys are colors and a quantity
        This function will add the json object and then go through and count the numbers and update the actual quantity
        :param color_grouping:
        :return:
        """
        total_qnt = 0
        vals = False
        for key in color_grouping.keys():
            vals = True
            qnt = color_grouping[key]
            total_qnt = total_qnt + int(qnt)

        if vals or reset:
            self.actual = total_qnt

        self.color_groupings = color_grouping
        self.update_ndb()
        return True

    def get_schema(self):
        schema = self.get_bq_schema()
        return schema

    def get_values_dict(self):
        return self.get_dict()

    @property
    def next(self):
        return ItemMonth.get_or_create(self.item_type, self.item, self._growMonthParent.next_week)

    @property
    def prior(self):
        return ItemMonth.get_or_create(self.item_type, self.item, self._growMonthParent.prior_week)

    @property
    def forecasts(self):
        fcast = 0
        for supp in self.supply:
            fcast = fcast + supp.get_forecast()
        return fcast

    @property
    def reserves(self):
        """Pulling this information through the _growMonthParent"""
        return self._growMonthParent.getSummary().getItemReserves(self.item_type, self.item_name)

    def get_total_reserved(self):
        return self._growMonthParent.getSummary().getReserveAmtByItem(self.item_type, self.item_name)

    @classmethod
    def get_or_create(cls,itemType, itemInfo, growMonth):
        itemObj = ItemMonth.GetSBObj(itemInfo['path'])
        return growMonth.get_or_create_itemmonth(itemType,itemObj)

    @classmethod
    def CleanItemType(cls,item_type):
        lower = item_type.lower()
        if (lower.endswith('s')):
            return lower[:-1]
        return lower
    
    @property
    def clean_item_type(self):
        return ItemMonth.CleanItemType(self.item_type)

    def iw_summary(self):
        ps = {}
        ps['_id'] = self.id
        ps['item'] = self.item['name']
        ps['lookup_name'] = self.item_name
        ps['item_id'] = self.item['id']
        ps['month_id'] = self.grow_month
        ps['actual'] = self.actual
        ps['inventory_set'] = self.inventory_set
        ps['forecast'] = self.forecasts
        ps['num_reserved'] = self.get_total_reserved()
        return ps

    def availability(self):
        rsvs = self.get_total_reserved()
        fcast = self.forecasts
        if self.actual > 0:
            return self.actual - rsvs

        return fcast - rsvs

    def dict_summary(self):
        invSetInd = self.inventory_set
        enteredInventory = 0 if self.actual is None else self.actual
        remainingInventory = self.calc_actual
        prevMonthInventory = self.prev_actual
        addedInventory = self.inventory_add
        monthReserves = self.reserve_total
        itemMonthExists = self.exists
        return {'status': {'entry_exists': itemMonthExists, 
                           'inventory_set': invSetInd,
                           'name':self.name,
                           'clean_name':self.item_name,
                           'grow_month':self.grow_month,
                           'item_type':self.item_type}, 
                'stats':
                         {'set_inventory': 0 if enteredInventory is None else enteredInventory,
                          'added_inventory': 0 if addedInventory is None else addedInventory,
                          'remaining_inventory': 0 if remainingInventory is None else remainingInventory,
                          'prev_month_inventory': 0 if prevMonthInventory is None else prevMonthInventory,
                          'month_reserves': monthReserves}}