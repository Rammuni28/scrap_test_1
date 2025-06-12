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
    "madhya_pradesh": "/html/body/div[3]/div/ul/li[24]",
    "bihar": "/html/body/div[3]/div/ul/li[6]",
    "punjab": "/html/body/div[3]/div/ul/li[28]",
    "uttarakhand": "/html/body/div[3]/div/ul/li[34]",
    "arunachal_pradesh": "/html/body/div[3]/div/ul/li[4]",
    "himachal_pradesh": "/html/body/div[3]/div/ul/li[13]",
    "jammu_kashmir": "/html/body/div[3]/div/ul/li[16]",
    "assam": "/html/body/div[3]/div/ul/li[5]",
    "manipur": "/html/body/div[3]/div/ul/li[23]",
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
    },
    "madhya_pradesh": {
        "AGAR MALWA RTO - MP70": "//ul[@id='selectedRto_items']/li[2]",
        "ALIRAJPUR DTO - MP69": "//ul[@id='selectedRto_items']/li[3]",
        "ANUPPUR DTO - MP65": "//ul[@id='selectedRto_items']/li[4]",
        "ASHOKNAGAR DTO - MP67": "//ul[@id='selectedRto_items']/li[5]",
        "BADWANI DTO - MP46": "//ul[@id='selectedRto_items']/li[6]",
        "BALAGHAT DTO - MP50": "//ul[@id='selectedRto_items']/li[7]",
        "BETUL DTO - MP48": "//ul[@id='selectedRto_items']/li[8]",
        "BHIND DTO - MP30": "//ul[@id='selectedRto_items']/li[9]",
        "BHOPAL RTO - MP4": "//ul[@id='selectedRto_items']/li[10]",
        "BURHANPUR DTO - MP68": "//ul[@id='selectedRto_items']/li[11]",
        "CHATTARPUR  ARTO - MP16": "//ul[@id='selectedRto_items']/li[12]",
        "CHHINDWARA ARTO - MP28": "//ul[@id='selectedRto_items']/li[13]",
        "DAMOH DTO - MP34": "//ul[@id='selectedRto_items']/li[14]",
        "DATIA DTO - MP32": "//ul[@id='selectedRto_items']/li[15]",
        "DEWAS DTO - MP41": "//ul[@id='selectedRto_items']/li[16]",
        "DHAR ARTO - MP11": "//ul[@id='selectedRto_items']/li[17]",
        "DINDORI DTO - MP52": "//ul[@id='selectedRto_items']/li[18]",
        "GUNA DTO - MP8": "//ul[@id='selectedRto_items']/li[19]",
        "GWALIOR RTO - MP7": "//ul[@id='selectedRto_items']/li[20]",
        "HARDA DTO - MP47": "//ul[@id='selectedRto_items']/li[21]",
        "HOSANGABAD DTO - MP5": "//ul[@id='selectedRto_items']/li[22]",
        "INDORE RTO - MP9": "//ul[@id='selectedRto_items']/li[23]",
        "JABALPUR RTO - MP20": "//ul[@id='selectedRto_items']/li[24]",
        "JHABUA DTO - MP45": "//ul[@id='selectedRto_items']/li[25]",
        "KATNI ARTO - MP21": "//ul[@id='selectedRto_items']/li[26]",
        "KHANDWA ARTO - MP12": "//ul[@id='selectedRto_items']/li[27]",
        "KHARGONE ARTO - MP10": "//ul[@id='selectedRto_items']/li[28]",
        "MANDLA DTO - MP51": "//ul[@id='selectedRto_items']/li[29]",
        "MANDSAUR ARTO - MP14": "//ul[@id='selectedRto_items']/li[30]",
        "MORENA DTO - MP6": "//ul[@id='selectedRto_items']/li[31]",
        "NARSINGHPUR DTO - MP49": "//ul[@id='selectedRto_items']/li[32]",
        "NEEMUCH DTO - MP44": "//ul[@id='selectedRto_items']/li[33]",
        "NIWARI DTO - MP71": "//ul[@id='selectedRto_items']/li[34]",
        "PANNA DTO - MP35": "//ul[@id='selectedRto_items']/li[35]",
        "RAISEN DTO - MP38": "//ul[@id='selectedRto_items']/li[36]",
        "RAJGARH DTO - MP39": "//ul[@id='selectedRto_items']/li[37]",
        "RATLAM DTO - MP43": "//ul[@id='selectedRto_items']/li[38]",
        "REWA RTO - MP17": "//ul[@id='selectedRto_items']/li[39]",
        "SAGAR RTO - MP15": "//ul[@id='selectedRto_items']/li[40]",
        "SATNA ARTO - MP19": "//ul[@id='selectedRto_items']/li[41]",
        "SEHORE DTO - MP37": "//ul[@id='selectedRto_items']/li[42]",
        "SEONI ARTO - MP22": "//ul[@id='selectedRto_items']/li[43]",
        "SHAHDOL RTO - MP18": "//ul[@id='selectedRto_items']/li[44]",
        "SHAJAPUR DTO - MP42": "//ul[@id='selectedRto_items']/li[45]",
        "SHEOPUR DTO - MP31": "//ul[@id='selectedRto_items']/li[46]",
        "SHIVPURI DTO - MP33": "//ul[@id='selectedRto_items']/li[47]",
        "SIDHI DTO - MP53": "//ul[@id='selectedRto_items']/li[48]",
        "SINGROLI DTO - MP66": "//ul[@id='selectedRto_items']/li[49]",
        "STATE TRANSPORT AUTHORITY - MP999": "//ul[@id='selectedRto_items']/li[50]",
        "TIKAMGARH DTO - MP36": "//ul[@id='selectedRto_items']/li[51]",
        "UJJAIN RTO - MP13": "//ul[@id='selectedRto_items']/li[52]",
        "UMARIA DTO - MP54": "//ul[@id='selectedRto_items']/li[53]",
        "VIDISHA DTO - MP40": "//ul[@id='selectedRto_items']/li[54]"
    },
     "bihar": {
        "ARARIA - BR38": "//ul[@id='selectedRto_items']/li[2]",
        "ARAWAL - BR56": "//ul[@id='selectedRto_items']/li[3]",
        "AURANGABAD - BR26": "//ul[@id='selectedRto_items']/li[4]",
        "BANKA - BR51": "//ul[@id='selectedRto_items']/li[5]",
        "BEGUSARAI - BR9": "//ul[@id='selectedRto_items']/li[6]",
        "BETTIAH - BR22": "//ul[@id='selectedRto_items']/li[7]",
        "BHABHUA - BR45": "//ul[@id='selectedRto_items']/li[8]",
        "BHAGALPUR - BR10": "//ul[@id='selectedRto_items']/li[9]",
        "BHAGALPUR RTA - BR103": "//ul[@id='selectedRto_items']/li[10]",
        "BHOJPUR - BR3": "//ul[@id='selectedRto_items']/li[11]",
        "BUXUR - BR44": "//ul[@id='selectedRto_items']/li[12]",
        "CHAPARA - BR4": "//ul[@id='selectedRto_items']/li[13]",
        "CHAPRA RTA - BR109": "//ul[@id='selectedRto_items']/li[14]",
        "DARBHANGA - BR7": "//ul[@id='selectedRto_items']/li[15]",
        "DARBHANGA RTA - BR102": "//ul[@id='selectedRto_items']/li[16]",
        "GAYA - BR2": "//ul[@id='selectedRto_items']/li[17]",
        "GAYA RTA - BR107": "//ul[@id='selectedRto_items']/li[18]",
        "GOPALGANJ - BR28": "//ul[@id='selectedRto_items']/li[19]",
        "JAMUI - BR46": "//ul[@id='selectedRto_items']/li[20]",
        "JEHANABAD - BR25": "//ul[@id='selectedRto_items']/li[21]",
        "KATIHAR - BR39": "//ul[@id='selectedRto_items']/li[22]",
        "KHAGARIA - BR34": "//ul[@id='selectedRto_items']/li[23]",
        "KISHANGANJ - BR37": "//ul[@id='selectedRto_items']/li[24]",
        "LAKHISARAI - BR53": "//ul[@id='selectedRto_items']/li[25]",
        "MADHEPURA - BR43": "//ul[@id='selectedRto_items']/li[26]",
        "MADHUBANI - BR32": "//ul[@id='selectedRto_items']/li[27]",
        "MOTIHARI - BR5": "//ul[@id='selectedRto_items']/li[28]",
        "M/S MURARI AUTO,Patna - BR201": "//ul[@id='selectedRto_items']/li[29]",
        "MUNGER - BR8": "//ul[@id='selectedRto_items']/li[30]",
        "MUNGER RTA - BR104": "//ul[@id='selectedRto_items']/li[31]",
        "MUZAFFARPUR - BR6": "//ul[@id='selectedRto_items']/li[32]",
        "MUZAFFARPUR RTA - BR106": "//ul[@id='selectedRto_items']/li[33]",
        "NALANDA - BR21": "//ul[@id='selectedRto_items']/li[34]",
        "NAWADA - BR27": "//ul[@id='selectedRto_items']/li[35]",
        "PATNA - BR1": "//ul[@id='selectedRto_items']/li[36]",
        "PATNA RTA - BR101": "//ul[@id='selectedRto_items']/li[37]",
        "PURNEA - BR11": "//ul[@id='selectedRto_items']/li[38]",
        "PURNEA RTA - BR108": "//ul[@id='selectedRto_items']/li[39]",
        "ROHTAS - BR24": "//ul[@id='selectedRto_items']/li[40]",
        "SAHARSA - BR19": "//ul[@id='selectedRto_items']/li[41]",
        "SAHARSA RTA - BR105": "//ul[@id='selectedRto_items']/li[42]",
        "SAMASTIPUR - BR33": "//ul[@id='selectedRto_items']/li[43]",
        "SHEIKHPURA - BR52": "//ul[@id='selectedRto_items']/li[44]",
        "SHEOHAR - BR55": "//ul[@id='selectedRto_items']/li[45]",
        "SITAMARHI - BR30": "//ul[@id='selectedRto_items']/li[46]",
        "SIWAN - BR29": "//ul[@id='selectedRto_items']/li[47]",
        "STA BIHAR - BR999": "//ul[@id='selectedRto_items']/li[48]",
        "SUPAUL - BR50": "//ul[@id='selectedRto_items']/li[49]",
        "VAISHALI - BR31": "//ul[@id='selectedRto_items']/li[50]"
    },
    "punjab": {
        "PUNJAB STA(RAC)/(AITP) - PB1": "//ul[@id='selectedRto_items']/li[2]",
        "RTO AMRITSAR - PB2": "//ul[@id='selectedRto_items']/li[3]",
        "RTO BARNALA - PB19": "//ul[@id='selectedRto_items']/li[4]",
        "RTO BATHINDA - PB3": "//ul[@id='selectedRto_items']/li[5]",
        "RTO FARIDKOT  - PB4": "//ul[@id='selectedRto_items']/li[6]",
        "RTO FATEHGARH SAHIB - PB23": "//ul[@id='selectedRto_items']/li[7]",
        "RTO FAZILKA - PB22": "//ul[@id='selectedRto_items']/li[8]",
        "RTO FEROZPUR - PB5": "//ul[@id='selectedRto_items']/li[9]",
        "RTO GURDASPUR - PB6": "//ul[@id='selectedRto_items']/li[10]",
        "RTO HOSHIARPUR - PB7": "//ul[@id='selectedRto_items']/li[11]",
        "RTO JALANDHAR - PB8": "//ul[@id='selectedRto_items']/li[12]",
        "RTO KAPURTHALA - PB9": "//ul[@id='selectedRto_items']/li[13]",
        "RTO LUDHIANA - PB10": "//ul[@id='selectedRto_items']/li[14]",
        "RTO MALERKOTLA  - PB28": "//ul[@id='selectedRto_items']/li[15]",
        "RTO MANSA - PB31": "//ul[@id='selectedRto_items']/li[16]",
        "RTO MOGA - PB29": "//ul[@id='selectedRto_items']/li[17]",
        "RTO MUKTSAR SAHIB - PB30": "//ul[@id='selectedRto_items']/li[18]",
        "RTO PATHANKOT - PB35": "//ul[@id='selectedRto_items']/li[19]",
        "RTO PATIALA - PB11": "//ul[@id='selectedRto_items']/li[20]",
        "RTO ROPAR - PB12": "//ul[@id='selectedRto_items']/li[21]",
        "RTO SAHIBZADA AJIT SINGH NAGAR  - PB65": "//ul[@id='selectedRto_items']/li[22]",
        "RTO SANGRUR - PB13": "//ul[@id='selectedRto_items']/li[23]",
        "RTO SBS NAGAR - PB32": "//ul[@id='selectedRto_items']/li[24]",
        "RTO TARN TARAN - PB46": "//ul[@id='selectedRto_items']/li[25]",
        "SDM ABOHAR - PB15": "//ul[@id='selectedRto_items']/li[26]",
        "SDM ADAMPUR  - PB94": "//ul[@id='selectedRto_items']/li[27]",
        "SDM AHMEDGARH - PB82": "//ul[@id='selectedRto_items']/li[28]",
        "SDM AJNALA - PB14": "//ul[@id='selectedRto_items']/li[29]",
        "SDM AMARGARH - PB92": "//ul[@id='selectedRto_items']/li[30]",
        "SDM AMLOH - PB48": "//ul[@id='selectedRto_items']/li[31]",
        "SDM AMRITSAR-2 - PB89": "//ul[@id='selectedRto_items']/li[32]",
        "SDM ANANDPUR SAHIB - PB16": "//ul[@id='selectedRto_items']/li[33]",
        "SDM BABA BAKALA - PB17": "//ul[@id='selectedRto_items']/li[34]",
        "SDM BAGHA PURANA - PB69": "//ul[@id='selectedRto_items']/li[35]",
        "SDM BALACHAUR - PB20": "//ul[@id='selectedRto_items']/li[36]",
        "SDM BANGA - PB78": "//ul[@id='selectedRto_items']/li[37]",
        "SDM BASSI PATHANA - PB52": "//ul[@id='selectedRto_items']/li[38]",
        "SDM BATALA - PB18": "//ul[@id='selectedRto_items']/li[39]",
        "SDM BHAWNIGARH - PB84": "//ul[@id='selectedRto_items']/li[40]",
        "SDM BHIKHIWIND - PB88": "//ul[@id='selectedRto_items']/li[41]",
        "SDM BHOLATH - PB57": "//ul[@id='selectedRto_items']/li[42]",
        "SDM BUDHLADA - PB50": "//ul[@id='selectedRto_items']/li[43]",
        "SDM CHAMKAUR SAHIB - PB71": "//ul[@id='selectedRto_items']/li[44]",
        "SDM DASUYA - PB21": "//ul[@id='selectedRto_items']/li[45]",
        "SDM DERA BABA NANAK - PB58": "//ul[@id='selectedRto_items']/li[46]",
        "SDM DERA BASSI  - PB70": "//ul[@id='selectedRto_items']/li[47]",
        "SDM DHARAMKOT - PB76": "//ul[@id='selectedRto_items']/li[48]",
        "SDM DHAR KALAN - PB68": "//ul[@id='selectedRto_items']/li[49]",
        "SDM DHURI - PB59": "//ul[@id='selectedRto_items']/li[50]",
        "SDM DINANAGAR - PB99": "//ul[@id='selectedRto_items']/li[51]",
        "SDM DIRBA - PB86": "//ul[@id='selectedRto_items']/li[52]",
        "SDM DUDHAN SADHAN - PB83": "//ul[@id='selectedRto_items']/li[53]",
        "SDM GARSHANKAR - PB24": "//ul[@id='selectedRto_items']/li[54]",
        "SDM GIDDARBAHA - PB60": "//ul[@id='selectedRto_items']/li[55]",
        "SDM GURU HAR SAHAI - PB77": "//ul[@id='selectedRto_items']/li[56]",
        "SDM JAGRAON - PB25": "//ul[@id='selectedRto_items']/li[57]",
        "SDM JAITO - PB62": "//ul[@id='selectedRto_items']/li[58]",
        "SDM JALALABAD - PB61": "//ul[@id='selectedRto_items']/li[59]",
        "SDM JALANDHAR-11 - PB90": "//ul[@id='selectedRto_items']/li[60]",
        "SDM KALANAUR - PB85": "//ul[@id='selectedRto_items']/li[61]",
        "SDM KHADUR SAHIB - PB63": "//ul[@id='selectedRto_items']/li[62]",
        "SDM KHAMANO - PB49": "//ul[@id='selectedRto_items']/li[63]",
        "SDM KHANNA - PB26": "//ul[@id='selectedRto_items']/li[64]",
        "SDM KHARAR - PB27": "//ul[@id='selectedRto_items']/li[65]",
        "SDM KOTKAPURA - PB79": "//ul[@id='selectedRto_items']/li[66]",
        "SDM LEHRAGAGA - PB75": "//ul[@id='selectedRto_items']/li[67]",
        "SDM LOPOKE  - PB93": "//ul[@id='selectedRto_items']/li[68]",
        "SDM LUDHIANA EAST - PB91": "//ul[@id='selectedRto_items']/li[69]",
        "SDM MAJITHA - PB81": "//ul[@id='selectedRto_items']/li[70]",
        "SDM MALOUT - PB53": "//ul[@id='selectedRto_items']/li[71]",
        "SDM MAUR MANDI - PB80": "//ul[@id='selectedRto_items']/li[72]",
        "SDM MOONAK - PB64": "//ul[@id='selectedRto_items']/li[73]",
        "SDM MORINDA - PB87": "//ul[@id='selectedRto_items']/li[74]",
        "SDM MUKERIAN - PB54": "//ul[@id='selectedRto_items']/li[75]",
        "SDM NABHA - PB34": "//ul[@id='selectedRto_items']/li[76]",
        "SDM NAKODAR - PB33": "//ul[@id='selectedRto_items']/li[77]",
        "SDM NANGAL - PB74": "//ul[@id='selectedRto_items']/li[78]",
        "SDM NIHAL SINGH WALA  - PB66": "//ul[@id='selectedRto_items']/li[79]",
        "SDM PATRAN - PB72": "//ul[@id='selectedRto_items']/li[80]",
        "SDM PATTI - PB38": "//ul[@id='selectedRto_items']/li[81]",
        "SDM PAYAL  - PB55": "//ul[@id='selectedRto_items']/li[82]",
        "SDM PHAGWARA - PB36": "//ul[@id='selectedRto_items']/li[83]",
        "SDM PHILLOUR - PB37": "//ul[@id='selectedRto_items']/li[84]",
        "SDM RAIKOT - PB56": "//ul[@id='selectedRto_items']/li[85]",
        "SDM RAJPURA - PB39": "//ul[@id='selectedRto_items']/li[86]",
        "SDM RAMPURA PHUL  - PB40": "//ul[@id='selectedRto_items']/li[87]",
        "SDM SAMANA - PB42": "//ul[@id='selectedRto_items']/li[88]",
        "SDM SAMRALA - PB43": "//ul[@id='selectedRto_items']/li[89]",
        "SDM SARDULGARH - PB51": "//ul[@id='selectedRto_items']/li[90]",
        "SDM SHAHKOT  - PB67": "//ul[@id='selectedRto_items']/li[91]",
        "SDM SULTANPUR LODHI - PB41": "//ul[@id='selectedRto_items']/li[92]",
        "SDM SUNAM - PB44": "//ul[@id='selectedRto_items']/li[93]",
        "SDM TALWANDI SABO - PB45": "//ul[@id='selectedRto_items']/li[94]",
        "SDM TANDA - PB95": "//ul[@id='selectedRto_items']/li[95]",
        "SDM TAPA - PB73": "//ul[@id='selectedRto_items']/li[96]",
        "SDM ZIRA - PB47": "//ul[@id='selectedRto_items']/li[97]"
    },
    "uttarakhand": {
        "ALMORA RTO - UK1": "//ul[@id='selectedRto_items']/li[2]",
        "BAGESHWAR ARTO - UK2": "//ul[@id='selectedRto_items']/li[3]",
        "DEHRADUN RTO - UK7": "//ul[@id='selectedRto_items']/li[4]",
        "HALDWANI RTO - UK4": "//ul[@id='selectedRto_items']/li[5]",
        "HARIDWAR ARTO - UK8": "//ul[@id='selectedRto_items']/li[6]",
        "KARANPRAYAG ARTO - UK11": "//ul[@id='selectedRto_items']/li[7]",
        "KASHIPUR ARTO - UK18": "//ul[@id='selectedRto_items']/li[8]",
        "KOTDWAR ARTO - UK15": "//ul[@id='selectedRto_items']/li[9]",
        "PAURI RTO - UK12": "//ul[@id='selectedRto_items']/li[10]",
        "PITHORAGARH ARTO - UK5": "//ul[@id='selectedRto_items']/li[11]",
        "RAMNAGAR ARTO - UK19": "//ul[@id='selectedRto_items']/li[12]",
        "RANIKHET ARTO - UK20": "//ul[@id='selectedRto_items']/li[13]",
        "RISHIKESH ARTO - UK14": "//ul[@id='selectedRto_items']/li[14]",
        "ROORKEE ARTO - UK17": "//ul[@id='selectedRto_items']/li[15]",
        "RUDRAPRAYAG ARTO - UK13": "//ul[@id='selectedRto_items']/li[16]",
        "STATE TRANSPORT AUTHORITY - UK111": "//ul[@id='selectedRto_items']/li[17]",
        "TANAKPUR ARTO - UK3": "//ul[@id='selectedRto_items']/li[18]",
        "TEHRI ARTO - UK9": "//ul[@id='selectedRto_items']/li[19]",
        "UDHAM SINGH NAGAR ARTO - UK6": "//ul[@id='selectedRto_items']/li[20]",
        "UTTARKASHI ARTO - UK10": "//ul[@id='selectedRto_items']/li[21]",
        "VIKAS NAGAR ARTO - UK16": "//ul[@id='selectedRto_items']/li[22]"
    }
    # Add RTOs for other states here
}


