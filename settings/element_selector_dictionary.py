from enum import Enum
from selenium.webdriver.common.by import By


class Elements(Enum):
    LOGIN_BUTTON = "login_button"
    EMAIL = "email"
    PASSWORD = "password"
    PROFILE_BUTTON = "profile_button"
    JOB_DETAILS = "job_details"
    ALL="all"
    SEARCH_FIELD="search"
    SEARCH_FIELD_MAIN="search_main"
    SEARCH_LIST_BANNER="search_list_banner"
    COLLAPSED_SEARCH_BUTTON="collapsed_search_button"
    SEE_ALL_RESULTS="see_all_results"
    JOB_VIEW_MORE_BUTTON="job_view_more_button"
    JOB_SEARCH_BOX ="job_search_box"
    JOB_PAGE_TITLE="job_page_title"
    JOB_PAGE_DETAILS="job_page_details"
    JOB_PAGE_COMPANY_NAME_LOCATION="job_page_company_name_location"
    JOB_PAGE_APPLY_ERROR="job_page_apply_error"
    JOB_PAGE_SKILLS_MATCH="job_page_skills_match"



elements={
    Elements.LOGIN_BUTTON:{ "selectBy":By.CSS_SELECTOR,"selector":'[data-id="sign-in-form__submit-btn"]'},
    Elements.EMAIL:{ "selectBy":By.ID,"selector":"session_key"},
    Elements.PASSWORD:{ "selectBy":By.ID,"selector":"session_password"},
    Elements.PROFILE_BUTTON:{ "selectBy":By.XPATH,"selector":"//*[contains(@class, 'feed-identity-module__member-photo')]"},
    # Elements.JOB_DETAILS:{ "selectBy":By.XPATH,"selector": '//*[contains(@class, "jobs-description-content")]'},
    Elements.ALL:{"selectBy":By.XPATH,"selector":"//*"},
    Elements.SEARCH_FIELD:{"selectBy":By.XPATH,"selector":"//*[contains(@class, 'jobs-search-box__text-input')]"},
    Elements.SEARCH_LIST_BANNER:{"selectBy":By.XPATH,"selector":"//*[contains(@class, 'jobs-search-results-list__header')]"},
    Elements.SEARCH_FIELD_MAIN:{"selectBy":By.XPATH,"selector":"//*[contains(@class, 'search-global-typeahead__input')]"},
    Elements.JOB_SEARCH_BOX:{"selectBy":By.XPATH,"selector":"//*[contains(@class, 'jobs-search-box__text-input')]"},
    # Elements.COLLAPSED_SEARCH_BUTTON:{"selectBy":By.XPATH,"selector":"//*[contains(@class, 'typeahead-suggestion search-global-typeahead__suggestion')]"}
    Elements.COLLAPSED_SEARCH_BUTTON:{"selectBy":By.XPATH,"selector":"//*[contains(@class, 'search-global-typeahead__suggestion')]//div[contains(@class, 'search-global-typeahead-hit--escape-hatch')]"},
    Elements.SEE_ALL_RESULTS:{"selectBy":By.XPATH,"selector":"//*[contains(@class, 'search-results__cluster-bottom-banner')]"},
    Elements.JOB_VIEW_MORE_BUTTON:{"selectBy":By.XPATH,"selector":"//*[contains(@class, 'jobs-description__footer-button')]"},
    Elements.JOB_PAGE_TITLE:{"selectBy":By.XPATH,"selector":"//*[contains(@class, 'job-details-jobs-unified-top-card__job-title')]"},
    Elements.JOB_PAGE_DETAILS:{"selectBy":By.XPATH,"selector":"//*[contains(@class, 'job-details-jobs-unified-top-card__job-insight')]"},
    Elements.JOB_PAGE_COMPANY_NAME_LOCATION:{"selectBy":By.XPATH,"selector":"//*[contains(@class, 'job-details-jobs-unified-top-card__primary-description')]"},
    Elements.JOB_PAGE_APPLY_ERROR:{"selectBy":By.XPATH,"selector":"//*[contains(@class, 'jobs-details-top-card__apply-error')]"},
    Elements.JOB_PAGE_SKILLS_MATCH:{"selectBy":By.XPATH,"selector":"//*[contains(@class, 'job-details-how-you-match__skills-item-wrapper')]"},
}
    
    
# element = driver.find_element_by_xpath("//div[contains(@class, 'typeahead-suggestion') and contains(@class, 'search-global-typeahead__suggestion')]//div[contains(@class, 'search-global-typeahead-hit')]")
# https://www.w3schools.com/xml/xpath_syntax.asp

# { "selectBy":By.XPATH,"selector":"//*[contains(@class, 'identity')]"}
# This will find the first element on the page whose class attribute contains the word "username".
# You can modify the XPath expression to match other patterns as well

# Find the parent element based on criteria for its child
# parent_element = driver.find_element_by_xpath("//div[contains(@class, 'parent-class')]/child::tag[child-criteria]")


# identify element with partial class match with * in css
# driver.findElement(By.cssSelector("input[class*='input']"));

# identify element with partial class match with ^ in css
# driver.findElement(By.cssSelector("input[class^='gsc']"));

# identify element with partial class match with $ in css
# driver.findElement(By.cssSelector("input[class$='put']"));

# identify element with partial class match with contains in xpath
# driver.findElement(By.xpath("//input[contains(@class,'input')]"));

# identify element with partial class match with starts-with in xpath
# driver.findElement(By.xpath("//input[starts-with(@class,'gsc')]"));