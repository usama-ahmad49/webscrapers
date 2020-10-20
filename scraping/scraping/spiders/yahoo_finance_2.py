from selenium import webdriver
# # from seleniumwire import webdriver
import yahoo_fin.stock_info as si
import requests
import json
import scrapy
from yahoo_fin import options
import csv
import time

csvHeader = ['name', 'ticker', 'fiftyTwoWeekRange', 'marketCap', 'beta_5Y_monthly', 'PE Ratio', 'trailingEps', 'earningsDate', 'dividendRate', 'exDividendDate', '1y_Target_Est', 'totalRevenue TTM', 'totalRevenue 2016', 'totalRevenue 2017', 'totalRevenue 2018', 'totalRevenue 2019', 'totalRevenue 06/2020', 'totalRevenue 03/2020', 'totalRevenue 12/2019', 'totalRevenue 09/2019', 'operatingIncome TTM', 'operatingIncome 2017', 'operatingIncome 2018', 'operatingIncome 2019', 'PretaxIncome TTM', 'PretaxIncome 2017', 'PretaxIncome 2018', 'PretaxIncome 2019', 'taxProvision TTM', 'taxProvision 2017', 'taxProvision 2018', 'taxProvision 2019', 'netIncomeCommonStockholder TTM', 'netIncomeCommonStockholder 2017', 'netIncomeCommonStockholder 2018', 'netIncomeCommonStockholder 2019', 'dilutedNIComStockholders TTM', 'dilutedNIComStockholders 2017', 'dilutedNIComStockholders 2018', 'dilutedNIComStockholders 2019', 'dilutedEPS TTM', 'dilutedEPS 2017', 'dilutedEPS 2018', 'dilutedEPS 2019', 'intrestExpense TTM', 'intrestExpense 2017', 'intrestExpense 2018', 'intrestExpense 2019', 'EBIT TTM', 'EBIT 2017', 'EBIT 2018', 'EBIT 2019', 'operatingIncome 06/2020', 'operatingIncome 03/2020', 'operatingIncome 12/2019', 'operatingIncome 09/2019', 'PretaxIncome 06/2020', 'PretaxIncome 03/2020', 'PretaxIncome 12/2019', 'PretaxIncome 09/2019', 'taxProvision 06/2020', 'taxProvision 03/2020', 'taxProvision 12/2019', 'taxProvision 09/2019', 'netIncomeCommonStockholder 06/2020', 'netIncomeCommonStockholder 03/2020', 'netIncomeCommonStockholder 12/2019', 'netIncomeCommonStockholder 09/2019', 'dilutedNIComStockholders 06/2020', 'dilutedNIComStockholders 03/2020', 'dilutedNIComStockholders 12/2019', 'dilutedNIComStockholders 09/2019', 'dilutedEPS 06/2020', 'dilutedEPS 03/2020', 'dilutedEPS 12/2019', 'dilutedEPS 09/2019', 'intrestExpense 06/2020', 'intrestExpense 03/2020', 'intrestExpense 12/2019', 'intrestExpense 09/2019', 'EBIT 06/2020', 'EBIT 03/2020', 'EBIT 12/2019', 'EBIT 09/2019', 'totalAssets 2019', 'totalAssets 2018', 'totalAssets 2017', 'totalAssets 2016', 'totalCurrentAssets 2019', 'totalCurrentAssets 2018', 'totalCurrentAssets 2017', 'totalCurrentAssets 2016', 'Cash,CashEquilalents&ShortTermInvestments 2019', 'Cash,CashEquilalents&ShortTermInvestments 2018', 'Cash,CashEquilalents&ShortTermInvestments 2017', 'Receivables 2019', 'Receivables 2018', 'Receivables 2017', 'Receivables 2016', 'Inventory 2019', 'Inventory 2018', 'Inventory 2017', 'Inventory 2016', 'longTermDebt 2019', 'longTermDebt 2018', 'longTermDebt 2017', 'longTermDebt 2016', 'stockholdersEquity 2019', 'stockholdersEquity 2018', 'stockholdersEquity 2017', 'stockholdersEquity 2016', 'totalLiab 2019', 'totalLiab 2018', 'totalLiab 2017', 'totalLiab 2016', 'totalAssets 06/2020', 'totalAssets 03/2020', 'totalAssets 12/2019', 'totalAssets 09/2019', 'totalCurrentAssets 06/2020', 'totalCurrentAssets 03/2020', 'totalCurrentAssets 12/2019', 'totalCurrentAssets 09/2019', 'Receivables 06/2020', 'Receivables 03/2020', 'Receivables 12/2019', 'Receivables 09/2019', 'Inventory 06/2020', 'Inventory 03/2020', 'Inventory 12/2019', 'Inventory 09/2019', 'longTermDebt 06/2020', 'longTermDebt 03/2020', 'longTermDebt 12/2019', 'longTermDebt 09/2019', 'stockholdersEquity 06/2020', 'stockholdersEquity 03/2020', 'stockholdersEquity 12/2019', 'stockholdersEquity 09/2019', 'totalLiab 06/2020', 'totalLiab 03/2020', 'totalLiab 12/2019', 'totalLiab 09/2019', 'operatingCashFlow TTM', 'operatingCashFlow 2019', 'operatingCashFlow 2018', 'operatingCashFlow 2017', 'investingCashFlow TTM', 'investingCashFlow 2019', 'investingCashFlow 2018', 'investingCashFlow 2017', 'cashFlowFromContinuingInvestingActivities TTM', 'cashFlowFromContinuingInvestingActivities 2019', 'cashFlowFromContinuingInvestingActivities 2018', 'cashFlowFromContinuingInvestingActivities 2017', 'financingCashFlow TTM', 'financingCashFlow 2019', 'financingCashFlow 2018', 'financingCashFlow 2017', 'endCashPosition TTM', 'endCashPosition 2019', 'endCashPosition 2018', 'endCashPosition 2017', 'incomeTaxPaidSupplementalData TTM', 'incomeTaxPaidSupplementalData 2019', 'incomeTaxPaidSupplementalData 2018', 'incomeTaxPaidSupplementalData 2017', 'capitalExpenditure TTM', 'capitalExpenditure 2019', 'capitalExpenditure 2018', 'capitalExpenditure 2017', 'issuanceOfCapitalStock TTM', 'issuanceOfCapitalStock 2019', 'issuanceOfCapitalStock 2018', 'issuanceOfCapitalStock 2017', 'issuanceOfDebt TTM', 'issuanceOfDebt 2019', 'issuanceOfDebt 2018', 'issuanceOfDebt 2017', 'repaymentOfDebt TTM', 'repaymentOfDebt 2019', 'repaymentOfDebt 2018', 'repaymentOfDebt 2017', 'repurchaseOfCapitalStock TTM', 'repurchaseOfCapitalStock 2019', 'repurchaseOfCapitalStock 2018', 'repurchaseOfCapitalStock 2017', 'freeCashFlow TTM', 'freeCashFlow 2019', 'freeCashFlow 2018', 'freeCashFlow 2017', 'operatingCashFlow 06/2020', 'operatingCashFlow 03/2020', 'operatingCashFlow 12/2020', 'operatingCashFlow 09/2020', 'investingCashFlow 06/2020', 'investingCashFlow 03/2020', 'investingCashFlow 12/2019', 'investingCashFlow 09/2019', 'cashFlowFromContinuingInvestingActivities 06/2020', 'cashFlowFromContinuingInvestingActivities 03/2020', 'cashFlowFromContinuingInvestingActivities 12/2019', 'cashFlowFromContinuingInvestingActivities 09/2019', 'financingCashFlow 06/2020', 'financingCashFlow 03/2020', 'financingCashFlow 12/2019', 'financingCashFlow 09/2019', 'capitalExpenditure 06/2020', 'capitalExpenditure 03/2020', 'capitalExpenditure 12/2019', 'capitalExpenditure 09/2019', 'issuanceOfCapitalStock 06/2020', 'avg.Estimate CurrentQtr', 'avg.Estimate NextQtr', 'avg.Estimate CurrentYear', 'avg.Estimate NextYear', 'salesGrowth CurrentQtr', 'salesGrowth NextQtr', 'salesGrowth CurrentYear', 'salesGrowth NextYear', 'revenueEstimate Current Year', 'revenueEstimate Next Year', 'growthEstimates CurrentQtr', 'growthEstimates NextQtr', 'growthEstimates CurrentYear', 'growthEstimates NextYear', 'growthEstimates Next5Years', 'revenueEstimate next Year']
csv_file = open("yahoo_finance.csv", 'w', newline='')
writer = csv.DictWriter(csv_file, fieldnames=csvHeader)
writer.writeheader()


def get_dict_value(data, key_list, default=''):
    for key in key_list:
        if data and isinstance(data, dict):
            data = data.get(key, default)
        else:
            return default
    return data


