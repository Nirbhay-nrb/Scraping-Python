from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# url of the website
url = 'https://hprera.nic.in/PublicDashboard'

# initialising the driver
driver = webdriver.Chrome()
driver.implicitly_wait(10) # implicit wait for 10 seconds for elements to load before fetching them

# opening the website and maximising the window
driver.get(url)
driver.maximize_window()
time.sleep(5) # waiting for the elements in the page to load

# finding the projects section and extracting the list of projects
# path : reg-Projects > form-row > col-lg-6 (multiple elements with this ID)
projects_section = driver.find_element(By.ID, 'reg-Projects')
form_row = projects_section.find_element(By.CLASS_NAME, 'form-row')
projects_list = form_row.find_elements(By.CLASS_NAME, 'col-lg-6')

# declaration of the final list of projects and the tags that need to be checked
projects = [] # final list to be displayed
toCheck = ['Name', 'Permanent Address','GSTIN No.', 'PAN No.']

# iterating all the projects 
for project in projects_list:
    flag = True # flag to check if the project has all the required tags
    if len(projects) == 5:
        break # breaks the loop when the final list has 5 projects
    project_desc = {} # dictionary to store the details of the current project
    # getting the name of the project 
    name = project.find_element(By.TAG_NAME,'span')
    project_desc['Project Name'] = name.text
    # clicking the rera number link to open up the window
    rera_number = project.find_element(By.TAG_NAME,'a')
    rera_number.click()
    time.sleep(3) # 3 second wait for the details to load

    # switching the driver to the new window
    modal_window_handle = driver.window_handles[-1]
    driver.switch_to.window(modal_window_handle)
    # extracting the rows of the table where the details are stored
    table_rows = driver.find_elements(By.TAG_NAME, 'tr')
    for row in table_rows:
        # iterating over each row 
        table_cells = row.find_elements(By.TAG_NAME, 'td')
        if table_cells[0].text in toCheck: # if the field is present in the toCheck List
            if table_cells[1].text == '-NA-': # if the value of the field is -NA- (empty), then set the flag as FALSE and continue to the next row
                flag = False
                continue
            project_desc[table_cells[0].text] = table_cells[1].text # adding the field and its value to the dictionary
    if flag: # if the flag is true, then all the tags have been checked and the project is added to the final list
        projects.append(project_desc)
    # closing the modal window
    close_button = driver.find_element(By.XPATH, '//button[contains(text(), "Close")]') 
    close_button.click() 
    # switching the driver back to the main window 
    driver.switch_to.window(driver.window_handles[0])

# Close the browser window
driver.quit()

# printing the final list of projects
print('------FINAL PROJECTS LIST------')
i = 1
for project in projects:
    print('Project '+str(i)+':')
    for key in project:
        print(key+' : '+project[key])
    print('-----------------------------')
    i += 1