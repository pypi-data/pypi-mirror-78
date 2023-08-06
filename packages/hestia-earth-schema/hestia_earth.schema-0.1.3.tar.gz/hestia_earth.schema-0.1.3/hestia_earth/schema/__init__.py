# auto-generated content
from collections import OrderedDict
from enum import Enum
from pkgutil import extend_path


__path__ = extend_path(__path__, __name__)
SCHEMA_VERSION = '0.1.3'


class NodeType(Enum):
    ACTOR = 'Actor'
    CYCLE = 'Cycle'
    INVENTORY = 'Inventory'
    ORGANISATION = 'Organisation'
    SITE = 'Site'
    SOURCE = 'Source'
    TERM = 'Term'


class SchemaType(Enum):
    ACTOR = 'Actor'
    BIBLIOGRAPHY = 'Bibliography'
    COMPLETENESS = 'Completeness'
    CYCLE = 'Cycle'
    EMISSION = 'Emission'
    INFRASTRUCTURE = 'Infrastructure'
    INPUT = 'Input'
    INVENTORY = 'Inventory'
    MEASUREMENT = 'Measurement'
    ORGANISATION = 'Organisation'
    PRACTICE = 'Practice'
    PRODUCT = 'Product'
    PROPERTY = 'Property'
    SITE = 'Site'
    SOURCE = 'Source'
    TERM = 'Term'


class Actor:
    def __init__(self):
        self.required = ['lastName', 'dataPrivate']
        self.fields = OrderedDict()
        self.fields['type'] = NodeType.ACTOR.value
        self.fields['name'] = ''
        self.fields['firstName'] = ''
        self.fields['lastName'] = ''
        self.fields['orcid'] = ''
        self.fields['scopusID'] = ''
        self.fields['primaryInstitution'] = ''
        self.fields['city'] = ''
        self.fields['country'] = None
        self.fields['email'] = ''
        self.fields['website'] = None
        self.fields['dataPrivate'] = False

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class BibliographyDocumentType(Enum):
    BILL = 'bill'
    BOOK = 'book'
    BOOK_SECTION = 'book_section'
    CASE = 'case'
    COMPUTER_PROGRAM = 'computer_program'
    CONFERENCE_PROCEEDINGS = 'conference_proceedings'
    ENCYCLOPEDIA_ARTICLE = 'encyclopedia_article'
    FILM = 'film'
    GENERIC = 'generic'
    HEARING = 'hearing'
    JOURNAL = 'journal'
    MAGAZINE_ARTICLE = 'magazine_article'
    NEWSPAPER_ARTICLE = 'newspaper_article'
    PATENT = 'patent'
    REPORT = 'report'
    STATUTE = 'statute'
    TELEVISION_BROADCAST = 'television_broadcast'
    THESIS = 'thesis'
    WEB_PAGE = 'web_page'
    WORKING_PAPER = 'working_paper'


class Bibliography:
    def __init__(self):
        self.required = ['name', 'title', 'authors', 'outlet', 'year']
        self.fields = OrderedDict()
        self.fields['type'] = SchemaType.BIBLIOGRAPHY.value
        self.fields['name'] = ''
        self.fields['documentDOI'] = ''
        self.fields['title'] = ''
        self.fields['arxivID'] = ''
        self.fields['scopus'] = ''
        self.fields['mendeleyID'] = ''
        self.fields['documentType'] = ''
        self.fields['authors'] = []
        self.fields['outlet'] = ''
        self.fields['year'] = None
        self.fields['volume'] = None
        self.fields['issue'] = None
        self.fields['chapter'] = ''
        self.fields['pages'] = ''
        self.fields['publisher'] = ''
        self.fields['city'] = ''
        self.fields['editors'] = []
        self.fields['institutionPub'] = []
        self.fields['websites'] = []
        self.fields['dateAccessed'] = []
        self.fields['abstract'] = ''

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class Completeness:
    def __init__(self):
        self.required = ['fertilizer', 'soilAmendments', 'pesticides', 'water', 'electricityFuel', 'productsCoProducts', 'cropResidue', 'manureCompostManagement']
        self.fields = OrderedDict()
        self.fields['type'] = SchemaType.COMPLETENESS.value
        self.fields['fertilizer'] = False
        self.fields['soilAmendments'] = False
        self.fields['pesticides'] = False
        self.fields['water'] = False
        self.fields['electricityFuel'] = False
        self.fields['productsCoProducts'] = False
        self.fields['cropResidue'] = False
        self.fields['manureCompostManagement'] = False

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class CycleAltStartDateDefinition(Enum):
    SOIL_PREPARATION_DATE = 'soil preparation date'
    SOWING_DATE = 'sowing date'


