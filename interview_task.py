import csv
import json
from typing import Optional, Any
from datetime import datetime, timedelta

class PackUnit():
    BAG = "BAG"
    BALE = "BALE"
    BARREL = "BARREL"
    BASKET = "BASKET"
    BIN = "BIN"
    BIN_OF_36 = "BIN_OF_36"
    BIN_OF_45 = "BIN_OF_45"
    BIN_OF_60 = "BIN_OF_60"
    BOARD_FOOT = "BOARD_FOOT"
    BOTTLE = "BOTTLE"
    BOX = "BOX"
    BUNCH = "BUNCH"
    BUNDLE = "BUNDLE"
    BUSHEL = "BUSHEL"
    CAN = "CAN"
    CARD = "CARD"
    CARTON = "CARTON"
    CASE = "CASE"
    CENTIMETER = "CENTIMETER"
    CLAMSHELL_BOX = "CLAMSHELL_BOX"
    CONTAINER = "CONTAINER"
    COUNT = "COUNT"
    CRATE = "CRATE"
    CUBIC_CENTIMETER = "CUBIC_CENTIMETER"
    CUBIC_FOOT = "CUBIC_FOOT"
    CUBIC_YARD = "CUBIC_YARD"
    CURIE = "CURIE"
    CYLINDER = "CYLINDER"
    DAY = "DAY"
    DEAL = "DEAL"
    DEWAR = "DEWAR"
    DIAMETER = "DIAMETER"
    DOZEN = "DOZEN"
    DRUM = "DRUM"
    EACH = "EACH"
    EIGHTH_WHEEL = "EIGHTH_WHEEL"
    FISH = "FISH"
    FLAT = "FLAT"
    FOOT = "FOOT"
    GALLON = "GALLON"
    GRAIN = "GRAIN"
    GRAM = "GRAM"
    GROSS = "GROSS"
    HALF_BUSHEL = "HALF_BUSHEL"
    HALF_CASE = "HALF_CASE"
    HALF_DOZEN = "HALF_DOZEN"
    HALF_FLAT = "HALF_FLAT"
    HALF_GALLON = "HALF_GALLON"
    HALF_WHEEL = "HALF_WHEEL"
    HOUR = "HOUR"
    HUNDRED = "HUNDRED"
    HUNDRED_WEIGHT = "HUNDRED_WEIGHT"
    INCH = "INCH"
    JAR = "JAR"
    KEG = "KEG"
    KILOGRAM = "KILOGRAM"
    KIT = "KIT"
    LAMBDA = "LAMBDA"
    LENGTH = "LENGTH"
    LINEAR_FOOT = "LINEAR_FOOT"
    LINEAR_YARD = "LINEAR_YARD"
    LITER = "LITER"
    LOAF = "LOAF"
    LOIN = "LOIN"
    LOT = "LOT"
    MASTER_CASE = "MASTER_CASE"
    METER = "METER"
    MICRON = "MICRON"
    MILLIGRAM = "MILLIGRAM"
    MILLILITER = "MILLILITER"
    MILLIMETER = "MILLIMETER"
    MINUTE = "MINUTE"
    MONTH = "MONTH"
    NUMBER_10_CAN = "NUMBER_10_CAN", "#10 can"
    NUMBER_6_CAN = "NUMBER_6_CAN", "#6 can"
    OMEGA = "OMEGA"
    OUNCE = "OUNCE"
    PACK = "PACK"
    PACKAGE = "PACKAGE"
    PAGE = "PAGE"
    PAIL = "PAIL"
    PAIR = "PAIR"
    PALLET = "PALLET"
    PECK = "PECK"
    PIECE = "PIECE"
    PINT = "PINT"
    PORTION = "PORTION"
    POUND = "POUND"
    QUART = "QUART"
    QUARTER = "QUARTER"
    QUARTER_WHEEL = "QUARTER_WHEEL"
    REAM = "REAM"
    ROD = "ROD"
    ROLL = "ROLL"
    SACK = "SACK"
    SEGMENT = "SEGMENT"
    SET = "SET"
    SHEET = "SHEET"
    SIDE = "SIDE"
    SLEEVE = "SLEEVE"
    SPOOL = "SPOOL"
    SQUARE_FOOT = "SQUARE_FOOT"
    SQUARE_YARD = "SQUARE_YARD"
    TAIL = "TAIL"
    THOUSAND = "THOUSAND"
    TRANSACTION = "TRANSACTION"
    TRAY = "TRAY"
    TUB = "TUB"
    TUBE = "TUBE"
    UNIT = "UNIT"
    VIAL = "VIAL"
    WEEK = "WEEK"
    WHEEL = "WHEEL"
    WING = "WING"
    YARD = "YARD"
    YEAR = "YEAR"

class ItemKey():
    code: Optional[str]
    integration_id: Optional[str]
    unit_of_measure: Optional[PackUnit]
    base_unit_of_measure: Optional[PackUnit]
    unit_count: Optional[float]
    min_unit_size: Optional[float]
    max_unit_size: Optional[float]

class ItemMetadataConfiguration():
    erp_unit: str
    additional_info: dict[str, Any]