tickers = ["AAPL", "AMGN", "AXP", "BA", "CAT", "CRM", "CSCO", "CVX", "DIS", "DOW", "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "KO", "MCD", "MMM", "MRK", "MSFT", "NKE", "PG", "TRV", "UNH", "V", "VZ", "WBA", "WMT", "AACG", "AACQ", "AACQU", "AACQW", "AAL", "AAME", "AAOI", "AAON", "AAPL", "AAWW", "AAXJ", "AAXN", "ABCB", "ABEO", "ABIO", "ABMD", "ABTX", "ABUS", "ACAD", "ACAM", "ACAMU", "ACAMW", "ACBI", "ACCD", "ACER", "ACET", "ACEV", "ACEVU", "ACEVW", "ACGL", "ACGLO", "ACGLP", "ACHC", "ACHV", "ACIA", "ACIU", "ACIW", "ACLS", "ACMR", "ACNB", "ACOR", "ACRS", "ACRX", "ACST", "ACT", "ACTCU", "ACTG", "ACWI", "ACWX", "ADAP", "ADBE", "ADES", "ADI", "ADIL", "ADILW", "ADMA", "ADMP", "ADMS", "ADP", "ADPT", "ADRE", "ADRO", "ADSK", "ADTN", "ADTX", "ADUS", "ADVM", "ADXN", "ADXS", "AEGN", "AEHR", "AEIS", "AEMD", "AEP", "AEPPL", "AEPPZ", "AERI", "AESE", "AEY", "AEYE", "AEZS", "AFIB", "AFIN", "AFINP",
           "AFMD", "AFYA", "AGBA", "AGBAR", "AGBAU", "AGBAW", "AGCUU", "AGEN", "AGFS", "AGIO", "AGLE", "AGMH", "AGNC", "AGNCM", "AGNCN", "AGNCO", "AGNCP", "AGRX", "AGTC", "AGYS", "AGZD", "AHACU", "AHCO", "AHPI", "AIA", "AIH", "AIHS", "AIKI", "AIMC", "AIMT", "AINV", "AIQ", "AIRG", "AIRR", "AIRT", "AIRTP", "AIRTW", "AKAM", "AKBA", "AKCA", "AKER", "AKRO", "AKTS", "AKTX", "AKU", "AKUS", "ALAC", "ALACR", "ALACU", "ALACW", "ALBO", "ALCO", "ALDX", "ALEC", "ALGN", "ALGT", "ALIM", "ALJJ", "ALKS", "ALLK", "ALLO", "ALLT", "ALNA", "ALNY", "ALOT", "ALPN", "ALRM", "ALRN", "ALRS", "ALSK", "ALT", "ALTA", "ALTM", "ALTR", "ALTY", "ALVR", "ALXN", "ALXO", "ALYA", "AMAG", "AMAL", "AMAT", "AMBA", "AMCA", "AMCI", "AMCIU", "AMCIW", "AMCX", "AMD", "AMED", "AMEH", "AMGN", "AMHC", "AMHCU", "AMHCW", "AMKR", "AMNB", "AMOT", "AMPH", "AMRB", "AMRH", "AMRHW", "AMRK", "AMRN", "AMRS", "AMSC", "AMSF", "AMST", "AMSWA",
           "AMTB", "AMTBB", "AMTD", "AMTI", "AMTX", "AMWD", "AMYT", "AMZN", "ANAB", "ANAT", "ANCN", "ANDA", "ANDAR", "ANDAU", "ANDAW", "ANDE", "ANGI", "ANGL", "ANGO", "ANIK", "ANIP", "ANIX", "ANNX", "ANPC", "ANSS", "ANTE", "ANY", "AOSL", "AOUT", "APA", "APDN", "APEI", "APEN", "APEX", "APHA", "API", "APLS", "APLT", "APM", "APOG", "APOP", "APOPW", "APPF", "APPN", "APPS", "APRE", "APTO", "APTX", "APVO", "APWC", "APXT", "APXTU", "APXTW", "APYX", "AQB", "AQMS", "AQST", "ARAV", "ARAY", "ARCB", "ARCC", "ARCE", "ARCT", "ARDS", "ARDX", "AREC", "ARGX", "ARKR", "ARLP", "ARNA", "AROW", "ARPO", "ARQT", "ARTL", "ARTLW", "ARTNA", "ARTW", "ARVN", "ARWR", "ARYA", "ARYB", "ARYBU", "ARYBW", "ASET", "ASLN", "ASMB", "ASML", "ASND", "ASO", "ASPS", "ASPU", "ASRT", "ASRV", "ASRVP", "ASTC", "ASTE", "ASUR", "ASYS", "ATAX", "ATCX", "ATCXW", "ATEC", "ATEX", "ATHA", "ATHE", "ATHX", "ATIF", "ATLC", "ATLO", "ATNI",
           "ATNX", "ATOM", "ATOS", "ATRA", "ATRC", "ATRI", "ATRO", "ATRS", "ATSG", "ATVI", "ATXI", "AUB", "AUBAP", "AUBN", "AUDC", "AUPH", "AUTL", "AUTO", "AUVI", "AVAV", "AVCO", "AVCT", "AVCTW", "AVDL", "AVEO", "AVGO", "AVGOP", "AVGR", "AVID", "AVNW", "AVO", "AVRO", "AVT", "AVXL", "AWH", "AWRE", "AXAS", "AXDX", "AXGN", "AXGT", "AXLA", "AXNX", "AXSM", "AXTI", "AY", "AYLA", "AYRO", "AYTU", "AZN", "AZPN", "AZRX", "BAND", "BANF", "BANFP", "BANR", "BANX", "BASI", "BATRA", "BATRK", "BBBY", "BBCP", "BBGI", "BBH", "BBI", "BBIO", "BBQ", "BBSI", "BCBP", "BCDA", "BCDAW", "BCEL", "BCLI", "BCML", "BCOR", "BCOV", "BCOW", "BCPC", "BCRX", "BCTG", "BCYC", "BDGE", "BDSI", "BDTX", "BEAM", "BEAT", "BECN", "BEEM", "BEEMW", "BELFA", "BELFB", "BFC", "BFIN", "BFIT", "BFRA", "BFST", "BGCP", "BGFV", "BGNE", "BGRN", "BHAT", "BHF", "BHFAL", "BHFAO", "BHFAP", "BHTG", "BIB", "BICK", "BIDU", "BIGC", "BIIB", "BILI",
           "BIMI", "BIOC", "BIOL", "BIS", "BIVI", "BJK", "BJRI", "BKCC", "BKEP", "BKEPP", "BKNG", "BKSC", "BKYI", "BL", "BLBD", "BLCM", "BLCN", "BLCT", "BLDP", "BLDR", "BLFS", "BLI", "BLIN", "BLKB", "BLMN", "BLNK", "BLNKW", "BLPH", "BLRX", "BLU", "BLUE", "BMCH", "BMLP", "BMRA", "BMRC", "BMRN", "BMTC", "BND", "BNDW", "BNDX", "BNFT", "BNGO", "BNGOW", "BNR", "BNSO", "BNTC", "BNTX", "BOCH", "BOKF", "BOKFL", "BOMN", "BOOM", "BOSC", "BOTJ", "BOTZ", "BOWXU", "BOXL", "BPFH", "BPMC", "BPOP", "BPOPM", "BPOPN", "BPRN", "BPTH", "BPY", "BPYPN", "BPYPO", "BPYPP", "BPYU", "BPYUP", "BRID", "BRKL", "BRKR", "BRKS", "BRLI", "BRLIR", "BRLIU", "BRLIW", "BROG", "BROGW", "BRP", "BRPA", "BRPAR", "BRPAU", "BRPAW", "BRQS", "BRY", "BSAE", "BSBE", "BSBK", "BSCE", "BSCK", "BSCL", "BSCM", "BSCN", "BSCO", "BSCP", "BSCQ", "BSCR", "BSCS", "BSCT", "BSCU", "BSDE", "BSET", "BSGM", "BSJK", "BSJL", "BSJM", "BSJN", "BSJO",
           "BSJP", "BSJQ", "BSJR", "BSJS", "BSML", "BSMM", "BSMN", "BSMO", "BSMP", "BSMQ", "BSMR", "BSMS", "BSMT", "BSMU", "BSQR", "BSRR", "BSTC", "BSVN", "BSY", "BTAI", "BTAQU", "BTBT", "BTEC", "BUG", "BUSE", "BVXV", "BWAY", "BWB", "BWEN", "BWFG", "BWMX", "BXRX", "BYFC", "BYND", "BYSI", "BZUN", "CAAS", "CABA", "CAC", "CACC", "CACG", "CAKE", "CALA", "CALB", "CALM", "CALT", "CAMP", "CAMT", "CAN", "CAPAU", "CAPR", "CAR", "CARA", "CARE", "CARG", "CARV", "CARZ", "CASA", "CASH", "CASI", "CASS", "CASY", "CATB", "CATC", "CATH", "CATM", "CATY", "CBAN", "CBAT", "CBAY", "CBFV", "CBIO", "CBLI", "CBMB", "CBMG", "CBNK", "CBPO", "CBRL", "CBSH", "CBTX", "CCAP", "CCB", "CCBG", "CCCC", "CCCL", "CCD", "CCLP", "CCMP", "CCNC", "CCNE", "CCNEP", "CCOI", "CCRC", "CCRN", "CCXI", "CD", "CDC", "CDEV", "CDK", "CDL", "CDLX", "CDMO", "CDMOP", "CDNA", "CDNS", "CDTX", "CDW", "CDXC", "CDXS", "CDZI", "CECE", "CEFA",
           "CELC", "CELH", "CEMI", "CENT", "CENTA", "CENX", "CERC", "CERN", "CERS", "CETV", "CETX", "CETXP", "CETXW", "CEVA", "CEY", "CEZ", "CFA", "CFB", "CFBI", "CFBK", "CFFA", "CFFAU", "CFFAW", "CFFI", "CFFN", "CFIIU", "CFMS", "CFO", "CFRX", "CG", "CGBD", "CGEN", "CGIX", "CGNX", "CGO", "CGRO", "CGROU", "CGROW", "CHB", "CHCI", "CHCO", "CHDN", "CHEF", "CHEK", "CHEKZ", "CHFS", "CHI", "CHKP", "CHMA", "CHMG", "CHNA", "CHNG", "CHNGU", "CHNR", "CHPM", "CHPMU", "CHPMW", "CHRS", "CHRW", "CHSCL", "CHSCM", "CHSCN", "CHSCO", "CHSCP", "CHTR", "CHUY", "CHW", "CHY", "CIBR", "CID", "CIDM", "CIGI", "CIH", "CIIC", "CIICU", "CIICW", "CIL", "CINF", "CIVB", "CIZ", "CIZN", "CJJD", "CKPT", "CLAR", "CLBK", "CLBS", "CLCT", "CLDB", "CLDX", "CLEU", "CLFD", "CLGN", "CLIR", "CLLS", "CLMT", "CLNE", "CLOU", "CLPS", "CLPT", "CLRB", "CLRBZ", "CLRG", "CLRO", "CLSD", "CLSK", "CLSN", "CLVS", "CLWT", "CLXT", "CMBM",
           "CMCO", "CMCSA", "CMCT", "CMCTP", "CME", "CMFNL", "CMLFU", "CMLS", "CMPI", "CMPR", "CMPS", "CMRX", "CMTL", "CNBKA", "CNCE", "CNCR", "CNDT", "CNET", "CNFR", "CNFRL", "CNNB", "CNOB", "CNSL", "CNSP", "CNST", "CNTG", "CNTY", "CNXN", "COCP", "CODA", "CODX", "COFS", "COHR", "COHU", "COKE", "COLB", "COLL", "COLM", "COMM", "COMT", "CONE", "CONN", "COOP", "CORE", "CORT", "COST", "COUP", "COWN", "COWNL", "COWNZ", "CPAA", "CPAAU", "CPAAW", "CPAH", "CPHC", "CPIX", "CPLP", "CPRT", "CPRX", "CPSH", "CPSI", "CPSS", "CPST", "CPTA", "CPTAG", "CPTAL", "CPZ", "CRAI", "CRBP", "CRDF", "CREE", "CREG", "CRESY", "CREX", "CREXW", "CRIS", "CRMT", "CRNC", "CRNT", "CRNX", "CRON", "CROX", "CRSA", "CRSAU", "CRSAW", "CRSP", "CRSR", "CRTD", "CRTDW", "CRTO", "CRTX", "CRUS", "CRVL", "CRVS", "CRWD", "CRWS", "CSA", "CSB", "CSBR", "CSCO", "CSCW", "CSF", "CSGP", "CSGS", "CSII", "CSIQ", "CSML", "CSOD", "CSPI",
           "CSQ", "CSSE", "CSSEN", "CSSEP", "CSTE", "CSTL", "CSTR", "CSWC", "CSWCL", "CSWI", "CSX", "CTAS", "CTBI", "CTG", "CTHR", "CTIB", "CTIC", "CTMX", "CTRE", "CTRM", "CTRN", "CTSH", "CTSO", "CTXR", "CTXRW", "CTXS", "CUBA", "CUE", "CUTR", "CVAC", "CVBF", "CVCO", "CVCY", "CVET", "CVGI", "CVGW", "CVLG", "CVLT", "CVLY", "CVV", "CWBC", "CWBR", "CWCO", "CWST", "CXDC", "CXDO", "CXSE", "CYAD", "CYAN", "CYBE", "CYBR", "CYCC", "CYCCP", "CYCN", "CYRN", "CYRX", "CYTK", "CZNC", "CZR", "CZWI", "DADA", "DAIO", "DAKT", "DALI", "DARE", "DAX", "DBVT", "DBX", "DCOM", "DCOMP", "DCPH", "DCT", "DCTH", "DDIV", "DDOG", "DENN", "DFFN", "DFHT", "DFHTU", "DFHTW", "DFNL", "DFPH", "DFPHU", "DFPHW", "DGICA", "DGICB", "DGII", "DGLY", "DGRE", "DGRS", "DGRW", "DHC", "DHCNI", "DHCNL", "DHIL", "DINT", "DIOD", "DISCA", "DISCB", "DISCK", "DISH", "DJCO", "DKNG", "DLHC", "DLPN", "DLPNW", "DLTH", "DLTR", "DMAC", "DMLP",
           "DMRC", "DMTK", "DMXF", "DNKN", "DNLI", "DOCU", "DOGZ", "DOMO", "DOOO", "DORM", "DOX", "DOYU", "DPHC", "DPHCU", "DPHCW", "DRAD", "DRADP", "DRIO", "DRIOW", "DRIV", "DRNA", "DRRX", "DRTT", "DSGX", "DSKE", "DSKEW", "DSPG", "DSWL", "DTEA", "DTIL", "DTSS", "DUO", "DUOT", "DUSA", "DVAX", "DVLU", "DVOL", "DVY", "DWAS", "DWAT", "DWAW", "DWCR", "DWEQ", "DWFI", "DWLD", "DWMC", "DWPP", "DWSH", "DWSN", "DWUS", "DXCM", "DXGE", "DXJS", "DXLG", "DXPE", "DXYN", "DYAI", "DYN", "DYNT", "DZSI", "EA", "EARS", "EAST", "EBAY", "EBAYL", "EBIX", "EBIZ", "EBMT", "EBON", "EBSB", "EBTC", "ECHO", "ECOL", "ECOLW", "ECOR", "ECOW", "ECPG", "EDAP", "EDIT", "EDNT", "EDOC", "EDRY", "EDSA", "EDTK", "EDUC", "EDUT", "EEFT", "EEMA", "EFAS", "EFOI", "EFSC", "EGAN", "EGBN", "EGLE", "EGOV", "EGRX", "EH", "EHTH", "EIDX", "EIGI", "EIGR", "EKSO", "ELOX", "ELSE", "ELTK", "EMB", "EMCB", "EMCF", "EMIF", "EMKR", "EML",
           "EMXC", "ENDP", "ENG", "ENLV", "ENOB", "ENPH", "ENSG", "ENTA", "ENTG", "ENTX", "ENTXW", "ENZL", "EOLS", "EPAY", "EPIX", "EPSN", "EPZM", "EQ", "EQBK", "EQIX", "EQOS", "EQOSW", "EQRR", "ERES", "ERESU", "ERESW", "ERIC", "ERIE", "ERII", "ERYP", "ESBK", "ESCA", "ESEA", "ESGD", "ESGE", "ESGR", "ESGRO", "ESGRP", "ESGU", "ESLT", "ESPO", "ESPR", "ESQ", "ESSA", "ESSC", "ESSCR", "ESSCU", "ESSCW", "ESTA", "ESXB", "ETAC", "ETACU", "ETACW", "ETFC", "ETNB", "ETON", "ETSY", "ETTX", "EUFN", "EVBG", "EVER", "EVFM", "EVGBC", "EVGN", "EVK", "EVLMC", "EVLO", "EVOK", "EVOL", "EVOP", "EVSTC", "EWBC", "EWJE", "EWJV", "EWZS", "EXAS", "EXC", "EXEL", "EXFO", "EXLS", "EXPC", "EXPCU", "EXPCW", "EXPD", "EXPE", "EXPI", "EXPO", "EXTR", "EYE", "EYEG", "EYEN", "EYES", "EYESW", "EYPT", "EZPW", "FAAR", "FAB", "FAD", "FALN", "FAMI", "FANG", "FANH", "FARM", "FARO", "FAST", "FAT", "FATBP", "FATBW", "FATE", "FB",
           "FBIO", "FBIOP", "FBIZ", "FBMS", "FBNC", "FBRX", "FBSS", "FBZ", "FCA", "FCACU", "FCAL", "FCAN", "FCAP", "FCBC", "FCBP", "FCCO", "FCCY", "FCEF", "FCEL", "FCFS", "FCNCA", "FCNCP", "FCRD", "FCVT", "FDBC", "FDIV", "FDNI", "FDT", "FDTS", "FDUS", "FDUSG", "FDUSL", "FDUSZ", "FEIM", "FELE", "FEM", "FEMB", "FEMS", "FENC", "FEP", "FEUZ", "FEX", "FEYE", "FFBC", "FFBW", "FFHL", "FFIC", "FFIN", "FFIV", "FFNW", "FFWM", "FGBI", "FGEN", "FGM", "FHB", "FHK", "FIBK", "FID", "FIII", "FIIIU", "FIIIW", "FINX", "FISI", "FISV", "FITB", "FITBI", "FITBO", "FITBP", "FIVE", "FIVN", "FIXD", "FIXX", "FIZZ", "FJP", "FKO", "FKU", "FLDM", "FLEX", "FLGT", "FLIC", "FLIR", "FLL", "FLMN", "FLMNW", "FLN", "FLNT", "FLUX", "FLWS", "FLXN", "FLXS", "FMAO", "FMB", "FMBH", "FMBI", "FMBIO", "FMBIP", "FMCI", "FMCIU", "FMCIW", "FMHI", "FMK", "FMNB", "FMTX", "FNCB", "FNHC", "FNK", "FNKO", "FNLC", "FNWB", "FNX", "FNY",
           "FOCS", "FOLD", "FONR", "FORD", "FORK", "FORM", "FORR", "FORTY", "FOSL", "FOX", "FOXA", "FOXF", "FPA", "FPAY", "FPRX", "FPXE", "FPXI", "FRAF", "FRAN", "FRBA", "FRBK", "FREE", "FREEW", "FREQ", "FRG", "FRGAP", "FRGI", "FRHC", "FRLN", "FRME", "FROG", "FRPH", "FRPT", "FRSX", "FRTA", "FSBW", "FSDC", "FSEA", "FSFG", "FSLR", "FSRV", "FSRVU", "FSRVW", "FSTR", "FSV", "FSZ", "FTA", "FTAC", "FTACU", "FTACW", "FTAG", "FTC", "FTCS", "FTDR", "FTEK", "FTFT", "FTGC", "FTHI", "FTHM", "FTIVU", "FTLB", "FTNT", "FTOCU", "FTRI", "FTSL", "FTSM", "FTXD", "FTXG", "FTXH", "FTXL", "FTXN", "FTXO", "FTXR", "FULC", "FULT", "FUNC", "FUND", "FUSB", "FUSN", "FUTU", "FUV", "FV", "FVC", "FVCB", "FVE", "FWONA", "FWONK", "FWP", "FWRD", "FXNC", "FYC", "FYT", "FYX", "GABC", "GAIA", "GAIN", "GAINL", "GAINM", "GALT", "GAN", "GARS", "GASS", "GBCI", "GBDC", "GBIO", "GBLI", "GBLIL", "GBT", "GCBC", "GDEN", "GDRX",
           "GDS", "GDYN", "GDYNW", "GEC", "GECC", "GECCL", "GECCM", "GECCN", "GENC", "GENE", "GENY", "GEOS", "GERN", "GEVO", "GFED", "GFN", "GFNCP", "GFNSL", "GGAL", "GH", "GHIV", "GHIVU", "GHIVW", "GHSI", "GIFI", "GIGE", "GIGM", "GIII", "GILD", "GILT", "GLAD", "GLADD", "GLADL", "GLBS", "GLBZ", "GLDD", "GLDI", "GLG", "GLIBA", "GLIBP", "GLMD", "GLNG", "GLPG", "GLPI", "GLRE", "GLSI", "GLUU", "GLYC", "GMAB", "GMBL", "GMBLW", "GMDA", "GMHI", "GMHIU", "GMHIW", "GMLP", "GMLPP", "GNCA", "GNFT", "GNLN", "GNMA", "GNMK", "GNOM", "GNPX", "GNRS", "GNRSU", "GNRSW", "GNSS", "GNTX", "GNTY", "GNUS", "GO", "GOCO", "GOGL", "GOGO", "GOOD", "GOODM", "GOODN", "GOOG", "GOOGL", "GOSS", "GOVX", "GOVXW", "GP", "GPOR", "GPP", "GPRE", "GPRO", "GRAY", "GRBK", "GRCY", "GRCYU", "GRCYW", "GRFS", "GRID", "GRIF", "GRIL", "GRIN", "GRMN", "GRNQ", "GRNV", "GRNVR", "GRNVU", "GRNVW", "GROW", "GRPN", "GRSV", "GRSVU", "GRSVW",
           "GRTS", "GRTX", "GRVY", "GRWG", "GSBC", "GSHD", "GSIT", "GSKY", "GSM", "GSMG", "GSMGW", "GSUM", "GT", "GTEC", "GTH", "GTHX", "GTIM", "GTLS", "GTYH", "GURE", "GVP", "GWGH", "GWPH", "GWRS", "GXGX", "GXGXU", "GXGXW", "GXTG", "GYRO", "HA", "HAFC", "HAIN", "HALL", "HALO", "HAPP", "HARP", "HAS", "HAYN", "HBAN", "HBANN", "HBANO", "HBCP", "HBIO", "HBMD", "HBNC", "HBP", "HBT", "HCAC", "HCACU", "HCACW", "HCAP", "HCAPZ", "HCAT", "HCCH", "HCCHR", "HCCHU", "HCCHW", "HCCI", "HCCO", "HCCOU", "HCCOW", "HCDI", "HCKT", "HCM", "HCSG", "HDS", "HDSN", "HEAR", "HEBT", "HEC", "HECCU", "HECCW", "HEES", "HELE", "HEPA", "HERD", "HERO", "HEWG", "HFBL", "HFFG", "HFWA", "HGBL", "HGEN", "HGSH", "HHR", "HIBB", "HIFS", "HIHO", "HIMX", "HJLI", "HJLIW", "HLAL", "HLG", "HLIO", "HLIT", "HLNE", "HMHC", "HMNF", "HMST", "HMSY", "HMTV", "HNDL", "HNNA", "HNRG", "HOFT", "HOFV", "HOFVW", "HOL", "HOLI", "HOLUU",
           "HOLUW", "HOLX", "HOMB", "HONE", "HOOK", "HOPE", "HOTH", "HOVNP", "HPK", "HPKEW", "HQI", "HQY", "HRMY", "HROW", "HRTX", "HRZN", "HSAQ", "HSDT", "HSIC", "HSII", "HSKA", "HSON", "HSTM", "HSTO", "HTBI", "HTBK", "HTBX", "HTGM", "HTHT", "HTIA", "HTLD", "HTLF", "HTLFP", "HUBG", "HUGE", "HUIZ", "HURC", "HURN", "HUSN", "HVBC", "HWBK", "HWC", "HWCC", "HWCPL", "HWCPZ", "HWKN", "HX", "HYAC", "HYACU", "HYACW", "HYLS", "HYMC", "HYMCW", "HYMCZ", "HYRE", "HYXF", "HYZD", "HZNP", "IAC", "IART", "IBB", "IBBJ", "IBCP", "IBEX", "IBKR", "IBOC", "IBTA", "IBTB", "IBTD", "IBTE", "IBTF", "IBTG", "IBTH", "IBTI", "IBTJ", "IBTK", "IBTX", "IBUY", "ICAD", "ICBK", "ICCC", "ICCH", "ICFI", "ICHR", "ICLK", "ICLN", "ICLR", "ICMB", "ICON", "ICPT", "ICUI", "IDCC", "IDEX", "IDLB", "IDN", "IDRA", "IDXG", "IDXX", "IDYA", "IEA", "IEAWW", "IEC", "IEF", "IEI", "IEP", "IESC", "IEUS", "IFGL", "IFMK", "IFRX", "IFV",
           "IGACU", "IGF", "IGIB", "IGIC", "IGICW", "IGMS", "IGOV", "IGSB", "IHRT", "III", "IIIN", "IIIV", "IIN", "IIVI", "IIVIP", "IJT", "IKNX", "ILMN", "ILPT", "IMAB", "IMAC", "IMACW", "IMBI", "IMGN", "IMKTA", "IMMP", "IMMR", "IMMU", "IMNM", "IMOS", "IMRA", "IMRN", "IMRNW", "IMTE", "IMTX", "IMTXW", "IMUX", "IMV", "IMVT", "IMXI", "INAQU", "INBK", "INBKL", "INBKZ", "INBX", "INCY", "INDB", "INDY", "INFI", "INFN", "INFR", "INGN", "INMB", "INMD", "INO", "INOD", "INOV", "INPX", "INSE", "INSG", "INSM", "INSU", "INSUU", "INSUW", "INTC", "INTG", "INTU", "INVA", "INVE", "INZY", "IONS", "IOSP", "IOVA", "IPAR", "IPDN", "IPGP", "IPHA", "IPKW", "IPLDP", "IPWR", "IQ", "IRBT", "IRCP", "IRDM", "IRIX", "IRMD", "IROQ", "IRTC", "IRWD", "ISBC", "ISDX", "ISEE", "ISEM", "ISHG", "ISIG", "ISNS", "ISRG", "ISSC", "ISTB", "ISTR", "ITACU", "ITCI", "ITI", "ITIC", "ITMR", "ITOS", "ITRI", "ITRM", "ITRN", "IUS",
           "IUSB", "IUSG", "IUSS", "IUSV", "IVA", "IVAC", "IXUS", "IZEA", "JACK", "JAGX", "JAKK", "JAMF", "JAN", "JAZZ", "JBHT", "JBLU", "JBSS", "JCOM", "JCS", "JCTCF", "JD", "JFIN", "JFU", "JG", "JJSF", "JKHY", "JKI", "JMPNL", "JMPNZ", "JNCE", "JOBS", "JOUT", "JRJC", "JRSH", "JRVR", "JSM", "JSMD", "JSML", "JVA", "JYNT", "KALA", "KALU", "KALV", "KBAL", "KBLM", "KBLMR", "KBLMU", "KBLMW", "KBNT", "KBNTW", "KBSF", "KBWB", "KBWD", "KBWP", "KBWR", "KBWY", "KC", "KCAPL", "KDP", "KE", "KELYA", "KELYB", "KEQU", "KERN", "KERNW", "KFFB", "KFRC", "KHC", "KIDS", "KIN", "KINS", "KIRK", "KLAC", "KLDO", "KLIC", "KLXE", "KMDA", "KNDI", "KNSA", "KNSL", "KOD", "KOPN", "KOR", "KOSS", "KPTI", "KRKR", "KRMA", "KRMD", "KRNT", "KRNY", "KROS", "KRTX", "KRUS", "KRYS", "KSMT", "KSMTU", "KSMTW", "KSPN", "KTCC", "KTOS", "KTOV", "KTOVW", "KTRA", "KURA", "KVHI", "KXIN", "KYMR", "KZIA", "KZR", "LACQ", "LACQU",
           "LACQW", "LAKE", "LAMR", "LANC", "LAND", "LANDP", "LARK", "LASR", "LATN", "LATNU", "LATNW", "LAUR", "LAWS", "LAZY", "LBAI", "LBC", "LBRDA", "LBRDK", "LBTYA", "LBTYB", "LBTYK", "LCA", "LCAHU", "LCAHW", "LCAPU", "LCNB", "LCUT", "LDEM", "LDSF", "LE", "LECO", "LEDS", "LEGH", "LEGN", "LEGR", "LEVL", "LEVLP", "LFAC", "LFACU", "LFACW", "LFUS", "LFVN", "LGHL", "LGHLW", "LGIH", "LGND", "LHCG", "LI", "LIFE", "LILA", "LILAK", "LINC", "LIND", "LIQT", "LITE", "LIVE", "LIVK", "LIVKU", "LIVKW", "LIVN", "LIVX", "LIZI", "LJPC", "LKCO", "LKFN", "LKQ", "LLIT", "LLNW", "LMAT", "LMB", "LMBS", "LMFA", "LMFAW", "LMNL", "LMNR", "LMNX", "LMPX", "LMRK", "LMRKN", "LMRKO", "LMRKP", "LMST", "LNDC", "LNGR", "LNSR", "LNT", "LNTH", "LOAC", "LOACR", "LOACU", "LOACW", "LOAN", "LOB", "LOCO", "LOGC", "LOGI", "LONE", "LOOP", "LOPE", "LORL", "LOVE", "LPCN", "LPLA", "LPRO", "LPSN", "LPTH", "LPTX", "LQDA", "LQDT",
           "LRCX", "LRGE", "LRMR", "LSAC", "LSACU", "LSACW", "LSBK", "LSCC", "LSTR", "LSXMA", "LSXMB", "LSXMK", "LTBR", "LTRN", "LTRPA", "LTRPB", "LTRX", "LULU", "LUMO", "LUNA", "LUNG", "LVGO", "LVHD", "LWAY", "LX", "LXEH", "LXRX", "LYFT", "LYL", "LYRA", "LYTS", "MACK", "MAGS", "MANH", "MANT", "MAR", "MARA", "MARK", "MARPS", "MASI", "MAT", "MATW", "MAXN", "MAYS", "MBB", "MBCN", "MBII", "MBIN", "MBINO", "MBINP", "MBIO", "MBNKP", "MBOT", "MBRX", "MBUU", "MBWM", "MCAC", "MCACR", "MCACU", "MCBC", "MCBS", "MCEF", "MCEP", "MCFT", "MCHI", "MCHP", "MCHX", "MCMJ", "MCMJW", "MCRB", "MCRI", "MDB", "MDCA", "MDGL", "MDGS", "MDGSW", "MDIA", "MDIV", "MDJH", "MDLZ", "MDNA", "MDRR", "MDRRP", "MDRX", "MDWD", "MEDP", "MEDS", "MEIP", "MELI", "MEOH", "MERC", "MESA", "MESO", "METC", "METX", "METXW", "MFH", "MFIN", "MFINL", "MFNC", "MGEE", "MGEN", "MGI", "MGIC", "MGLN", "MGNI", "MGNX", "MGPI", "MGRC", "MGTA",
           "MGTX", "MGYR", "MHLD", "MICT", "MIDD", "MIK", "MILN", "MIME", "MIND", "MINDP", "MIRM", "MIST", "MITK", "MITO", "MKD", "MKGI", "MKSI", "MKTX", "MLAB", "MLAC", "MLACU", "MLACW", "MLCO", "MLHR", "MLND", "MLVF", "MMAC", "MMLP", "MMSI", "MMYT", "MNCL", "MNCLU", "MNCLW", "MNDO", "MNKD", "MNOV", "MNPR", "MNRO", "MNSB", "MNSBP", "MNST", "MNTX", "MOBL", "MOFG", "MOGO", "MOHO", "MOMO", "MOR", "MORF", "MORN", "MOSY", "MOTS", "MOXC", "MPAA", "MPB", "MPWR", "MRAM", "MRBK", "MRCC", "MRCCL", "MRCY", "MREO", "MRIN", "MRKR", "MRLN", "MRNA", "MRNS", "MRSN", "MRTN", "MRTX", "MRUS", "MRVL", "MSBI", "MSEX", "MSFT", "MSON", "MSTR", "MSVB", "MTBC", "MTBCP", "MTC", "MTCH", "MTCR", "MTEM", "MTEX", "MTLS", "MTP", "MTRX", "MTSC", "MTSI", "MTSL", "MU", "MVBF", "MVIS", "MWK", "MXIM", "MYFW", "MYGN", "MYL", "MYOK", "MYOS", "MYRG", "MYSZ", "MYT", "NAII", "NAKD", "NAOV", "NARI", "NATH", "NATI", "NATR",
           "NAVI", "NBAC", "NBACR", "NBACU", "NBACW", "NBEV", "NBIX", "NBL", "NBLX", "NBN", "NBRV", "NBSE", "NBTB", "NCBS", "NCMI", "NCNA", "NCNO", "NCSM", "NCTY", "NDAQ", "NDLS", "NDRA", "NDRAW", "NDSN", "NEO", "NEOG", "NEON", "NEOS", "NEPH", "NEPT", "NERV", "NESR", "NESRW", "NETE", "NEWA", "NEWT", "NEWTI", "NEWTL", "NEXT", "NFBK", "NFE", "NFIN", "NFINU", "NFINW", "NFLX", "NFTY", "NGHC", "NGHCN", "NGHCO", "NGHCP", "NGHCZ", "NGM", "NH", "NHIC", "NHICU", "NHICW", "NHLD", "NHLDW", "NHTC", "NICE", "NICK", "NIU", "NK", "NKLA", "NKSH", "NKTR", "NKTX", "NLOK", "NLTX", "NMCI", "NMFC", "NMFCL", "NMIH", "NMMCU", "NMRD", "NMRK", "NMTR", "NNBR", "NNDM", "NNOX", "NODK", "NOVN", "NOVS", "NOVSU", "NOVSW", "NOVT", "NPA", "NPAUU", "NPAWW", "NRBO", "NRC", "NRIM", "NRIX", "NSEC", "NSIT", "NSSC", "NSTG", "NSYS", "NTAP", "NTCT", "NTEC", "NTES", "NTGR", "NTIC", "NTLA", "NTNX", "NTRA", "NTRP", "NTRS",
           "NTRSO", "NTUS", "NTWK", "NUAN", "NURO", "NUVA", "NUZE", "NVAX", "NVCN", "NVCR", "NVDA", "NVEC", "NVEE", "NVFY", "NVIV", "NVMI", "NVUS", "NWBI", "NWE", "NWFL", "NWGI", "NWL", "NWLI", "NWPX", "NWS", "NWSA", "NXGN", "NXPI", "NXST", "NXTC", "NXTD", "NXTG", "NYMT", "NYMTM", "NYMTN", "NYMTO", "NYMTP", "NYMX", "OAS", "OBAS", "OBCI", "OBLN", "OBNK", "OBSV", "OCC", "OCCI", "OCCIP", "OCFC", "OCFCP", "OCGN", "OCSI", "OCSL", "OCUL", "ODFL", "ODP", "ODT", "OEG", "OESX", "OFED", "OFIX", "OFLX", "OFS", "OFSSG", "OFSSI", "OFSSL", "OFSSZ", "OGI", "OIIM", "OKTA", "OLB", "OLD", "OLED", "OLLI", "OM", "OMAB", "OMCL", "OMER", "OMEX", "OMP", "ON", "ONB", "ONCR", "ONCS", "ONCT", "ONCY", "ONEM", "ONEQ", "ONEW", "ONTX", "ONTXW", "ONVO", "OPBK", "OPCH", "OPES", "OPESU", "OPESW", "OPGN", "OPHC", "OPI", "OPINI", "OPINL", "OPK", "OPNT", "OPOF", "OPRA", "OPRT", "OPRX", "OPTN", "OPTT", "ORBC", "ORGO",
           "ORGS", "ORIC", "ORLY", "ORMP", "ORPH", "ORRF", "ORSN", "ORSNR", "ORSNU", "ORSNW", "ORTX", "OSBC", "OSIS", "OSMT", "OSN", "OSPN", "OSS", "OSTK", "OSUR", "OSW", "OTEL", "OTEX", "OTIC", "OTLK", "OTLKW", "OTRK", "OTRKP", "OTTR", "OVBC", "OVID", "OVLY", "OXBR", "OXBRW", "OXFD", "OXLC", "OXLCM", "OXLCO", "OXLCP", "OXSQ", "OXSQL", "OXSQZ", "OYST", "OZK", "PAAS", "PACB", "PACW", "PAE", "PAEWW", "PAHC", "PAND", "PANL", "PASG", "PATI", "PATK", "PAVM", "PAVMW", "PAVMZ", "PAYS", "PAYX", "PBCT", "PBCTP", "PBFS", "PBHC", "PBIP", "PBPB", "PBTS", "PBYI", "PCAR", "PCB", "PCH", "PCOM", "PCRX", "PCSA", "PCSB", "PCTI", "PCTY", "PCVX", "PCYG", "PCYO", "PDBC", "PDCE", "PDCO", "PDD", "PDEV", "PDEX", "PDFS", "PDLB", "PDLI", "PDP", "PDSB", "PEBK", "PEBO", "PECK", "PEGA", "PEIX", "PENN", "PEP", "PERI", "PESI", "PETQ", "PETS", "PETZ", "PEY", "PEZ", "PFBC", "PFBI", "PFC", "PFF", "PFG", "PFHD", "PFI",
           "PFIE", "PFIN", "PFIS", "PFLT", "PFM", "PFMT", "PFPT", "PFSW", "PGC", "PGEN", "PGJ", "PGNY", "PHAS", "PHAT", "PHCF", "PHIO", "PHIOW", "PHO", "PHUN", "PHUNW", "PI", "PICO", "PID", "PIE", "PIH", "PIHPP", "PINC", "PIO", "PIRS", "PIXY", "PIZ", "PKBK", "PKOH", "PKW", "PLAB", "PLAY", "PLBC", "PLC", "PLCE", "PLIN", "PLL", "PLMR", "PLPC", "PLRX", "PLSE", "PLUG", "PLUS", "PLW", "PLXP", "PLXS", "PLYA", "PMBC", "PMD", "PME", "PMVP", "PNBK", "PNFP", "PNFPP", "PNNT", "PNNTG", "PNQI", "PNRG", "PNTG", "POAI", "PODD", "POLA", "POOL", "POTX", "POWI", "POWL", "PPBI", "PPC", "PPD", "PPH", "PPIH", "PPSI", "PRAA", "PRAH", "PRCP", "PRDO", "PRFT", "PRFX", "PRFZ", "PRGS", "PRGX", "PRIM", "PRLD", "PRN", "PROF", "PROG", "PROV", "PRPH", "PRPL", "PRPLW", "PRPO", "PRQR", "PRSC", "PRTA", "PRTH", "PRTK", "PRTS", "PRVB", "PRVL", "PS", "PSAC", "PSACU", "PSACW", "PSC", "PSCC", "PSCD", "PSCE", "PSCF", "PSCH",
           "PSCI", "PSCM", "PSCT", "PSCU", "PSEC", "PSET", "PSHG", "PSL", "PSM", "PSMT", "PSNL", "PSTI", "PSTV", "PSTX", "PT", "PTAC", "PTACU", "PTACW", "PTC", "PTCT", "PTE", "PTEN", "PTF", "PTGX", "PTH", "PTI", "PTMN", "PTNR", "PTON", "PTRS", "PTSI", "PTVCA", "PTVCB", "PTVE", "PUI", "PULM", "PUYI", "PVAC", "PVBC", "PWFL", "PWOD", "PXI", "PXLW", "PXS", "PY", "PYPD", "PYPL", "PYZ", "PZZA", "QABA", "QADA", "QADB", "QAT", "QCLN", "QCOM", "QCRH", "QDEL", "QELLU", "QFIN", "QH", "QIWI", "QK", "QLGN", "QLYS", "QMCO", "QNST", "QQEW", "QQQ", "QQQN", "QQQX", "QQXT", "QRHC", "QRTEA", "QRTEB", "QRTEP", "QRVO", "QTEC", "QTNT", "QTRX", "QTT", "QUIK", "QUMU", "QURE", "QYLD", "QYLG", "RACA", "RADA", "RAIL", "RAND", "RAPT", "RARE", "RAVE", "RAVN", "RBB", "RBBN", "RBCAA", "RBCN", "RBKB", "RBNC", "RCEL", "RCHGU", "RCII", "RCKT", "RCKY", "RCM", "RCMT", "RCON", "RDCM", "RDFN", "RDHL", "RDI", "RDIB", "RDNT",
           "RDUS", "RDVT", "RDVY", "RDWR", "REAL", "REDU", "REED", "REFR", "REG", "REGI", "REGN", "REKR", "RELL", "RELV", "REPH", "REPL", "RESN", "RETA", "RETO", "REXN", "REYN", "RFAP", "RFDI", "RFEM", "RFEU", "RFIL", "RGCO", "RGEN", "RGLD", "RGLS", "RGNX", "RGP", "RIBT", "RICK", "RIGL", "RILY", "RILYG", "RILYH", "RILYI", "RILYL", "RILYM", "RILYN", "RILYO", "RILYP", "RILYZ", "RING", "RIOT", "RIVE", "RKDA", "RLAY", "RLMD", "RMBI", "RMBL", "RMBS", "RMCF", "RMNI", "RMR", "RMRM", "RMTI", "RNA", "RNDB", "RNDM", "RNDV", "RNEM", "RNET", "RNLC", "RNLX", "RNMC", "RNSC", "RNST", "RNWK", "ROAD", "ROBT", "ROCH", "ROCHU", "ROCHW", "ROCK", "ROIC", "ROKU", "ROLL", "ROST", "RP", "RPAY", "RPD", "RPRX", "RPTX", "RRBI", "RRGB", "RRR", "RSSS", "RTH", "RTLR", "RTRX", "RUBY", "RUHN", "RUN", "RUSHA", "RUSHB", "RUTH", "RVMD", "RVNC", "RVSB", "RWLK", "RXT", "RYAAY", "RYTM", "SABR", "SABRP", "SAFM", "SAFT",
           "SAGE", "SAIA", "SAIIU", "SAL", "SALM", "SAMA", "SAMAU", "SAMAW", "SAMG", "SANM", "SANW", "SAQN", "SAQNU", "SAQNW", "SASR", "SATS", "SAVA", "SBAC", "SBBP", "SBCF", "SBFG", "SBGI", "SBLK", "SBLKZ", "SBNY", "SBPH", "SBRA", "SBSI", "SBT", "SBUX", "SCHL", "SCHN", "SCKT", "SCOR", "SCPH", "SCPL", "SCSC", "SCVL", "SCWX", "SCYX", "SCZ", "SDC", "SDG", "SDGR", "SDVY", "SEAC", "SECO", "SEDG", "SEED", "SEEL", "SEIC", "SELB", "SELF", "SENEA", "SENEB", "SESN", "SFBC", "SFBS", "SFET", "SFIX", "SFM", "SFNC", "SFST", "SG", "SGA", "SGBX", "SGC", "SGEN", "SGH", "SGLB", "SGLBW", "SGMA", "SGMO", "SGMS", "SGOC", "SGRP", "SGRY", "SHBI", "SHEN", "SHIP", "SHIPW", "SHIPZ", "SHOO", "SHSP", "SHV", "SHY", "SHYF", "SIBN", "SIC", "SIEB", "SIEN", "SIFY", "SIGA", "SIGI", "SILC", "SILK", "SIMO", "SINA", "SINO", "SINT", "SIRI", "SITM", "SIVB", "SIVBP", "SJ", "SKOR", "SKYS", "SKYW", "SKYY", "SLAB", "SLCT",
           "SLDB", "SLGG", "SLGL", "SLGN", "SLM", "SLMBP", "SLN", "SLNO", "SLP", "SLQD", "SLRC", "SLRX", "SLS", "SLVO", "SMBC", "SMBK", "SMCI", "SMCP", "SMED", "SMH", "SMIT", "SMMC", "SMMCU", "SMMCW", "SMMF", "SMMT", "SMPL", "SMSI", "SMTC", "SMTX", "SNBP", "SNBR", "SNCA", "SNCR", "SND", "SNDE", "SNDL", "SNDX", "SNES", "SNEX", "SNFCA", "SNGX", "SNGXW", "SNLN", "SNOA", "SNPS", "SNSR", "SNSS", "SNUG", "SNY", "SOCL", "SOHO", "SOHOB", "SOHON", "SOHOO", "SOHU", "SOLO", "SOLOW", "SOLY", "SONA", "SONM", "SONN", "SONO", "SOXX", "SP", "SPCB", "SPFI", "SPI", "SPKE", "SPKEP", "SPLK", "SPNE", "SPNS", "SPOK", "SPPI", "SPQQ", "SPRO", "SPRT", "SPSC", "SPT", "SPTN", "SPWH", "SPWR", "SQBG", "SQLV", "SQQQ", "SRAC", "SRACU", "SRACW", "SRAX", "SRCE", "SRCL", "SRDX", "SRET", "SREV", "SRGA", "SRNE", "SRPT", "SRRA", "SRRK", "SRTS", "SSB", "SSBI", "SSKN", "SSNC", "SSNT", "SSP", "SSPK", "SSPKU", "SSPKW", "SSRM",
           "SSSS", "SSTI", "SSYS", "STAA", "STAF", "STAY", "STBA", "STCN", "STEP", "STFC", "STIM", "STKL", "STKS", "STLD", "STMP", "STND", "STNE", "STOK", "STRA", "STRL", "STRM", "STRO", "STRS", "STRT", "STSA", "STWOU", "STX", "STXB", "SUMO", "SUMR", "SUNS", "SUNW", "SUPN", "SURF", "SUSB", "SUSC", "SUSL", "SVA", "SVACU", "SVBI", "SVC", "SVMK", "SVRA", "SVVC", "SWAV", "SWBI", "SWIR", "SWKH", "SWKS", "SWTX", "SXTC", "SY", "SYBT", "SYBX", "SYKE", "SYNA", "SYNC", "SYNH", "SYNL", "SYPR", "SYRS", "SYTA", "SYTAW", "TA", "TACO", "TACT", "TAIT", "TANH", "TANNI", "TANNL", "TANNZ", "TAOP", "TARA", "TAST", "TATT", "TAYD", "TBBK", "TBIO", "TBK", "TBKCP", "TBLT", "TBLTW", "TBNK", "TBPH", "TC", "TCBI", "TCBIL", "TCBIP", "TCBK", "TCCO", "TCDA", "TCF", "TCFC", "TCFCP", "TCMD", "TCOM", "TCON", "TCPC", "TCRR", "TCX", "TDAC", "TDACU", "TDACW", "TDIV", "TEAM", "TECH", "TECTP", "TEDU", "TELA", "TELL", "TENB",
           "TENX", "TER", "TESS", "TEUM", "TFFP", "TFSL", "TGA", "TGLS", "TGTX", "TH", "THBR", "THBRU", "THBRW", "THCA", "THCAU", "THCAW", "THCB", "THCBU", "THCBW", "THFF", "THMO", "THRM", "THRY", "THTX", "THWWW", "TIG", "TIGO", "TIGR", "TILE", "TIPT", "TITN", "TLC", "TLGT", "TLND", "TLRY", "TLSA", "TLT", "TMDI", "TMDX", "TMUS", "TNAV", "TNDM", "TNXP", "TOMZ", "TOPS", "TOTA", "TOTAR", "TOTAU", "TOTAW", "TOUR", "TOWN", "TPCO", "TPIC", "TPTX", "TQQQ", "TRCH", "TREE", "TRHC", "TRIB", "TRIL", "TRIP", "TRMB", "TRMD", "TRMK", "TRMT", "TRNS", "TROW", "TRS", "TRST", "TRUE", "TRUP", "TRVG", "TRVI", "TRVN", "TSBK", "TSC", "TSCAP", "TSCBP", "TSCO", "TSEM", "TSHA", "TSLA", "TSRI", "TTD", "TTEC", "TTEK", "TTGT", "TTMI", "TTNP", "TTOO", "TTTN", "TTWO", "TUR", "TURN", "TUSA", "TUSK", "TVTY", "TW", "TWCTU", "TWIN", "TWNK", "TWNKW", "TWOU", "TWST", "TXG", "TXMD", "TXN", "TXRH", "TYHT", "TYME", "TZAC",
           "TZACU", "TZACW", "TZOO", "UAE", "UAL", "UBCP", "UBFO", "UBOH", "UBSI", "UBX", "UCBI", "UCBIO", "UCL", "UCTT", "UEIC", "UEPS", "UFCS", "UFO", "UFPI", "UFPT", "UG", "UHAL", "UIHC", "ULBI", "ULH", "ULTA", "UMBF", "UMPQ", "UMRX", "UNAM", "UNB", "UNIT", "UNTY", "UONE", "UONEK", "UPLD", "UPWK", "URBN", "URGN", "UROV", "USAK", "USAP", "USAU", "USCR", "USEG", "USIG", "USIO", "USLB", "USLM", "USMC", "USOI", "USWS", "USWSW", "USXF", "UTHR", "UTMD", "UTSI", "UVSP", "UXIN", "VACQU", "VALU", "VBFC", "VBIV", "VBLT", "VBTX", "VC", "VCEL", "VCIT", "VCLT", "VCNX", "VCSH", "VCTR", "VCYT", "VECO", "VEON", "VERB", "VERBW", "VERI", "VERO", "VERU", "VERX", "VERY", "VETS", "VFF", "VG", "VGIT", "VGLT", "VGSH", "VIAC", "VIACA", "VIAV", "VICR", "VIE", "VIGI", "VIHAU", "VIOT", "VIR", "VIRC", "VIRT", "VISL", "VITL", "VIVE", "VIVO", "VJET", "VKTX", "VKTXW", "VLDR", "VLDRW", "VLGEA", "VLY", "VLYPO",
           "VLYPP", "VMAC", "VMACU", "VMACW", "VMBS", "VMD", "VNDA", "VNET", "VNOM", "VNQI", "VOD", "VONE", "VONG", "VONV", "VOXX", "VRA", "VRAY", "VRCA", "VREX", "VRIG", "VRM", "VRME", "VRMEW", "VRNA", "VRNS", "VRNT", "VRRM", "VRSK", "VRSN", "VRTS", "VRTU", "VRTX", "VSAT", "VSDA", "VSEC", "VSMV", "VSPRU", "VSTA", "VSTM", "VTC", "VTGN", "VTHR", "VTIP", "VTNR", "VTRU", "VTSI", "VTVT", "VTWG", "VTWO", "VTWV", "VUZI", "VVPR", "VWOB", "VXRT", "VXUS", "VYGR", "VYMI", "VYNE", "WABC", "WAFD", "WAFU", "WASH", "WATT", "WB", "WBA", "WBND", "WCLD", "WDAY", "WDC", "WDFC", "WEN", "WERN", "WETF", "WEYS", "WHF", "WHFBZ", "WHLM", "WHLR", "WHLRD", "WHLRP", "WIFI", "WILC", "WIMI", "WINA", "WINC", "WING", "WINS", "WINT", "WIRE", "WISA", "WIX", "WKEY", "WKHS", "WLDN", "WLFC", "WLTW", "WMG", "WMGI", "WNEB", "WOOD", "WORX", "WPRT", "WRLD", "WRTC", "WSBC", "WSBCP", "WSBF", "WSC", "WSFS", "WSG", "WSTG", "WSTL",
           "WTBA", "WTER", "WTFC", "WTFCM", "WTFCP", "WTRE", "WTREP", "WTRH", "WVE", "WVFC", "WVVI", "WVVIP", "WW", "WWD", "WWR", "WYNN", "XAIR", "XBIO", "XBIOW", "XBIT", "XCUR", "XEL", "XELA", "XELB", "XENE", "XENT", "XERS", "XFOR", "XGN", "XLNX", "XLRN", "XNCR", "XNET", "XOMA", "XONE", "XP", "XPEL", "XPER", "XRAY", "XSPA", "XT", "XTLB", "YGYI", "YGYIP", "YI", "YIN", "YJ", "YLCO", "YLDE", "YMAB", "YNDX", "YORW", "YRCW", "YTEN", "YTRA", "YVR", "YY", "Z", "ZAGG", "ZAZZT", "ZBRA", "ZBZZT", "ZCMD", "ZCZZT", "ZEAL", "ZEUS", "ZG", "ZGNX", "ZGYH", "ZGYHR", "ZGYHU", "ZGYHW", "ZI", "ZION", "ZIONL", "ZIONN", "ZIONO", "ZIONP", "ZIOP", "ZIXI", "ZJZZT", "ZKIN", "ZLAB", "ZM", "ZNGA", "ZNTL", "ZS", "ZSAN", "ZUMZ", "ZVO", "ZVZZC", "ZVZZT", "ZWZZT", "ZXYZ.A", "ZXZZT", "ZYNE", "ZYXI", "A", "AAL", "AAP", "AAPL", "ABBV", "ABC", "ABMD", "ABT", "ACN", "ADBE", "ADI", "ADM", "ADP", "ADSK", "AEE", "AEP", "AES",
           "AFL", "AIG", "AIV", "AIZ", "AJG", "AKAM", "ALB", "ALGN", "ALK", "ALL", "ALLE", "ALXN", "AMAT", "AMCR", "AMD", "AME", "AMGN", "AMP", "AMT", "AMZN", "ANET", "ANSS", "ANTM", "AON", "AOS", "APA", "APD", "APH", "APTV", "ARE", "ATO", "ATVI", "AVB", "AVGO", "AVY", "AWK", "AXP", "AZO", "BA", "BAC", "BAX", "BBY", "BDX", "BEN", "BF.B", "BIIB", "BIO", "BK", "BKNG", "BKR", "BLK", "BLL", "BMY", "BR", "BRK.B", "BSX", "BWA", "BXP", "C", "CAG", "CAH", "CARR", "CAT", "CB", "CBOE", "CBRE", "CCI", "CCL", "CDNS", "CDW", "CE", "CERN", "CF", "CFG", "CHD", "CHRW", "CHTR", "CI", "CINF", "CL", "CLX", "CMA", "CMCSA", "CME", "CMG", "CMI", "CMS", "CNC", "CNP", "COF", "COG", "COO", "COP", "COST", "CPB", "CPRT", "CRM", "CSCO", "CSX", "CTAS", "CTLT", "CTSH", "CTVA", "CTXS", "CVS", "CVX", "CXO", "D", "DAL", "DD", "DE", "DFS", "DG", "DGX", "DHI", "DHR", "DIS", "DISCA", "DISCK", "DISH", "DLR", "DLTR", "DOV",
           "DOW", "DPZ", "DRE", "DRI", "DTE", "DUK", "DVA", "DVN", "DXC", "DXCM", "EA", "EBAY", "ECL", "ED", "EFX", "EIX", "EL", "EMN", "EMR", "EOG", "EQIX", "EQR", "ES", "ESS", "ETFC", "ETN", "ETR", "ETSY", "EVRG", "EW", "EXC", "EXPD", "EXPE", "EXR", "F", "FANG", "FAST", "FB", "FBHS", "FCX", "FDX", "FE", "FFIV", "FIS", "FISV", "FITB", "FLIR", "FLS", "FLT", "FMC", "FOX", "FOXA", "FRC", "FRT", "FTI", "FTNT", "FTV", "GD", "GE", "GILD", "GIS", "GL", "GLW", "GM", "GOOG", "GOOGL", "GPC", "GPN", "GPS", "GRMN", "GS", "GWW", "HAL", "HAS", "HBAN", "HBI", "HCA", "HD", "HES", "HFC", "HIG", "HII", "HLT", "HOLX", "HON", "HPE", "HPQ", "HRL", "HSIC", "HST", "HSY", "HUM", "HWM", "IBM", "ICE", "IDXX", "IEX", "IFF", "ILMN", "INCY", "INFO", "INTC", "INTU", "IP", "IPG", "IPGP", "IQV", "IR", "IRM", "ISRG", "IT", "ITW", "IVZ", "J", "JBHT", "JCI", "JKHY", "JNJ", "JNPR", "JPM", "K", "KEY", "KEYS", "KHC", "KIM",
           "KLAC", "KMB", "KMI", "KMX", "KO", "KR", "KSU", "L", "LB", "LDOS", "LEG", "LEN", "LH", "LHX", "LIN", "LKQ", "LLY", "LMT", "LNC", "LNT", "LOW", "LRCX", "LUMN", "LUV", "LVS", "LW", "LYB", "LYV", "MA", "MAA", "MAR", "MAS", "MCD", "MCHP", "MCK", "MCO", "MDLZ", "MDT", "MET", "MGM", "MHK", "MKC", "MKTX", "MLM", "MMC", "MMM", "MNST", "MO", "MOS", "MPC", "MRK", "MRO", "MS", "MSCI", "MSFT", "MSI", "MTB", "MTD", "MU", "MXIM", "MYL", "NBL", "NCLH", "NDAQ", "NEE", "NEM", "NFLX", "NI", "NKE", "NLOK", "NLSN", "NOC", "NOV", "NOW", "NRG", "NSC", "NTAP", "NTRS", "NUE", "NVDA", "NVR", "NWL", "NWS", "NWSA", "O", "ODFL", "OKE", "OMC", "ORCL", "ORLY", "OTIS", "OXY", "PAYC", "PAYX", "PBCT", "PCAR", "PEAK", "PEG", "PEP", "PFE", "PFG", "PG", "PGR", "PH", "PHM", "PKG", "PKI", "PLD", "PM", "PNC", "PNR", "PNW", "PPG", "PPL", "PRGO", "PRU", "PSA", "PSX", "PVH", "PWR", "PXD", "PYPL", "QCOM", "QRVO",
           "RCL", "RE", "REG", "REGN", "RF", "RHI", "RJF", "RL", "RMD", "ROK", "ROL", "ROP", "ROST", "RSG", "RTX", "SBAC", "SBUX", "SCHW", "SEE", "SHW", "SIVB", "SJM", "SLB", "SLG", "SNA", "SNPS", "SO", "SPG", "SPGI", "SRE", "STE", "STT", "STX", "STZ", "SWK", "SWKS", "SYF", "SYK", "SYY", "T", "TAP", "TDG", "TDY", "TEL", "TER", "TFC", "TFX", "TGT", "TIF", "TJX", "TMO", "TMUS", "TPR", "TROW", "TRV", "TSCO", "TSN", "TT", "TTWO", "TWTR", "TXN", "TXT", "TYL", "UA", "UAA", "UAL", "UDR", "UHS", "ULTA", "UNH", "UNM", "UNP", "UPS", "URI", "USB", "V", "VAR", "VFC", "VIAC", "VLO", "VMC", "VNO", "VRSK", "VRSN", "VRTX", "VTR", "VZ", "WAB", "WAT", "WBA", "WDC", "WEC", "WELL", "WFC", "WHR", "WLTW", "WM", "WMB", "WMT", "WRB", "WRK", "WST", "WU", "WY", "WYNN", "XEL", "XLNX", "XOM", "XRAY", "XRX", "XYL", "YUM", "ZBH", "ZBRA", "ZION", "ZTS"]