class CycleFunctionalUnitMeasure(Enum):
    _1_HA = '1 ha'
    RELATIVE = 'relative'


class Cycle:
    def __init__(self):
        self.required = ['site', 'defaultSource', 'endDate', 'functionalUnitMeasure', 'dataCompleteness', 'dataPrivate']
        self.fields = OrderedDict()
        self.fields['type'] = NodeType.CYCLE.value
        self.fields['name'] = ''
        self.fields['description'] = ''
        self.fields['site'] = None
        self.fields['defaultSource'] = None
        self.fields['endDate'] = ''
        self.fields['startDate'] = ''
        self.fields['cycleDuration'] = None
        self.fields['altStartDate'] = ''
        self.fields['altStartDateDefinition'] = ''
        self.fields['functionalUnitMeasure'] = ''
        self.fields['functionalUnitDetails'] = ''
        self.fields['numberOfCycles'] = None
        self.fields['dataCompleteness'] = None
        self.fields['inputs'] = []
        self.fields['emissions'] = []
        self.fields['products'] = []
        self.fields['practices'] = []
        self.fields['dataPrivate'] = False

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class EmissionStatsDefinition(Enum):
    CYCLES = 'cycles'
    ORGANISATIONS = 'organisations'
    REPLICATIONS = 'replications'
    SITES = 'sites'


class EmissionMethodTier(Enum):
    BACKGROUND = 'background'
    MEASURED = 'measured'
    TIER_1 = 'tier 1'
    TIER_2 = 'tier 2'
    TIER_3 = 'tier 3'


class EmissionDataState(Enum):
    AGGREGATED = 'aggregated'
    ORIGINAL = 'original'
    RECALCULATED = 'recalculated'


class Emission:
    def __init__(self):
        self.required = ['term', 'value', 'methodTier']
        self.fields = OrderedDict()
        self.fields['type'] = SchemaType.EMISSION.value
        self.fields['term'] = None
        self.fields['description'] = ''
        self.fields['value'] = None
        self.fields['relDays'] = None
        self.fields['sd'] = None
        self.fields['min'] = None
        self.fields['max'] = None
        self.fields['statsDefinition'] = ''
        self.fields['startDate'] = None
        self.fields['endDate'] = None
        self.fields['emissionDuration'] = None
        self.fields['properties'] = []
        self.fields['method'] = None
        self.fields['methodDescription'] = ''
        self.fields['methodTier'] = ''
        self.fields['characterisation'] = None
        self.fields['source'] = None
        self.fields['dataState'] = ''
        self.fields['dataVersion'] = ''

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class InfrastructureDataState(Enum):
    AGGREGATED = 'aggregated'
    GAP_FILLED = 'gap-filled'
    ORIGINAL = 'original'


class Infrastructure:
    def __init__(self):
        self.required = []
        self.fields = OrderedDict()
        self.fields['type'] = SchemaType.INFRASTRUCTURE.value
        self.fields['term'] = None
        self.fields['name'] = ''
        self.fields['startDate'] = ''
        self.fields['endDate'] = ''
        self.fields['lifespan'] = None
        self.fields['lifespanHours'] = None
        self.fields['mass'] = None
        self.fields['area'] = None
        self.fields['inputs'] = []
        self.fields['source'] = None
        self.fields['dataState'] = ''
        self.fields['dataVersion'] = None

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class InputStatsDefinition(Enum):
    CYCLES = 'cycles'
    ORGANISATIONS = 'organisations'
    REPLICATIONS = 'replications'
    SITES = 'sites'


