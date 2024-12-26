'''
   _____      __                 __  __                   
  / ___/___  / /___  ______     / / / /_______  __________
  \__ \/ _ \/ __/ / / / __ \   / / / / ___/ _ \/ ___/ ___/
 ___/ /  __/ /_/ /_/ / /_/ /  / /_/ (__  )  __/ /  (__  ) 
/____/\___/\__/\__,_/ .___/   \____/____/\___/_/  /____/  
                   /_/                                    
'''
USE ROLE USERADMIN;

CREATE USER IF NOT EXISTS TimExamUser
    PASSWORD = 'TimExamUser123'
    DEFAULT_WAREHOUSE = exam_wh;

CREATE USER IF NOT EXISTS KristoferExamUser
    PASSWORD = 'KristoferExamUser123'
    DEFAULT_WAREHOUSE = exam_wh;