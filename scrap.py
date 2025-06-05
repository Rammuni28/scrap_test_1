from typing import Self
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os
from pathlib import Path

# ================== CONFIGURATION SECTION ==================
# STATES to scrape (add more state XPaths as needed)
STATES_CONFIG = {
    "uttar_pradesh": "/html/body/div[3]/div/ul/li[35]",
    "maharashtra": "/html/body/div[3]/div/ul/li[21]",
    "rajasthan": "/html/body/div[3]/div/ul/li[30]",
    "Chhattisgarh": "/html/body/div[3]/div/ul/li[7]",
    "jharkhand": "/html/body/div[3]/div/ul/li[15]",
    # Add more states here if needed
    # "maharashtra": "//*[@id='j_idt37_27']", 
    # "karnataka": "//*[@id='j_idt37_29']",
}

# YEARS to scrape (add more year XPaths as needed)
YEARS_CONFIG = {
    "2025": "//*[@id='selectedYear_1']",
    "2024": "//*[@id='selectedYear_2']",
    
    # Add more years here if needed
    # "2022": "//*[@id='selectedYear_3']",
}

# RTO configurations per state (add more RTOs as needed)
# RTO_CONFIG = {
#     "uttar_pradesh": {
#         "Agra RTO - UP80": "//*[@id='selectedRto_items']/li[2]",
#     }
#     # Add RTOs for other states here
# }
RTO_CONFIG = {
    "uttar_pradesh": {
        "Agra RTO - UP80": "//*[@id='selectedRto_items']/li[2]",
        "AKBARPUR(AMBEDKAR NAGAR) - UP45": "//*[@id='selectedRto_items']/li[3]",
        "ALIGARH RTO - UP81": "//*[@id='selectedRto_items']/li[4]",
        "Amethi ARTO - UP36": "//*[@id='selectedRto_items']/li[5]",
        "ARTO OFFICE RAMPUR - UP22": "//*[@id='selectedRto_items']/li[6]",
        "AURAIYA - UP79": "//*[@id='selectedRto_items']/li[7]",
        "AYODHYA RTO - UP42": "//*[@id='selectedRto_items']/li[8]",
        "Azamgarh RTO - UP50": "//*[@id='selectedRto_items']/li[9]",
        "Badaun - UP24": "//*[@id='selectedRto_items']/li[10]",
        "Baghpat - UP17": "//*[@id='selectedRto_items']/li[11]",
        "Bahraich - UP40": "//*[@id='selectedRto_items']/li[12]",
        "Ballia - UP60": "//*[@id='selectedRto_items']/li[13]",
        "Balrampur - UP47": "//*[@id='selectedRto_items']/li[14]",
        "BANDARTO - UP90": "//*[@id='selectedRto_items']/li[15]",
        "Barabanki ARTO - UP41": "//*[@id='selectedRto_items']/li[16]",
        "BAREILLY - UP25": "//*[@id='selectedRto_items']/li[17]",
        "BASTI RTO - UP51": "//*[@id='selectedRto_items']/li[18]",
        "Bhadohi(SANT RAVIDAS NAGAR) - UP66": "//*[@id='selectedRto_items']/li[19]",
        "Bijnor - UP20": "//*[@id='selectedRto_items']/li[20]",
        "Bulandshahar - UP13": "//*[@id='selectedRto_items']/li[21]",
        "Chandauli - UP67": "//*[@id='selectedRto_items']/li[22]",
        "Chitrakoot - UP96": "//*[@id='selectedRto_items']/li[23]",
        "DEORIA - UP52": "//*[@id='selectedRto_items']/li[24]",
        "Etah - UP82": "//*[@id='selectedRto_items']/li[25]",
        "Etawah - UP75": "//*[@id='selectedRto_items']/li[26]",
        "Farrukhabad - UP76": "//*[@id='selectedRto_items']/li[27]",
        "FATHEHPUR - UP71": "//*[@id='selectedRto_items']/li[28]",
        "FEROZABAD - UP83": "//*[@id='selectedRto_items']/li[29]",
        "GHAZIABAD - UP14": "//*[@id='selectedRto_items']/li[30]",
        "Ghazipur - UP61": "//*[@id='selectedRto_items']/li[31]",
        "GONDA - UP43": "//*[@id='selectedRto_items']/li[32]",
        "Gorakhpur RTO - UP53": "//*[@id='selectedRto_items']/li[33]",
        "HAMIRPUR(UP) - UP91": "//*[@id='selectedRto_items']/li[34]",
        "Hapur - UP37": "//*[@id='selectedRto_items']/li[35]",
        "HARDOI - UP30": "//*[@id='selectedRto_items']/li[36]",
        "HATHRAS - UP86": "//*[@id='selectedRto_items']/li[37]",
        "JAUNPUR - UP62": "//*[@id='selectedRto_items']/li[38]",
        "JhansiRTO - UP93": "//*[@id='selectedRto_items']/li[39]",
        "JPNAGAR - UP23": "//*[@id='selectedRto_items']/li[40]",
        "Kannauj - UP74": "//*[@id='selectedRto_items']/li[41]",
        "Kanpur Dehat - UP77": "//*[@id='selectedRto_items']/li[42]",
        "KANPUR NAGAR - UP78": "//*[@id='selectedRto_items']/li[43]",
        "Kasganj(kashi ram nagar) - UP87": "//*[@id='selectedRto_items']/li[44]",
        "Kaushambi - UP73": "//*[@id='selectedRto_items']/li[45]",
        "LAKHIMPUR KHERI - UP31": "//*[@id='selectedRto_items']/li[46]",
        "Lalitpur - UP94": "//*[@id='selectedRto_items']/li[47]",
        "MAHANAGAR ARTO LUCKNOW (UP321) - UP321": "//*[@id='selectedRto_items']/li[48]",
        "Maharajganj - UP56": "//*[@id='selectedRto_items']/li[49]",
        "Mahoba - UP95": "//*[@id='selectedRto_items']/li[50]",
        "Mainpuri - UP84": "//*[@id='selectedRto_items']/li[51]",
        "MATHURA - UP85": "//*[@id='selectedRto_items']/li[52]",
        "Mau - UP54": "//*[@id='selectedRto_items']/li[53]",
        "MEERUT RTO - UP15": "//*[@id='selectedRto_items']/li[54]",
        "MIRZAPUR RTO - UP63": "//*[@id='selectedRto_items']/li[55]",
        "MORADABAD - UP21": "//*[@id='selectedRto_items']/li[56]",
        "M/S Sai Dham Super Srv Soln Pvt Ltd Ghaziabad - UP214": "//*[@id='selectedRto_items']/li[57]",
        "MuzaffarNagar - UP12": "//*[@id='selectedRto_items']/li[58]",
        "Noida - UP16": "//*[@id='selectedRto_items']/li[59]",
        "Orai - UP92": "//*[@id='selectedRto_items']/li[60]",
        "PADRAUNA(KUSHI NAGAR) - UP57": "//*[@id='selectedRto_items']/li[61]",
        "Pilibhit - UP26": "//*[@id='selectedRto_items']/li[62]",
        "PRATAPGARH - UP72": "//*[@id='selectedRto_items']/li[63]",
        "Prayagraj RTO - UP70": "//*[@id='selectedRto_items']/li[64]",
        "Raibareilly - UP33": "//*[@id='selectedRto_items']/li[65]",
        "SAHARANPUR RTO - UP11": "//*[@id='selectedRto_items']/li[66]",
        "SAHJAHANPUR - UP27": "//*[@id='selectedRto_items']/li[67]",
        "Sambhal ARTO - UP38": "//*[@id='selectedRto_items']/li[68]",
        "Sant Kabir Nagar - UP58": "//*[@id='selectedRto_items']/li[69]",
        "SHAMLI ARTO - UP19": "//*[@id='selectedRto_items']/li[70]",
        "Shravasti - UP46": "//*[@id='selectedRto_items']/li[71]",
        "Siddharth Nagar(naugarh) - UP55": "//*[@id='selectedRto_items']/li[72]",
        "Sitapur - UP34": "//*[@id='selectedRto_items']/li[73]",
        "SONBHADRA - UP64": "//*[@id='selectedRto_items']/li[74]",
        "STATE TRANSPORT AUTHORITY - UP999": "//*[@id='selectedRto_items']/li[75]",
        "Sultanpur - UP44": "//*[@id='selectedRto_items']/li[76]",
        "TRANSPORT NAGAR RTO LUCKNOW (UP32) - UP32": "//*[@id='selectedRto_items']/li[77]",
        "Unnao - UP35": "//*[@id='selectedRto_items']/li[78]",
        "VARANASI RTO - UP65": "//*[@id='selectedRto_items']/li[79]"
    },
    "maharashtra": {
        "AKLUJ - MH45": "//ul[@id='selectedRto_items']/li[2]",
        "AMBEJOGAI - MH44": "//ul[@id='selectedRto_items']/li[3]",
        "AMRAWATI - MH27": "//ul[@id='selectedRto_items']/li[4]",
        "BARAMATI - MH42": "//ul[@id='selectedRto_items']/li[5]",
        "BEED - MH23": "//ul[@id='selectedRto_items']/li[6]",
        "BHADGAON - MH54": "//ul[@id='selectedRto_items']/li[7]",
        "BHANDARA - MH36": "//ul[@id='selectedRto_items']/li[8]",
        "BULDHANA - MH28": "//ul[@id='selectedRto_items']/li[9]",
        "CHALISGAON - MH52": "//ul[@id='selectedRto_items']/li[10]",
        "CHHATRAPATI SAMBHAJINAGAR - MH20": "//ul[@id='selectedRto_items']/li[11]",
        "Chiplun Chiplun Track - MH202": "//ul[@id='selectedRto_items']/li[12]",
        "DHARASHIV - MH25": "//ul[@id='selectedRto_items']/li[13]",
        "DHULE - MH18": "//ul[@id='selectedRto_items']/li[14]",
        "DY REGIONAL TRANSPORT OFFICE, HINGOLI - MH38": "//ul[@id='selectedRto_items']/li[15]",
        "DY RTO RATNAGIRI - MH8": "//ul[@id='selectedRto_items']/li[16]",
        "GADCHIROLI - MH33": "//ul[@id='selectedRto_items']/li[17]",
        "GONDHIA - MH35": "//ul[@id='selectedRto_items']/li[18]",
        "ICHALKARANJI - MH51": "//ul[@id='selectedRto_items']/li[19]",
        "JALANA - MH21": "//ul[@id='selectedRto_items']/li[20]",
        "KALYAN - MH5": "//ul[@id='selectedRto_items']/li[21]",
        "KARAD - MH50": "//ul[@id='selectedRto_items']/li[22]",
        "KHAMGAON - MH56": "//ul[@id='selectedRto_items']/li[23]",
        "KOLHAPUR - MH9": "//ul[@id='selectedRto_items']/li[24]",
        "MALEGAON - MH41": "//ul[@id='selectedRto_items']/li[25]",
        "MIRA BHAYANDAR - MH58": "//ul[@id='selectedRto_items']/li[26]",
        "MUMBAI (CENTRAL) - MH1": "//ul[@id='selectedRto_items']/li[27]",
        "MUMBAI (EAST) - MH3": "//ul[@id='selectedRto_items']/li[28]",
        "MUMBAI (WEST) - MH2": "//ul[@id='selectedRto_items']/li[29]",
        "NAGPUR (EAST) - MH49": "//ul[@id='selectedRto_items']/li[30]",
        "NAGPUR (RURAL) - MH40": "//ul[@id='selectedRto_items']/li[31]",
        "NAGPUR (U) - MH31": "//ul[@id='selectedRto_items']/li[32]",
        "NANDED - MH26": "//ul[@id='selectedRto_items']/li[33]",
        "NANDURBAR - MH39": "//ul[@id='selectedRto_items']/li[34]",
        "NASHIK - MH15": "//ul[@id='selectedRto_items']/li[35]",
        "PANVEL - MH46": "//ul[@id='selectedRto_items']/li[36]",
        "PARBHANI - MH22": "//ul[@id='selectedRto_items']/li[37]",
        "PEN (RAIGAD) - MH6": "//ul[@id='selectedRto_items']/li[38]",
        "PHALTAN - MH53": "//ul[@id='selectedRto_items']/li[39]",
        "PUNE - MH12": "//ul[@id='selectedRto_items']/li[40]",
        "RTO AHEMEDNAGAR - MH16": "//ul[@id='selectedRto_items']/li[41]",
        "RTO AKOLA - MH30": "//ul[@id='selectedRto_items']/li[42]",
        "R.T.O.BORIVALI - MH47": "//ul[@id='selectedRto_items']/li[43]",
        "RTO CHANDRAPUR - MH34": "//ul[@id='selectedRto_items']/li[44]",
        "RTO JALGAON - MH19": "//ul[@id='selectedRto_items']/li[45]",
        "RTO LATUR - MH24": "//ul[@id='selectedRto_items']/li[46]",
        "RTO MH04-Mira Bhayander FitnessTrack - MH203": "//ul[@id='selectedRto_items']/li[47]",
        "RTO PIMPRI CHINCHWAD - MH14": "//ul[@id='selectedRto_items']/li[48]",
        "RTO SATARA - MH11": "//ul[@id='selectedRto_items']/li[49]",
        "RTO SOLAPUR - MH13": "//ul[@id='selectedRto_items']/li[50]",
        "SANGLI - MH10": "//ul[@id='selectedRto_items']/li[51]",
        "SINDHUDURG(KUDAL) - MH7": "//ul[@id='selectedRto_items']/li[52]",
        "SRIRAMPUR - MH17": "//ul[@id='selectedRto_items']/li[53]",
        "TC OFFICE - MH99": "//ul[@id='selectedRto_items']/li[54]",
        "THANE - MH4": "//ul[@id='selectedRto_items']/li[55]",
        "UDGIR - MH55": "//ul[@id='selectedRto_items']/li[56]",
        "VASAI - MH48": "//ul[@id='selectedRto_items']/li[57]",
        "VASHI (NEW MUMBAI) - MH43": "//ul[@id='selectedRto_items']/li[58]",
        "WARDHA - MH32": "//ul[@id='selectedRto_items']/li[59]",
        "WASHIM - MH37": "//ul[@id='selectedRto_items']/li[60]",
        "YAWATMAL - MH29": "//ul[@id='selectedRto_items']/li[61]"
    },
     "rajasthan": {
        "ABU ROAD DTO - RJ38": "//ul[@id='selectedRto_items']/li[2]",
        "Adinath Fitness Center - RJ260": "//ul[@id='selectedRto_items']/li[3]",
        "Agarwal Fitness Center - RJ225": "//ul[@id='selectedRto_items']/li[4]",
        "AJMER RTO - RJ1": "//ul[@id='selectedRto_items']/li[5]",
        "A&L Company - RJ267": "//ul[@id='selectedRto_items']/li[6]",
        "Alwar Auto Mobile Fitness Center - RJ243": "//ul[@id='selectedRto_items']/li[7]",
        "Alwar Fitness Center - RJ254": "//ul[@id='selectedRto_items']/li[8]",
        "ALWAR RTO - RJ2": "//ul[@id='selectedRto_items']/li[9]",
        "ARAVALI FITNESS TESTING CENTER - RJ218": "//ul[@id='selectedRto_items']/li[10]",
        "Arihant Vehicle Fitness Center - RJ257": "//ul[@id='selectedRto_items']/li[11]",
        "Atharva Enterprises - RJ261": "//ul[@id='selectedRto_items']/li[12]",
        "BALAJI ALLIANCE - RJ280": "//ul[@id='selectedRto_items']/li[13]",
        "BALAJI FITNESS CENTER (BHILWARA) - RJ210": "//ul[@id='selectedRto_items']/li[14]",
        "BALAJI FITNESS CENTER (HANUMANGARH) - RJ209": "//ul[@id='selectedRto_items']/li[15]",
        "BALOTRA DTO - RJ39": "//ul[@id='selectedRto_items']/li[16]",
        "BANSWARA DTO - RJ3": "//ul[@id='selectedRto_items']/li[17]",
        "BANSWARA VEHICLE FITNESS CENTER - RJ276": "//ul[@id='selectedRto_items']/li[18]",
        "BARAN DTO - RJ28": "//ul[@id='selectedRto_items']/li[19]",
        "BARMER DTO - RJ4": "//ul[@id='selectedRto_items']/li[20]",
        "BEAWAR DTO - RJ36": "//ul[@id='selectedRto_items']/li[21]",
        "BHARATPUR RTO - RJ5": "//ul[@id='selectedRto_items']/li[22]",
        "Bharat Vahan Fitness Center - RJ250": "//ul[@id='selectedRto_items']/li[23]",
        "BHILWARA DTO - RJ6": "//ul[@id='selectedRto_items']/li[24]",
        "BHINMAL DTO - RJ46": "//ul[@id='selectedRto_items']/li[25]",
        "BHIWARI DTO - RJ40": "//ul[@id='selectedRto_items']/li[26]",
        "BIKANER RTO - RJ7": "//ul[@id='selectedRto_items']/li[27]",
        "BUNDI DTO - RJ8": "//ul[@id='selectedRto_items']/li[28]",
        "CHITTORGARH RTO - RJ9": "//ul[@id='selectedRto_items']/li[29]",
        "CHOMU DTO - RJ41": "//ul[@id='selectedRto_items']/li[30]",
        "CHURU DTO - RJ10": "//ul[@id='selectedRto_items']/li[31]",
        "DAUSA RTO - RJ29": "//ul[@id='selectedRto_items']/li[32]",
        "DHOLPUR DTO - RJ11": "//ul[@id='selectedRto_items']/li[33]",
        "DIDWANA DTO - RJ37": "//ul[@id='selectedRto_items']/li[34]",
        "DUDU DTO - RJ47": "//ul[@id='selectedRto_items']/li[35]",
        "DUDU FITNESS CENTER - RJ281": "//ul[@id='selectedRto_items']/li[36]",
        "DUNGARPUR DTO - RJ12": "//ul[@id='selectedRto_items']/li[37]",
        "EXPLORE IT SERVICES PVT. LTD. - RJ228": "//ul[@id='selectedRto_items']/li[38]",
        "FREEDOM MOTORS - RJ224": "//ul[@id='selectedRto_items']/li[39]",
        "Ganesh Ji Fitness Center - RJ226": "//ul[@id='selectedRto_items']/li[40]",
        "G.Y. Fitness Center - RJ223": "//ul[@id='selectedRto_items']/li[41]",
        "HANUMANGARH DTO - RJ31": "//ul[@id='selectedRto_items']/li[42]",
        "Hindustan Automobiles - RJ251": "//ul[@id='selectedRto_items']/li[43]",
        "Indira Vehicle Fitness Centre - RJ269": "//ul[@id='selectedRto_items']/li[44]",
        "INFINITY FITNESS CENTER - RJ231": "//ul[@id='selectedRto_items']/li[45]",
        "JAGATPURA, JAIPUR ARTO - RJ141": "//ul[@id='selectedRto_items']/li[46]",
        "Jai Bhawani Fitness Center - RJ236": "//ul[@id='selectedRto_items']/li[47]",
        "JAIPUR (FIRST) RTO - RJ14": "//ul[@id='selectedRto_items']/li[48]",
        "JAIPUR (SECOND) RTO - RJ59": "//ul[@id='selectedRto_items']/li[49]",
        "Jaipur Vehicle Fitness and Maintenance Center - RJ234": "//ul[@id='selectedRto_items']/li[50]",
        "JAISALMER DTO - RJ15": "//ul[@id='selectedRto_items']/li[51]",
        "JALORE DTO - RJ16": "//ul[@id='selectedRto_items']/li[52]",
        "JALORE FITNESS CENTRE - RJ282": "//ul[@id='selectedRto_items']/li[53]",
        "JHALAWAR DTO - RJ17": "//ul[@id='selectedRto_items']/li[54]",
        "JHUNJHUNU DTO - RJ18": "//ul[@id='selectedRto_items']/li[55]",
        "Jodhpur Parivahan Fitness Centre - RJ242": "//ul[@id='selectedRto_items']/li[56]",
        "JODHPUR RTO - RJ19": "//ul[@id='selectedRto_items']/li[57]",
        "KAROLI DTO - RJ34": "//ul[@id='selectedRto_items']/li[58]",
        "KEKRI DTO - RJ48": "//ul[@id='selectedRto_items']/li[59]",
        "KHETRI DTO - RJ53": "//ul[@id='selectedRto_items']/li[60]",
        "KISHANGARH DTO - RJ42": "//ul[@id='selectedRto_items']/li[61]",
        "KOTA RTO - RJ20": "//ul[@id='selectedRto_items']/li[62]",
        "Kota Vehicle Fitness Center - RJ263": "//ul[@id='selectedRto_items']/li[63]",
        "KOTPUTALI DTO - RJ32": "//ul[@id='selectedRto_items']/li[64]",
        "Laxmi Parivahan Fitness Center - RJ266": "//ul[@id='selectedRto_items']/li[65]",
        "Mahadev Fitness Center - RJ233": "//ul[@id='selectedRto_items']/li[66]",
        "MAHADEV FITNESS CENTER BHILWARA - RJ274": "//ul[@id='selectedRto_items']/li[67]",
        "MAHADEV FITNESS CENTER JODHPUR - RJ273": "//ul[@id='selectedRto_items']/li[68]",
        "MAHAVEER JAIN FITNESS CENTRE - RJ229": "//ul[@id='selectedRto_items']/li[69]",
        "MAHAVEER PRASAD RAM KISHAN - RJ232": "//ul[@id='selectedRto_items']/li[70]",
        "Marudhara Transport Company - RJ271": "//ul[@id='selectedRto_items']/li[71]",
        "Marwar Fitness Center - RJ249": "//ul[@id='selectedRto_items']/li[72]",
        "Matsya Fitness Center - RJ220": "//ul[@id='selectedRto_items']/li[73]",
        "M & D Automobile Fitness Center - RJ222": "//ul[@id='selectedRto_items']/li[74]",
        "Meel Motors - RJ230": "//ul[@id='selectedRto_items']/li[75]",
        "Meera Fitness Center - RJ247": "//ul[@id='selectedRto_items']/li[76]",
        "MEERA FITNESS TESTING CENTER CHITTORGARH - RJ215": "//ul[@id='selectedRto_items']/li[77]",
        "M.K. Fitness Center - RJ239": "//ul[@id='selectedRto_items']/li[78]",
        "M/S Dholpur Fitness Center - RJ201": "//ul[@id='selectedRto_items']/li[79]",
        "M/S Jagdamba Fitness Center - RJ203": "//ul[@id='selectedRto_items']/li[80]",
        "M/S Nandan Fitness Testing Center - RJ204": "//ul[@id='selectedRto_items']/li[81]",
        "M/S OM Fitness & Service Center - RJ202": "//ul[@id='selectedRto_items']/li[82]",
        "Naganaray Fitness Center - RJ255": "//ul[@id='selectedRto_items']/li[83]",
        "NAGAUR DTO - RJ21": "//ul[@id='selectedRto_items']/li[84]",
        "Navdeep Fitness Test Center - RJ248": "//ul[@id='selectedRto_items']/li[85]",
        "Navdurga Vahan Fitness Center - RJ245": "//ul[@id='selectedRto_items']/li[86]",
        "Navkar Shri Fitness Testing Center - RJ216": "//ul[@id='selectedRto_items']/li[87]",
        "NOHAR DTO - RJ49": "//ul[@id='selectedRto_items']/li[88]",
        "NOKHA DTO - RJ50": "//ul[@id='selectedRto_items']/li[89]",
        "Nokha Vehicle Fitness Center - RJ253": "//ul[@id='selectedRto_items']/li[90]",
        "PALI RTO - RJ22": "//ul[@id='selectedRto_items']/li[91]",
        "Parasvnath Fitness Center - RJ240": "//ul[@id='selectedRto_items']/li[92]",
        "PAWAN VEHICLE FITNESS CENTER PVT LTD - RJ277": "//ul[@id='selectedRto_items']/li[93]",
        "PHALODI DTO - RJ43": "//ul[@id='selectedRto_items']/li[94]",
        "PIPAR CITY DTO - RJ54": "//ul[@id='selectedRto_items']/li[95]",
        "POKHRAN DTO - RJ55": "//ul[@id='selectedRto_items']/li[96]",
        "PRATAPGARH DTO - RJ35": "//ul[@id='selectedRto_items']/li[97]",
        "Preksha Parivahan Fitness Center - RJ265": "//ul[@id='selectedRto_items']/li[98]",
        "Prerna Parivahan Fitness Center - RJ272": "//ul[@id='selectedRto_items']/li[99]",
        "RAJASTHAN VEHICLE FITNESS CENTER - RJ283": "//ul[@id='selectedRto_items']/li[100]",
        "RAJSAMAND DTO - RJ30": "//ul[@id='selectedRto_items']/li[101]",
        "RAMGANJMANDI DTO - RJ33": "//ul[@id='selectedRto_items']/li[102]",
        "R.K. Fitness Center - RJ221": "//ul[@id='selectedRto_items']/li[103]",
        "Royal Motors - RJ268": "//ul[@id='selectedRto_items']/li[104]",
        "SADULSHAHAR DTO - RJ56": "//ul[@id='selectedRto_items']/li[105]",
        "SAHAPURA (BHILWARA) DTO - RJ51": "//ul[@id='selectedRto_items']/li[106]",
        "SAHAPURA (JAIPUR) DTO - RJ52": "//ul[@id='selectedRto_items']/li[107]",
        "SALUMBAR DTO - RJ58": "//ul[@id='selectedRto_items']/li[108]",
        "SAWAI MADHOPUR DTO - RJ25": "//ul[@id='selectedRto_items']/li[109]",
        "Schoolnet India Limited - RJ256": "//ul[@id='selectedRto_items']/li[110]",
        "SHAHPURA BHILWARA FITNESS CENTER - RJ275": "//ul[@id='selectedRto_items']/li[111]",
        "SHAHPURA VEHICLE FITNESS CENTER (JAIPUR) - RJ213": "//ul[@id='selectedRto_items']/li[112]",
        "Shanti Vehicle Fitness Testing Center - RJ208": "//ul[@id='selectedRto_items']/li[113]",
        "Shashank Automobiles - RJ227": "//ul[@id='selectedRto_items']/li[114]",
        "SHIV KRIPA FITNESS CENTER PVT LTD - RJ279": "//ul[@id='selectedRto_items']/li[115]",
        "SHREE BALAJI FITNESS CENTER PALI - RJ241": "//ul[@id='selectedRto_items']/li[116]",
        "Shree Fitness Center - RJ211": "//ul[@id='selectedRto_items']/li[117]",
        "Shree Kamdhenu Fitness Center - RJ219": "//ul[@id='selectedRto_items']/li[118]",
        "SHREE SHYAM VEHICLE FITNESS CENTER - RJ246": "//ul[@id='selectedRto_items']/li[119]",
        "SHRI BALAJI FITNESS CENTER BIKANER - RJ206": "//ul[@id='selectedRto_items']/li[120]",
        "Shri Bikaner Fitness Center - RJ205": "//ul[@id='selectedRto_items']/li[121]",
        "Shri Fitness Center - RJ259": "//ul[@id='selectedRto_items']/li[122]",
        "Shri Force Fitness Center - RJ217": "//ul[@id='selectedRto_items']/li[123]",
        "Shri Karni Fitness Center - RJ214": "//ul[@id='selectedRto_items']/li[124]",
        "SHRI MAHALAXMI FITNESS CENTER - RJ278": "//ul[@id='selectedRto_items']/li[125]",
        "Shri Vinayak Auto Fitness Center - RJ252": "//ul[@id='selectedRto_items']/li[126]",
        "SIKAR RTO - RJ23": "//ul[@id='selectedRto_items']/li[127]",
        "Sikar Vehicle Fitness Center - RJ212": "//ul[@id='selectedRto_items']/li[128]",
        "SIROHI DTO - RJ24": "//ul[@id='selectedRto_items']/li[129]",
        "Speedline Auto Fitness Private Limited - RJ270": "//ul[@id='selectedRto_items']/li[130]",
        "SRI GANGANAGAR DTO - RJ13": "//ul[@id='selectedRto_items']/li[131]",
        "SUJANGARH DTO - RJ44": "//ul[@id='selectedRto_items']/li[132]",
        "SUMERPUR DTO - RJ57": "//ul[@id='selectedRto_items']/li[133]",
        "Swarna Shri Fitness Testing Center - RJ207": "//ul[@id='selectedRto_items']/li[134]",
        "TIRUPATI ASSOCIATES - RJ238": "//ul[@id='selectedRto_items']/li[135]",
        "TIRUPATI ASSOCIATES MORIJA CHOMU - RJ237": "//ul[@id='selectedRto_items']/li[136]",
        "TIRUPATI FITNESS CENTER - RJ235": "//ul[@id='selectedRto_items']/li[137]",
        "TONK DTO - RJ26": "//ul[@id='selectedRto_items']/li[138]",
        "Tonk Fitness Center - RJ244": "//ul[@id='selectedRto_items']/li[139]",
        "Udaipur Fitness Center - RJ262": "//ul[@id='selectedRto_items']/li[140]",
        "UDAIPUR RTO - RJ27": "//ul[@id='selectedRto_items']/li[141]",
        "Vaahan Fitness Center - RJ264": "//ul[@id='selectedRto_items']/li[142]",
        "VATSAL ENTERPRISES - RJ258": "//ul[@id='selectedRto_items']/li[143]"
  
    },
    "Chhattisgarh": {
        "AIG(F/P) PHQ - CG3": "//ul[@id='selectedRto_items']/li[2]",
        "Ambikapur RTO - CG15": "//ul[@id='selectedRto_items']/li[3]",
        "BAIKUNTHPUR DTO - CG16": "//ul[@id='selectedRto_items']/li[4]",
        "Baloda Bazar DTO - CG22": "//ul[@id='selectedRto_items']/li[5]",
        "Balod DTO - CG24": "//ul[@id='selectedRto_items']/li[6]",
        "Balrampur DTO - CG30": "//ul[@id='selectedRto_items']/li[7]",
        "Bemetara DTO - CG25": "//ul[@id='selectedRto_items']/li[8]",
        "Bijapur DTO - CG20": "//ul[@id='selectedRto_items']/li[9]",
        "Bilaspur RTO - CG10": "//ul[@id='selectedRto_items']/li[10]",
        "Dantewada DTO - CG18": "//ul[@id='selectedRto_items']/li[11]",
        "Dhamtari DTO - CG5": "//ul[@id='selectedRto_items']/li[12]",
        "DURG RTO - CG7": "//ul[@id='selectedRto_items']/li[13]",
        "Gariyaband DTO - CG23": "//ul[@id='selectedRto_items']/li[14]",
        "Gaurela-Pendra-Marwahi DTO - CG31": "//ul[@id='selectedRto_items']/li[15]",
        "JAGDALPUR RTO - CG17": "//ul[@id='selectedRto_items']/li[16]",
        "Janjgir Champa DTO - CG11": "//ul[@id='selectedRto_items']/li[17]",
        "Jashpur DTO - CG14": "//ul[@id='selectedRto_items']/li[18]",
        "KANKER DTO - CG19": "//ul[@id='selectedRto_items']/li[19]",
        "KAWARDHA DTO - CG9": "//ul[@id='selectedRto_items']/li[20]",
        "KONDAGAON DTO - CG27": "//ul[@id='selectedRto_items']/li[21]",
        "Korba DTO - CG12": "//ul[@id='selectedRto_items']/li[22]",
        "Mahasamund DTO - CG6": "//ul[@id='selectedRto_items']/li[23]",
        "Mungeli DTO - CG28": "//ul[@id='selectedRto_items']/li[24]",
        "Narayanpur DTO - CG21": "//ul[@id='selectedRto_items']/li[25]",
        "Raigarh DTO - CG13": "//ul[@id='selectedRto_items']/li[26]",
        "Raipur RTO - CG4": "//ul[@id='selectedRto_items']/li[27]",
        "Rajnandgaon ARTO - CG8": "//ul[@id='selectedRto_items']/li[28]",
        "RTA TC NAWA RAIPUR - CG998": "//ul[@id='selectedRto_items']/li[29]",
        "State Transport Authority - CG99": "//ul[@id='selectedRto_items']/li[30]",
        "Sukma DTO - CG26": "//ul[@id='selectedRto_items']/li[31]",
        "Surajpur DTO - CG29": "//ul[@id='selectedRto_items']/li[32]"
        # Add more RTOs here if needed
    },
    "jharkhand": {
        "Authorised Testing Centre (TUV SUD), Ranchi - JH201": "//ul[@id='selectedRto_items']/li[2]",
        "Authorized Fitness Centre(VAHAN),Dhanbad - JH202": "//ul[@id='selectedRto_items']/li[3]",
        "BOKARO - JH9": "//ul[@id='selectedRto_items']/li[4]",
        "CHATRA - JH13": "//ul[@id='selectedRto_items']/li[5]",
        "DEOGHAR - JH15": "//ul[@id='selectedRto_items']/li[6]",
        "DHANBAD - JH10": "//ul[@id='selectedRto_items']/li[7]",
        "DTO OFFICE DUMKA - JH4": "//ul[@id='selectedRto_items']/li[8]",
        "EAST SINGHBHUM (JAMSHEDPUR) - JH5": "//ul[@id='selectedRto_items']/li[9]",
        "GARHWA - JH14": "//ul[@id='selectedRto_items']/li[10]",
        "GIRIDIH - JH11": "//ul[@id='selectedRto_items']/li[11]",
        "GODDA - JH17": "//ul[@id='selectedRto_items']/li[12]",
        "GUMLA - JH7": "//ul[@id='selectedRto_items']/li[13]",
        "HAZARIBAG - JH2": "//ul[@id='selectedRto_items']/li[14]",
        "JAMTARA - JH21": "//ul[@id='selectedRto_items']/li[15]",
        "KHUNTI - JH23": "//ul[@id='selectedRto_items']/li[16]",
        "KODERMA - JH12": "//ul[@id='selectedRto_items']/li[17]",
        "LATEHAR - JH19": "//ul[@id='selectedRto_items']/li[18]",
        "LOHARDAGA - JH8": "//ul[@id='selectedRto_items']/li[19]",
        "M/s Auto Fitness Centre,Ranchi - JH203": "//ul[@id='selectedRto_items']/li[20]",
        "M/s Auto Tech Vehicle Fitness,Ranchi - JH205": "//ul[@id='selectedRto_items']/li[21]",
        "M/S Global Automated Fitness,Hazaribag - JH206": "//ul[@id='selectedRto_items']/li[22]",
        "M/s Universal Automated Fitness Centre, East Singhbhum - JH204": "//ul[@id='selectedRto_items']/li[23]",
        "PAKUR - JH16": "//ul[@id='selectedRto_items']/li[24]",
        "PALAMU - JH3": "//ul[@id='selectedRto_items']/li[25]",
        "RAMGARH - JH24": "//ul[@id='selectedRto_items']/li[26]",
        "RANCHI - JH1": "//ul[@id='selectedRto_items']/li[27]",
        "SAHEBGANJ - JH18": "//ul[@id='selectedRto_items']/li[28]",
        "SARAIKELA-KHARSAWAN - JH22": "//ul[@id='selectedRto_items']/li[29]",
        "SIMDEGA - JH20": "//ul[@id='selectedRto_items']/li[30]",
        "STATE TRANSPORT AUTHORITY - JH99": "//ul[@id='selectedRto_items']/li[31]",
        "WEST SINGHBHUM (CHAIBASA) - JH6": "//ul[@id='selectedRto_items']/li[32]"
    }
    # Add RTOs for other states here
}