class InputDataState(Enum):
    AGGREGATED = 'aggregated'
    GAP_FILLED = 'gap-filled'
    ORIGINAL = 'original'


class Input:
    def __init__(self):
        self.required = ['term']
        self.fields = OrderedDict()
        self.fields['type'] = SchemaType.INPUT.value
        self.fields['term'] = None
        self.fields['description'] = ''
        self.fields['value'] = None
        self.fields['relDays'] = None
        self.fields['sd'] = None
        self.fields['min'] = None
        self.fields['max'] = None
        self.fields['statsDefinition'] = ''
        self.fields['currency'] = ''
        self.fields['price'] = None
        self.fields['cost'] = None
        self.fields['properties'] = []
        self.fields['reliability'] = None
        self.fields['methodDescription'] = ''
        self.fields['inventory'] = None
        self.fields['source'] = None
        self.fields['dataState'] = ''
        self.fields['dataVersion'] = ''

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class Inventory:
    def __init__(self):
        self.required = ['timestamp']
        self.fields = OrderedDict()
        self.fields['type'] = NodeType.INVENTORY.value
        self.fields['name'] = ''
        self.fields['timestamp'] = None
        self.fields['versionDetails'] = ''
        self.fields['cycle'] = None
        self.fields['product'] = None
        self.fields['functionalUnitMeasure'] = ''
        self.fields['functionalUnitQuantity'] = None
        self.fields['inventoryTable'] = []
        self.fields['dataPrivate'] = False

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class MeasurementStatsDefinition(Enum):
    CYCLES = 'cycles'
    ORGANISATIONS = 'organisations'
    REPLICATIONS = 'replications'
    SITES = 'sites'


class MeasurementDataState(Enum):
    AGGREGATED = 'aggregated'
    GAP_FILLED = 'gap-filled'
    ORIGINAL = 'original'


class Measurement:
    def __init__(self):
        self.required = ['term', 'value']
        self.fields = OrderedDict()
        self.fields['type'] = SchemaType.MEASUREMENT.value
        self.fields['term'] = None
        self.fields['method'] = None
        self.fields['methodDescription'] = ''
        self.fields['endDate'] = ''
        self.fields['startDate'] = ''
        self.fields['value'] = None
        self.fields['sd'] = None
        self.fields['min'] = None
        self.fields['max'] = None
        self.fields['statsDefinition'] = ''
        self.fields['depthUpper'] = None
        self.fields['depthLower'] = None
        self.fields['source'] = None
        self.fields['dataState'] = ''
        self.fields['dataVersion'] = ''

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class Organisation:
    def __init__(self):
        self.required = ['dataPrivate']
        self.fields = OrderedDict()
        self.fields['type'] = NodeType.ORGANISATION.value
        self.fields['name'] = ''
        self.fields['boundary'] = None
        self.fields['area'] = None
        self.fields['latitude'] = None
        self.fields['longitude'] = None
        self.fields['streetAddress'] = ''
        self.fields['city'] = ''
        self.fields['addressRegion'] = ''
        self.fields['country'] = None
        self.fields['postOfficeBoxNumber'] = ''
        self.fields['postalCode'] = ''
        self.fields['startDate'] = ''
        self.fields['endDate'] = ''
        self.fields['dataPrivate'] = False

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class PracticeStatsDefinition(Enum):
    CYCLES = 'cycles'
    ORGANISATIONS = 'organisations'
    REPLICATIONS = 'replications'
    SITES = 'sites'


class PracticeDataState(Enum):
    AGGREGATED = 'aggregated'
    GAP_FILLED = 'gap-filled'
    ORIGINAL = 'original'