def getValues():
    for ticker in tickers:
        time.sleep(10)
        driver = webdriver.Chrome()
        base_url = 'https://finance.yahoo.com/quote/{}?p={}'.format(ticker, ticker)
        try:
            driver.get(base_url)
            try:
                driver.find_element_by_xpath('//*[@id="YDC-Lead"]')
            except:
                continue
        except:
            try:
                driver.get(base_url)
            except:
                driver.quit()
                print('website didnt load')
                continue

        if driver.find_element_by_xpath('//*[@id="quote-nav"]/ul/li[8]/a/span').text != 'Financials':
            try:
                response = requests.get(base_url)
                request_data = driver.page_source
                text = response.content.decode('utf-8')
                response = scrapy.Selector(text=text)
                json_str = request_data[request_data.find('root.App.main = ') + len('root.App.main = '):]
                # data2 = json.loads(json_str[:json_str.find('}(this));') - 2][0].response.body)
                data = json.loads(json_str[:json_str.find('}(this));') - 2])
            except:
                continue

            item = dict()
            try:
                item['name'] = response.css('h1 ::text').extract_first('')
            except:
                item['name'] = '-'
            try:
                item['ticker']=ticker
            except:
                item['ticker']='-'
            try:
                item['fiftyTwoWeekRange'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'StreamDataStore', 'quoteData', ticker, 'fiftyTwoWeekRange', 'raw'])
            except:
                item['fiftyTwoWeekRange'] = '-'

            try:
                item['beta_5Y_monthly'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'defaultKeyStatistics', 'beta3Year', 'fmt'])
            except:
                item['beta_5Y_monthly'] = '-'
            try:
                item['PE Ratio'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'summaryDetail', 'trailingPE', 'fmt'])
            except:
                item['PE Ratio'] = 'N/A'
            try:
                item['earningsDate'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'defaultKeyStatistics', 'fundInceptionDate', 'fmt'])
            except:
                item['earningsDate'] = '-'

            driver.quit()
            writer.writerow(item)
            csv_file.flush()
            continue

        try:
            response = requests.get(base_url)
            request_data = driver.page_source
            text = response.content.decode('utf-8')
            response = scrapy.Selector(text=text)
            json_str = request_data[request_data.find('root.App.main = ') + len('root.App.main = '):]
            # data2 = json.loads(json_str[:json_str.find('}(this));') - 2][0].response.body)
            data = json.loads(json_str[:json_str.find('}(this));') - 2])
        except:
            driver.quit()
            writer.writerow(item)
            csv_file.flush()
            continue
        item = dict()
        try:
            item['name'] = response.css('h1 ::text').extract_first('')
        except:
            item['name'] = '-'
        try:
            item['ticker'] = ticker
        except:
            item['ticker'] = '-'
        try:
            item['fiftyTwoWeekRange'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'StreamDataStore', 'quoteData', ticker, 'fiftyTwoWeekRange', 'raw'])
        except:
            item['fiftyTwoWeekRange'] = '-'
        try:
            item['marketCap'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'StreamDataStore', 'quoteData', ticker, 'marketCap', 'fmt'])
        except:
            item['marketCap'] = '-'
        try:
            item['beta_5Y_monthly'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'defaultKeyStatistics', 'beta', 'fmt'])
        except:
            item['beta_5Y_monthly'] = '-'
        try:
            item['PE Ratio'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'summaryDetail', 'trailingPE', 'fmt'])
        except:
            item['PE Ratio'] = '-'
        try:
            item['trailingEps'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'defaultKeyStatistics', 'trailingEps', 'fmt'])
        except:
            item['trailingEps'] = '-'
        try:
            item['earningsDate'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'earnings', 'earningsChart', 'earningsDate'])[0]['fmt']
        except:
            item['earningsDate'] = '-'
        try:
            item['dividendRate'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'summaryDetail', 'dividendRate', 'fmt'])
        except:
            item['dividendRate'] = '-'
        try:
            item['exDividendDate'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'summaryDetail', 'exDividendDate', 'fmt'])
        except:
            item['exDividendDate'] = '-'
        try:
            item['1y_Target_Est'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'financialData', 'targetMeanPrice', 'raw'])
        except:
            item['1y_Target_Est'] = '-'
        # annual
        try:
            item['totalRevenue TTM'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'financialData', 'totalRevenue', 'fmt'])
        except:
            item['totalRevenue TTM'] = '-'
        try:
            item['totalRevenue 2016'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'earnings', 'financialsChart', 'yearly'])[0]['revenue']['raw']
        except:
            item['totalRevenue 2016'] = '-'
        try:
            item['totalRevenue 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'earnings', 'financialsChart', 'yearly'])[1]['revenue']['raw']
        except:
            item['totalRevenue 2017'] = '-'
        try:
            item['totalRevenue 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'earnings', 'financialsChart', 'yearly'])[2]['revenue']['raw']
        except:
            item['totalRevenue 2018'] = '-'
        try:
            item['totalRevenue 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'earnings', 'financialsChart', 'yearly'])[3]['revenue']['raw']
        except:
            item['totalRevenue 2019'] = '-'
        try:
            item['totalRevenue 06/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'earnings', 'financialsChart', 'quarterly'])[3]['revenue']['raw']
        except:
            item['totalRevenue 06/2020'] = '-'
        try:
            item['totalRevenue 03/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'earnings', 'financialsChart', 'quarterly'])[2]['revenue']['raw']
        except:
            item['totalRevenue 03/2020'] = '-'
        try:
            item['totalRevenue 12/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'earnings', 'financialsChart', 'quarterly'])[1]['revenue']['raw']
        except:
            item['totalRevenue 12/2019'] = '-'
        try:
            item['totalRevenue 09/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'earnings', 'financialsChart', 'quarterly'])[0]['revenue']['raw']
        except:
            item['totalRevenue 09/2019'] = '-'

        try:
            driver.find_element_by_xpath('//*[@id="quote-nav"]/ul/li[8]').click()
            time.sleep(5)
            driver.refresh()
            time.sleep(5)
            requests_data = driver.page_source
            json_strn = requests_data[requests_data.find('root.App.main = ') + len('root.App.main = '):]
            data = json.loads(json_strn[:json_strn.find('}(this));') - 2])
        except:
            driver.quit()
            writer.writerow(item)
            csv_file.flush()
            continue

        try:
            item['operatingIncome TTM'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'trailingOperatingIncome'])[0]['reportedValue']['raw']
        except:
            item['operatingIncome TTM'] = '-'
        try:
            item['operatingIncome 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualTotalOperatingIncomeAsReported'])[0]['reportedValue']['raw']
        except:
            item['operatingIncome 2017'] = '-'
        try:
            item['operatingIncome 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualTotalOperatingIncomeAsReported'])[1]['reportedValue']['raw']
        except:
            item['operatingIncome 2018'] = '-'
        try:
            item['operatingIncome 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualTotalOperatingIncomeAsReported'])[2]['reportedValue']['raw']
        except:
            item['operatingIncome 2019'] = '-'

        try:
            item['PretaxIncome TTM'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'trailingPretaxIncome'])[0]['reportedValue']['raw']
        except:
            item['PretaxIncome TTM'] = '-'
        try:
            item['PretaxIncome 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualPretaxIncome'])[0]['reportedValue']['raw']
        except:
            item['PretaxIncome 2017'] = '-'
        try:
            item['PretaxIncome 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualPretaxIncome'])[1]['reportedValue']['raw']
        except:
            item['PretaxIncome 2018'] = '-'
        try:
            item['PretaxIncome 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualPretaxIncome'])[2]['reportedValue']['raw']
        except:
            item['PretaxIncome 2019'] = '-'

        try:
            item['taxProvision TTM'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'trailingTaxProvision'])[0]['reportedValue']['raw']
        except:
            item['taxProvision TTM'] = '-'
        try:
            item['taxProvision 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualTaxProvision'])[0]['reportedValue']['raw']
        except:
            item['taxProvision 2017'] = '-'
        try:
            item['taxProvision 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualTaxProvision'])[1]['reportedValue']['raw']
        except:
            item['taxProvision 2018'] = '-'
        try:
            item['taxProvision 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualTaxProvision'])[2]['reportedValue']['raw']
        except:
            item['taxProvision 2019'] = '-'

        try:
            item['netIncomeCommonStockholder TTM'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'trailingNetIncomeCommonStockholders'])[0]['reportedValue']['raw']
        except:
            item['netIncomeCommonStockholder TTM'] = '-'
        try:
            item['netIncomeCommonStockholder 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualNetIncomeCommonStockholders'])[0]['reportedValue']['raw']
        except:
            item['netIncomeCommonStockholder 2017'] = '-'
        try:
            item['netIncomeCommonStockholder 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualNetIncomeCommonStockholders'])[1]['reportedValue']['raw']
        except:
            item['netIncomeCommonStockholder 2018'] = '-'
        try:
            item['netIncomeCommonStockholder 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualNetIncomeCommonStockholders'])[2]['reportedValue']['raw']
        except:
            item['netIncomeCommonStockholder 2019'] = '-'

        try:
            item['dilutedNIComStockholders TTM'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'trailingDilutedNIAvailtoComStockholders'])[0]['reportedValue']['raw']
        except:
            item['dilutedNIComStockholders TTM'] = '-'
        try:
            item['dilutedNIComStockholders 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualDilutedNIAvailtoComStockholders'])[0]['reportedValue']['raw']
        except:
            item['dilutedNIComStockholders 2017'] = '-'
        try:
            item['dilutedNIComStockholders 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualDilutedNIAvailtoComStockholders'])[1]['reportedValue']['raw']
        except:
            item['dilutedNIComStockholders 2018'] = '-'
        try:
            item['dilutedNIComStockholders 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualDilutedNIAvailtoComStockholders'])[2]['reportedValue']['raw']
        except:
            item['dilutedNIComStockholders 2019'] = '-'
        try:
            item['dilutedEPS TTM'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'trailingDilutedEPS'])[0]['reportedValue']['raw']
        except:
            item['dilutedEPS TTM'] = '-'
        try:
            item['dilutedEPS 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualDilutedEPS'])[0]['reportedValue']['raw']
        except:
            item['dilutedEPS 2017'] = '-'
        try:
            item['dilutedEPS 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualDilutedEPS'])[1]['reportedValue']['raw']
        except:
            item['dilutedEPS 2018'] = '-'
        try:
            item['dilutedEPS 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualDilutedEPS'])[2]['reportedValue']['raw']
        except:
            item['dilutedEPS 2019'] = '-'

        try:
            item['intrestExpense TTM'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'trailingInterestExpense'])[0]['reportedValue']['raw']
        except:
            item['intrestExpense TTM'] = '-'
        try:
            item['intrestExpense 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualInterestExpense'])[0]['reportedValue']['raw']
        except:
            item['intrestExpense 2017'] = '-'
        try:
            item['intrestExpense 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualInterestExpense'])[1]['reportedValue']['raw']
        except:
            item['intrestExpense 2018'] = '-'
        try:
            item['intrestExpense 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualInterestExpense'])[2]['reportedValue']['raw']
        except:
            item['intrestExpense 2019'] = '-'

        try:
            item['EBIT TTM'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'trailingEBIT'])[0]['reportedValue']['raw']
        except:
            item['EBIT TTM'] = '-'
        try:
            item['EBIT 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualEBIT'])[0]['reportedValue']['raw']
        except:
            item['EBIT 2017'] = '-'
        try:
            item['EBIT 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualEBIT'])[1]['reportedValue']['raw']
        except:
            item['EBIT 2018'] = '-'
        try:
            item['EBIT 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualEBIT'])[2]['reportedValue']['raw']
        except:
            item['EBIT 2019'] = '-'

        # quarterly
        try:
            driver.find_element_by_xpath('//*[@id="Col1-1-Financials-Proxy"]/section/div[1]/div[2]/button').click()
            time.sleep(2)
            # driver.refresh()
            # time.sleep(5)
            requests_data = driver.page_source
            json_strn = requests_data[requests_data.find('root.App.main = ') + len('root.App.main = '):]
            data = json.loads(json_strn[:json_strn.find('}(this));') - 2])
        except:
            driver.quit()
            writer.writerow(item)
            csv_file.flush()
            continue
        try:
            item['operatingIncome 06/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory'])[0]['operatingIncome']['raw']
        except:
            item['operatingIncome 06/2020'] = '-'
        try:
            item['operatingIncome 03/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory'])[1]['operatingIncome']['raw']
        except:
            item['operatingIncome 03/2020'] = '-'
        try:
            item['operatingIncome 12/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory'])[2]['operatingIncome']['raw']
        except:
            item['operatingIncome 12/2019'] = '-'
        try:
            item['operatingIncome 09/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory'])[3]['operatingIncome']['raw']
        except:
            item['operatingIncome 09/2019'] = '-'

        try:
            item['PretaxIncome 06/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory'])[0]['incomeBeforeTax']['raw']
        except:
            item['PretaxIncome 06/2020'] = '-'
        try:
            item['PretaxIncome 03/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory'])[1]['incomeBeforeTax']['raw']
        except:
            item['PretaxIncome 03/2020'] = '-'
        try:
            item['PretaxIncome 12/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory'])[2]['incomeBeforeTax']['raw']
        except:
            item['PretaxIncome 12/2019'] = '-'
        try:
            item['PretaxIncome 09/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory'])[3]['incomeBeforeTax']['raw']
        except:
            item['PretaxIncome 09/2019'] = '-'

        try:
            item['taxProvision 06/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory'])[0]['incomeTaxExpense']['raw']
        except:
            item['taxProvision 06/2020'] = '-'
        try:
            item['taxProvision 03/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory'])[1]['incomeTaxExpense']['raw']
        except:
            item['taxProvision 03/2020'] = '-'
        try:
            item['taxProvision 12/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory'])[2]['incomeTaxExpense']['raw']
        except:
            item['taxProvision 12/2019'] = '-'
        try:
            item['taxProvision 09/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory'])[3]['incomeTaxExpense']['raw']
        except:
            item['taxProvision 09/2019'] = '-'

        try:
            item['netIncomeCommonStockholder 06/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory'])[0]['netIncome']['raw']
        except:
            item['netIncomeCommonStockholder 06/2020'] = '-'
        try:
            item['netIncomeCommonStockholder 03/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory'])[1]['netIncome']['raw']
        except:
            item['netIncomeCommonStockholder 03/2020'] = '-'
        try:
            item['netIncomeCommonStockholder 12/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory'])[2]['netIncome']['raw']
        except:
            item['netIncomeCommonStockholder 12/2019'] = '-'
        try:
            item['netIncomeCommonStockholder 09/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory'])[3]['netIncome']['raw']
        except:
            item['netIncomeCommonStockholder 09/2019'] = '-'

        try:
            item['dilutedNIComStockholders 06/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory'])[0]['netIncome']['raw']
        except:
            item['dilutedNIComStockholders 06/2020'] = '-'
        try:
            item['dilutedNIComStockholders 03/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory'])[0]['netIncome']['raw']
        except:
            item['dilutedNIComStockholders 03/2020'] = '-'
        try:
            item['dilutedNIComStockholders 12/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory'])[0]['netIncome']['raw']
        except:
            item['dilutedNIComStockholders 12/2019'] = '-'
        try:
            item['dilutedNIComStockholders 09/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory'])[0]['netIncome']['raw']
        except:
            item['dilutedNIComStockholders 09/2019'] = '-'

        item['dilutedEPS 06/2020'] = '-'
        item['dilutedEPS 03/2020'] = '-'
        item['dilutedEPS 12/2019'] = '-'
        item['dilutedEPS 09/2019'] = '-'

        try:
            item['intrestExpense 06/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory'])[0]['interestExpense']['raw']
        except:
            item['intrestExpense 06/2020'] = '-'
        try:
            item['intrestExpense 03/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory'])[1]['interestExpense']['raw']
        except:
            item['intrestExpense 03/2020'] = '-'
        try:
            item['intrestExpense 12/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory'])[2]['interestExpense']['raw']
        except:
            item['intrestExpense 12/2019'] = '-'
        try:
            item['intrestExpense 09/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory'])[3]['interestExpense']['raw']
        except:
            item['intrestExpense 09/2019'] = '-'

        try:
            item['EBIT 06/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory'])[0]['ebit']['raw']
        except:
            item['EBIT 06/2020'] = '-'
        try:
            item['EBIT 03/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory'])[1]['ebit']['raw']
        except:
            item['EBIT 03/2020'] = '-'
        try:
            item['EBIT 12/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory'])[2]['ebit']['raw']
        except:
            item['EBIT 12/2019'] = '-'
        try:
            item['EBIT 09/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory'])[3]['ebit']['raw']
        except:
            item['EBIT 09/2019'] = '-'

        # annual
        try:
            driver.find_element_by_xpath('//*[@id="Col1-1-Financials-Proxy"]/section/div[1]/div[1]/div/a[1]').click()
            time.sleep(5)
            driver.refresh()
            time.sleep(5)
            requests_data = driver.page_source
            json_strn = requests_data[requests_data.find('root.App.main = ') + len('root.App.main = '):]
            data = json.loads(json_strn[:json_strn.find('}(this));') - 2])
        except:
            driver.quit()
            writer.writerow(item)
            csv_file.flush()
            continue

        try:
            item['totalAssets 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistory', 'balanceSheetStatements'])[0]['totalAssets']['raw']
        except:
            item['totalAssets 2019'] = '-'
        try:
            item['totalAssets 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistory', 'balanceSheetStatements'])[1]['totalAssets']['raw']
        except:
            item['totalAssets 2018'] = '-'
        try:
            item['totalAssets 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistory', 'balanceSheetStatements'])[2]['totalAssets']['raw']
        except:
            item['totalAssets 2017'] = '-'

        try:
            item['totalAssets 2016'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistory', 'balanceSheetStatements'])[3]['totalAssets']['raw']
        except:
            item['totalAssets 2016'] = '-'

        try:
            item['totalCurrentAssets 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistory', 'balanceSheetStatements'])[0]['totalCurrentAssets']['raw']
        except:
            item['totalCurrentAssets 2019'] = '-'
        try:
            item['totalCurrentAssets 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistory', 'balanceSheetStatements'])[1]['totalCurrentAssets']['raw']
        except:
            item['totalCurrentAssets 2018'] = '-'
        try:
            item['totalCurrentAssets 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistory', 'balanceSheetStatements'])[2]['totalCurrentAssets']['raw']
        except:
            item['totalCurrentAssets 2017'] = '-'
        try:
            item['totalCurrentAssets 2016'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistory', 'balanceSheetStatements'])[3]['totalCurrentAssets']['raw']
        except:
            item['totalCurrentAssets 2016'] = '-'

        try:
            item['Cash,CashEquilalents&ShortTermInvestments 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualCashCashEquivalentsAndShortTermInvestments'])[2]['reportedValue']['raw']
        except:
            item['Cash,CashEquilalents&ShortTermInvestments 2019'] = '-'
        try:
            item['Cash,CashEquilalents&ShortTermInvestments 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualCashCashEquivalentsAndShortTermInvestments'])[1]['reportedValue']['raw']
        except:
            item['Cash,CashEquilalents&ShortTermInvestments 2018'] = '-'
        try:
            item['Cash,CashEquilalents&ShortTermInvestments 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualCashCashEquivalentsAndShortTermInvestments'])[0]['reportedValue']['raw']
        except:
            item['Cash,CashEquilalents&ShortTermInvestments 2017'] = '-' \
                                                                     ''
        try:
            item['Receivables 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistory', 'balanceSheetStatements'])[3]['netReceivables']['raw']
        except:
            item['Receivables 2019'] = '-'
        try:
            item['Receivables 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistory', 'balanceSheetStatements'])[2]['netReceivables']['raw']
        except:
            item['Receivables 2018'] = '-'
        try:
            item['Receivables 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistory', 'balanceSheetStatements'])[1]['netReceivables']['raw']
        except:
            item['Receivables 2017'] = '-'
        try:
            item['Receivables 2016'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistory', 'balanceSheetStatements'])[0]['netReceivables']['raw']
        except:
            item['Receivables 2016'] = '-'

        try:
            item['Inventory 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistory', 'balanceSheetStatements'])[3]['inventory']['raw']
        except:
            item['Inventory 2019'] = '-'
        try:
            item['Inventory 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistory', 'balanceSheetStatements'])[2]['inventory']['raw']
        except:
            item['Inventory 2018'] = '-'
        try:
            item['Inventory 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistory', 'balanceSheetStatements'])[1]['inventory']['raw']
        except:
            item['Inventory 2017'] = '-'
        try:
            item['Inventory 2016'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistory', 'balanceSheetStatements'])[0]['inventory']['raw']
        except:
            item['Inventory 2016'] = '-'

        try:
            item['longTermDebt 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistory', 'balanceSheetStatements'])[3]['longTermDebt']['raw']
        except:
            item['longTermDebt 2019'] = '-'
        try:
            item['longTermDebt 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistory', 'balanceSheetStatements'])[2]['longTermDebt']['raw']
        except:
            item['longTermDebt 2018'] = '-'
        try:
            item['longTermDebt 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistory', 'balanceSheetStatements'])[1]['longTermDebt']['raw']
        except:
            item['longTermDebt 2017'] = '-'
        try:
            item['longTermDebt 2016'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistory', 'balanceSheetStatements'])[0]['longTermDebt']['raw']
        except:
            item['longTermDebt 2016'] = '-'

        try:
            item['stockholdersEquity 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistory', 'balanceSheetStatements'])[3]['totalStockholderEquity']['raw']
        except:
            item['stockholdersEquity 2019'] = '-'
        try:
            item['stockholdersEquity 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistory', 'balanceSheetStatements'])[2]['totalStockholderEquity']['raw']
        except:
            item['stockholdersEquity 2018'] = '-'
        try:
            item['stockholdersEquity 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistory', 'balanceSheetStatements'])[1]['totalStockholderEquity']['raw']
        except:
            item['stockholdersEquity 2017'] = '-'
        try:
            item['stockholdersEquity 2016'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistory', 'balanceSheetStatements'])[0]['totalStockholderEquity']['raw']
        except:
            item['stockholdersEquity 2016'] = '-'
        try:
            item['totalLiab 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistory', 'balanceSheetStatements'])[0]['totalLiab']['raw']
        except:
            item['totalLiab 2019'] = '-'
        try:
            item['totalLiab 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistory', 'balanceSheetStatements'])[1]['totalLiab']['raw']
        except:
            item['totalLiab 2018'] = '-'
        try:
            item['totalLiab 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistory', 'balanceSheetStatements'])[2]['totalLiab']['raw']
        except:
            item['totalLiab 2017'] = '-'
        try:
            item['totalLiab 2016'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistory', 'balanceSheetStatements'])[3]['totalLiab']['raw']
        except:
            item['totalLiab 2016'] = '-'

        # quarter

        try:
            driver.find_element_by_xpath('//*[@id="Col1-1-Financials-Proxy"]/section/div[1]/div[2]/button').click()
            time.sleep(2)
            requests_data = driver.page_source
            json_strn = requests_data[requests_data.find('root.App.main = ') + len('root.App.main = '):]
            data = json.loads(json_strn[:json_strn.find('}(this));') - 2])
        except:
            driver.quit()
            writer.writerow(item)
            csv_file.flush()
            continue

        try:
            item['totalAssets 06/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistoryQuarterly', 'balanceSheetStatements'])[0]['totalAssets']['raw']
        except:
            item['totalAssets 06/2020'] = '-'
        try:
            item['totalAssets 03/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistoryQuarterly', 'balanceSheetStatements'])[1]['totalAssets']['raw']
        except:
            item['totalAssets 03/2020'] = '-'
        try:
            item['totalAssets 12/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistoryQuarterly', 'balanceSheetStatements'])[2]['totalAssets']['raw']
        except:
            item['totalAssets 12/2019'] = '-'
        try:
            item['totalAssets 09/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistoryQuarterly', 'balanceSheetStatements'])[3]['totalAssets']['raw']
        except:
            item['totalAssets 09/2019'] = '-'

        try:
            item['totalCurrentAssets 06/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistoryQuarterly', 'balanceSheetStatements'])[0]['totalCurrentAssets']['raw']
        except:
            item['totalCurrentAssets 06/2020'] = '-'
        try:
            item['totalCurrentAssets 03/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistoryQuarterly', 'balanceSheetStatements'])[1]['totalCurrentAssets']['raw']
        except:
            item['totalCurrentAssets 03/2020'] = '-'
        try:
            item['totalCurrentAssets 12/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistoryQuarterly', 'balanceSheetStatements'])[2]['totalCurrentAssets']['raw']
        except:
            item['totalCurrentAssets 12/2019'] = '-'
        try:
            item['totalCurrentAssets 09/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistoryQuarterly', 'balanceSheetStatements'])[3]['totalCurrentAssets']['raw']
        except:
            item['totalCurrentAssets 09/2019'] = '-'

        try:
            item['Receivables 06/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistoryQuarterly', 'balanceSheetStatements'])[0]['netReceivables']['raw']
        except:
            item['Receivables 06/2020'] = '-'
        try:
            item['Receivables 03/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistoryQuarterly', 'balanceSheetStatements'])[1]['netReceivables']['raw']
        except:
            item['Receivables 03/2020'] = '-'
        try:
            item['Receivables 12/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistoryQuarterly', 'balanceSheetStatements'])[2]['netReceivables']['raw']
        except:
            item['Receivables 12/2019'] = '-'
        try:
            item['Receivables 09/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistoryQuarterly', 'balanceSheetStatements'])[3]['netReceivables']['raw']
        except:
            item['Receivables 09/2019'] = '-'

        try:
            item['Inventory 06/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistoryQuarterly', 'balanceSheetStatements'])[0]['inventory']['raw']
        except:
            item['Inventory 06/2020'] = '-'
        try:
            item['Inventory 03/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistoryQuarterly', 'balanceSheetStatements'])[1]['inventory']['raw']
        except:
            item['Inventory 03/2020'] = '-'
        try:
            item['Inventory 12/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistoryQuarterly', 'balanceSheetStatements'])[2]['inventory']['raw']
        except:
            item['Inventory 12/2019'] = '-'
        try:
            item['Inventory 09/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistoryQuarterly', 'balanceSheetStatements'])[3]['inventory']['raw']
        except:
            item['Inventory 09/2019'] = '-'

        try:
            item['longTermDebt 06/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistoryQuarterly', 'balanceSheetStatements'])[0]['longTermDebt']['raw']
        except:
            item['longTermDebt 06/2020'] = '-'
        try:
            item['longTermDebt 03/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistoryQuarterly', 'balanceSheetStatements'])[1]['longTermDebt']['raw']
        except:
            item['longTermDebt 03/2020'] = '-'
        try:
            item['longTermDebt 12/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistoryQuarterly', 'balanceSheetStatements'])[2]['longTermDebt']['raw']
        except:
            item['longTermDebt 12/2019'] = '-'
        try:
            item['longTermDebt 09/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistoryQuarterly', 'balanceSheetStatements'])[3]['longTermDebt']['raw']
        except:
            item['longTermDebt 09/2019'] = '-'

        try:
            item['stockholdersEquity 06/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistoryQuarterly', 'balanceSheetStatements'])[0]['totalStockholderEquity']['raw']
        except:
            item['stockholdersEquity 06/2020'] = '-'
        try:
            item['stockholdersEquity 03/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistoryQuarterly', 'balanceSheetStatements'])[1]['totalStockholderEquity']['raw']
        except:
            item['stockholdersEquity 03/2020'] = '-'
        try:
            item['stockholdersEquity 12/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistoryQuarterly', 'balanceSheetStatements'])[2]['totalStockholderEquity']['raw']
        except:
            item['stockholdersEquity 12/2019'] = '-'
        try:
            item['stockholdersEquity 09/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistoryQuarterly', 'balanceSheetStatements'])[3]['totalStockholderEquity']['raw']
        except:
            item['stockholdersEquity 09/2019'] = '-'

        try:
            item['totalLiab 06/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistoryQuarterly', 'balanceSheetStatements'])[0]['totalLiab']['raw']
        except:
            item['totalLiab 06/2020'] = '-'
        try:
            item['totalLiab 03/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistoryQuarterly', 'balanceSheetStatements'])[1]['totalLiab']['raw']
        except:
            item['totalLiab 03/2020'] = '-'
        try:
            item['totalLiab 12/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistoryQuarterly', 'balanceSheetStatements'])[2]['totalLiab']['raw']
        except:
            item['totalLiab 12/2019'] = '-'
        try:
            item['totalLiab 09/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'balanceSheetHistoryQuarterly', 'balanceSheetStatements'])[3]['totalLiab']['raw']
        except:
            item['totalLiab 09/2019'] = '-'

        try:
            driver.find_element_by_xpath('//*[@id="Col1-1-Financials-Proxy"]/section/div[1]/div[1]/div/a[2]').click()
            time.sleep(5)
            driver.refresh()
            time.sleep(5)
            requests_data = driver.page_source
            json_strn = requests_data[requests_data.find('root.App.main = ') + len('root.App.main = '):]
            data = json.loads(json_strn[:json_strn.find('}(this));') - 2])
        except:
            driver.quit()
            writer.writerow(item)
            csv_file.flush()
            continue

        try:
            item['operatingCashFlow TTM'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'trailingOperatingCashFlow'])[0]['reportedValue']['raw']
        except:
            item['operatingCashFlow TTM'] = '-'
        try:
            item['operatingCashFlow 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualOperatingCashFlow'])[2]['reportedValue']['raw']
        except:
            item['operatingCashFlow 2019'] = '-'
        try:
            item['operatingCashFlow 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualOperatingCashFlow'])[1]['reportedValue']['raw']
        except:
            item['operatingCashFlow 2018'] = '-'
        try:
            item['operatingCashFlow 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualOperatingCashFlow'])[0]['reportedValue']['raw']
        except:
            item['operatingCashFlow 2017'] = '-'

        try:
            item['investingCashFlow TTM'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'trailingInvestingCashFlow'])[0]['reportedValue']['raw']
        except:
            item['investingCashFlow TTM'] = '-'
        try:
            item['investingCashFlow 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualInvestingCashFlow'])[2]['reportedValue']['raw']
        except:
            item['investingCashFlow 2019'] = '-'
        try:
            item['investingCashFlow 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualInvestingCashFlow'])[1]['reportedValue']['raw']
        except:
            item['investingCashFlow 2018'] = '-'
        try:
            item['investingCashFlow 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualInvestingCashFlow'])[0]['reportedValue']['raw']
        except:
            item['investingCashFlow 2017'] = '-'

        try:
            item['cashFlowFromContinuingInvestingActivities TTM'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'trailingCashFlowFromContinuingInvestingActivities'])[0]['reportedValue']['raw']
        except:
            item['cashFlowFromContinuingInvestingActivities TTM'] = '-'
        try:
            item['cashFlowFromContinuingInvestingActivities 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualCashFlowFromContinuingInvestingActivities'])[2]['reportedValue']['raw']
        except:
            item['cashFlowFromContinuingInvestingActivities 2019'] = '-'
        try:
            item['cashFlowFromContinuingInvestingActivities 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualCashFlowFromContinuingInvestingActivities'])[1]['reportedValue']['raw']
        except:
            item['cashFlowFromContinuingInvestingActivities 2018'] = '-'
        try:
            item['cashFlowFromContinuingInvestingActivities 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualCashFlowFromContinuingInvestingActivities'])[0]['reportedValue']['raw']
        except:
            item['cashFlowFromContinuingInvestingActivities 2017'] = '-'

        try:
            item['financingCashFlow TTM'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'trailingFinancingCashFlow'])[0]['reportedValue']['raw']
        except:
            item['financingCashFlow TTM'] = '-'
        try:
            item['financingCashFlow 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualFinancingCashFlow'])[2]['reportedValue']['raw']
        except:
            item['financingCashFlow 2019'] = '-'
        try:
            item['financingCashFlow 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualFinancingCashFlow'])[1]['reportedValue']['raw']
        except:
            item['financingCashFlow 2018'] = '-'
        try:
            item['financingCashFlow 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualFinancingCashFlow'])[0]['reportedValue']['raw']
        except:
            item['financingCashFlow 2017'] = '-'

        try:
            item['endCashPosition TTM'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'trailingEndCashPosition'])[0]['reportedValue']['raw']
        except:
            item['endCashPosition TTM'] = '-'
        try:
            item['endCashPosition 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualEndCashPosition'])[2]['reportedValue']['raw']
        except:
            item['endCashPosition 2019'] = '-'
        try:
            item['endCashPosition 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualEndCashPosition'])[1]['reportedValue']['raw']
        except:
            item['endCashPosition 2018'] = '-'
        try:
            item['endCashPosition 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualEndCashPosition'])[0]['reportedValue']['raw']
        except:
            item['endCashPosition 2017'] = '-'

        try:
            item['incomeTaxPaidSupplementalData TTM'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'trailingIncomeTaxPaidSupplementalData'])[0]['reportedValue']['raw']
        except:
            item['incomeTaxPaidSupplementalData TTM'] = '-'
        try:
            item['incomeTaxPaidSupplementalData 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualIncomeTaxPaidSupplementalData'])[2]['reportedValue']['raw']
        except:
            item['incomeTaxPaidSupplementalData 2019'] = '-'
        try:
            item['incomeTaxPaidSupplementalData 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualIncomeTaxPaidSupplementalData'])[1]['reportedValue']['raw']
        except:
            item['incomeTaxPaidSupplementalData 2018'] = '-'
        try:
            item['incomeTaxPaidSupplementalData 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualIncomeTaxPaidSupplementalData'])[0]['reportedValue']['raw']
        except:
            item['incomeTaxPaidSupplementalData 2017'] = '-'

        try:
            item['capitalExpenditure TTM'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'trailingCapitalExpenditure'])[0]['reportedValue']['raw']
        except:
            item['capitalExpenditure TTM'] = '-'
        try:
            item['capitalExpenditure 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualCapitalExpenditure'])[2]['reportedValue']['raw']
        except:
            item['capitalExpenditure 2019'] = '-'
        try:
            item['capitalExpenditure 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualCapitalExpenditure'])[1]['reportedValue']['raw']
        except:
            item['capitalExpenditure 2018'] = '-'
        try:
            item['capitalExpenditure 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualCapitalExpenditure'])[0]['reportedValue']['raw']
        except:
            item['capitalExpenditure 2017'] = '-'

        try:
            item['issuanceOfCapitalStock TTM'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'trailingIssuanceOfCapitalStock'])[0]['reportedValue']['raw']
        except:
            item['issuanceOfCapitalStock TTM'] = '-'
        try:
            item['issuanceOfCapitalStock 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualIssuanceOfCapitalStock'])[2]['reportedValue']['raw']
        except:
            item['issuanceOfCapitalStock 2019'] = '-'
        try:
            item['issuanceOfCapitalStock 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualIssuanceOfCapitalStock'])[1]['reportedValue']['raw']
        except:
            item['issuanceOfCapitalStock 2018'] = '-'
        try:
            item['issuanceOfCapitalStock 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualIssuanceOfCapitalStock'])[0]['reportedValue']['raw']
        except:
            item['issuanceOfCapitalStock 2017'] = '-'

        try:
            item['issuanceOfDebt TTM'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'trailingIssuanceOfDebt'])[0]['reportedValue']['raw']
        except:
            item['issuanceOfDebt TTM'] = '-'
        try:
            item['issuanceOfDebt 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualIssuanceOfDebt'])[2]['reportedValue']['raw']
        except:
            item['issuanceOfDebt 2019'] = '-'
        try:
            item['issuanceOfDebt 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualIssuanceOfDebt'])[1]['reportedValue']['raw']
        except:
            item['issuanceOfDebt 2018'] = '-'
        try:
            item['issuanceOfDebt 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualIssuanceOfDebt'])[0]['reportedValue']['raw']
        except:
            item['issuanceOfDebt 2017'] = '-'

        try:
            item['repaymentOfDebt TTM'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'trailingRepaymentOfDebt'])[0]['reportedValue']['raw']
        except:
            item['repaymentOfDebt TTM'] = '-'
        try:
            item['repaymentOfDebt 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualRepaymentOfDebt'])[2]['reportedValue']['raw']
        except:
            item['repaymentOfDebt 2019'] = '-'
        try:
            item['repaymentOfDebt 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualRepaymentOfDebt'])[1]['reportedValue']['raw']
        except:
            item['repaymentOfDebt 2018'] = '-'
        try:
            item['repaymentOfDebt 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualRepaymentOfDebt'])[0]['reportedValue']['raw']
        except:
            item['repaymentOfDebt 2017'] = '-'

        try:
            item['repurchaseOfCapitalStock TTM'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'trailingRepurchaseOfCapitalStock'])[0]['reportedValue']['raw']
        except:
            item['repurchaseOfCapitalStock TTM'] = '-'
        try:
            item['repurchaseOfCapitalStock 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualRepurchaseOfCapitalStock'])[2]['reportedValue']['raw']
        except:
            item['repurchaseOfCapitalStock 2019'] = '-'
        try:
            item['repurchaseOfCapitalStock 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualRepurchaseOfCapitalStock'])[1]['reportedValue']['raw']
        except:
            item['repurchaseOfCapitalStock 2018'] = '-'
        try:
            item['repurchaseOfCapitalStock 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualRepurchaseOfCapitalStock'])[0]['reportedValue']['raw']
        except:
            item['repurchaseOfCapitalStock 2017'] = '-'

        try:
            item['freeCashFlow TTM'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'trailingFreeCashFlow'])[0]['reportedValue']['raw']
        except:
            item['freeCashFlow TTM'] = '-'
        try:
            item['freeCashFlow 2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualFreeCashFlow'])[2]['reportedValue']['raw']
        except:
            item['freeCashFlow 2019'] = '-'
        try:
            item['freeCashFlow 2018'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualFreeCashFlow'])[1]['reportedValue']['raw']
        except:
            item['freeCashFlow 2018'] = '-'
        try:
            item['freeCashFlow 2017'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteTimeSeriesStore', 'timeSeries', 'annualFreeCashFlow'])[0]['reportedValue']['raw']
        except:
            item['freeCashFlow 2017'] = '-'

        try:
            driver.find_element_by_xpath('//*[@id="Col1-1-Financials-Proxy"]/section/div[1]/div[2]/button').click()
            time.sleep(2)
            requests_data = driver.page_source
            json_strn = requests_data[requests_data.find('root.App.main = ') + len('root.App.main = '):]
            data = json.loads(json_strn[:json_strn.find('}(this));') - 2])
        except:
            driver.quit()
            writer.writerow(item)
            csv_file.flush()
            continue

        try:
            item['operatingCashFlow 06/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'cashflowStatementHistoryQuarterly', 'cashflowStatements'])[0]['totalCashFromOperatingActivities']['raw']
        except:
            item['operatingCashFlow 06/2020'] = '-'
        try:
            item['operatingCashFlow 03/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'cashflowStatementHistoryQuarterly', 'cashflowStatements'])[1]['totalCashFromOperatingActivities']['raw']
        except:
            item['operatingCashFlow 03/2020'] = '-'
        try:
            item['operatingCashFlow 12/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'cashflowStatementHistoryQuarterly', 'cashflowStatements'])[2]['totalCashFromOperatingActivities']['raw']
        except:
            item['operatingCashFlow 03/2020'] = '-'
        try:
            item['operatingCashFlow 09/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'cashflowStatementHistoryQuarterly', 'cashflowStatements'])[3]['totalCashFromOperatingActivities']['raw']
        except:
            item['operatingCashFlow 09/2020'] = '-'

        try:
            item['investingCashFlow 06/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'cashflowStatementHistoryQuarterly', 'cashflowStatements'])[0]['totalCashflowsFromInvestingActivities']['raw']
        except:
            item['investingCashFlow 06/2020'] = '-'
        try:
            item['investingCashFlow 03/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'cashflowStatementHistoryQuarterly', 'cashflowStatements'])[1]['totalCashflowsFromInvestingActivities']['raw']
        except:
            item['investingCashFlow 03/2020'] = '-'
        try:
            item['investingCashFlow 12/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'cashflowStatementHistoryQuarterly', 'cashflowStatements'])[2]['totalCashflowsFromInvestingActivities']['raw']
        except:
            item['investingCashFlow 12/2019'] = '-'
        try:
            item['investingCashFlow 09/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'cashflowStatementHistoryQuarterly', 'cashflowStatements'])[3]['totalCashflowsFromInvestingActivities']['raw']
        except:
            item['investingCashFlow 09/2019'] = '-'

        try:
            item['cashFlowFromContinuingInvestingActivities 06/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'cashflowStatementHistoryQuarterly', 'cashflowStatements'])[0]['totalCashflowsFromInvestingActivities']['raw']
        except:
            item['cashFlowFromContinuingInvestingActivities 06/2020'] = '-'
        try:
            item['cashFlowFromContinuingInvestingActivities 03/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'cashflowStatementHistoryQuarterly', 'cashflowStatements'])[1]['totalCashflowsFromInvestingActivities']['raw']
        except:
            item['cashFlowFromContinuingInvestingActivities 03/2020'] = '-'
        try:
            item['cashFlowFromContinuingInvestingActivities 12/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'cashflowStatementHistoryQuarterly', 'cashflowStatements'])[2]['totalCashflowsFromInvestingActivities']['raw']
        except:
            item['cashFlowFromContinuingInvestingActivities 12/2019'] = '-'
        try:
            item['cashFlowFromContinuingInvestingActivities 09/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'cashflowStatementHistoryQuarterly', 'cashflowStatements'])[3]['totalCashflowsFromInvestingActivities']['raw']
        except:
            item['cashFlowFromContinuingInvestingActivities 09/2019'] = '-'

        try:
            item['financingCashFlow 06/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'cashflowStatementHistoryQuarterly', 'cashflowStatements'])[0]['totalCashFromFinancingActivities']['raw']
        except:
            item['financingCashFlow 06/2020'] = '-'
        try:
            item['financingCashFlow 03/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'cashflowStatementHistoryQuarterly', 'cashflowStatements'])[1]['totalCashFromFinancingActivities']['raw']
        except:
            item['financingCashFlow 03/2020'] = '-'
        try:
            item['financingCashFlow 12/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'cashflowStatementHistoryQuarterly', 'cashflowStatements'])[2]['totalCashFromFinancingActivities']['raw']
        except:
            item['financingCashFlow 12/2019'] = '-'
        try:
            item['financingCashFlow 09/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'cashflowStatementHistoryQuarterly', 'cashflowStatements'])[3]['totalCashFromFinancingActivities']['raw']
        except:
            item['financingCashFlow 09/2019'] = '-'

        try:
            item['capitalExpenditure 06/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'cashflowStatementHistoryQuarterly', 'cashflowStatements'])[0]['capitalExpenditures']['raw']
        except:
            item['capitalExpenditure 06/2020'] = '-'
        try:
            item['capitalExpenditure 03/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'cashflowStatementHistoryQuarterly', 'cashflowStatements'])[1]['capitalExpenditures']['raw']
        except:
            item['capitalExpenditure 03/2020'] = '-'
        try:
            item['capitalExpenditure 12/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'cashflowStatementHistoryQuarterly', 'cashflowStatements'])[2]['capitalExpenditures']['raw']
        except:
            item['capitalExpenditure 12/2019'] = '-'
        try:
            item['capitalExpenditure 09/2019'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'cashflowStatementHistoryQuarterly', 'cashflowStatements'])[3]['capitalExpenditures']['raw']
        except:
            item['capitalExpenditure 09/2019'] = '-'

        try:
            item['issuanceOfCapitalStock 06/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'cashflowStatementHistoryQuarterly', 'cashflowStatements'])[0]['issuanceOfStock']['raw']
        except:
            item['issuanceOfCapitalStock 06/2020'] = '0'
        try:
            item['issuanceOfCapitalStock 06/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'cashflowStatementHistoryQuarterly', 'cashflowStatements'])[1]['issuanceOfStock']['raw']
        except:
            item['issuanceOfCapitalStock 06/2020'] = '-'
        try:
            item['issuanceOfCapitalStock 06/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'cashflowStatementHistoryQuarterly', 'cashflowStatements'])[2]['issuanceOfStock']['raw']
        except:
            item['issuanceOfCapitalStock 06/2020'] = '-'
        try:
            item['issuanceOfCapitalStock 06/2020'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'cashflowStatementHistoryQuarterly', 'cashflowStatements'])[3]['issuanceOfStock']['raw']
        except:
            item['issuanceOfCapitalStock 06/2020'] = '-'

        try:
            driver.find_element_by_xpath('//*[@id="quote-nav"]/ul/li[9]/a').click()
            time.sleep(5)
            driver.refresh()
            time.sleep(5)
            requests_data = driver.page_source
            json_strn = requests_data[requests_data.find('root.App.main = ') + len('root.App.main = '):]
            data = json.loads(json_strn[:json_strn.find('}(this));') - 2])
        except:
            driver.quit()
            writer.writerow(item)
            csv_file.flush()
            continue

        try:
            item['avg.Estimate CurrentQtr'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'earningsTrend', 'trend'])[0]['revenueEstimate']['avg']['raw']
        except:
            item['avg.Estimate CurrentQtr'] = '-'

        try:
            item['avg.Estimate NextQtr'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'earningsTrend', 'trend'])[1]['revenueEstimate']['avg']['raw']
        except:
            item['avg.Estimate NextQtr'] = '-'
        try:
            item['avg.Estimate CurrentYear'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'earningsTrend', 'trend'])[2]['revenueEstimate']['avg']['raw']
        except:
            item['avg.Estimate CurrentYear'] = '-'
        try:
            item['avg.Estimate NextYear'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'earningsTrend', 'trend'])[3]['revenueEstimate']['avg']['raw']
        except:
            item['avg.Estimate NextYear'] = '-'

        try:
            item['salesGrowth CurrentQtr'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'earningsTrend', 'trend'])[0]['revenueEstimate']['growth']['fmt']
        except:
            item['salesGrowth CurrentQtr'] = '-'
        try:
            item['salesGrowth NextQtr'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'earningsTrend', 'trend'])[1]['revenueEstimate']['growth']['fmt']
        except:
            item['salesGrowth NextQtr'] = '-'
        try:
            item['salesGrowth CurrentYear'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'earningsTrend', 'trend'])[2]['revenueEstimate']['growth']['fmt']
        except:
            item['salesGrowth CurrentYear'] = '-'
        try:
            item['salesGrowth NextYear'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'earningsTrend', 'trend'])[3]['revenueEstimate']['growth']['fmt']
        except:
            item['salesGrowth NextYear'] = '-'

        # try:
        #     item['EPSCurrentEstimate CurrentQtr'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'earningsTrend', 'trend'])[0]['epsTrend']['current']['raw']
        # except:
        #     item['EPSCurrentEstimate CurrentQtr'] = '-'
        # try:
        #     item['EPSCurrentEstimate NextQtr'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'earningsTrend', 'trend'])[1]['epsTrend']['current']['raw']
        # except:
        #     item['EPSCurrentEstimate NextQtr'] = '-'
        # try:
        #     item['EPSCurrentEstimate CurrentYear'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'earningsTrend', 'trend'])[2]['epsTrend']['current']['raw']
        # except:
        #     item['EPSCurrentEstimate CurrentYear'] = '-'
        # try:
        #     item['EPSCurrentEstimate NextYear'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'earningsTrend', 'trend'])[3]['epsTrend']['current']['raw']
        # except:
        #     item['EPSCurrentEstimate NextYear'] = '-'

        try:
            item['revenueEstimate Current Year'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'earningsTrend', 'trend'])[2]['revenueEstimate']['avg']['fmt']
        except:
            item['revenueEstimate Current Year'] ='-'
        try:
            item['revenueEstimate Next Year'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'earningsTrend', 'trend'])[3]['revenueEstimate']['avg']['fmt']
        except:
            item['revenueEstimate next Year'] ='-'

        try:
            item['growthEstimates CurrentQtr'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'earningsTrend', 'trend'])[0]['growth']['raw']
        except:
            item['growthEstimates CurrentQtr'] = '-'
        try:
            item['growthEstimates NextQtr'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'earningsTrend', 'trend'])[1]['growth']['raw']
        except:
            item['growthEstimates NextQtr'] = '-'
        try:
            item['growthEstimates CurrentYear'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'earningsTrend', 'trend'])[2]['growth']['raw']
        except:
            item['growthEstimates CurrentYear'] = '-'
        try:
            item['growthEstimates NextYear'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'earningsTrend', 'trend'])[3]['growth']['raw']
        except:
            item['growthEstimates NextYear'] = '-'
        try:
            item['growthEstimates Next5Years'] = get_dict_value(data, ['context', 'dispatcher', 'stores', 'QuoteSummaryStore', 'earningsTrend', 'trend'])[4]['growth']['raw']
        except:
            item['growthEstimates Next5Years'] = '-'

        driver.quit()
        writer.writerow(item)
        csv_file.flush()


if __name__ == '__main__':
    getValues()

    print('process end')
