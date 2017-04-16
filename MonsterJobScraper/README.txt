                            MONSTER JOB SCRAPER




--      DEPENDENCIES FOR SCRIPT   --

Python version - 2.7
BeautofulSoup
selenium         [http://selenium-python.readthedocs.io/installation.html]
phantomjs        [Download executable from here - http://phantomjs.org/download.html and store in project directory]
mysql-python

Alternatively pip can be used to install dependencies as  BeautofulSoup,mysqldb-python,selenium



----------------------------------------------------------------------------------------------------------------------------




-  HOW TO USE  -


Script Takes two input parameters - Keyword + Timeline(Number of days jobs posted)
i.e. -
>    Python MonsteJobsScraper 'Java' 7

                 OR

>    Python MonsterJobScraper 'Android Developer' 3





----------------------------------------------------------------------------------------------------------------------------



    --    MODULE DETAILS      --


Module has 2main files -      MonsterJobScraper.py + MySqlDB.py.
   -  MySqlDB            ->     handles DB search and update part.
   -  MonsterJobScraper  ->     Scrape records + JD.

-All Job Description will be saved in outputJobs folder and filename will be saved in MySQLDB.

-Logfile will be by the name - ghostdriver.log (phantomjs driver logs)  +   MonsterJobs.log (Module logs).

-Database tables are stored in DB-schema file.

-Added comment in each function defination to ease understanding.




----------------------------------------------------------------------------------------------------------------------------