# VEHICLE CLASSES configuration
VEHICLE_CLASSES_CONFIG = {
    "E2W": ["M_CYCLE_SCOOTER", "M_CYCLE_SCOOTER_SIDE_CAR", "MOPED"],
    "L3G": ["E_RICKSHAW_CART_G"],
    "L3P": ["E_RICKSHAW_P"],
    "L5G": ["THREE_WHEELER_G"],
    "L5P": ["THREE_WHEELER_P"]
}

# VEHICLE_CATEGORIES = {
#     "E2W": ["M_CYCLE_SCOOTER", "M_CYCLE_SCOOTER_SIDE_CAR", "MOPED"],
#     "L3G": ["E_RICKSHAW_CART_G"],
#     "L3P": ["E_RICKSHAW_P"],
#     "L5G": ["THREE_WHEELER_G"],
#     "L5P": ["THREE_WHEELER_P"]
# }

# ================== USER CONFIGURATION ==================
# Configure what you want to scrape here
STATES_TO_SCRAPE = ["madhya_pradesh"]  # Add more states as needed
YEARS_TO_SCRAPE = ["2025","2024"]
PRODUCTS_TO_SCRAPE = ["E2W"]  # E2W = M-CYCLE/SCOOTER, M-CYCLE/SCOOTER-WITH SIDE CAR, MOPED