# VEHICLE CLASSES configuration
VEHICLE_CLASSES_CONFIG = {
    "E2W": ["TWO_WHEELER_NT", "TWO_WHEELER_T"],
    "L3G": ["THREE_WHEELER_NT", "THREE_WHEELER_T"],
    "L3P": ["THREE_WHEELER_NT", "THREE_WHEELER_T"],
    "L5G": ["THREE_WHEELER_NT", "THREE_WHEELER_T"],
    "L5P": ["THREE_WHEELER_NT", "THREE_WHEELER_T"]
}

# ================== USER CONFIGURATION ==================
# Configure what you want to scrape here
STATES_TO_SCRAPE = ["Chhattisgarh"]  # Add more states as needed
YEARS_TO_SCRAPE = ["2025"]
PRODUCTS_TO_SCRAPE = ["L3P"]  # Can include "E2W", "L3G", "L3P", "L5G", "L5P"
# RTO_TO_SCRAPE = [ "ABU ROAD DTO - RJ38",
#         "Adinath Fitness Center - RJ260",
#         "Agarwal Fitness Center - RJ225",
#         "AJMER RTO - RJ1",
#         "A&L Company - RJ267",
#         "Alwar Auto Mobile Fitness Center - RJ243",
#         "Alwar Fitness Center - RJ254",
#         "ALWAR RTO - RJ2",
#         "ARAVALI FITNESS TESTING CENTER - RJ218",
#         "Arihant Vehicle Fitness Center - RJ257",
#         "Atharva Enterprises - RJ261",
#         "BALAJI ALLIANCE - RJ280",
#         "BALAJI FITNESS CENTER (BHILWARA) - RJ210",
#         "BALAJI FITNESS CENTER (HANUMANGARH) - RJ209",
#         "BALOTRA DTO - RJ39",
#         "BANSWARA DTO - RJ3",
#         "BANSWARA VEHICLE FITNESS CENTER - RJ276",
#         "BARAN DTO - RJ28",
#         "BARMER DTO - RJ4",
#         "BEAWAR DTO - RJ36",
#         "BHARATPUR RTO - RJ5",
#         "Bharat Vahan Fitness Center - RJ250",
#         "BHILWARA DTO - RJ6",
#         "BHINMAL DTO - RJ46",
#         "BHIWARI DTO - RJ40",
#         "BIKANER RTO - RJ7",
#         "BUNDI DTO - RJ8",
#         "CHITTORGARH RTO - RJ9",
#         "CHOMU DTO - RJ41",
#         "CHURU DTO - RJ10",
#         "DAUSA RTO - RJ29",
#         "DHOLPUR DTO - RJ11",
#         "DIDWANA DTO - RJ37",
#         "DUDU DTO - RJ47",
#         "DUDU FITNESS CENTER - RJ281",
#         "DUNGARPUR DTO - RJ12",
#         "EXPLORE IT SERVICES PVT. LTD. - RJ228",
#         "FREEDOM MOTORS - RJ224",
#         "Ganesh Ji Fitness Center - RJ226",
#         "G.Y. Fitness Center - RJ223",
#         "HANUMANGARH DTO - RJ31",
#         "Hindustan Automobiles - RJ251",
#         "Indira Vehicle Fitness Centre - RJ269",
#         "INFINITY FITNESS CENTER - RJ231",
#         "JAGATPURA, JAIPUR ARTO - RJ141",
#         "Jai Bhawani Fitness Center - RJ236",
#         "JAIPUR (FIRST) RTO - RJ14",
#         "JAIPUR (SECOND) RTO - RJ59",
#         "Jaipur Vehicle Fitness and Maintenance Center - RJ234",
#         "JAISALMER DTO - RJ15",
#         "JALORE DTO - RJ16",
#         "JALORE FITNESS CENTRE - RJ282",
#         "JHALAWAR DTO - RJ17",
#         "JHUNJHUNU DTO - RJ18",
#         "Jodhpur Parivahan Fitness Centre - RJ242",
#         "JODHPUR RTO - RJ19",
#         "KAROLI DTO - RJ34",
#         "KEKRI DTO - RJ48",
#         "KHETRI DTO - RJ53",
#         "KISHANGARH DTO - RJ42",
#         "KOTA RTO - RJ20",
#         "Kota Vehicle Fitness Center - RJ263",
#         "KOTPUTALI DTO - RJ32",
#         "Laxmi Parivahan Fitness Center - RJ266",
#         "Mahadev Fitness Center - RJ233",
#         "MAHADEV FITNESS CENTER BHILWARA - RJ274",
#         "MAHADEV FITNESS CENTER JODHPUR - RJ273",
#         "MAHAVEER JAIN FITNESS CENTRE - RJ229",
#         "MAHAVEER PRASAD RAM KISHAN - RJ232",
#         "Marudhara Transport Company - RJ271",
#         "Marwar Fitness Center - RJ249",
#         "Matsya Fitness Center - RJ220",
#         "M & D Automobile Fitness Center - RJ222",
#         "Meel Motors - RJ230",
#         "Meera Fitness Center - RJ247",
#         "MEERA FITNESS TESTING CENTER CHITTORGARH - RJ215",
#         "M.K. Fitness Center - RJ239",
#         "M/S Dholpur Fitness Center - RJ201",
#         "M/S Jagdamba Fitness Center - RJ203",
#         "M/S Nandan Fitness Testing Center - RJ204",
#         "M/S OM Fitness & Service Center - RJ202",
#         "Naganaray Fitness Center - RJ255",
#         "NAGAUR DTO - RJ21",
#         "Navdeep Fitness Test Center - RJ248",
#         "Navdurga Vahan Fitness Center - RJ245",
#         "Navkar Shri Fitness Testing Center - RJ216",
#         "NOHAR DTO - RJ49",
#         "NOKHA DTO - RJ50",
#         "Nokha Vehicle Fitness Center - RJ253",
#         "PALI RTO - RJ22",
#         "Parasvnath Fitness Center - RJ240",
#         "PAWAN VEHICLE FITNESS CENTER PVT LTD - RJ277",
#         "PHALODI DTO - RJ43",
#         "PIPAR CITY DTO - RJ54",
#         "POKHRAN DTO - RJ55",
#         "PRATAPGARH DTO - RJ35",
#         "Preksha Parivahan Fitness Center - RJ265",
#         "Prerna Parivahan Fitness Center - RJ272",
#         "RAJASTHAN VEHICLE FITNESS CENTER - RJ283",
#         "RAJSAMAND DTO - RJ30",
#         "RAMGANJMANDI DTO - RJ33",
#         "R.K. Fitness Center - RJ221",
#         "Royal Motors - RJ268",
#         "SADULSHAHAR DTO - RJ56",
#         "SAHAPURA (BHILWARA) DTO - RJ51",
#         "SAHAPURA (JAIPUR) DTO - RJ52",
#         "SALUMBAR DTO - RJ58",
#         "SAWAI MADHOPUR DTO - RJ25",
#         "Schoolnet India Limited - RJ256",
#         "SHAHPURA BHILWARA FITNESS CENTER - RJ275",
#         "SHAHPURA VEHICLE FITNESS CENTER (JAIPUR) - RJ213",
#         "Shanti Vehicle Fitness Testing Center - RJ208",
#         "Shashank Automobiles - RJ227",
#         "SHIV KRIPA FITNESS CENTER PVT LTD - RJ279",
#         "SHREE BALAJI FITNESS CENTER PALI - RJ241",
#         "Shree Fitness Center - RJ211",
#         "Shree Kamdhenu Fitness Center - RJ219",
#         "SHREE SHYAM VEHICLE FITNESS CENTER - RJ246",
#         "SHRI BALAJI FITNESS CENTER BIKANER - RJ206",
#         "Shri Bikaner Fitness Center - RJ205",
#         "Shri Fitness Center - RJ259",
#         "Shri Force Fitness Center - RJ217",
#         "Shri Karni Fitness Center - RJ214",
#         "SHRI MAHALAXMI FITNESS CENTER - RJ278",
#         "Shri Vinayak Auto Fitness Center - RJ252",
#         "SIKAR RTO - RJ23",
#         "Sikar Vehicle Fitness Center - RJ212",
#         "SIROHI DTO - RJ24",
#         "Speedline Auto Fitness Private Limited - RJ270",
#         "SRI GANGANAGAR DTO - RJ13",
#         "SUJANGARH DTO - RJ44",
#         "SUMERPUR DTO - RJ57",
#         "Swarna Shri Fitness Testing Center - RJ207",
#         "TIRUPATI ASSOCIATES - RJ238",
#         "TIRUPATI ASSOCIATES MORIJA CHOMU - RJ237",
#         "TIRUPATI FITNESS CENTER - RJ235",
#         "TONK DTO - RJ26",
#         "Tonk Fitness Center - RJ244",
#         "Udaipur Fitness Center - RJ262",
#         "UDAIPUR RTO - RJ27",
#         "Vaahan Fitness Center - RJ264",
#         "VATSAL ENTERPRISES - RJ258"]  # RTOs to scrape for each state
RTO_TO_SCRAPE = [
    "AIG(F/P) PHQ - CG3",
    "Ambikapur RTO - CG15",
    "BAIKUNTHPUR DTO - CG16",
    "Baloda Bazar DTO - CG22",
    "Balod DTO - CG24",
    "Balrampur DTO - CG30",
    "Bemetara DTO - CG25",
    "Bijapur DTO - CG20",
    "Bilaspur RTO - CG10",
    "Dantewada DTO - CG18",
    "Dhamtari DTO - CG5",
    "DURG RTO - CG7",
    "Gariyaband DTO - CG23",
    "Gaurela-Pendra-Marwahi DTO - CG31",
    "JAGDALPUR RTO - CG17",
    "Janjgir Champa DTO - CG11",
    "Jashpur DTO - CG14",
    "KANKER DTO - CG19",
    "KAWARDHA DTO - CG9",
    "KONDAGAON DTO - CG27",
    "Korba DTO - CG12",
    "Mahasamund DTO - CG6",
    "Mungeli DTO - CG28",
    "Narayanpur DTO - CG21",
    "Raigarh DTO - CG13",
    "Raipur RTO - CG4",
    "Rajnandgaon ARTO - CG8",
    "RTA TC NAWA RAIPUR - CG998",
    "State Transport Authority - CG99",
    "Sukma DTO - CG26",
    "Surajpur DTO - CG29"
]

