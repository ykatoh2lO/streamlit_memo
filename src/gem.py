import json
import pickle
from enum import StrEnum, unique
from urllib import request

import yaml
import pandas as pd
import geopandas as gpd
from shapely.geometry import shape
from shapely.ops import unary_union

# WGS84 の緯度経度と Web メルカトル
WGS84_BL = 'EPSG:4326'
WGS84_PM = 'EPSG:3857'


@unique
class GadmCountry(StrEnum):
    """ GADM から境界データをダウンロードできる国一覧: https://gadm.org/download_country.html の countrySelect """
    AFG = 'AFG_Afghanistan_3'
    XAD = 'XAD_Akrotiri and Dhekelia_2'
    ALA = 'ALA_Åland_3'
    ALB = 'ALB_Albania_4'
    DZA = 'DZA_Algeria_3'
    ASM = 'ASM_American Samoa_4'
    AND = 'AND_Andorra_2'
    AGO = 'AGO_Angola_4'
    AIA = 'AIA_Anguilla_2'
    ATA = 'ATA_Antarctica_1'
    ATG = 'ATG_Antigua and Barbuda_2'
    ARG = 'ARG_Argentina_3'
    ARM = 'ARM_Armenia_2'
    ABW = 'ABW_Aruba_1'
    AUS = 'AUS_Australia_3'
    AUT = 'AUT_Austria_5'
    AZE = 'AZE_Azerbaijan_3'
    BHS = 'BHS_Bahamas_2'
    BHR = 'BHR_Bahrain_2'
    BGD = 'BGD_Bangladesh_5'
    BRB = 'BRB_Barbados_2'
    BLR = 'BLR_Belarus_3'
    BEL = 'BEL_Belgium_5'
    BLZ = 'BLZ_Belize_2'
    BEN = 'BEN_Benin_4'
    BMU = 'BMU_Bermuda_2'
    BTN = 'BTN_Bhutan_3'
    BOL = 'BOL_Bolivia_4'
    BES = 'BES_Bonaire Saint Eustatius and Saba_2'
    BIH = 'BIH_Bosnia and Herzegovina_4'
    BWA = 'BWA_Botswana_3'
    BVT = 'BVT_Bouvet Island_1'
    BRA = 'BRA_Brazil_3'
    IOT = 'IOT_British Indian Ocean Territory_1'
    VGB = 'VGB_British Virgin Islands_2'
    BRN = 'BRN_Brunei_3'
    BGR = 'BGR_Bulgaria_3'
    BFA = 'BFA_Burkina Faso_4'
    BDI = 'BDI_Burundi_5'
    CPV = 'CPV_Cabo Verde_2'
    KHM = 'KHM_Cambodia_4'
    CMR = 'CMR_Cameroon_4'
    CAN = 'CAN_Canada_4'
    XCA = 'XCA_Caspian Sea_1'
    CYM = 'CYM_Cayman Islands_2'
    CAF = 'CAF_Central African Republic_3'
    TCD = 'TCD_Chad_4'
    CHL = 'CHL_Chile_4'
    CHN = 'CHN_China_4'  # feature が 4 つ
    CXR = 'CXR_Christmas Island_1'
    XCL = 'XCL_Clipperton Island_1'
    CCK = 'CCK_Cocos Islands_1'
    COL = 'COL_Colombia_3'
    COM = 'COM_Comoros_2'
    COG = 'COG_Congo_3'
    COK = 'COK_Cook Islands_2'
    CRI = 'CRI_Costa Rica_4'
    CIV = 'CIV_Côte d\'Ivoire_5'
    HRV = 'HRV_Croatia_3'
    CUB = 'CUB_Cuba_3'
    CUW = 'CUW_Curaçao_1'
    CYP = 'CYP_Cyprus_2'
    CZE = 'CZE_Czech Republic_3'
    COD = 'COD_Democratic Republic of the Congo_3'
    DNK = 'DNK_Denmark_3'
    DJI = 'DJI_Djibouti_3'
    DMA = 'DMA_Dominica_2'
    DOM = 'DOM_Dominican Republic_3'
    TLS = 'TLS_East Timor_4'
    ECU = 'ECU_Ecuador_4'
    EGY = 'EGY_Egypt_3'
    SLV = 'SLV_El Salvador_3'
    GNQ = 'GNQ_Equatorial Guinea_3'
    ERI = 'ERI_Eritrea_3'
    EST = 'EST_Estonia_4'
    SWZ = 'SWZ_Eswatini_3'
    ETH = 'ETH_Ethiopia_4'
    FLK = 'FLK_Falkland Islands_1'
    FRO = 'FRO_Faroe Islands_3'
    FJI = 'FJI_Fiji_3'
    FIN = 'FIN_Finland_5'
    FRA = 'FRA_France_5'
    GUF = 'GUF_French Guiana_3'
    PYF = 'PYF_French Polynesia_2'
    ATF = 'ATF_French Southern Territories_2'
    GAB = 'GAB_Gabon_3'
    GMB = 'GMB_Gambia_3'
    GEO = 'GEO_Georgia_3'
    DEU = 'DEU_Germany_5'
    GHA = 'GHA_Ghana_3'
    GIB = 'GIB_Gibraltar_1'
    GRC = 'GRC_Greece_4'
    GRL = 'GRL_Greenland_2'
    GRD = 'GRD_Grenada_2'
    GLP = 'GLP_Guadeloupe_3'
    GUM = 'GUM_Guam_2'
    GTM = 'GTM_Guatemala_3'
    GGY = 'GGY_Guernsey_2'
    GIN = 'GIN_Guinea_4'
    GNB = 'GNB_Guinea-Bissau_3'
    GUY = 'GUY_Guyana_3'
    HTI = 'HTI_Haiti_5'
    HMD = 'HMD_Heard Island and McDonald Islands_1'
    HND = 'HND_Honduras_3'
    HUN = 'HUN_Hungary_3'
    ISL = 'ISL_Iceland_3'
    IND = 'IND_India_4'  # feature が 6 つ
    IDN = 'IDN_Indonesia_5'
    IRN = 'IRN_Iran_3'
    IRQ = 'IRQ_Iraq_3'
    IRL = 'IRL_Ireland_3'
    IMN = 'IMN_Isle of Man_2'
    ISR = 'ISR_Israel_2'
    ITA = 'ITA_Italy_4'
    JAM = 'JAM_Jamaica_2'
    JPN = 'JPN_Japan_3'
    JEY = 'JEY_Jersey_2'
    JOR = 'JOR_Jordan_3'
    KAZ = 'KAZ_Kazakhstan_3'
    KEN = 'KEN_Kenya_4'
    KIR = 'KIR_Kiribati_1'
    XKO = 'XKO_Kosovo_3'
    KWT = 'KWT_Kuwait_2'
    KGZ = 'KGZ_Kyrgyzstan_3'
    LAO = 'LAO_Laos_3'
    LVA = 'LVA_Latvia_3'
    LBN = 'LBN_Lebanon_4'
    LSO = 'LSO_Lesotho_2'
    LBR = 'LBR_Liberia_4'
    LBY = 'LBY_Libya_2'
    LIE = 'LIE_Liechtenstein_2'
    LTU = 'LTU_Lithuania_3'
    LUX = 'LUX_Luxembourg_5'
    MKD = 'MKD_Macedonia_2'
    MDG = 'MDG_Madagascar_5'
    MWI = 'MWI_Malawi_4'
    MYS = 'MYS_Malaysia_3'
    MDV = 'MDV_Maldives_1'
    MLI = 'MLI_Mali_5'
    MLT = 'MLT_Malta_3'
    MHL = 'MHL_Marshall Islands_2'
    MTQ = 'MTQ_Martinique_3'
    MRT = 'MRT_Mauritania_3'
    MUS = 'MUS_Mauritius_2'
    MYT = 'MYT_Mayotte_2'
    MEX = 'MEX_Mexico_3'
    FSM = 'FSM_Micronesia_3'
    MDA = 'MDA_Moldova_2'
    MCO = 'MCO_Monaco_1'
    MNG = 'MNG_Mongolia_3'
    MNE = 'MNE_Montenegro_2'
    MSR = 'MSR_Montserrat_2'
    MAR = 'MAR_Morocco_5'
    MOZ = 'MOZ_Mozambique_4'
    MMR = 'MMR_Myanmar_4'
    NAM = 'NAM_Namibia_3'
    NRU = 'NRU_Nauru_2'
    NPL = 'NPL_Nepal_5'
    NLD = 'NLD_Netherlands_3'
    NCL = 'NCL_New Caledonia_3'
    NZL = 'NZL_New Zealand_3'
    NIC = 'NIC_Nicaragua_3'
    NER = 'NER_Niger_4'
    NGA = 'NGA_Nigeria_3'
    NIU = 'NIU_Niue_1'
    NFK = 'NFK_Norfolk Island_1'
    PRK = 'PRK_North Korea_3'
    ZNC = 'ZNC_Northern Cyprus_2'
    MNP = 'MNP_Northern Mariana Islands_2'
    NOR = 'NOR_Norway_3'
    OMN = 'OMN_Oman_3'
    PAK = 'PAK_Pakistan_4'  # feature が 2 つ
    PLW = 'PLW_Palau_2'
    PSE = 'PSE_Palestine_3'
    PAN = 'PAN_Panama_4'
    PNG = 'PNG_Papua New Guinea_3'
    XPI = 'XPI_Paracel Islands_1'
    PRY = 'PRY_Paraguay_3'
    PER = 'PER_Peru_4'
    PHL = 'PHL_Philippines_4'
    PCN = 'PCN_Pitcairn Islands_1'
    POL = 'POL_Poland_4'
    PRT = 'PRT_Portugal_4'
    PRI = 'PRI_Puerto Rico_2'
    QAT = 'QAT_Qatar_2'
    REU = 'REU_Réunion_3'
    ROU = 'ROU_Romania_3'
    RUS = 'RUS_Russia_4'
    RWA = 'RWA_Rwanda_5'
    BLM = 'BLM_Saint-Barthélemy_3'
    MAF = 'MAF_Saint-Martin_1'
    SHN = 'SHN_Saint Helena_3'
    KNA = 'KNA_Saint Kitts and Nevis_2'
    LCA = 'LCA_Saint Lucia_2'
    SPM = 'SPM_Saint Pierre and Miquelon_2'
    VCT = 'VCT_Saint Vincent and the Grenadines_2'
    WSM = 'WSM_Samoa_3'
    SMR = 'SMR_San Marino_2'
    STP = 'STP_São Tomé and Príncipe_3'
    SAU = 'SAU_Saudi Arabia_3'
    SEN = 'SEN_Senegal_5'
    SRB = 'SRB_Serbia_3'
    SYC = 'SYC_Seychelles_2'
    SLE = 'SLE_Sierra Leone_4'
    SGP = 'SGP_Singapore_2'
    SXM = 'SXM_Sint Maarten_1'
    SVK = 'SVK_Slovakia_3'
    SVN = 'SVN_Slovenia_3'
    SLB = 'SLB_Solomon Islands_3'
    SOM = 'SOM_Somalia_3'
    ZAF = 'ZAF_South Africa_5'
    SGS = 'SGS_South Georgia and the South Sandwich Islands_1'
    KOR = 'KOR_South Korea_4'
    SSD = 'SSD_South Sudan_4'
    ESP = 'ESP_Spain_5'
    XSP = 'XSP_Spratly Islands_1'
    LKA = 'LKA_Sri Lanka_3'
    SDN = 'SDN_Sudan_4'
    SUR = 'SUR_Suriname_3'
    SJM = 'SJM_Svalbard and Jan Mayen_2'
    SWE = 'SWE_Sweden_3'
    CHE = 'CHE_Switzerland_4'
    SYR = 'SYR_Syria_3'
    TWN = 'TWN_Taiwan_3'
    TJK = 'TJK_Tajikistan_4'
    TZA = 'TZA_Tanzania_4'
    THA = 'THA_Thailand_4'
    TGO = 'TGO_Togo_4'
    TKL = 'TKL_Tokelau_2'
    TON = 'TON_Tonga_3'
    TTO = 'TTO_Trinidad and Tobago_2'
    TUN = 'TUN_Tunisia_3'
    TUR = 'TUR_Turkey_3'
    TKM = 'TKM_Turkmenistan_3'
    TCA = 'TCA_Turks and Caicos Islands_2'
    TUV = 'TUV_Tuvalu_2'
    UGA = 'UGA_Uganda_5'
    UKR = 'UKR_Ukraine_3'
    ARE = 'ARE_United Arab Emirates_4'
    GBR = 'GBR_United Kingdom_5'
    USA = 'USA_United States_3'
    UMI = 'UMI_United States Minor Outlying Islands_2'
    URY = 'URY_Uruguay_3'
    UZB = 'UZB_Uzbekistan_3'
    VUT = 'VUT_Vanuatu_3'
    VAT = 'VAT_Vatican City_1'
    VEN = 'VEN_Venezuela_3'
    VNM = 'VNM_Vietnam_4'
    VIR = 'VIR_Virgin Islands U.S._3'
    WLF = 'WLF_Wallis and Futuna_3'
    ESH = 'ESH_Western Sahara_2'
    YEM = 'YEM_Yemen_3'
    ZMB = 'ZMB_Zambia_3'
    ZWE = 'ZWE_Zimbabwe_4'

    def get_dagm_polygon(self):
        """ GADM から GeoJSON を取得し，各 feature の geometry をマージしたポリゴンを返す """
        # NOTE: 北方領土がロシア領になっていたので他のデータのほうがいいかも
        with request.urlopen(f'https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_{self.name}_0.json') as res:
            features = json.loads(res.read())['features']  # feature は基本的には 1 つだけど例外あり
            return unary_union([shape(feature['geometry']) for feature in features])


