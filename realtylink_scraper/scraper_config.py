import dataclasses


CLASS_PAGE_PAGINATION = "pager-current"
CLASS_RESID_LINK = "property-thumbnail-summary-link"
CLASS_NEXT_BUTTON = "next"
CLASS_IMG_NEXT_BUTTON = "nav-next"


CSS_IMAGE_LIB = "a[onclick*='addDataLayerPhotoViewer']"
CSS_IMAGE_OBJECT = ".description strong"

XPATH_TITLE = '//h1[@itemprop="category"]/span[@data-id="PageTitle"]'
XPATH_REGION = '//*[@id="overview"]/div[1]/div[1]/div/div[1]/div[1]/h2'
XPATH_ADDRESS = '//*[@id="overview"]/div[1]/div[1]/div/div[1]/div[1]/h2'
XPATH_DESCR = '//*[@id="overview"]/div[3]/div[2]/div/div[2]'
XPATH_PRICE = '/html/body/main/div[7]/div[2]/div/div[2]/div[1]/div/div[3]/div/article/div[1]/div[1]/div/div[2]/div[1]/span[4]'
XPATH_BEDROOM = '/html/body/main/div[7]/div[2]/div/div[2]/div[1]/div/div[3]/div/article/div[3]/div[1]/div[4]/div[2]'
XPATH_FLOOR_AREA = '/html/body/main/div[7]/div[2]/div/div[2]/div[1]/div/div[3]/div/article/div[3]/div[1]/div[6]/div[1]/div[2]/span'


@dataclasses.dataclass
class Residence:
    link: str
    title: str
    region: str
    address: str
    description: str
    image_links: list
    publish_date: str
    price: float
    bedrooms: int
    floor_area: int