class Practice:
    def __init__(self):
        self.required = []
        self.fields = OrderedDict()
        self.fields['type'] = SchemaType.PRACTICE.value
        self.fields['term'] = None
        self.fields['description'] = ''
        self.fields['value'] = None
        self.fields['sd'] = None
        self.fields['min'] = None
        self.fields['max'] = None
        self.fields['statsDefinition'] = ''
        self.fields['startDate'] = ''
        self.fields['endDate'] = ''
        self.fields['properties'] = []
        self.fields['reliability'] = None
        self.fields['methodDescription'] = ''
        self.fields['source'] = None
        self.fields['dataState'] = ''
        self.fields['dataVersion'] = ''

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class ProductStatsDefinition(Enum):
    CYCLES = 'cycles'
    ORGANISATIONS = 'organisations'
    REPLICATIONS = 'replications'
    SITES = 'sites'


class ProductDataState(Enum):
    AGGREGATED = 'aggregated'
    GAP_FILLED = 'gap-filled'
    ORIGINAL = 'original'


class Product:
    def __init__(self):
        self.required = ['term', 'value']
        self.fields = OrderedDict()
        self.fields['type'] = SchemaType.PRODUCT.value
        self.fields['term'] = None
        self.fields['description'] = ''
        self.fields['value'] = None
        self.fields['relDays'] = None
        self.fields['sd'] = None
        self.fields['min'] = None
        self.fields['max'] = None
        self.fields['statsDefinition'] = ''
        self.fields['currency'] = ''
        self.fields['price'] = None
        self.fields['revenue'] = None
        self.fields['economicValueShare'] = None
        self.fields['properties'] = []
        self.fields['reliability'] = None
        self.fields['methodDescription'] = ''
        self.fields['destination'] = None
        self.fields['source'] = None
        self.fields['dataState'] = ''
        self.fields['dataVersion'] = ''

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class PropertyValueType(Enum):
    AUTO = 'auto'
    BOOLEAN = 'boolean'
    NUMBER = 'number'
    STRING = 'string'


class PropertyDataState(Enum):
    AGGREGATED = 'aggregated'
    GAP_FILLED = 'gap-filled'
    ORIGINAL = 'original'
    RECALCULATED = 'recalculated'


class Property:
    def __init__(self):
        self.required = []
        self.fields = OrderedDict()
        self.fields['type'] = SchemaType.PROPERTY.value
        self.fields['term'] = None
        self.fields['key'] = None
        self.fields['value'] = None
        self.fields['valueType'] = ''
        self.fields['iri'] = None
        self.fields['sd'] = None
        self.fields['source'] = None
        self.fields['dataState'] = ''
        self.fields['dataVersion'] = ''

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class SiteSiteType(Enum):
    AQUACULTURE_PENS = 'aquaculture pens'
    BUILDING = 'building'
    CROPLAND = 'cropland'
    FOREST = 'forest'
    OTHER_NATURAL_VEGETATION = 'other natural vegetation'
    PERMANENT_PASTURE = 'permanent pasture'
    POND = 'pond'


class SiteDataState(Enum):
    AGGREGATED = 'aggregated'
    ORIGINAL = 'original'
    RECALCULATED = 'recalculated'