class StrippedNonEmptyString():
    strip_whitespace = True
    min_length = 1

class Item():
    key: ItemKey

    # Required for create
    display_name: StrippedNonEmptyString
    name: StrippedNonEmptyString
    unit_of_measure: PackUnit

    # Required for create, but with defaults
    is_active: bool = True
    min_unit_size: float = 1.0
    max_unit_size: float = 1.0
    show_by_default: bool = True
    unit_count: float = 1.0

    # Nullable properties
    available_quantity: Optional[float]
    base_price_in_micros: Optional[int]
    base_unit_of_measure: Optional[PackUnit]
    category: Optional[str]
    code: Optional[str]
    description: Optional[str]
    integration_id: Optional[str]
    lead_time_days: Optional[int]
    metadata: Optional[ItemMetadataConfiguration]
    photo_url_list: Optional[list[str]]
    upc_list: Optional[list[str]]


class TestBundleGenerator():

    def generate_items(self):

        items = []
        jsonl_file_path = 'output.jsonl'


        file1 = './prices.csv'
        file2 = './leadtime.csv'
        
        with open(file1, 'r', encoding = "ISO-8859-1") as prices_file, open(file2, 'r', encoding = "ISO-8859-1") as leadtime_file, open(jsonl_file_path, 'w') as jsonl_file:
            reader = csv.DictReader(prices_file)
            leadtime_reader = csv.DictReader(leadtime_file)
            exclusion_keywords = ["Adjustment","Charge","Certificate", "Description"]
            item_number_to_on_hand_quantity_map = {}
            item_number_to_required_date_map = {}
            items = [] 


            for row in reader:
                item_number_to_on_hand_quantity_map[row["Item Number"].strip()] = row["On Hand Quantity".strip()]
            
            for row in leadtime_reader:
                item_number_to_required_date_map[row["Item Number"].strip()] = row["Required Date".strip()]


            try:
                for row in reader:
                    row = {
                        key: value.strip() if isinstance(value ,str) else value for key, value in row.items()
                    }
                    item_number_to_on_hand_quantity_map[row["Item Number"]] = row["On Hand Quantity"]

                    if any(keyword in row["Description Line 1"] for keyword in exclusion_keywords) or row["Brand Name"] == "":
                        continue

                    key = ItemKey()
                    item = Item()
                        

                    item.key = key.__dict__

                    item.display_name = row["Description Line 1"].replace("?","").replace("�","")
                    item.name = row["Description Line 1"].replace("?","").replace("�","")
                    item.is_active = True
                    item.min_unit_size = 1.0
                    item.max_unit_size = 1.0
                    item.show_by_default =  False if row["Brand Name"] == "Allez" and any(letter in row["Item Number"] for letter in ["G","P","W","F","O","U","P","A","N","R"]) else True
                    item.unit_count = row["Item Avg. Weight"] if row["Priced by Weight"] == "Y" else 1.0
                    item.base_unit_of_measure = PackUnit.POUND if row["Priced by Weight"] == "Y" else None
                    item.category = row["Class Name"]
                    item.code = row["Item Number"]
                    

                    # Logic for description 

                    temp = []
                    if row["Description Line 1"][-1] == "*":
                        temp.append("Call your sales rep to special order" )
                    if row["Brand Name"] != "": 
                        temp.append(row["Brand Name"])
                    if row["Pack Size"] != "": 
                        temp.append(row["Pack Size"])
                    if row["Priced by Weight"][-1] == "Y":
                        temp.append("Average Weight" )
                    
                    if len(temp) == 1 :
                        item.description = temp[0]
                    else:
                        item.description = " | ".join(temp)

                    item.integration_id = row["Item Number"]

                    # Logic for lead_time_days

                    if int(row["On Hand Quantity"]) > 0:
                        item.lead_time_days = None

                    item1 = row["Item Number"]
                    print(item1["On Hand Quantity"])
                    filter_letters = ["P", "S", "G"]

                    if row["Item Number"][-1] in filter_letters:
                        item2 = (row["Item Number"].replace("P",""))
                    else:
                        item2 = item1 + "P"

                    if row["On Hand Quantity"] > 0 or item_number_to_on_hand_quantity_map[item2] > 0:
                        item.lead_time_days = None
                    if row["On Hand Quantity"] <= 0 and item_number_to_on_hand_quantity_map[item2] <= 0 :
                        if item1 or item2 in leadtime_reader:
                            required_date_str = item_number_to_required_date_map[row["Item Number"]] 
                            required_date = datetime.strptime(required_date_str, '%m/%d/%y')

                            today = datetime.now().date()
                            lead_time = (required_date - today).days + 1
                            item.lead_time_days = lead_time
                        else:
                            item.lead_time_days = 14

        


                    


                    # item.lead_time_days = row["Description Line 1"]


        #             item.unit_of_measure = row["Unit of Measure"]
        #             item.metadata = ItemMetadataConfiguration().__dict__

    
                    items.append(item)

                    jsonl_file.write(json.dumps(item.__dict__) + '\n')


            except UnicodeDecodeError as e:
                print(row)  
                raise e

 
if __name__ == "__main__":
    generator = TestBundleGenerator()
    generator.generate_items()