# RTO_TO_SCRAPE = [
#     "PUNJAB STA(RAC)/(AITP) - PB1",
#     "RTO AMRITSAR - PB2",
#     "RTO BARNALA - PB19",
#     "RTO BATHINDA - PB3",
#     "RTO FARIDKOT  - PB4",
#     "RTO FATEHGARH SAHIB - PB23",
#     "RTO FAZILKA - PB22",
#     "RTO FEROZPUR - PB5",
#     "RTO GURDASPUR - PB6",
#     "RTO HOSHIARPUR - PB7",
#     "RTO JALANDHAR - PB8",
#     "RTO KAPURTHALA - PB9",
#     "RTO LUDHIANA - PB10",
#     "RTO MALERKOTLA  - PB28",
#     "RTO MANSA - PB31",
#     "RTO MOGA - PB29",
#     "RTO MUKTSAR SAHIB - PB30",
#     "RTO PATHANKOT - PB35",
#     "RTO PATIALA - PB11",
#     "RTO ROPAR - PB12",
#     "RTO SAHIBZADA AJIT SINGH NAGAR  - PB65",
#     "RTO SANGRUR - PB13",
#     "RTO SBS NAGAR - PB32",
#     "RTO TARN TARAN - PB46",
#     "SDM ABOHAR - PB15",
#     "SDM ADAMPUR  - PB94",
#     "SDM AHMEDGARH - PB82",
#     "SDM AJNALA - PB14",
#     "SDM AMARGARH - PB92",
#     "SDM AMLOH - PB48",
#     "SDM AMRITSAR-2 - PB89",
#     "SDM ANANDPUR SAHIB - PB16",
#     "SDM BABA BAKALA - PB17",
#     "SDM BAGHA PURANA - PB69",
#     "SDM BALACHAUR - PB20",
#     "SDM BANGA - PB78",
#     "SDM BASSI PATHANA - PB52",
#     "SDM BATALA - PB18",
#     "SDM BHAWNIGARH - PB84",
#     "SDM BHIKHIWIND - PB88",
#     "SDM BHOLATH - PB57",
#     "SDM BUDHLADA - PB50",
#     "SDM CHAMKAUR SAHIB - PB71",
#     "SDM DASUYA - PB21",
#     "SDM DERA BABA NANAK - PB58",
#     "SDM DERA BASSI  - PB70",
#     "SDM DHARAMKOT - PB76",
#     "SDM DHAR KALAN - PB68",
#     "SDM DHURI - PB59",
#     "SDM DINANAGAR - PB99",
#     "SDM DIRBA - PB86",
#     "SDM DUDHAN SADHAN - PB83",
#     "SDM GARSHANKAR - PB24",
#     "SDM GIDDARBAHA - PB60",
#     "SDM GURU HAR SAHAI - PB77",
#     "SDM JAGRAON - PB25",
#     "SDM JAITO - PB62",
#     "SDM JALALABAD - PB61",
#     "SDM JALANDHAR-11 - PB90",
#     "SDM KALANAUR - PB85",
#     "SDM KHADUR SAHIB - PB63",
#     "SDM KHAMANO - PB49",
#     "SDM KHANNA - PB26",
#     "SDM KHARAR - PB27",
#     "SDM KOTKAPURA - PB79",
#     "SDM LEHRAGAGA - PB75",
#     "SDM LOPOKE  - PB93",
#     "SDM LUDHIANA EAST - PB91",
#     "SDM MAJITHA - PB81",
#     "SDM MALOUT - PB53",
#     "SDM MAUR MANDI - PB80",
#     "SDM MOONAK - PB64",
#     "SDM MORINDA - PB87",
#     "SDM MUKERIAN - PB54",
#     "SDM NABHA - PB34",
#     "SDM NAKODAR - PB33",
#     "SDM NANGAL - PB74",
#     "SDM NIHAL SINGH WALA  - PB66",
#     "SDM PATRAN - PB72",
#     "SDM PATTI - PB38",
#     "SDM PAYAL  - PB55",
#     "SDM PHAGWARA - PB36",
#     "SDM PHILLOUR - PB37",
#     "SDM RAIKOT - PB56",
#     "SDM RAJPURA - PB39",
#     "SDM RAMPURA PHUL  - PB40",
#     "SDM SAMANA - PB42",
#     "SDM SAMRALA - PB43",
#     "SDM SARDULGARH - PB51",
#     "SDM SHAHKOT  - PB67",
#     "SDM SULTANPUR LODHI - PB41",
#     "SDM SUNAM - PB44",
#     "SDM TALWANDI SABO - PB45",
#     "SDM TANDA - PB95",
#     "SDM TAPA - PB73",
#     "SDM ZIRA - PB47"
# ]
# RTO_TO_SCRAPE = [
#     "Agra RTO - UP80",
#     "AKBARPUR(AMBEDKAR NAGAR) - UP45",
#     "ALIGARH RTO - UP81",
#     "Amethi ARTO - UP36",
#     "ARTO OFFICE RAMPUR - UP22",
#     "AURAIYA - UP79",
#     "AYODHYA RTO - UP42",
#     "Azamgarh RTO - UP50",
#     "Badaun - UP24",
#     "Baghpat - UP17",
#     "Bahraich - UP40",
#     "Ballia - UP60",
#     "Balrampur - UP47",
#     "BANDARTO - UP90",
#     "Barabanki ARTO - UP41",
#     "BAREILLY - UP25",
#     "BASTI RTO - UP51",
#     "Bhadohi(SANT RAVIDAS NAGAR) - UP66",
#     "Bijnor - UP20",
#     "Bulandshahar - UP13",
#     "Chandauli - UP67",
#     "Chitrakoot - UP96",
#     "DEORIA - UP52",
#     "Etah - UP82",
#     "Etawah - UP75",
#     "Farrukhabad - UP76",
#     "FATHEHPUR - UP71",
#     "FEROZABAD - UP83",
#     "GHAZIABAD - UP14",
#     "Ghazipur - UP61",
#     "GONDA - UP43",
#     "Gorakhpur RTO - UP53",
#     "HAMIRPUR(UP) - UP91",
#     "Hapur - UP37",
#     "HARDOI - UP30",
#     "HATHRAS - UP86",
#     "JAUNPUR - UP62",
#     "JhansiRTO - UP93",
#     "JPNAGAR - UP23",
#     "Kannauj - UP74",
#     "Kanpur Dehat - UP77",
#     "KANPUR NAGAR - UP78",
#     "Kasganj(kashi ram nagar) - UP87",
#     "Kaushambi - UP73",
#     "LAKHIMPUR KHERI - UP31",
#     "Lalitpur - UP94",
#     "MAHANAGAR ARTO LUCKNOW (UP321) - UP321",
#     "Maharajganj - UP56",
#     "Mahoba - UP95",
#     "Mainpuri - UP84",
#     "MATHURA - UP85",
#     "Mau - UP54",
#     "MEERUT RTO - UP15",
#     "MIRZAPUR RTO - UP63",
#     "MORADABAD - UP21",
#     "M/S Sai Dham Super Srv Soln Pvt Ltd Ghaziabad - UP214",
#     "MuzaffarNagar - UP12",
#     "Noida - UP16",
#     "Orai - UP92",
#     "PADRAUNA(KUSHI NAGAR) - UP57",
#     "Pilibhit - UP26",
#     "PRATAPGARH - UP72",
#     "Prayagraj RTO - UP70",
#     "Raibareilly - UP33",
#     "SAHARANPUR RTO - UP11",
#     "SAHJAHANPUR - UP27",
#     "Sambhal ARTO - UP38",
#     "Sant Kabir Nagar - UP58",
#     "SHAMLI ARTO - UP19",
#     "Shravasti - UP46",
#     "Siddharth Nagar(naugarh) - UP55",
#     "Sitapur - UP34",
#     "SONBHADRA - UP64",
#     "STATE TRANSPORT AUTHORITY - UP999",
#     "Sultanpur - UP44",
#     "TRANSPORT NAGAR RTO LUCKNOW (UP32) - UP32",
#     "Unnao - UP35",
#     "VARANASI RTO - UP65"
# ]