# RTO_TO_SCRAPE = [
#     "Authorised Testing Centre (TUV SUD), Ranchi - JH201",
#         "Authorized Fitness Centre(VAHAN),Dhanbad - JH202",
#         "BOKARO - JH9",
#         "CHATRA - JH13",
#         "DEOGHAR - JH15",
#         "DHANBAD - JH10",
#         "DTO OFFICE DUMKA - JH4",
#         "EAST SINGHBHUM (JAMSHEDPUR) - JH5",
#         "GARHWA - JH14",
#         "GIRIDIH - JH11",
#         "GODDA - JH17",
#         "GUMLA - JH7",
#         "HAZARIBAG - JH2",
#         "JAMTARA - JH21",
#         "KHUNTI - JH23",
#         "KODERMA - JH12",
#         "LATEHAR - JH19",
#         "LOHARDAGA - JH8",
#         "M/s Auto Fitness Centre,Ranchi - JH203",
#         "M/s Auto Tech Vehicle Fitness,Ranchi - JH205",
#         "M/S Global Automated Fitness,Hazaribag - JH206",
#         "M/s Universal Automated Fitness Centre, East Singhbhum - JH204",
#         "PAKUR - JH16",
#         "PALAMU - JH3",
#         "RAMGARH - JH24",
#         "RANCHI - JH1",
#         "SAHEBGANJ - JH18",
#         "SARAIKELA-KHARSAWAN - JH22",
#         "SIMDEGA - JH20",
#         "STATE TRANSPORT AUTHORITY - JH99",
#         "WEST SINGHBHUM (CHAIBASA) - JH6"
# ]
# RTO_TO_SCRAPE = [
#     "AKLUJ - MH45",
#     "AMBEJOGAI - MH44",
#     "AMRAWATI - MH27",
#     "BARAMATI - MH42",
#     "BEED - MH23",
#     "BHADGAON - MH54",
#     "BHANDARA - MH36",
#     "BULDHANA - MH28",
#     "CHALISGAON - MH52",
#     "CHHATRAPATI SAMBHAJINAGAR - MH20",
#     "Chiplun Chiplun Track - MH202",
#     "DHARASHIV - MH25",
#     "DHULE - MH18",
#     "DY REGIONAL TRANSPORT OFFICE, HINGOLI - MH38",
#     "DY RTO RATNAGIRI - MH8",
#     "GADCHIROLI - MH33",
#     "GONDHIA - MH35",
#     "ICHALKARANJI - MH51",
#     "JALANA - MH21",
#     "KALYAN - MH5",
#     "KARAD - MH50",
#     "KHAMGAON - MH56",
#     "KOLHAPUR - MH9",
#     "MALEGAON - MH41",
#     "MIRA BHAYANDAR - MH58",
#     "MUMBAI (CENTRAL) - MH1",
#     "MUMBAI (EAST) - MH3",
#     "MUMBAI (WEST) - MH2",
#     "NAGPUR (EAST) - MH49",
#     "NAGPUR (RURAL) - MH40",
#     "NAGPUR (U) - MH31",
#     "NANDED - MH26",
#     "NANDURBAR - MH39",
#     "NASHIK - MH15",
#     "PANVEL - MH46",
#     "PARBHANI - MH22",
#     "PEN (RAIGAD) - MH6",
#     "PHALTAN - MH53",
#     "PUNE - MH12",
#     "RTO AHEMEDNAGAR - MH16",
#     "RTO AKOLA - MH30",
#     "R.T.O.BORIVALI - MH47",
#     "RTO CHANDRAPUR - MH34",
#     "RTO JALGAON - MH19",
#     "RTO LATUR - MH24",
#     "RTO MH04-Mira Bhayander FitnessTrack - MH203",
#     "RTO PIMPRI CHINCHWAD - MH14",
#     "RTO SATARA - MH11",
#     "RTO SOLAPUR - MH13",
#     "SANGLI - MH10",
#     "SINDHUDURG(KUDAL) - MH7",
#     "SRIRAMPUR - MH17",
#     "TC OFFICE - MH99",
#     "THANE - MH4",
#     "UDGIR - MH55",
#     "VASAI - MH48",
#     "VASHI (NEW MUMBAI) - MH43",
#     "WARDHA - MH32",
#     "WASHIM - MH37",
#     "YAWATMAL - MH29"
# ]


