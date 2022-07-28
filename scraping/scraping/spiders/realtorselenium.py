import psycopg2
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


def parse_data(link):
    driver.get(link)
    response = scrapy.Selector(text=driver.page_source)

    bedroom = "unavailable"
    TotalBathrooms = "unavailable"
    FullBathrooms = "unavailable"
    HalfBathrooms = "unavailable"
    BathroomDescription = "unavailable"
    GarageSpaces = "unavailable"
    CoolingFeatures = "unavailable"
    InteriorFeatures = "unavailable"
    HeatingFeatures = "unavailable"
    DiningRoomDescription = "unavailable"
    ExteriorandLotFeatures = "unavailable"
    WaterFeatures = "unavailable"
    WaterfrontDescription = "unavailable"
    PoolFeatures = "unavailable"
    PoolDescription = "unavailable"
    Mode = "unavailable"
    ParkingFeatures = "unavailable"
    View = "unavailable"
    OtherEquipment = "unavailable"
    ElementarySchool = "unavailable"
    HighSchool = "unavailable"
    MiddleSchool = "unavailable"
    AssociationFeeAmenitie = "unavailable"
    Association = "unavailable"
    AssociationAmenities = "unavailable"
    AssociationFee = "unavailable"
    AssociationFeeFrequency = "unavailable"
    CalculatedTotalMonthlyAssociation = "unavailable"
    MaintenanceDescription = "unavailable"
    PetDescription = "unavailable"
    AnnualTaxAmount = "unavailable"
    SourceListingStatus = "unavailable"
    County = "unavailable"
    Directions = "unavailable"
    TaxYear = "unavailable"
    Restrictions = "unavailable"
    SourcePropertyType = "unavailable"
    Area = "unavailable"
    SourceNeighborhood = "unavailable"
    PostalCode = "unavailable"
    PublicSurveySection = "unavailable"
    Subdivision = "unavailable"
    Zoning = "unavailable"
    SourceSystemName = "unavailable"
    TotalSquareFeetLiving = "unavailable"
    YearBuilt = "unavailable"
    ConstructionMaterials = "unavailable"
    DirectionFaces = "unavailable"
    PropertyAge = "unavailable"
    Roof = "unavailable"
    LevelsorStories = "unavailable"
    StructureType = "unavailable"
    HouseStyle = "unavailable"
    TotalAreaSqft = "unavailable"
    YearBuiltDetails = "unavailable"
    ArchitecturalStyle = "unavailable"
    Sewer = "unavailable"
    WaterSource = "unavailable"

    if 'Property Details' in ''.join(response.css('section[data-label="Property Details"] h2::text').extract()).strip():
        link = link
        try:
            ListingType = response.xpath('//*[@id="__next"]/div[2]/div/div[2]/div/div/section[2]/div[4]/div[1]/span[2]::text').extract_first()
        except:
            try:
                ListingType = response.xpath('//*[@id="ldp-hero-photo-wrap"]/div[3]/div[1]/div/span::text').extract_first()
            except:
                try:
                    ListingType = response.xpath('//*[@id="label-sold"]::text').extract_first()
                except:
                    ListingType = ''
        try:
            description = response.css('section[data-label="Property Details"] div.desc::text').extract_first().strip().replace("'", "")
        except:
            description = 'unavailable'
        for res in response.css('section[data-label="Property Details"] div.feature-item'):
            if 'Bedrooms' in res.css('h4::text').extract_first():
                for re in res.css('ul li'):
                    bedroom = re.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
            if 'Bathrooms' in res.css('h4::text').extract_first():
                for r in res.css('ul li'):
                    if 'Total Bathrooms' in r.css('::text').extract_first():
                        TotalBathrooms = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Full Bathrooms' in r.css('::text').extract_first():
                        FullBathrooms = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if '1/2 Bathrooms' in r.css('::text').extract_first():
                        HalfBathrooms = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Bathroom Description' in r.css('::text').extract_first():
                        BathroomDescription = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
            if 'Interior Features' in res.css('h4::text').extract_first():
                for r in res.css('ul li'):
                    InteriorFeatures = ''.join(r.css('::text').extract_first()).replace("'", "")
            if 'Heating and Cooling' in res.css('h4::text').extract_first():
                for r in res.css('ul li'):
                    if 'Cooling Features' in r.css('::text').extract_first():
                        CoolingFeatures = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Heating Features' in r.css('::text').extract_first():
                        HeatingFeatures = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
            if 'Kitchen and Dining' in res.css('h4::text').extract_first():
                for r in res.css('ul li'):
                    if 'Dining Room Description' in r.css('::text').extract_first():
                        DiningRoomDescription = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
            if 'Exterior and Lot Features' in res.css('h4::text').extract_first():
                for r in res.css('ul li'):
                    ExteriorandLotFeatures = ''.join(r.css('::text').extract_first()).replace("'", "")
            if 'Waterfront and Water Access' in res.css('h4::text').extract_first():
                for r in res.css('ul li'):
                    if 'Water Features' in r.css('::text').extract_first():
                        WaterFeatures = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Waterfront Description' in r.css('::text').extract_first():
                        WaterfrontDescription = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
            if 'Pool and Spa' in res.css('h4::text').extract_first():
                for r in res.css('ul li'):
                    if 'Pool Features: Pool YN' in r.css('::text').extract_first():
                        PoolFeatures = r.css('::text').extract_first().split('YN:')[-1].split(',')[
                            0].strip().replace("'", "")
                    if 'Pool Description' in r.css('::text').extract_first():
                        PoolDescription = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
            if 'Manufactured and Mobile Info' in res.css('h4::text').extract_first():
                for r in res.css('ul li'):
                    if 'Mode' in r.css('::text').extract_first():
                        Mode = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
            if 'Garage and Parking' in res.css('h4::text').extract_first():
                for r in res.css('ul li'):
                    if 'Garage Spaces' in r.css('::text').extract_first():
                        GarageSpaces = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Parking Features' in r.css('::text').extract_first():
                        ParkingFeatures = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
            if 'Home Features' in res.css('h4::text').extract_first():
                for r in res.css('ul li'):
                    if 'Garage Spaces' in r.css('::text').extract_first():
                        GarageSpaces = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Parking Features' in r.css('::text').extract_first():
                        ParkingFeatures = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
            if 'School Information' in res.css('h4::text').extract_first():
                for r in res.css('ul li'):
                    if 'Elementary School' in r.css('::text').extract_first():
                        ElementarySchool = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'High School' in r.css('::text').extract_first():
                        HighSchool = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Middle School' in r.css('::text').extract_first():
                        MiddleSchool = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
            if 'Homeowners Association' in res.css('h4::text').extract_first():
                for r in res.css('ul li'):
                    if 'Association Fee Amenitie' in r.css('::text').extract_first():
                        AssociationFeeAmenitie = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Association:' in r.css('::text').extract_first():
                        Association = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Association Amenities:' in r.css('::text').extract_first():
                        AssociationAmenities = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Association Fee:' in r.css('::text').extract_first():
                        AssociationFee = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Association Fee Frequency:' in r.css('::text').extract_first():
                        AssociationFeeFrequency = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Calculated Total Monthly Association' in r.css('::text').extract_first():
                        CalculatedTotalMonthlyAssociation = r.css('::text').extract_first().split(':')[
                            -1].strip().replace("'", "")
                    if 'Maintenance Description' in r.css('::text').extract_first():
                        MaintenanceDescription = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Pet Description' in r.css('::text').extract_first():
                        PetDescription = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
            if 'Other Property Info' in res.css('h4::text').extract_first():
                for r in res.css('ul li'):
                    if 'Annual Tax Amount' in r.css('::text').extract_first():
                        AnnualTaxAmount = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Source Listing Status' in r.css('::text').extract_first():
                        SourceListingStatus = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'County' in r.css('::text').extract_first():
                        County = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Directions' in r.css('::text').extract_first():
                        Directions = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Tax Year' in r.css('::text').extract_first():
                        TaxYear = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Restrictions' in r.css('::text').extract_first():
                        Restrictions = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Source Property Type' in r.css('::text').extract_first():
                        SourcePropertyType = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Area' in r.css('::text').extract_first():
                        Area = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Source Neighborhood' in r.css('::text').extract_first():
                        SourceNeighborhood = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Postal Code' in r.css('::text').extract_first():
                        PostalCode = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Public Survey Section' in r.css('::text').extract_first():
                        PublicSurveySection = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Subdivision' in r.css('::text').extract_first():
                        Subdivision = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Zoning' in r.css('::text').extract_first():
                        Zoning = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Source System Name' in r.css('::text').extract_first():
                        SourceSystemName = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
            if 'Building and Construction' in res.css('h4::text').extract_first():
                for r in res.css('ul li'):
                    if 'Total Square Feet Living' in r.css('::text').extract_first():
                        TotalSquareFeetLiving = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Year Built' in r.css('::text').extract_first():
                        YearBuilt = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Construction Materials' in r.css('::text').extract_first():
                        ConstructionMaterials = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Direction Faces' in r.css('::text').extract_first():
                        DirectionFaces = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Property Age' in r.css('::text').extract_first():
                        PropertyAge = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Roof' in r.css('::text').extract_first():
                        Roof = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Levels or Stories' in r.css('::text').extract_first():
                        LevelsorStories = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Structure Type' in r.css('::text').extract_first():
                        StructureType = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'House Style' in r.css('::text').extract_first():
                        HouseStyle = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Total Area Sqft' in r.css('::text').extract_first():
                        TotalAreaSqft = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Year Built Details' in r.css('::text').extract_first():
                        YearBuiltDetails = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Architectural Style' in r.css('::text').extract_first():
                        ArchitecturalStyle = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
            if 'Utilities' in res.css('h4::text').extract_first():
                for r in res.css('ul li'):
                    if 'Sewer' in r.css('::text').extract_first():
                        Sewer = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                    if 'Water Source' in r.css('::text').extract_first():
                        WaterSource = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
        cur.execute(
            'INSERT INTO public.realtortable("PropertyUrl", "ListingType", description, bedroom, "TotalBathrooms", "FullBathrooms", "HalfBathrooms", "BathroomDescription", "InteriorFeatures", "CoolingFeatures", "HeatingFeatures", "DiningRoomDescription", "ExteriorandLotFeatures", "WaterFeatures", "WaterfrontDescription", "PoolFeatures", "PoolDescription", "ManufacturedMode", "GarageSpaces", "ParkingFeatures", "HomeFeaturesView", "OtherEquipment", "ElementarySchool", "HighSchool", "MiddleSchool", "AssociationFeeAmenitie", "Association", "AssociationAmenities", "AssociationFee", "AssociationFeeFrequency", "CalculatedTotalMonthlyAssociation", "MaintenanceDescription", "PetDescription", "AnnualTaxAmount", "SourceListingStatus", "County", "Directions", "TaxYear", "Restrictions", "SourcePropertyType", "Area", "SourceNeighborhood", "PostalCode", "PublicSurveySection", "Subdivision", "Zoning", "SourceSystemName", "TotalSquareFeetLiving", "YearBuilt", "ConstructionMaterials", "DirectionFaces", "PropertyAge", "Roof", "LevelsorStories", "StructureType", "HouseStyle", "TotalAreaSqft", "YearBuiltDetails", "ArchitecturalStyle", "Sewer", "WaterSource")' + f"VALUES ('{link}', '{ListingType}', '{description}', '{bedroom}', '{TotalBathrooms}', '{FullBathrooms}', '{HalfBathrooms}', '{BathroomDescription}', '{InteriorFeatures}', '{CoolingFeatures}', '{HeatingFeatures}', '{DiningRoomDescription}', '{ExteriorandLotFeatures}', '{WaterFeatures}', '{WaterfrontDescription}', '{PoolFeatures}', '{PoolDescription}', '{Mode}', '{GarageSpaces}', '{ParkingFeatures}', '{View}', '{OtherEquipment}', '{ElementarySchool}', '{HighSchool}', '{MiddleSchool}', '{AssociationFeeAmenitie}', '{Association}', '{AssociationAmenities}', '{AssociationFee}', '{AssociationFeeFrequency}', '{CalculatedTotalMonthlyAssociation}', '{MaintenanceDescription}', '{PetDescription}', '{AnnualTaxAmount}', '{SourceListingStatus}', '{County}', '{Directions}', '{TaxYear}', '{Restrictions}', '{SourcePropertyType}', '{Area}', '{SourceNeighborhood}', '{PostalCode}', '{PublicSurveySection}', '{Subdivision}', '{Zoning}', '{SourceSystemName}', '{TotalSquareFeetLiving}', '{YearBuilt}', '{ConstructionMaterials}', '{DirectionFaces}', '{PropertyAge}', '{Roof}', '{LevelsorStories}', '{StructureType}', '{HouseStyle}', '{TotalAreaSqft}', '{YearBuiltDetails}', '{ArchitecturalStyle}', '{Sewer}', '{WaterSource}')" + 'ON CONFLICT ( "PropertyUrl" ) DO UPDATE SET "PropertyUrl" = excluded."PropertyUrl"')
        connection.commit()
    elif 'Property Details' in ''.join(response.css('#ldp-collapsed-property-details h2::text').extract()).strip():
        link = link
        try:
            ListingType = response.css('#ldp-hero-photo-wrap > div.photo-control.control-bottom.hero-photo-controls.js-hero-photo-controls > div.ldp-property-status.visible-lg-inline.visible-md-inline.display-inline-block > div > span::text').extract_first()
        except:
            try:
                ListingType = response.css('#__next > div:nth-child(2) > div > div:nth-child(3) > div > div > section.hero-carousel > div.jsx-3501245071.photo-gallery-overlay > div.jsx-3542126314.property-labels > span.jsx-3484526439.label.label-dark-transparent::text').extract_first()
            except:
                try:
                    ListingType = response.css('#label-sold::text').extract_first()
                except:
                    ListingType = ''
        try:
            description = ''.join(response.css('#ldp-detail-overview ::text').extract()).strip().replace('\n', '').replace(' ', '').replace("'", "")
        except:
            description = 'unavailable'
        j = 0
        for i, res in enumerate(response.css('#load-more-features .row')):
            for re in res.css('.col-lg-3.col-sm-6.col-xs-6.col-xxs-12.ldp-features-image-tag'):
                if 'Bedrooms' in re.css('h4::text').extract_first():
                    bedroom = re.css('ul li::text').extract_first().split(':')[-1].strip().replace("'", "")
                if 'Bathrooms' in re.css('h4::text').extract_first():
                    for r in re.css('ul li'):
                        if 'Total Bathrooms' in r.css('::text').extract_first():
                            TotalBathrooms = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Full Bathrooms' in r.css('::text').extract_first():
                            FullBathrooms = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if '1/2 Bathrooms' in r.css('::text').extract_first():
                            HalfBathrooms = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Bathroom Description' in r.css('::text').extract_first():
                            BathroomDescription = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
            if i == 0:
                continue

            if 'Interior Features' in response.css('#load-more-features h4.title-subsection-sm.font-bold')[
                j].css('::text').extract_first():
                InteriorFeatures = ''.join(res.css(' ::text').extract()).strip().replace("'", "")

            if 'Heating and Cooling' in response.css('#load-more-features h4.title-subsection-sm.font-bold')[
                j].css('::text').extract_first():
                for re in res.css('.list-default'):
                    for r in re.css('li'):
                        if 'Cooling Features' in r.css('::text').extract_first():
                            CoolingFeatures = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Heating Features' in r.css('::text').extract_first():
                            HeatingFeatures = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")

            if 'Kitchen and Dining' in response.css('#load-more-features h4.title-subsection-sm.font-bold')[
                j].css('::text').extract_first():
                for re in res.css('.list-default'):
                    for r in re.css('li'):
                        if 'Dining Room Description' in r.css('::text').extract_first():
                            DiningRoomDescription = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")

            if 'Exterior and Lot Features' in response.css('#load-more-features h4.title-subsection-sm.font-bold')[j].css('::text').extract_first():
                ExteriorandLotFeatures = ''.join(res.css(' ::text').extract()).strip().replace("'", "")

            if 'Waterfront and Water Access' in response.css('#load-more-features h4.title-subsection-sm.font-bold')[j].css('::text').extract_first():
                for re in res.css('.list-default'):
                    for r in re.css('li'):
                        if 'Water Features' in r.css('::text').extract_first():
                            WaterFeatures = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Waterfront Description' in r.css('::text').extract_first():
                            WaterfrontDescription = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")

            if 'Pool and Spa' in response.css('#load-more-features h4.title-subsection-sm.font-bold')[j].css('::text').extract_first():
                for re in res.css('.list-default'):
                    for r in re.css('li'):
                        if 'Pool Features: Pool YN' in r.css('::text').extract_first():
                            PoolFeatures = r.css('::text').extract_first().split('YN:')[-1].split(',')[
                                0].strip().replace("'", "")
                        if 'Pool Description' in r.css('::text').extract_first():
                            PoolDescription = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")

            if 'Manufactured and Mobile Info' in response.css('#load-more-features h4.title-subsection-sm.font-bold')[j].css('::text').extract_first():
                for re in res.css('.list-default'):
                    for r in re.css('li'):
                        if 'Mode' in r.css('::text').extract_first():
                            Mode = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")

            if 'Garage and Parking' in response.css('#load-more-features h4.title-subsection-sm.font-bold')[j].css('::text').extract_first():
                for re in res.css('.list-default'):
                    for r in re.css('li'):
                        if 'Garage Spaces' in r.css('::text').extract_first():
                            GarageSpaces = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Parking Features' in r.css('::text').extract_first():
                            ParkingFeatures = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")

            if 'Home Features' in response.css('#load-more-features h4.title-subsection-sm.font-bold')[j].css('::text').extract_first():
                for re in res.css('.list-default'):
                    for r in re.css('li'):
                        if 'View' in r.css('::text').extract_first():
                            View = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Other Equipment' in r.css('::text').extract_first():
                            OtherEquipment = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")

            if 'School Information' in response.css('#load-more-features h4.title-subsection-sm.font-bold')[j].css('::text').extract_first():
                for re in res.css('.list-default'):
                    for r in re.css('li'):
                        if 'Elementary School' in r.css('::text').extract_first():
                            ElementarySchool = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'High School' in r.css('::text').extract_first():
                            HighSchool = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Middle School' in r.css('::text').extract_first():
                            MiddleSchool = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")

            if 'Homeowners Association' in response.css('#load-more-features h4.title-subsection-sm.font-bold')[j].css('::text').extract_first():
                for re in res.css('.list-default'):
                    for r in re.css('li'):
                        if 'Association Fee Amenitie' in r.css('::text').extract_first():
                            AssociationFeeAmenitie = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Association:' in r.css('::text').extract_first():
                            Association = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Association Amenities:' in r.css('::text').extract_first():
                            AssociationAmenities = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Association Fee:' in r.css('::text').extract_first():
                            AssociationFee = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Association Fee Frequency:' in r.css('::text').extract_first():
                            AssociationFeeFrequency = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Calculated Total Monthly Association' in r.css('::text').extract_first():
                            CalculatedTotalMonthlyAssociation = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Maintenance Description' in r.css('::text').extract_first():
                            MaintenanceDescription = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Pet Description' in r.css('::text').extract_first():
                            PetDescription = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")

            if 'Other Property Info' in response.css('#load-more-features h4.title-subsection-sm.font-bold')[j].css('::text').extract_first():
                for re in res.css('.list-default'):
                    for r in re.css('li'):
                        if 'Annual Tax Amount' in r.css('::text').extract_first():
                            AnnualTaxAmount = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Source Listing Status' in r.css('::text').extract_first():
                            SourceListingStatus = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'County' in r.css('::text').extract_first():
                            County = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Directions' in r.css('::text').extract_first():
                            Directions = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Tax Year' in r.css('::text').extract_first():
                            TaxYear = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Restrictions' in r.css('::text').extract_first():
                            Restrictions = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Source Property Type' in r.css('::text').extract_first():
                            SourcePropertyType = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Area' in r.css('::text').extract_first():
                            Area = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Source Neighborhood' in r.css('::text').extract_first():
                            SourceNeighborhood = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Postal Code' in r.css('::text').extract_first():
                            PostalCode = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Public Survey Section' in r.css('::text').extract_first():
                            PublicSurveySection = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Subdivision' in r.css('::text').extract_first():
                            Subdivision = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Zoning' in r.css('::text').extract_first():
                            Zoning = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Source System Name' in r.css('::text').extract_first():
                            SourceSystemName = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")

            if 'Building and Construction' in response.css('#load-more-features h4.title-subsection-sm.font-bold')[j].css('::text').extract_first():
                for re in res.css('.list-default'):
                    for r in re.css('li'):
                        if 'Total Square Feet Living' in r.css('::text').extract_first():
                            TotalSquareFeetLiving = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Year Built' in r.css('::text').extract_first():
                            YearBuilt = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Construction Materials' in r.css('::text').extract_first():
                            ConstructionMaterials = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Direction Faces' in r.css('::text').extract_first():
                            DirectionFaces = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Property Age' in r.css('::text').extract_first():
                            PropertyAge = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Roof' in r.css('::text').extract_first():
                            Roof = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Levels or Stories' in r.css('::text').extract_first():
                            LevelsorStories = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Structure Type' in r.css('::text').extract_first():
                            StructureType = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'House Style' in r.css('::text').extract_first():
                            HouseStyle = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Total Area Sqft' in r.css('::text').extract_first():
                            TotalAreaSqft = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Year Built Details' in r.css('::text').extract_first():
                            YearBuiltDetails = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Architectural Style' in r.css('::text').extract_first():
                            ArchitecturalStyle = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")

            if 'Utilities' in response.css('#load-more-features h4.title-subsection-sm.font-bold')[j].css('::text').extract_first():
                for re in res.css('.list-default'):
                    for r in re.css('li'):
                        if 'Sewer' in r.css('::text').extract_first():
                            Sewer = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")
                        if 'Water Source' in r.css('::text').extract_first():
                            WaterSource = r.css('::text').extract_first().split(':')[-1].strip().replace("'", "")

            j += 1
        cur.execute(
            'INSERT INTO public.realtortable("PropertyUrl", "ListingType", description, bedroom, "TotalBathrooms", "FullBathrooms", "HalfBathrooms", "BathroomDescription", "InteriorFeatures", "CoolingFeatures", "HeatingFeatures", "DiningRoomDescription", "ExteriorandLotFeatures", "WaterFeatures", "WaterfrontDescription", "PoolFeatures", "PoolDescription", "ManufacturedMode", "GarageSpaces", "ParkingFeatures", "HomeFeaturesView", "OtherEquipment", "ElementarySchool", "HighSchool", "MiddleSchool", "AssociationFeeAmenitie", "Association", "AssociationAmenities", "AssociationFee", "AssociationFeeFrequency", "CalculatedTotalMonthlyAssociation", "MaintenanceDescription", "PetDescription", "AnnualTaxAmount", "SourceListingStatus", "County", "Directions", "TaxYear", "Restrictions", "SourcePropertyType", "Area", "SourceNeighborhood", "PostalCode", "PublicSurveySection", "Subdivision", "Zoning", "SourceSystemName", "TotalSquareFeetLiving", "YearBuilt", "ConstructionMaterials", "DirectionFaces", "PropertyAge", "Roof", "LevelsorStories", "StructureType", "HouseStyle", "TotalAreaSqft", "YearBuiltDetails", "ArchitecturalStyle", "Sewer", "WaterSource")' + f"VALUES ('{link}', '{ListingType}', '{description}', '{bedroom}', '{TotalBathrooms}', '{FullBathrooms}', '{HalfBathrooms}', '{BathroomDescription}', '{InteriorFeatures}', '{CoolingFeatures}', '{HeatingFeatures}', '{DiningRoomDescription}', '{ExteriorandLotFeatures}', '{WaterFeatures}', '{WaterfrontDescription}', '{PoolFeatures}', '{PoolDescription}', '{Mode}', '{GarageSpaces}', '{ParkingFeatures}', '{View}', '{OtherEquipment}', '{ElementarySchool}', '{HighSchool}', '{MiddleSchool}', '{AssociationFeeAmenitie}', '{Association}', '{AssociationAmenities}', '{AssociationFee}', '{AssociationFeeFrequency}', '{CalculatedTotalMonthlyAssociation}', '{MaintenanceDescription}', '{PetDescription}', '{AnnualTaxAmount}', '{SourceListingStatus}', '{County}', '{Directions}', '{TaxYear}', '{Restrictions}', '{SourcePropertyType}', '{Area}', '{SourceNeighborhood}', '{PostalCode}', '{PublicSurveySection}', '{Subdivision}', '{Zoning}', '{SourceSystemName}', '{TotalSquareFeetLiving}', '{YearBuilt}', '{ConstructionMaterials}', '{DirectionFaces}', '{PropertyAge}', '{Roof}', '{LevelsorStories}', '{StructureType}', '{HouseStyle}', '{TotalAreaSqft}', '{YearBuiltDetails}', '{ArchitecturalStyle}', '{Sewer}', '{WaterSource}')" + 'ON CONFLICT ( "PropertyUrl" ) DO UPDATE SET "PropertyUrl" = excluded."PropertyUrl"')
        connection.commit()