def check_yaml_data(gem_data, country_data):
    """ YAML で書かれた情報で国の境界データを読み込めそうかチェックする """
    gadm_country = {gc.name for gc in GadmCountry}
    for country_alpha3, jname_gems in country_data.items():
        assert country_alpha3 in gadm_country, country_alpha3
        print(jname_gems['JNAME'], GadmCountry[country_alpha3])
        print('\t', [gem_data[gem]['JNAME'] for gem in jname_gems['GEMS']])


def yaml_to_pickle(gem_data, mineral_data, country_data):
    """ YAML で書かれた情報から表示用のデータ一式を作成して pickle 化する """
    mineral_info, mineral_gem = [], []
    for mname in mineral_data:
        data = mineral_data[mname]
        jname = data['JNAME']
        mineral_info.append([data['IDX'], jname, data['CRYSTAL'], data['MOHS']])
        mineral_gem.extend([[jname, gem_data[gem]['JNAME']] for gem in data['GEMS']])

    # 硬度や結晶の情報も含む
    df_mineral_info = pd.DataFrame(mineral_info, columns=['idx', '鉱物名', '結晶系', 'モース硬度']).set_index('idx')
    df_mineral_info.to_csv('mineral_info.csv', index=False, encoding='cp932')
    # 鉱物名と宝石名の対応
    df_mineral_gem = pd.DataFrame(mineral_gem, columns=['鉱物名', '宝石名'])
    df_mineral_gem.to_csv('mineral_gem.csv', index=False, encoding='cp932')
    print('mineral_data')

    country_gem, country_shape = [], []
    for country_alpha3, jname_gems in country_data.items():
        country_jname = jname_gems['JNAME']
        country_gem.extend([[country_jname, gem_data[gem]['JNAME']] for gem in jname_gems['GEMS']])
        country_shape.append([country_jname, GadmCountry[country_alpha3].get_dagm_polygon()])
        print(f'shape {country_alpha3}')

    # 国と宝石名の対応
    df_country_gem = pd.DataFrame(country_gem, columns=['国名', '宝石名'])
    df_country_gem.to_csv('country_gem.csv', index=False, encoding='cp932')
    # 産出国の境界データ
    gdf_country_shape = gpd.GeoDataFrame(pd.DataFrame(country_shape, columns=['国名', 'geometry'])).set_crs(WGS84_BL)
    gdf_country_shape.to_file(f'country_shape.fgb', driver='FlatGeobuf')

    with open('gem_data.pkl', 'wb') as fwb:
        pickle.dump({
            'df_mineral_info': df_mineral_info,
            'df_mineral_gem': df_mineral_gem,
            'df_country_gem': df_country_gem,
            'gdf_country_shape': gdf_country_shape,
        }, fwb)

def load_pickle():
    with open('gem_data.pkl', 'rb') as frb:
        return pickle.load(frb)

if __name__ == '__main__':
    # YAML から宝石一覧，鉱物一覧，産地一覧を読み込む
    with open('gem_data.yaml', 'rb') as f:
        dem_yaml = yaml.safe_load(f)
        gem_data = dem_yaml['GEM']
        mineral_data = dem_yaml['MINERAL']
        country_data = dem_yaml['MAP']

    # check_yaml_data(gem_data, country_data)

    yaml_to_pickle(gem_data, mineral_data, country_data)

    # print(load_pickle())