# Other configurations
Y_AXIS = "//*[@id='yaxisVar_4']"
X_AXIS = "//*[@id='xaxisVar_7']"
HEADLESS_MODE = True
DOWNLOAD_CSV = True

class VahanScraper:
    def __init__(self, headless=True, test_mode=False):
        """Initialize the scraper with Chrome driver or in test mode"""
        self.driver = None
        self.wait = None
        self.test_mode = test_mode
        
        # Set up downloads directory in the same folder as the script
        script_dir = Path(__file__).parent.absolute()
        self.download_dir = str(script_dir / "downloads")
        # Create downloads directory if it doesn't exist
        os.makedirs(self.download_dir, exist_ok=True)
        print(f"📁 Using download directory: {self.download_dir}")
        
        if not self.test_mode:
            self.setup_driver(headless)
        
    def setup_driver(self, headless=True):
        """Setup Chrome driver with options"""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Set download directory
        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)
        
    def navigate_to_site(self):
        """Navigate to the Vahan dashboard"""
        url = "https://vahan.parivahan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml"
        if self.test_mode:
            print(f"[TEST MODE] Would navigate to: {url}")
            return
        print(f"Navigating to: {url}")
        self.driver.get(url)
        time.sleep(3)
        
    def click_element(self, xpath, description, max_retries=10, wait_between=2):
        """Click an element with error handling and retries until success or max_retries"""
        if self.test_mode:
            print(f"[TEST MODE] Would click: {description} ({xpath})")
            return True
        for attempt in range(1, max_retries + 1):
            try:
                element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)
                element.click()
                print(f"✓ Clicked: {description} (attempt {attempt})")
                time.sleep(1)
                return True
            except Exception as e:
                print(f"✗ Attempt {attempt}: Failed to click: {description} ({e})")
                time.sleep(wait_between)
        print(f"✗ All {max_retries} attempts failed to click: {description}")
        return False
    
    def select_dropdown_option(self, dropdown_xpath, option_xpath, description, max_retries=3):
        """Select an option from dropdown with retries and logging"""
        for attempt in range(max_retries):
            if self.test_mode:
                print(f"[TEST MODE] Would select {description}: {dropdown_xpath} -> {option_xpath}")
                return True
            try:
                if self.click_element(dropdown_xpath, f"{description} dropdown"):
                    time.sleep(1)
                    if self.click_element(option_xpath, f"{description} option"):
                        return True
            except Exception as e:
                print(f"✗ Attempt {attempt + 1}: Failed to select {description} ({e})")
            if attempt < max_retries - 1:
                time.sleep(2)
        print(f"✗ All attempts failed to select: {description}")
        return False
    
    def select_state(self, state_xpath):
        """Select state from dropdown"""
        return self.select_dropdown_option(
            "/html/body/form/div[2]/div/div/div[1]/div[2]/div[3]/div/div[3]/span",
            state_xpath,
            "State"
        )

    def select_rto(self, rto_xpath):
        """Select RTO from dropdown"""
        return self.select_dropdown_option(
            "//*[@id='selectedRto']/div[3]/span",
            rto_xpath,
            "RTO"
        )
    
    def select_y_axis(self, y_axis_xpath="//*[@id='yaxisVar_4']"):
        """Select Y-axis variable"""
        return self.select_dropdown_option(
            "//*[@id='yaxisVar']/div[3]/span",
            y_axis_xpath,
            "Y-axis"
        )
    
    def select_x_axis(self, x_axis_xpath="//*[@id='xaxisVar_7']"):
        """Select X-axis variable"""
        return self.select_dropdown_option(
            "//*[@id='xaxisVar']/div[3]/span",
            x_axis_xpath,
            "X-axis"
        )
    
    def select_year(self, year_xpath="//*[@id='selectedYear_1']"):
        """Select year from dropdown"""
        return self.select_dropdown_option(
            "//*[@id='selectedYear']/div[3]/span",
            year_xpath,
            "Year"
        )
    
    def refresh_data(self):
        """Click refresh button (first reference)"""
        return self.click_element('/html/body/form/div[2]/div/div/div[1]/div[3]/div[3]/div/button', "Refresh")
    
    def expand_filter_panel(self):
        """Click expand button to open filter panel"""
        return self.click_element("//*[@id='filterLayout-toggler']/span/a/span", "Expand filter panel")
    
    def select_checkbox(self, checkbox_xpath, label_xpath, description):
        """Select a checkbox with verification"""
        if self.test_mode:
            print(f"[TEST MODE] Would select checkbox: {description}")
            return True
            
        try:
            # First try to check if checkbox is already selected
            checkbox = self.wait.until(EC.presence_of_element_located((By.XPATH, checkbox_xpath)))
            
            # Check if already selected by looking for 'ui-state-active' class or similar
            is_selected = "ui-state-active" in checkbox.get_attribute("class") if checkbox.get_attribute("class") else False
            
            if not is_selected:
                # Scroll to element
                self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
                time.sleep(0.5)
                
                # Try clicking the checkbox
                if not self.click_element(checkbox_xpath, f"{description} checkbox"):
                    # If checkbox click fails, try clicking the label
                    print(f"Trying label click for: {description}")
                    self.click_element(label_xpath, f"{description} label")
                
                # Wait a bit for the selection to take effect
                time.sleep(1)
                
                # Try to verify selection, but don't fail if we can't verify
                try:
                    checkbox = self.driver.find_element(By.XPATH, checkbox_xpath)
                    is_now_selected = "ui-state-active" in checkbox.get_attribute("class") if checkbox.get_attribute("class") else False
                    
                    if is_now_selected:
                        print(f"✓ Successfully selected: {description}")
                    else:
                        # Even if we can't verify the selection, assume it worked if we didn't get an error
                        print(f"✓ Clicked {description} (verification skipped)")
                except:
                    # If we can't verify, assume it worked if we didn't get an error
                    print(f"✓ Clicked {description} (verification skipped)")
                
                return True
            else:
                print(f"✓ Already selected: {description}")
                return True
                
        except Exception as e:
            print(f"✗ Error selecting {description}: {e}")
            return False
    
    def select_vehicle_categories(self, categories):
        """Select vehicle categories based on list"""
        vehicle_options = {
            'TWO_WHEELER_NT': {
                'label': "//*[@id='VhCatg']/tbody/tr[2]/td/label",
                'checkbox': "//*[@id='VhCatg']/tbody/tr[2]/td/div/div[2]/span"
            },
            'TWO_WHEELER_T': {
                'label': "//*[@id='VhCatg']/tbody/tr[3]/td/label", 
                'checkbox': "//*[@id='VhCatg']/tbody/tr[3]/td/div/div[2]/span"
            },
            'THREE_WHEELER_NT': {
                'label': "//*[@id='VhCatg']/tbody/tr[5]/td/label",
                'checkbox': "//*[@id='VhCatg']/tbody/tr[5]/td/div/div[2]/span"
            },
            'THREE_WHEELER_T': {
                'label': "//*[@id='VhCatg']/tbody/tr[6]/td/label",
                'checkbox': "//*[@id='VhCatg']/tbody/tr[6]/td/div/div[2]/span"
            }
        }
        
        print(f"Selecting vehicle categories: {categories}")
        for category in categories:
            if category in vehicle_options:
                self.select_checkbox(
                    vehicle_options[category]['checkbox'],
                    vehicle_options[category]['label'],
                    f"Vehicle category: {category}"
                )
                time.sleep(1)  # Wait between selections
    
    def select_fuel_electric(self):
        """Select ELECTRIC(BOV) fuel option"""
        return self.select_checkbox(
            "//*[@id='fuel']/tbody/tr[8]/td/div/div[2]/span",
            "//*[@id='fuel']/tbody/tr[8]/td/label",
            "ELECTRIC(BOV) fuel"
        )
    
    def refresh_filters(self):
        """Click second refresh button after filters"""
        return self.click_element("/html/body/form/div[2]/div/div/div[3]/div/div[1]/div[1]/span/button", "Refresh filters")
    
    def select_vehicle_classes(self, classes):
        """Select vehicle classes for E3W"""
        class_options = {
            # L-3G and L-3P (E-Rickshaw types)
            'E_RICKSHAW_CART_G': {
                'label': "//*[@id='VhClass']/tbody/tr[37]/td/label",
                'checkbox': "//*[@id='VhClass']/tbody/tr[37]/td/div/div[2]/span",
                'description': "L-3G = E-Rickshaw With Cart (G)"
            },
            'E_RICKSHAW_P': {
                'label': "//*[@id='VhClass']/tbody/tr[38]/td/label",
                'checkbox': "//*[@id='VhClass']/tbody/tr[38]/td/div/div[2]/span",
                'description': "L-3P = E-Rickshaw (P)"
            },
            # L-5P and L-5G (Three Wheeler types)
            'THREE_WHEELER_PASSENGER': {
                'label': "//*[@id='VhClass']/tbody/tr[40]/td/label",
                'checkbox': "//*[@id='VhClass']/tbody/tr[40]/td/div/div[2]/span",
                'description': "L-5P = THREE WHEELER (PASSENGER)"
            },
            'THREE_WHEELER_GOODS': {
                'label': "//*[@id='VhClass']/tbody/tr[41]/td/label",
                'checkbox': "//*[@id='VhClass']/tbody/tr[41]/td/div/div[2]/span",
                'description': "L-5G = THREE WHEELER (GOODS)"
            }
        }
        
        print(f"Selecting vehicle classes: {classes}")
        for class_type in classes:
            if class_type in class_options:
                option = class_options[class_type] 
                print(f"Selecting: {option['description']}")
                self.select_checkbox(
                    option['checkbox'],
                    option['label'],
                    f"Vehicle class: {class_type} ({option['description']})"
                )
                time.sleep(1)  # Wait between selections
    
    def rename_downloaded_file(self, state_name, rto_name, year_name, product_type):
        """Rename the downloaded file based on category"""
        try:
            # Wait for the file to be downloaded
            time.sleep(3)  # Give some time for the download to start
            
            # Look for the most recently downloaded file
            downloaded_files = [f for f in os.listdir(self.download_dir) if f.endswith('.xlsx')]
            if not downloaded_files:
                print("❌ No downloaded files found")
                return False
                
            # Get the most recent file
            latest_file = max([os.path.join(self.download_dir, f) for f in downloaded_files], key=os.path.getctime)
            
            # Create new filename
            new_filename = f"{state_name}_{rto_name}_{year_name}_{product_type}.xlsx"
            new_filepath = os.path.join(self.download_dir, new_filename)
            
            # Rename the file
            os.rename(latest_file, new_filepath)
            print(f"✓ File renamed to: {new_filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error renaming file: {e}")
            return False

    def download_csv(self, state_name, rto_name, year_name, product_type, max_attempts=5):
        """Download CSV data with multiple attempts and rename the file"""
        download_xpath = '/html/body/form/div[2]/div/div/div[3]/div/div[2]/div/div/div[1]/div[1]/a/img'
        for attempt in range(1, max_attempts + 1):
            try:
                print(f"Download attempt {attempt}...")
                download_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, download_xpath)))
                self.driver.execute_script("arguments[0].scrollIntoView(true);", download_btn)
                time.sleep(1)
                download_btn.click()
                print(f"✓ Download button clicked (attempt {attempt})")
                time.sleep(3)
                
                # Rename the downloaded file
                if self.rename_downloaded_file(state_name, rto_name, year_name, product_type):
                    print("✓ Download and rename completed successfully")
                    return True
                else:
                    print("✗ Download succeeded but rename failed")
                    return False
                    
            except TimeoutException:
                print(f"✗ Download attempt {attempt} failed: Download button not found")
            except Exception as e:
                print(f"✗ Download attempt {attempt} failed: {e}")
            if attempt < max_attempts:
                print("Retrying download...")
                time.sleep(2)
        print("✗ All download attempts failed")
        return False
    
    def scrape_single_product(self, state_name, state_xpath, rto_name, rto_xpath, year_name, year_xpath, product_type):
        """Scrape data for a single product type"""
        try:
            print(f"\n{'='*80}")
            print(f"SCRAPING: State={state_name}, RTO={rto_name}, Year={year_name}, Product={product_type}")
            print(f"{'='*80}")
            
            # Navigate to site
            self.navigate_to_site()
            
            # Select basic options
            print("🔄 Selecting basic options...")
            self.select_state(state_xpath)
            self.select_rto(rto_xpath)
            self.select_y_axis(Y_AXIS)
            self.select_x_axis(X_AXIS)
            self.select_year(year_xpath)
            
            # First refresh
            print("🔄 Initial refresh...")
            self.refresh_data()
            time.sleep(3)
            
            # Expand filter panel
            print("🔄 Expanding filter panel...")
            self.expand_filter_panel()
            time.sleep(2)
            
            # Select vehicle categories based on product type
            print(f"🔄 Selecting vehicle categories for {product_type}...")
            vehicle_categories = VEHICLE_CLASSES_CONFIG.get(product_type, [])
            self.select_vehicle_categories(vehicle_categories)
            
            # Select fuel type (electric)
            print("🔄 Selecting ELECTRIC fuel type...")
            self.select_fuel_electric()
            
            # Select specific vehicle classes based on product type
            if product_type == "L3G":
                print("🔄 Selecting L-3G vehicle class...")
                self.select_vehicle_classes(['E_RICKSHAW_CART_G'])
            elif product_type == "L3P":
                print("🔄 Selecting L-3P vehicle class...")
                self.select_vehicle_classes(['E_RICKSHAW_P'])
            elif product_type == "L5G":
                print("🔄 Selecting L-5G vehicle class...")
                self.select_vehicle_classes(['THREE_WHEELER_GOODS'])
            elif product_type == "L5P":
                print("🔄 Selecting L-5P vehicle class...")
                self.select_vehicle_classes(['THREE_WHEELER_PASSENGER'])
            # E2W doesn't need specific vehicle class selection
            
            # Second refresh after filters
            print("🔄 Refreshing after filter selection...")
            self.refresh_filters()
            time.sleep(5)  # Wait for data to load
            
            # Download CSV
            if DOWNLOAD_CSV:
                print("📥 Downloading CSV...")
                success = self.download_csv(state_name, rto_name, year_name, product_type)
                if success:
                    print(f"✅ Successfully downloaded and renamed: {state_name}_{rto_name}_{year_name}_{product_type}")
                else:
                    print(f"❌ Failed to download: {state_name}_{rto_name}_{year_name}_{product_type}")
                    return False
            
            print(f"✅ {product_type} data extraction completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error during {product_type} scraping: {e}")
            return False
    
    def run_full_scraping_flow(self):
        """Run the complete scraping flow for all configurations"""
        total_tasks = len(STATES_TO_SCRAPE) * len(RTO_TO_SCRAPE) * len(YEARS_TO_SCRAPE) * len(PRODUCTS_TO_SCRAPE)
        completed_tasks = 0
        failed_tasks = []
        
        print(f"\n🚀 STARTING COMPLETE SCRAPING FLOW")
        print(f"Total tasks to complete: {total_tasks}")
        print(f"States: {STATES_TO_SCRAPE}")
        print(f"RTOs: {RTO_TO_SCRAPE}")
        print(f"Years: {YEARS_TO_SCRAPE}")
        print(f"Products: {PRODUCTS_TO_SCRAPE}")
        print(f"{'='*100}")
        
        try:
            # Loop through states
            for state_name in STATES_TO_SCRAPE:
                if state_name not in STATES_CONFIG:
                    print(f"❌ State '{state_name}' not found in STATES_CONFIG")
                    continue
                    
                state_xpath = STATES_CONFIG[state_name]
                
                # Loop through RTOs for this state
                for rto_name in RTO_TO_SCRAPE:
                    if state_name not in RTO_CONFIG or rto_name not in RTO_CONFIG[state_name]:
                        print(f"❌ RTO '{rto_name}' not found for state '{state_name}'")
                        continue
                        
                    rto_xpath = RTO_CONFIG[state_name][rto_name]
                    
                    # Loop through years
                    for year_name in YEARS_TO_SCRAPE:
                        if year_name not in YEARS_CONFIG:
                            print(f"❌ Year '{year_name}' not found in YEARS_CONFIG")
                            continue
                            
                        year_xpath = YEARS_CONFIG[year_name]
                        
                        # Loop through products
                        for product_type in PRODUCTS_TO_SCRAPE:
                            task_id = f"{state_name}_{rto_name}_{year_name}_{product_type}"
                            
                            print(f"\n📋 Task {completed_tasks + 1}/{total_tasks}: {task_id}")
                            
                            # Scrape this specific combination
                            success = self.scrape_single_product(
                                state_name, state_xpath,
                                rto_name, rto_xpath,
                                year_name, year_xpath,
                                product_type
                            )
                            
                            if success:
                                completed_tasks += 1
                                print(f"✅ Task completed: {task_id}")
                            else:
                                failed_tasks.append(task_id)
                                print(f"❌ Task failed: {task_id}")
                            
                            # Add delay between tasks to avoid being blocked
                            if product_type != PRODUCTS_TO_SCRAPE[-1] or year_name != YEARS_TO_SCRAPE[-1] or rto_name != RTO_TO_SCRAPE[-1] or state_name != STATES_TO_SCRAPE[-1]:
                                print("⏳ Waiting 5 seconds before next task...")
                                time.sleep(5)
        
        except KeyboardInterrupt:
            print("\n⚠️ Process interrupted by user")
        except Exception as e:
            print(f"\n❌ Unexpected error in scraping flow: {e}")
        
        # Final summary
        print(f"\n{'='*100}")
        print(f"🏁 SCRAPING FLOW COMPLETED")
        print(f"Total tasks: {total_tasks}")
        print(f"Completed successfully: {completed_tasks}")
        print(f"Failed tasks: {len(failed_tasks)}")
        
        if failed_tasks:
            print(f"\n❌ Failed tasks:")
            for task in failed_tasks:
                print(f"  - {task}")
        
        print(f"{'='*100}")
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("Browser closed")
        elif self.test_mode:
            print("[TEST MODE] Browser would be closed here.")


def main():
    """Main function to run the scraping flow"""
    print("🔧 VAHAN SCRAPER - FLOW CONTROL MODE")
    print(f"Configuration loaded:")
    print(f"  States: {STATES_TO_SCRAPE}")
    print(f"  RTOs: {RTO_TO_SCRAPE}")
    print(f"  Years: {YEARS_TO_SCRAPE}")
    print(f"  Products: {PRODUCTS_TO_SCRAPE}")
    print(f"  Headless: {HEADLESS_MODE}")
    print(f"  Download CSV: {DOWNLOAD_CSV}")
    
    # Initialize scraper
    scraper = VahanScraper(headless=HEADLESS_MODE)
    
    try:
        # Run the complete scraping flow
        scraper.run_full_scraping_flow()
        
    finally:
        scraper.close()


if __name__ == "__main__":
    main()
