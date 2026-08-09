#####################################
#
# Core data shapes passed beteen the scraper, pipeline, and UI.
#
#####################################
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from datetime import datetime, timedelta

#
# Default listing date range is from 2days - 2weeks old
#
DEFAULT_LISTING_TIMEDELTA_DAYS = 14  # default listing age range for SearchCriteria
DEFAULT_LISTING_TIMEDELTA_WEEKS = 2 # Redundent, days are perfered

DEFAULT_MOST_RECENT_LISTING_DATE = datetime.now() - timedelta(days=2) # default earliest listing date for SearchCriteria


#####################################
#
# SearchCriteria obtained from the user wizard.
# 
#####################################

#
# Configure for default notification method wizzard settings
# 
def set_default_notification_methods():    
    methods = [{"email": True}, {"sms": False}, {"dashboard": False}]
    
    # NOTE: uncomment to set default notificaiton methods all to True
    #return [{method: True} for method in methods]
    
    # NOTE: uncomment to set default notificaiton methods all to False
    #return [{method: False} for method in methods]
    
    return methods

#
# Structure of wizzard output, used to filter and score listings in the pipeline
#
@dataclass(repr=False,eq=True)
class SearchCriteria:
    #
    # From wizzard page "Welcome"
    #
    user_name: Optional[str] = None # User's name (string), used in other parts of program to be more personal
    # TODO: Is UUID created now or in sqlite pipeline?
    search_ID: int = 0 # Unique ID for the search criteria, used to identify the search criteria in the DB and other parts of the program
    
    #
    # From wizzard page "Preferences"
    #
    job_titles: List[str] = field(default_factory=list) # Select one or more from list of job titles (strings) inside of Job_Title_Database
    experience_level: List[str] = field(default_factory=list) # Select one or more from list of experience levels (strings) inside of Experience_Level_Database
    employment_type: List[str] = field(default_factory=list) # Select one or more from list of employment types (strings) inside of Employment_Type_Database
    company_size: List[str] = field(default_factory=list) # Select one or more from list of company sizes (strings) inside of Company_Size_Database
    primary_business_group: List[str] = field(default_factory=list) # Select one or more from list of primary business groups (strings) inside of Primary_Business_Group_Database
    salary_range: List[str] = field(default_factory=list) # Select one or more from list of salary ranges (strings) inside of Salary_Range_Database

    #
    # From wizzard page "Target Locations"
    #
    target_locations: List[str] = field(default_factory=list) # Select one or more from list of target locations (strings)()
    
    #
    # From wizzard page "Target Companies"
    #
    target_companies: List[str] = field(default_factory=list) # Select one or more from list of target companies (strings) inside of Target_Companies_Database
    
    #
    # From wizzard page "Upload Resume"
    # TODO: Consider changing this to a file path or a file object instead of a string, depending on how the resume is handled in the application/ able to be stored in DB.
    #       Can always convert to Path(str) in scraping logic and store as string in DB.
    resume_file_path: Optional[str] = field(default=None) # Path to the uploaded resume file (string)
    
    #
    # From wizzard page "Finish / Summary"
    #
    notification_methods: List[Dict[str, bool]] = field(default_factory=set_default_notification_methods) # Select to change default notification methods (email, sms, dashboard) from the options provided in the Finish / Summary page
    
    # Contact information for notifications, if none is requested, information will populate to dashboard when user opens application
    email_address: Optional[str] = field(default=None) # Email address for email notifications (string)
    sms_number: Optional[str] = field(default=None) # Phone number for SMS notifications (string)
    dashboard_notifications: Optional[bool] = field(default=None) # Whether to show notifications on the dashboard (boolean)
    
    most_recent_listing_age: datetime = field(default=DEFAULT_MOST_RECENT_LISTING_DATE)
    listing_age_range: timedelta = field(default=timedelta(days=DEFAULT_LISTING_TIMEDELTA_DAYS)) # Select a listing age range (timedelta) from the options provided in the Finish / Summary page
    # Listings will have to be within the range of [earliest_listing_date: datetime, earliest_listing_date - listing_age_range: timedelta]
    # Will create time window for listings age in later logic

#####################################
#
# JobListing result obtained from the scraper, scored by the pipeline, and stored in the DB.
# The dashboard access these listings from the DB
#
#####################################
@dataclass(repr=True,eq=True)
class JobListing:

    title: str
    company: str
    url: str
    location: str = ""
    salary: str = ""  # raw text; parse to a number in the pipeline if needed
    description: str = ""
    source: str = ""
    score: float = 0.0  # filled in by pipeline.py
    #id: str = 0 # UUID for the job listing used to ensure no duplicates. Uses hash of other fields to generate a unique ID

    def as_row(self) -> tuple:
        """Flat tuple for SQLite inserts (order must match storage.py)."""
        return (
            self.title,
            self.company,
            self.url,
            self.location,
            self.salary,
            self.description,
            self.source,
            self.score,
            self.id
        )