class Site:
    def __init__(self):
        self.required = ['siteType', 'defaultSource', 'country', 'dataPrivate']
        self.fields = OrderedDict()
        self.fields['type'] = NodeType.SITE.value
        self.fields['siteType'] = ''
        self.fields['name'] = ''
        self.fields['description'] = ''
        self.fields['organisation'] = None
        self.fields['defaultSource'] = None
        self.fields['numberOfSites'] = None
        self.fields['boundary'] = None
        self.fields['area'] = None
        self.fields['latitude'] = None
        self.fields['longitude'] = None
        self.fields['country'] = None
        self.fields['region'] = None
        self.fields['startDate'] = ''
        self.fields['endDate'] = ''
        self.fields['measurements'] = []
        self.fields['infrastructure'] = []
        self.fields['practices'] = []
        self.fields['dataState'] = ''
        self.fields['dataVersion'] = None
        self.fields['dataPrivate'] = False

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class Source:
    def __init__(self):
        self.required = []
        self.fields = OrderedDict()
        self.fields['type'] = NodeType.SOURCE.value
        self.fields['name'] = ''
        self.fields['bibliography'] = None
        self.fields['metaAnalysisBibliography'] = None
        self.fields['doiHESTIA'] = ''
        self.fields['uploadDate'] = None
        self.fields['uploadBy'] = None
        self.fields['uploadNotes'] = ''
        self.fields['validationDate'] = None
        self.fields['validationBy'] = []
        self.fields['intendedApplication'] = ''
        self.fields['studyReasons'] = ''
        self.fields['intendedAudience'] = ''
        self.fields['comparativeAssertions'] = False
        self.fields['design'] = ''

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class TermTermType(Enum):
    ANIMALPRODUCT = 'animalProduct'
    AQUACULTUREMANAGEMENT = 'aquacultureManagement'
    BIODIVERSITY = 'biodiversity'
    BUILDING = 'building'
    CHARACTERISATION = 'characterisation'
    CROP = 'crop'
    CROPESTABLISHMENT = 'cropEstablishment'
    CROPPRODUCT = 'cropProduct'
    CROPPROTECTION = 'cropProtection'
    CROPRESIDUEMANAGEMENT = 'cropResidueManagement'
    CROPSUPPORT = 'cropSupport'
    DAIRYMANAGEMENT = 'dairyManagement'
    DESTINATION = 'destination'
    ECOREGION = 'ecoregion'
    ELECTRICITY = 'electricity'
    EMISSION = 'emission'
    FUEL = 'fuel'
    INORGANICFERTILIZER = 'inorganicFertilizer'
    IRRIGATION = 'irrigation'
    LANDUSEMANAGEMENT = 'landUseManagement'
    LIVEANIMAL = 'liveAnimal'
    LIVEAQUATICSPECIES = 'liveAquaticSpecies'
    MACHINERY = 'machinery'
    MATERIAL = 'material'
    MEASUREMENT = 'measurement'
    MODEL = 'model'
    ORGANICFERTILIZER = 'organicFertilizer'
    PESTICIDEAI = 'pesticideAI'
    PESTICIDEBRANDNAME = 'pesticideBrandName'
    PROCESSEDFOOD = 'processedFood'
    PROPERTY = 'property'
    REGION = 'region'
    RESOURCEUSE = 'resourceUse'
    SEED = 'seed'
    SOILAMENDMENT = 'soilAmendment'
    SOILTEXTURE = 'soilTexture'
    SOILTYPE = 'soilType'
    STANDARDSLABELS = 'standardsLabels'
    USDASOILTYPE = 'usdaSoilType'
    WATER = 'water'
    WATERREGIME = 'waterRegime'