def parsewebpages(link):
    driver.get(link)
    response = scrapy.Selector(text=driver.page_source)
    if len(response.css('ul[data-testid="property-list-container"] li[data-testid="result-card"]')) == 0:
        for res in response.css('ul.srp-list-marginless.list-unstyled.prop-list li.component_property-card.js-component_property-card'):
            link = 'https://www.realtor.com' + res.css('::attr(href)').extract_first()
            linkslist.append(link)

    else:
        for res in response.css('ul[data-testid="property-list-container"] li[data-testid="result-card"]'):
            link = 'https://www.realtor.com' + res.css('::attr(href)').extract_first()
            linkslist.append(link)


def parsepage(link):
    driver.get(url=link)
    response = scrapy.Selector(text=driver.page_source)
    if 'Pardon Our Interruption' in response.css('body > div > div:nth-child(3) > h1 ::text').extract_first(''):
        driver.switch_to.frame(driver.find_element_by_xpath("#px-captcha"))
        driver.switch_to.frame(driver.find_element_by_xpath("body > div > iframe:nth-child(9)"))
        actions = ActionChains(driver)
        actions.click_and_hold(on_element=driver.find_element_by_xpath('//*[@id="px-captcha"]'))
        response = scrapy.Selector(text=driver.page_source)
        # clkAndHld.clickAndHold(WebElement).build().perform()
    try:
        total_pages = int(response.css('.pagination span.page')[-1].css('a::text').extract_first())
        i = 1
        while i <= total_pages:
            lnk = link + f'/pg-{i}/'
            urlpagelist.append(lnk)
            i += 1
    except:
        try:
            total_pages = int(
                response.css('div[data-testid="pagination"] .item')[-2].css('::text').extract_first())
            i = 1
            while i <= total_pages:
                lnk = link + f'/pg-{i}/'
                urlpagelist.append(lnk)
                i += 1
        except:
            parsepage(link)


if __name__ == '__main__':
    postcodeurllist = []
    urlpagelist = []
    linkslist = []
    connection = psycopg2.connect(
        host='localhost',
        database='realtordb',
        user='postgres',
        password='123456789',
        port='8080'
    )
    cur = connection.cursor()
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome()
    filezip = open('zipcodes.txt', 'r')
    zipcode = filezip.read().split('\n')

    postcodes = [z.strip() for z in zipcode if z.strip()]
    for pc in postcodes:
        urlsold = f'https://www.realtor.com/soldhomeprices/{pc}'
        postcodeurllist.append(urlsold)
    for pc in postcodes:
        urlbuy = f'https://www.realtor.com/realestateandhomes-search/{pc}'
        postcodeurllist.append(urlbuy)

    for link in postcodeurllist:
        parsepage(link)

    for link in urlpagelist:
        parsewebpages(link)

    for link in linkslist:
        parse_data(link)

    driver.quit()
    connection.close()