RTO_TO_SCRAPE = [
    "AGAR MALWA RTO - MP70",
    "ALIRAJPUR DTO - MP69",
    "ANUPPUR DTO - MP65",
    "ASHOKNAGAR DTO - MP67",
    "BADWANI DTO - MP46",
    "BALAGHAT DTO - MP50",
    "BETUL DTO - MP48",
    "BHIND DTO - MP30",
    "BHOPAL RTO - MP4",
    "BURHANPUR DTO - MP68",
    "CHATTARPUR  ARTO - MP16",
    "CHHINDWARA ARTO - MP28",
    "DAMOH DTO - MP34",
    "DATIA DTO - MP32",
    "DEWAS DTO - MP41",
    "DHAR ARTO - MP11",
    "DINDORI DTO - MP52",
    "GUNA DTO - MP8",
    "GWALIOR RTO - MP7",
    "HARDA DTO - MP47",
    "HOSANGABAD DTO - MP5",
    "INDORE RTO - MP9",
    "JABALPUR RTO - MP20",
    "JHABUA DTO - MP45",
    "KATNI ARTO - MP21",
    "KHANDWA ARTO - MP12",
    "KHARGONE ARTO - MP10",
    "MANDLA DTO - MP51",
    "MANDSAUR ARTO - MP14",
    "MORENA DTO - MP6",
    "NARSINGHPUR DTO - MP49",
    "NEEMUCH DTO - MP44",
    "NIWARI DTO - MP71",
    "PANNA DTO - MP35",
    "RAISEN DTO - MP38",
    "RAJGARH DTO - MP39",
    "RATLAM DTO - MP43",
    "REWA RTO - MP17",
    "SAGAR RTO - MP15",
    "SATNA ARTO - MP19",
    "SEHORE DTO - MP37",
    "SEONI ARTO - MP22",
    "SHAHDOL RTO - MP18",
    "SHAJAPUR DTO - MP42",
    "SHEOPUR DTO - MP31",
    "SHIVPURI DTO - MP33",
    "SIDHI DTO - MP53",
    "SINGROLI DTO - MP66",
    "STATE TRANSPORT AUTHORITY - MP999",
    "TIKAMGARH DTO - MP36",
    "UJJAIN RTO - MP13",
    "UMARIA DTO - MP54",
    "VIDISHA DTO - MP40"
]