class Term:
    def __init__(self):
        self.required = ['name']
        self.fields = OrderedDict()
        self.fields['type'] = NodeType.TERM.value
        self.fields['termType'] = ''
        self.fields['name'] = ''
        self.fields['synonyms'] = []
        self.fields['definition'] = ''
        self.fields['description'] = ''
        self.fields['units'] = ''
        self.fields['subClassOf'] = []
        self.fields['defaultProperties'] = []
        self.fields['dependentVariables'] = []
        self.fields['independentVariables'] = []

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class ActorJSONLD:
    def __init__(self):
        self.required = ['lastName', 'dataPrivate']
        self.fields = OrderedDict()
        self.fields['@type'] = NodeType.ACTOR.value
        self.fields['@id'] = ''
        self.fields['name'] = ''
        self.fields['firstName'] = ''
        self.fields['lastName'] = ''
        self.fields['orcid'] = ''
        self.fields['scopusID'] = ''
        self.fields['primaryInstitution'] = ''
        self.fields['city'] = ''
        self.fields['country'] = None
        self.fields['email'] = ''
        self.fields['website'] = None
        self.fields['dataPrivate'] = False

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class BibliographyJSONLD:
    def __init__(self):
        self.required = ['name', 'title', 'authors', 'outlet', 'year']
        self.fields = OrderedDict()
        self.fields['@type'] = SchemaType.BIBLIOGRAPHY.value
        self.fields['name'] = ''
        self.fields['documentDOI'] = ''
        self.fields['title'] = ''
        self.fields['arxivID'] = ''
        self.fields['scopus'] = ''
        self.fields['mendeleyID'] = ''
        self.fields['documentType'] = ''
        self.fields['authors'] = []
        self.fields['outlet'] = ''
        self.fields['year'] = None
        self.fields['volume'] = None
        self.fields['issue'] = None
        self.fields['chapter'] = ''
        self.fields['pages'] = ''
        self.fields['publisher'] = ''
        self.fields['city'] = ''
        self.fields['editors'] = []
        self.fields['institutionPub'] = []
        self.fields['websites'] = []
        self.fields['dateAccessed'] = []
        self.fields['abstract'] = ''

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class CompletenessJSONLD:
    def __init__(self):
        self.required = ['fertilizer', 'soilAmendments', 'pesticides', 'water', 'electricityFuel', 'productsCoProducts', 'cropResidue', 'manureCompostManagement']
        self.fields = OrderedDict()
        self.fields['@type'] = SchemaType.COMPLETENESS.value
        self.fields['fertilizer'] = False
        self.fields['soilAmendments'] = False
        self.fields['pesticides'] = False
        self.fields['water'] = False
        self.fields['electricityFuel'] = False
        self.fields['productsCoProducts'] = False
        self.fields['cropResidue'] = False
        self.fields['manureCompostManagement'] = False

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class CycleJSONLD:
    def __init__(self):
        self.required = ['site', 'defaultSource', 'endDate', 'functionalUnitMeasure', 'dataCompleteness', 'dataPrivate']
        self.fields = OrderedDict()
        self.fields['@type'] = NodeType.CYCLE.value
        self.fields['@id'] = ''
        self.fields['name'] = ''
        self.fields['description'] = ''
        self.fields['site'] = None
        self.fields['defaultSource'] = None
        self.fields['endDate'] = ''
        self.fields['startDate'] = ''
        self.fields['cycleDuration'] = None
        self.fields['altStartDate'] = ''
        self.fields['altStartDateDefinition'] = ''
        self.fields['functionalUnitMeasure'] = ''
        self.fields['functionalUnitDetails'] = ''
        self.fields['numberOfCycles'] = None
        self.fields['dataCompleteness'] = None
        self.fields['inputs'] = []
        self.fields['emissions'] = []
        self.fields['products'] = []
        self.fields['practices'] = []
        self.fields['dataPrivate'] = False

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class EmissionJSONLD:
    def __init__(self):
        self.required = ['term', 'value', 'methodTier']
        self.fields = OrderedDict()
        self.fields['@type'] = SchemaType.EMISSION.value
        self.fields['term'] = None
        self.fields['description'] = ''
        self.fields['value'] = None
        self.fields['relDays'] = None
        self.fields['sd'] = None
        self.fields['min'] = None
        self.fields['max'] = None
        self.fields['statsDefinition'] = ''
        self.fields['startDate'] = None
        self.fields['endDate'] = None
        self.fields['emissionDuration'] = None
        self.fields['properties'] = []
        self.fields['method'] = None
        self.fields['methodDescription'] = ''
        self.fields['methodTier'] = ''
        self.fields['characterisation'] = None
        self.fields['source'] = None
        self.fields['dataState'] = ''
        self.fields['dataVersion'] = ''

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class InfrastructureJSONLD:
    def __init__(self):
        self.required = []
        self.fields = OrderedDict()
        self.fields['@type'] = SchemaType.INFRASTRUCTURE.value
        self.fields['term'] = None
        self.fields['name'] = ''
        self.fields['startDate'] = ''
        self.fields['endDate'] = ''
        self.fields['lifespan'] = None
        self.fields['lifespanHours'] = None
        self.fields['mass'] = None
        self.fields['area'] = None
        self.fields['inputs'] = []
        self.fields['source'] = None
        self.fields['dataState'] = ''
        self.fields['dataVersion'] = None

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class InputJSONLD:
    def __init__(self):
        self.required = ['term']
        self.fields = OrderedDict()
        self.fields['@type'] = SchemaType.INPUT.value
        self.fields['term'] = None
        self.fields['description'] = ''
        self.fields['value'] = None
        self.fields['relDays'] = None
        self.fields['sd'] = None
        self.fields['min'] = None
        self.fields['max'] = None
        self.fields['statsDefinition'] = ''
        self.fields['currency'] = ''
        self.fields['price'] = None
        self.fields['cost'] = None
        self.fields['properties'] = []
        self.fields['reliability'] = None
        self.fields['methodDescription'] = ''
        self.fields['inventory'] = None
        self.fields['source'] = None
        self.fields['dataState'] = ''
        self.fields['dataVersion'] = ''

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class InventoryJSONLD:
    def __init__(self):
        self.required = ['timestamp']
        self.fields = OrderedDict()
        self.fields['@type'] = NodeType.INVENTORY.value
        self.fields['@id'] = ''
        self.fields['name'] = ''
        self.fields['timestamp'] = None
        self.fields['versionDetails'] = ''
        self.fields['cycle'] = None
        self.fields['product'] = None
        self.fields['functionalUnitMeasure'] = ''
        self.fields['functionalUnitQuantity'] = None
        self.fields['inventoryTable'] = []
        self.fields['dataPrivate'] = False

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class MeasurementJSONLD:
    def __init__(self):
        self.required = ['term', 'value']
        self.fields = OrderedDict()
        self.fields['@type'] = SchemaType.MEASUREMENT.value
        self.fields['term'] = None
        self.fields['method'] = None
        self.fields['methodDescription'] = ''
        self.fields['endDate'] = ''
        self.fields['startDate'] = ''
        self.fields['value'] = None
        self.fields['sd'] = None
        self.fields['min'] = None
        self.fields['max'] = None
        self.fields['statsDefinition'] = ''
        self.fields['depthUpper'] = None
        self.fields['depthLower'] = None
        self.fields['source'] = None
        self.fields['dataState'] = ''
        self.fields['dataVersion'] = ''

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class OrganisationJSONLD:
    def __init__(self):
        self.required = ['dataPrivate']
        self.fields = OrderedDict()
        self.fields['@type'] = NodeType.ORGANISATION.value
        self.fields['@id'] = ''
        self.fields['name'] = ''
        self.fields['boundary'] = None
        self.fields['area'] = None
        self.fields['latitude'] = None
        self.fields['longitude'] = None
        self.fields['streetAddress'] = ''
        self.fields['city'] = ''
        self.fields['addressRegion'] = ''
        self.fields['country'] = None
        self.fields['postOfficeBoxNumber'] = ''
        self.fields['postalCode'] = ''
        self.fields['startDate'] = ''
        self.fields['endDate'] = ''
        self.fields['dataPrivate'] = False

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class PracticeJSONLD:
    def __init__(self):
        self.required = []
        self.fields = OrderedDict()
        self.fields['@type'] = SchemaType.PRACTICE.value
        self.fields['term'] = None
        self.fields['description'] = ''
        self.fields['value'] = None
        self.fields['sd'] = None
        self.fields['min'] = None
        self.fields['max'] = None
        self.fields['statsDefinition'] = ''
        self.fields['startDate'] = ''
        self.fields['endDate'] = ''
        self.fields['properties'] = []
        self.fields['reliability'] = None
        self.fields['methodDescription'] = ''
        self.fields['source'] = None
        self.fields['dataState'] = ''
        self.fields['dataVersion'] = ''

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class ProductJSONLD:
    def __init__(self):
        self.required = ['term', 'value']
        self.fields = OrderedDict()
        self.fields['@type'] = SchemaType.PRODUCT.value
        self.fields['term'] = None
        self.fields['description'] = ''
        self.fields['value'] = None
        self.fields['relDays'] = None
        self.fields['sd'] = None
        self.fields['min'] = None
        self.fields['max'] = None
        self.fields['statsDefinition'] = ''
        self.fields['currency'] = ''
        self.fields['price'] = None
        self.fields['revenue'] = None
        self.fields['economicValueShare'] = None
        self.fields['properties'] = []
        self.fields['reliability'] = None
        self.fields['methodDescription'] = ''
        self.fields['destination'] = None
        self.fields['source'] = None
        self.fields['dataState'] = ''
        self.fields['dataVersion'] = ''

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class PropertyJSONLD:
    def __init__(self):
        self.required = []
        self.fields = OrderedDict()
        self.fields['@type'] = SchemaType.PROPERTY.value
        self.fields['term'] = None
        self.fields['key'] = None
        self.fields['value'] = None
        self.fields['valueType'] = ''
        self.fields['iri'] = None
        self.fields['sd'] = None
        self.fields['source'] = None
        self.fields['dataState'] = ''
        self.fields['dataVersion'] = ''

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class SiteJSONLD:
    def __init__(self):
        self.required = ['siteType', 'defaultSource', 'country', 'dataPrivate']
        self.fields = OrderedDict()
        self.fields['@type'] = NodeType.SITE.value
        self.fields['@id'] = ''
        self.fields['siteType'] = ''
        self.fields['name'] = ''
        self.fields['description'] = ''
        self.fields['organisation'] = None
        self.fields['defaultSource'] = None
        self.fields['numberOfSites'] = None
        self.fields['boundary'] = None
        self.fields['area'] = None
        self.fields['latitude'] = None
        self.fields['longitude'] = None
        self.fields['country'] = None
        self.fields['region'] = None
        self.fields['startDate'] = ''
        self.fields['endDate'] = ''
        self.fields['measurements'] = []
        self.fields['infrastructure'] = []
        self.fields['practices'] = []
        self.fields['dataState'] = ''
        self.fields['dataVersion'] = None
        self.fields['dataPrivate'] = False

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class SourceJSONLD:
    def __init__(self):
        self.required = []
        self.fields = OrderedDict()
        self.fields['@type'] = NodeType.SOURCE.value
        self.fields['@id'] = ''
        self.fields['name'] = ''
        self.fields['bibliography'] = None
        self.fields['metaAnalysisBibliography'] = None
        self.fields['doiHESTIA'] = ''
        self.fields['uploadDate'] = None
        self.fields['uploadBy'] = None
        self.fields['uploadNotes'] = ''
        self.fields['validationDate'] = None
        self.fields['validationBy'] = []
        self.fields['intendedApplication'] = ''
        self.fields['studyReasons'] = ''
        self.fields['intendedAudience'] = ''
        self.fields['comparativeAssertions'] = False
        self.fields['design'] = ''

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class TermJSONLD:
    def __init__(self):
        self.required = ['name']
        self.fields = OrderedDict()
        self.fields['@type'] = NodeType.TERM.value
        self.fields['@id'] = ''
        self.fields['termType'] = ''
        self.fields['name'] = ''
        self.fields['synonyms'] = []
        self.fields['definition'] = ''
        self.fields['description'] = ''
        self.fields['units'] = ''
        self.fields['subClassOf'] = []
        self.fields['defaultProperties'] = []
        self.fields['dependentVariables'] = []
        self.fields['independentVariables'] = []

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values
