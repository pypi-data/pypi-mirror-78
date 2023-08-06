from .. import GrowWeek
from .. import GrowMonth
from .. import ItemMonth
from .. import ItemMonthReserves
from .. import ItemMonthSummary
from .. import ItemReserve
from .. import ItemMonthCollection
from .. import DataNumberLookup

import jmespath

class SalesInventoryAPI(object):

    def __init__(self, logger):
        self.logger = logger

    def createReserveAPI(self, reserveDate, customer_id, location_id, product_id, reserved):
        gw = GrowWeek.GetGrowWeekByDate(reserveDate)
        newReserve = gw.create_reserve(
            customer_id, location_id, product_id, reserved, reserveDate)
        summ = gw.getSummary()
        return summ.add_reserve(newReserve)

    def updateReserveAPI(self, reserve_id, customer_id, location_id, product_id, reserved, reserveDate):
        gw = GrowWeek.GetGrowWeekByDate(reserveDate)
        updReserve = gw.update_reserve(
            reserve_id, customer_id, location_id, product_id, reserved, reserveDate)
        summ = gw.getSummary()
        return summ.update_reserve(updReserve)

    def deleteReserveAPI(self, reserve_id):
        ir = ItemReserve.getItemReserveInstance(reserve_id)
        if ir.exists:
            gw = ir._growWeekParent
            summ = gw.getSummary()
            summ.delete_reserve(ir)
            ir.delete_resp()
            return {"status": "success"}
        else:
            path = DataNumberLookup.get_path_for_dnl(reserve_id)
            docRef = ir._fsClient.document(path)
            gw_id = docRef.parent.parent.id
            gw = GrowWeek.getGrowWeekInstance(gw_id)
            summ = gw.getSummary()
            newSumm = [x for x in summ.summary if x.get(
                'id', '') != reserve_id]
            summ.summary = newSumm
            summ.update_ndb()
            return {"status": "success"}

    def getAllReservesAPI(self, reserveDate):
        gw = GrowWeek.GetGrowWeekByDate(reserveDate)
        irList = gw.reserves
        return [resv.get_dict() for resv in irList]

    def getSummReservesAPI(self, reserveDate):
        gw = GrowWeek.GetGrowWeekByDate(reserveDate)
        irList = gw.getSummary().summary
        return irList

    def getReserveAPI(self, reserve_id):
        ir = ItemReserve.getItemReserveInstance(reserve_id)
        return ir.get_dict()

    def _getItemMonth(self, gmId, itT, itN):
        cleanName = ItemMonth.CleanItemName(itN)
        return ItemMonth.getItemMonthInstance(gmId, itT, cleanName)

    def getItemMonthAPI(self, growMonthId, itemType, itemName):
        im = self._getItemMonth(growMonthId, itemType, itemName)
        return self._getItemMonthAPI(im)

    def _getGrowMonthAPI(self, month_id):
        return GrowMonth.getGrowMonthInstance(month_id)

    def _getItemMonthAPI(self, itemMonth):
        restSummary = itemMonth.dict_summary()
        return restSummary
    
    def refreshItemMonthInventory(self,growMonthId, itemType, itemName):
        im = self._getItemMonth(growMonthId, itemType, itemName)
        return self._refreshItemMonthInventory(im)
    
    def _refreshItemMonthInventory(self,itemMonth):
        itemMonth._refreshInventoryLevels()
        ItemMonthSummary.UpdateItemMonthSummary(itemMonth)
        return self._getItemMonthAPI(itemMonth)

    def setItemMonthInventory(self, growMonthId, itemType, itemName, inventoryAmount):
        im = self._getItemMonth(growMonthId, itemType, itemName)
        im.set_actual(inventoryAmount)
        ItemMonthSummary.UpdateItemMonthSummary(im)
        return self._getItemMonthAPI(im)

    def addItemMonthInventory(self, growMonthId, itemType, itemName, addedInventory):
        im = self._getItemMonth(growMonthId, itemType, itemName)
        im.add_inventory(addedInventory)
        ItemMonthSummary.UpdateItemMonthSummary(im)
        return self._getItemMonthAPI(im)

    def unsetItemMonthInventory(self, growMonthId, itemType, itemName):
        im = self._getItemMonth(growMonthId, itemType, itemName)
        im.unset_actual()
        ItemMonthSummary.UpdateItemMonthSummary(im)
        return self._getItemMonthAPI(im)

    def createItemMonthEntryAPI(self, growMonthId, itemType, itemName):
        im = self._getItemMonth(growMonthId, itemType, itemName)
        if not im.exists:
            im._refreshInventoryLevels()
        return True

    def getReservesByName(self, growMonthId, itemType, itemName):
        gm = self._getGrowMonthAPI(growMonthId)
        imr = ItemMonthReserves.getOrCreateMonthReserve(gm)
        reserves = imr.week_summaries
        return reserves.get(itemType,{}).get(ItemMonth.CleanItemName(itemName),[])
    
    def _updateArray(self, arrItem, itemType):
        arrItem['item_type'] = itemType
        itemName = [x[:-4] for x in list(arrItem.keys()) if x.endswith("_qty")][0]
        arrItem['qty'] = arrItem[itemName+"_qty"]
        arrItem['item_name'] = itemName
        return arrItem

    def getReservesAll(self,growMonthId,itemType):
        gm = self._getGrowMonthAPI(growMonthId)
        imr = ItemMonthReserves.getOrCreateMonthReserve(gm)
        reserves = imr.week_summaries
        rArray = jmespath.search(itemType+".*[*][]",reserves)
        return [self._updateArray(x,itemType) for x in rArray]

    def _monthSummaryDict(self, itemMonthReserves):
        return {'details':itemMonthReserves.week_summaries,'summary':itemMonthReserves.month_summary}

    def refreshMonthReservesByWeek(self, growWeekId):
        gm = GrowMonth.getGrowMonthByWeek(growWeekId)
        return self._doRefreshMonthReserves(gm)

    def refreshNext_12_ItemMonths(self,startMonthId, itemType):
        gm = self._getGrowMonthAPI(startMonthId)
        results = []
        for _ in range(12):
            print('Refreshing... '+str(gm.id))
            results.append(self._refreshItemMonthReserves(gm,itemType))
            gm = gm.next
        return jmespath.search("[*][]",results)

    def refreshItemMonthReservesByWeek(self,growWeekId, itemType):
        gm = GrowMonth.getGrowMonthByWeek(growWeekId)
        return self._refreshItemMonthReserves(gm,itemType)

    def refreshItemMonthReservesByMonth(self,growMonthId, itemType):
        gm = self._getGrowMonthAPI(growMonthId)
        return self._refreshItemMonthReserves(gm,itemType)
    
    def _refreshItemMonthReserves(self,growMonth, itemType):
        imc = ItemMonthCollection.getOrCreateInstance(itemType,growMonth)
        ims = imc.refresh_loaded_items()
        resp = []
        for im in ims:
            ItemMonthSummary.UpdateItemMonthSummary(im)
            resp.append(self._getItemMonthAPI(im))
        return resp

    def _doRefreshMonthReserves(self, growMonth):
        imr = ItemMonthReserves.getOrCreateMonthReserve(growMonth)
        imr.load_reserves()
        return self._monthSummaryDict(imr)
    
    def doRefreshMonthReserves(self, growMonthId):
        gm = self._getGrowMonthAPI(growMonthId)
        return self._doRefreshMonthReserves(gm)
        
    def getMonthReserveSummary(self, growMonthId):
        gm = self._getGrowMonthAPI(growMonthId)
        imr = ItemMonthReserves.getOrCreateMonthReserve(gm)
        return self._monthSummaryDict(imr)

    def _getGrowMonthRange(self,startGrowMonth, numMonths):
        year, month = startGrowMonth.split("_")
        retList = [startGrowMonth]
        for _ in range(numMonths-1):
            month = int(month) + 1
            if month == 13:
                year = int(year)+1
                month = 1
            retList.append(str(year)+"_"+str(month).zfill(2))
        return retList

    def getItemMonthSummary(self, itemType, startGrowMonth, numMonths=6):
        growMonths = self._getGrowMonthRange(startGrowMonth,numMonths)
        growMonths.sort()
        years = list(set([x.split("_")[0] for x in growMonths]))
        summs = []
        jPath = "[?status.grow_month == '"+growMonths[0]+"'] | [*].{name: status.name, clean_name: status.clean_name}"
        for year in years:
            startMonth = min([x for x in growMonths if x.split("_")[0] == year]).split("_")[1]
            endMonth = max([x for x in growMonths if x.split("_")[0] == year]).split("_")[1]
            ims = ItemMonthSummary.getInstanceByYearType(year,itemType)
            summs.append(ims.summary_info(startMonth,endMonth))
        summary = [item for sublist in summs for item in sublist]
        items = jmespath.search(jPath,summary)
        items = sorted(items, key = lambda i: i['name']) 
        return {'months': growMonths, 'items': items, 'summary': summary}