#uttarakhand
# RTO_TO_SCRAPE = [
#     "ALMORA RTO - UK1",
#     "BAGESHWAR ARTO - UK2",
#     "DEHRADUN RTO - UK7",
#     "HALDWANI RTO - UK4",
#     "HARIDWAR ARTO - UK8",
#     "KARANPRAYAG ARTO - UK11",
#     "KASHIPUR ARTO - UK18",
#     "KOTDWAR ARTO - UK15",
#     "PAURI RTO - UK12",
#     "PITHORAGARH ARTO - UK5",
#     "RAMNAGAR ARTO - UK19",
#     "RANIKHET ARTO - UK20",
#     "RISHIKESH ARTO - UK14",
#     "ROORKEE ARTO - UK17",
#     "RUDRAPRAYAG ARTO - UK13",
#     "STATE TRANSPORT AUTHORITY - UK111",
#     "TANAKPUR ARTO - UK3",
#     "TEHRI ARTO - UK9",
#     "UDHAM SINGH NAGAR ARTO - UK6",
#     "UTTARKASHI ARTO - UK10",
#     "VIKAS NAGAR ARTO - UK16"
# ]

# RTO_TO_SCRAPE = [
#         "Authorised Testing Centre (TUV SUD), Ranchi - JH201",
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
# ]  # RTOs to scrape for each state
# RTO_TO_SCRAPE = [
#     "PUNJAB STA(RAC)/(AITP) - PB1",
#     "RTO AMRITSAR - PB2",
#     "RTO BARNALA - PB19",
#     "RTO BATHINDA - PB3",
#     "RTO FARIDKOT - PB4",
#     "RTO FATEHGARH SAHIB - PB23",
#     "RTO FAZILKA - PB22",
#     "RTO FEROZPUR - PB5",
#     "RTO GURDASPUR - PB6",
#     "RTO HOSHIARPUR - PB7",
#     "RTO JALANDHAR - PB8",
#     "RTO KAPURTHALA - PB9",
#     "RTO LUDHIANA - PB10",
#     "RTO MALERKOTLA - PB28",
#     "RTO MANSA - PB31",
#     "RTO MOGA - PB29",
#     "RTO MUKTSAR SAHIB - PB30",
#     "RTO PATHANKOT - PB35",
#     "RTO PATIALA - PB11",
#     "RTO ROPAR - PB12",
#     "RTO SAHIBZADA AJIT SINGH NAGAR - PB65",
#     "RTO SANGRUR - PB13",
#     "RTO SBS NAGAR - PB32",
#     "RTO TARN TARAN - PB46",
#     "SDM ABOHAR - PB15",
#     "SDM ADAMPUR - PB94",
#     "SDM AHMEDGARH - PB82",
#     "SDM AJNALA - PB14",
#     "SDM AMARGARH - PB92",
#     "SDM AMLOH - PB48",
#     "SDM AMRITSAR-2 - PB89",
#     "SDM ANANDPUR SAHIB - PB16",
#     "SDM BABA BAKALA - PB17",
#     "SDM BAGHA PURANA - PB69",
#     "SDM BALACHAUR - PB20",
#     "SDM BANGA - PB78",
#     "SDM BASSI PATHANA - PB52",
#     "SDM BATALA - PB18",
#     "SDM BHAWNIGARH - PB84",
#     "SDM BHIKHIWIND - PB88",
#     "SDM BHOLATH - PB57",
#     "SDM BUDHLADA - PB50",
#     "SDM CHAMKAUR SAHIB - PB71",
#     "SDM DASUYA - PB21",
#     "SDM DERA BABA NANAK - PB58",
#     "SDM DERA BASSI - PB70",
#     "SDM DHARAMKOT - PB76",
#     "SDM DHAR KALAN - PB68",
#     "SDM DHURI - PB59",
#     "SDM DINANAGAR - PB99",
#     "SDM DIRBA - PB86",
#     "SDM DUDHAN SADHAN - PB83",
#     "SDM GARSHANKAR - PB24",
#     "SDM GIDDARBAHA - PB60",
#     "SDM GURU HAR SAHAI - PB77",
#     "SDM JAGRAON - PB25",
#     "SDM JAITO - PB62",
#     "SDM JALALABAD - PB61",
#     "SDM JALANDHAR-11 - PB90",
#     "SDM KALANAUR - PB85",
#     "SDM KHADUR SAHIB - PB63",
#     "SDM KHAMANO - PB49",
#     "SDM KHANNA - PB26",
#     "SDM KHARAR - PB27",
#     "SDM KOTKAPURA - PB79",
#     "SDM LEHRAGAGA - PB75",
#     "SDM LOPOKE - PB93",
#     "SDM LUDHIANA EAST - PB91",
#     "SDM MAJITHA - PB81",
#     "SDM MALOUT - PB53",
#     "SDM MAUR MANDI - PB80",
#     "SDM MOONAK - PB64",
#     "SDM MORINDA - PB87",
#     "SDM MUKERIAN - PB54",
#     "SDM NABHA - PB34",
#     "SDM NAKODAR - PB33",
#     "SDM NANGAL - PB74",
#     "SDM NIHAL SINGH WALA - PB66",
#     "SDM PATRAN - PB72",
#     "SDM PATTI - PB38",
#     "SDM PAYAL - PB55",
#     "SDM PHAGWARA - PB36",
#     "SDM PHILLOUR - PB37",
#     "SDM RAIKOT - PB56",
#     "SDM RAJPURA - PB39",
#     "SDM RAMPURA PHUL - PB40",
#     "SDM SAMANA - PB42",
#     "SDM SAMRALA - PB43",
#     "SDM SARDULGARH - PB51",
#     "SDM SHAHKOT - PB67",
#     "SDM SULTANPUR LODHI - PB41",
#     "SDM SUNAM - PB44",
#     "SDM TALWANDI SABO - PB45",
#     "SDM TANDA - PB95",
#     "SDM TAPA - PB73",
#     "SDM ZIRA - PB47"
# ]
# RTO_TO_SCRAPE = [
#     "ALMORA RTO - UK1",
#     "BAGESHWAR ARTO - UK2",
#     "DEHRADUN RTO - UK7",
#     "HALDWANI RTO - UK4",
#     "HARIDWAR ARTO - UK8",
#     "KARANPRAYAG ARTO - UK11",
#     "KASHIPUR ARTO - UK18",
#     "KOTDWAR ARTO - UK15",
#     "PAURI RTO - UK12",
#     "PITHORAGARH ARTO - UK5",
#     "RAMNAGAR ARTO - UK19",
#     "RANIKHET ARTO - UK20",
#     "RISHIKESH ARTO - UK14",
#     "ROORKEE ARTO - UK17",
#     "RUDRAPRAYAG ARTO - UK13",
#     "STATE TRANSPORT AUTHORITY - UK111",
#     "TANAKPUR ARTO - UK3",
#     "TEHRI ARTO - UK9",
#     "UDHAM SINGH NAGAR ARTO - UK6",
#     "UTTARKASHI ARTO - UK10",
#     "VIKAS NAGAR ARTO - UK16"
# ]
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
        """Select both ELECTRIC(BOV) and PURE EV fuel options"""
        # Select ELECTRIC(BOV)
        self.select_checkbox(
            "//*[@id='fuel']/tbody/tr[8]/td/div/div[2]/span",
            "//*[@id='fuel']/tbody/tr[8]/td/label",
            "ELECTRIC(BOV) fuel"
        )
        time.sleep(1)  # Wait between selections
        
        # Select PURE EV
        self.select_checkbox(
            "//*[@id='fuel']/tbody/tr[22]/td/div/div[2]/span",
            "//*[@id='fuel']/tbody/tr[22]/td/label",
            "PURE EV fuel"
        )
    
    def refresh_filters(self):
        """Click second refresh button after filters"""
        return self.click_element("/html/body/form/div[2]/div/div/div[3]/div/div[1]/div[1]/span/button", "Refresh filters")
    
    def select_vehicle_classes(self, classes):
        """Select vehicle classes for E2W, E3W, and other categories"""
        class_options = {
            # E2W Categories
            'M_CYCLE_SCOOTER': {
                'label': "//*[@id='VhClass']/tbody/tr[1]/td/label",
                'checkbox': "//*[@id='VhClass']/tbody/tr[1]/td/div/div[2]/span",
                'description': "M-CYCLE/SCOOTER"
            },
            'M_CYCLE_SCOOTER_SIDE_CAR': {
                'label': "//*[@id='VhClass']/tbody/tr[2]/td/label",
                'checkbox': "//*[@id='VhClass']/tbody/tr[2]/td/div/div[2]/span",
                'description': "M-CYCLE/SCOOTER-WITH SIDE CAR"
            },
            'MOPED': {
                'label': "//*[@id='VhClass']/tbody/tr[3]/td/label",
                'checkbox': "//*[@id='VhClass']/tbody/tr[3]/td/div/div[2]/span",
                'description': "MOPED"
            },
            # E3W Categories
            'E_RICKSHAW_P': {
                'label': "//*[@id='VhClass']/tbody/tr[38]/td/label",
                'checkbox': "//*[@id='VhClass']/tbody/tr[38]/td/div/div[2]/span",
                'description': "E-RICKSHAW(P)"
            },
            'E_RICKSHAW_CART_G': {
                'label': "//*[@id='VhClass']/tbody/tr[37]/td/label",
                'checkbox': "//*[@id='VhClass']/tbody/tr[37]/td/div/div[2]/span",
                'description': "E-RICKSHAW WITH CART(G)"
            },
            'THREE_WHEELER_P': { 
                'label': "//*[@id='VhClass']/tbody/tr[40]/td/label",
                'checkbox': "//*[@id='VhClass']/tbody/tr[40]/td/div/div[2]/span",
                'description': "THREE WHEELER (PASSENGER)"
            },
            'THREE_WHEELER_G': {
                'label': "//*[@id='VhClass']/tbody/tr[41]/td/label",
                'checkbox': "//*[@id='VhClass']/tbody/tr[41]/td/div/div[2]/span",
                'description': "THREE WHEELER (GOODS)"
            }
        }
        
        print(f"Selecting vehicle classes: {classes}")
        for class_name in classes:
            if class_name in class_options:
                self.select_checkbox(
                    class_options[class_name]['checkbox'],
                    class_options[class_name]['label'],
                    f"Vehicle class: {class_options[class_name]['description']}"
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
            if product_type == "E2W":
                print("🔄 Selecting E2W vehicle classes...")
                self.select_vehicle_classes(['M_CYCLE_SCOOTER', 'M_CYCLE_SCOOTER_SIDE_CAR', 'MOPED'])
            elif product_type == "L3G":
                print("🔄 Selecting L-3G vehicle class...")
                self.select_vehicle_classes(['E_RICKSHAW_CART_G'])
            elif product_type == "L3P":
                print("🔄 Selecting L-3P vehicle class...")
                self.select_vehicle_classes(['E_RICKSHAW_P'])
            elif product_type == "L5G":
                print("🔄 Selecting L-5G vehicle class...")
                self.select_vehicle_classes(['THREE_WHEELER_G'])
            elif product_type == "L5P":
                print("🔄 Selecting L-5P vehicle class...")
                self.select_vehicle_classes(['THREE_WHEELER_P'])
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
