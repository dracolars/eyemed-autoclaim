import tkinter.messagebox
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from tkinter import *
from tkinter import ttk

class EyemedInterface:
    # GUI COMPONENTS
    def __init__(self, master):

        #GUI COMPONENTS
        frameTop = Frame(master)
        frameTop.grid(row=0)
        frameMiddle = Frame(master)
        frameMiddle.grid(row=1)
        frameBottom = Frame(master)
        frameBottom.grid(row=2)

        master.grid_rowconfigure(1, weight=1)
        master.grid_columnconfigure(1, weight=1)
        #menu bar
        menu = Menu()
        master.config(menu=menu)
        subMenu = Menu(menu)
        menu.add_cascade(label="File", menu=subMenu)
        subMenu.add_command(label="New...", command=self.doNothing)
        subMenu.add_command(label="Fake Save", command=self.doNothing)
        subMenu.add_separator()
        subMenu.add_command(label="Exit", command=self.doNothing)
        editMenu = Menu(menu)
        menu.add_cascade(label="Edit", menu=editMenu)
        editMenu.add_command(label="Redo", command=self.doNothing)

        #status bar
        self.statusBar = Label(frameBottom, text="Preparing claim...", bd=1, relief=SUNKEN, anchor=W, width=40)
        #Dr list array
        doctorList = ["Dr. Jennifer Bird", "Dr. Derek Le"]

        #labels and input fields
        idLabel = Label(frameMiddle, text="Patient ID: ")
        self.idEntry = ttk.Entry(frameMiddle, width=17)
        dateLabel = Label(frameMiddle, text="Service Date: ")
        self.dateEntry = ttk.Entry(frameMiddle, width=17)
        self.doctorSelectionVar = StringVar(master)
        self.doctorSelectionVar.set(doctorList[0])
        self.doctorSelection = OptionMenu(frameMiddle, self.doctorSelectionVar, *doctorList)

        examLabel = Label(frameMiddle, text="Exam Type:")
        self.newExamVar = IntVar()
        self.establishedExamVar = IntVar()
        self.contactFitStandardVar = IntVar()
        self.contactFitSpecialtyVar = IntVar()
        self.newExam = ttk.Checkbutton(frameMiddle, text="NEW Patient Exam", variable=self.newExamVar, onvalue=1, offvalue=0)
        self.establishedExam = ttk.Checkbutton(frameMiddle, text="Established Patient Exam",
                                           variable=self.establishedExamVar, onvalue=1, offvalue=0)
        self.contactFitStandard = ttk.Checkbutton(frameMiddle, text="Standard Contact Fitting",
                                              variable=self.contactFitStandardVar, onvalue=1, offvalue=0)
        self.contactFitSpecialty = ttk.Checkbutton(frameMiddle, text="Specialty Contact Fitting",
                                               variable=self.contactFitSpecialtyVar, onvalue=1, offvalue=0)

        diagnosisCodeLabel = Label(frameMiddle, text="Diagnosis Code(s):")
        self.h5203Var = IntVar()
        self.h5213Var = IntVar()
        self.h52223Var = IntVar()
        self.h524Var = IntVar()
        self.Z0100Var = IntVar()
        self.h5203 = ttk.Checkbutton(frameMiddle, text="H52.03", variable=self.h5203Var, onvalue=1, offvalue=0)
        self.h5213 = ttk.Checkbutton(frameMiddle, text="H52.13", variable=self.h5213Var, onvalue=1, offvalue=0)
        self.h52223 = ttk.Checkbutton(frameMiddle, text="H52.223", variable=self.h52223Var, onvalue=1, offvalue=0)
        self.h524 = ttk.Checkbutton(frameMiddle, text="H52.4", variable=self.h524Var, onvalue=1, offvalue=0)
        self.Z0100 = ttk.Checkbutton(frameMiddle, text="Z01.00", variable=self.Z0100Var, onvalue=1, offvalue=0)
        otherDiagnosis = Label(frameMiddle, text="Other:")
        self.otherDiagnosisEntry = Entry(frameMiddle, width=12)

        startButton = ttk.Button(frameMiddle, text="Start Claim",  command=self.printExam)
        startButton.bind("<Button-1>")

        #positioning
        idLabel.grid(row=1, sticky=E)  # sticky can be N, S, E, W
        self.idEntry.grid(row=1, column=1)
        dateLabel.grid(row=2, sticky=E)
        self.dateEntry.grid(row=2, column=1)
        self.doctorSelection.grid(row=3, columnspan=2)
        examLabel.grid(row=4, sticky=W)
        self.newExam.grid(row=5, sticky=W)
        self.establishedExam.grid(row=6, sticky=W)
        self.contactFitStandard.grid(row=7, sticky=W)
        self.contactFitSpecialty.grid(row=8, sticky=W)
        diagnosisCodeLabel.grid(row=4, column=1, sticky=W)
        self.h5203.grid(row=5, column=1, sticky=W)
        self.h5213.grid(row=6, column=1, sticky=W)
        self.h52223.grid(row=7, column=1, sticky=W)
        self.h524.grid(row=8, column=1, sticky=W)
        self.Z0100.grid(row=9, column=1, sticky=W)
        otherDiagnosis.grid(row=10, column=1, sticky=W)
        self.otherDiagnosisEntry.grid(row=10, column=1, sticky=E)
        startButton.grid(columnspan=2, row=11)
        self.statusBar.pack(side=BOTTOM, fill=X)
    # Print Statements to check input
    def printExam(self):
        #Claim Variables
        self.statusBar.config(text="Starting claim...", fg='black')
        patientId = self.idEntry.get()
        serviceDate = self.dateEntry.get()
        doctor = self.doctorSelectionVar.get()
        if patientId == '' or serviceDate == "" or doctor == "":
            self.statusBar.config(text="Patient ID or Service Date cannot be blank!", fg='red')
        print(patientId + " " + serviceDate + " " + doctor)
        examsToClaim = self.getExam()
        diagnosis = self.getDiagnosis()
        print(examsToClaim)
        print(diagnosis)
        if examsToClaim and diagnosis and patientId != '' and serviceDate != '':
            self.claim(patientId, examsToClaim, diagnosis, doctor, serviceDate)
    # Get procedure codes
    def getExam(self):
        examsToClaim = []
        newExam = self.newExamVar.get().__bool__()
        estExam = self.establishedExamVar.get().__bool__()
        stdFit = self.contactFitStandardVar.get().__bool__()
        specialtyFit = self.contactFitSpecialtyVar.get().__bool__()
        if newExam and not estExam:
            examsToClaim.append('92004')
            examsToClaim.append('92015')
        elif estExam and not newExam:
            examsToClaim.append('92014')
            examsToClaim.append('92015')
        if stdFit and not specialtyFit:
            examsToClaim.append('92310')
        elif specialtyFit and not stdFit:
            examsToClaim.append('9231025')

        if (stdFit and specialtyFit or newExam and estExam):
            self.statusBar.config(text="Wrong exam selection combination.", fg="red")
        elif (examsToClaim):
            return examsToClaim
        else:
            self.statusBar.config(text="Wrong exam selection combination.", fg="red")
    # Get diagnosis codes
    def getDiagnosis(self):
        diagnosisList = []
        if self.h5203Var.get() == 1:
            diagnosisList.append('H52.03')
        if self.h5213Var.get() == 1:
            diagnosisList.append('H52.13')
        if self.h52223Var.get() == 1:
            diagnosisList.append('H52.223')
        if self.h524Var.get() == 1:
            diagnosisList.append('H52.4')
        if self.Z0100Var.get() == 1:
            diagnosisList.append('Z01.00')
        if self.otherDiagnosisEntry.get != '':
            otherDiagnosis = self.otherDiagnosisEntry.get().split()
            for diagnosis in otherDiagnosis:
                diagnosisList.append(diagnosis)
        if diagnosisList:
             return diagnosisList
        else:
            self.statusBar.config(text="Please select diagnosis code.")


    # Function to check website element exists
    def check_exists_by_xpath(self, driver, xpath):
        try:
            driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True


    # Test Function for Submenu
    def doNothing(self):
        print('ok ok nothing')
        tkinter.messagebox.showinfo('Message Window', 'You have pressed a button!')


    # interaction with Eyemed Website
    def claim(self, patientId, exams, diagnosis, dr, date):
        # Opening Web Browser and Website
        driver = webdriver.Chrome('./chromedriver')
        url_to_search = 'https://claims.eyemedvisioncare.com/claims/loginForm.emvc'
        # Locating login fields
        driver.get(url_to_search)
        username_field = driver.find_element_by_xpath('//*[@id="username"]')
        password_field = driver.find_element_by_xpath('//*[@id="password"]')
        submit_field = driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div[2]/div[2]/table/tbody/tr/td/fieldset/table/tbody/tr/td/form/p[3]/span/input')
        # Entering login credentials
        username_field.send_keys('OFFICE-ID-GOES-HERE')
        password_field.send_keys('OFFICE-ACCOUNT-PASSWORD-GOES-HERE')
        submit_field.click()

        # Changing to search by ID tab
        member_id_tab = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/a')
        member_id_tab.click()
        self.statusBar.config(text="Successfully logged in")

        # Locating Member ID and Service Date fields
        member_id_tab_search_field = driver.find_element_by_xpath('//*[@id="memberId"]')
        member_id_tab_date_field = driver.find_element_by_xpath('//*[@id="dateOfService"]')
        member_id_tab_submit = driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div[2]/div[2]/form[1]/table[2]/tbody/tr/td/span/input')

        # Entering Member Id and Date of Service    test: 11723433101
        member_id_tab_search_field.send_keys(patientId) # From passed argument
        member_id_tab_date_field.send_keys(date) # From passed argument
        member_id_tab_submit.click()
        self.statusBar.config(text="Entering member search", fg="black")

        # Members under same family ID table
        members_table = driver.find_element_by_xpath('//*[@id="memberSearchResults"]/tbody')
        member_found_flag: bool = False
        member_count: int = 1
        while (not member_found_flag) and member_count <= 8:
            if member_found_flag == False:
                xpath_name_string: str = '//*[@id="memberSearchResults"]/tbody/tr[' + str(member_count) + ']/td[1]'
                xpath_id_string: str = '//*[@id="memberSearchResults"]/tbody/tr[' + str(member_count) + ']/td[3]'
                this_member_id = driver.find_element_by_xpath(xpath_id_string)
                this_member_namelink = driver.find_element_by_xpath(xpath_name_string)
            if this_member_id.text == patientId:
                member_found_flag = True
                self.statusBar.config(text='Member selected: ' + this_member_namelink.text)
                print('Member selected: ' + this_member_namelink.text)
                this_member_namelink.click()
            else:
                member_count += 1
                continue
        if member_count > 8:
            self.statusBar.config(text='Member was not found. Please check.', fg="red")
            print('Member was not found. Please check.')

        # Selecting Office
        location_select_xpath = '// *[ @ id = "locationSelect"]'
        if self.check_exists_by_xpath(driver, location_select_xpath):
            select = Select(driver.find_element_by_xpath(location_select_xpath))
            select.select_by_value('1')  # This is Katy's index in dropdown menu.
            # Indices: League city-> 0, Katy-> 1, Houston-> 2

            location_submit = driver.find_element_by_xpath(
                '//*[@id="memberDetailsModel"]/table/tbody/tr[1]/th/span/input')
            location_submit.click()
            self.statusBar.config(text="Location selected = Katy", fg="blue")

        # Select Dr
        doctor_submit = driver.find_element_by_xpath('//*[@id="memberDetailsModel"]/table/tbody/tr[4]/td/span/input')

        if dr == 'Dr. Jennifer Bird':
            select = Select(driver.find_element_by_id('selectedPalIndex'))
            select.select_by_visible_text('BIRD, JENNIFER (A02993)')
            doctor_submit.click()
        elif dr =="Dr. Derek Le":
            select = Select(driver.find_element_by_id('selectedPalIndex'))
            select.select_by_visible_text('LE, DEREK (A35028)')
            doctor_submit.click()
        else:
            self.statusBar.config(text="Error selecting Dr.")
        self.statusBar.config(text="Dr Selected: " + dr)

        # Checking for benefit eligibility
        benefitsArray = []
        for x in range(1,6):
            benefits_table_xpath_string_availability = '//*[@id="facetsElig"]/tbody/tr[' + str(x) + ']/td[4]'
            benefits_table_item_selected = driver.find_element_by_xpath(benefits_table_xpath_string_availability)
            if benefits_table_item_selected.text == 'Yes':
                benefitsArray.append(True)
            else:
                benefitsArray.append(False)
        print(benefitsArray)

        # Select Exams to claim
        examYes = exams.__contains__('92015')
        fitYes = exams.__contains__('92310') or exams.__contains__('9231025')

        if examYes and fitYes and benefitsArray[0] == True and benefitsArray[4] == True:
            checkbox = driver.find_element_by_id('selectedEligibilityServiceType1')
            checkbox.click()

            checkbox = driver.find_element_by_id('selectedEligibilityServiceType5')
            checkbox.click()

            submit_ben_selected_button = driver.find_element_by_xpath(
                '//*[@id="bottomSubmit"]/tbody/tr/th/span[1]/input')
            submit_ben_selected_button.click()

            selectExam = Select(driver.find_element_by_id('selectedExamType'))
            selectExam.select_by_value(exams[0])

            selectRefraction = Select(driver.find_element_by_id('selectedRefractionCode'))
            selectRefraction.select_by_value(exams[1])

            selectDiagnosis = Select(driver.find_element_by_id('selectedDiagnosisCode'))
            selectDiagnosis.select_by_value(diagnosis[0])

            selectDisease = Select(driver.find_element_by_id('diseaseReporting'))
            selectDisease.select_by_value('false')

            selectCLFit = Select(driver.find_element_by_id('selectedFfEvaluationCode'))
            selectCLFit.select_by_value(exams[2])

            diagnosisFieldCLF = driver.find_element_by_xpath('//*[@id="otherFfDiagnosisCodes"]')
            diagnosticsString = ''
            for diagnostic in diagnosis[1:]:
                diagnosticsString = diagnosticsString + diagnostic + ','

            newdiagnosticsString = diagnosticsString.rstrip(',')
            diagnosisFieldCLF.send_keys(newdiagnosticsString)

            codesSubmit = driver.find_element_by_xpath('//*[@id="nextPageButton"]')
            codesSubmit.click()

            # Enter cost breakdown
            routineCostBox = driver.find_element_by_xpath('//*[@id="ucItems0.charges"]')
            refractionCostBox = driver.find_element_by_xpath('//*[@id="ucItems1.charges"]')
            clfitCostBox = driver.find_element_by_xpath('//*[@id="ucItems2.charges"]')

            routineCostBox.clear()
            routineCostBox.send_keys('145.00')
            refractionCostBox.clear()
            refractionCostBox.send_keys('45.00')
            if exams.__contains__('9231025'):
                fitCost = '99.00'
            else:
                fitCost = '79.00'
            clfitCostBox.clear()
            clfitCostBox.send_keys(fitCost)

            costSubmit = driver.find_element_by_xpath('//*[@id="nextPageButton"]')
            costSubmit.click()
        elif examYes and not fitYes and benefitsArray[0] == True:
            print('exonly')
            checkbox = driver.find_element_by_id('selectedEligibilityServiceType1')
            checkbox.click()

            submit_ben_selected_button = driver.find_element_by_xpath(
                '//*[@id="bottomSubmit"]/tbody/tr/th/span[1]/input')
            submit_ben_selected_button.click()

            selectExam = Select(driver.find_element_by_id('selectedExamType'))
            selectExam.select_by_value(exams[0])

            selectRefraction = Select(driver.find_element_by_id('selectedRefractionCode'))
            selectRefraction.select_by_value(exams[1])

            selectDiagnosis = Select(driver.find_element_by_id('selectedDiagnosisCode'))
            selectDiagnosis.select_by_value(diagnosis[0])

            selectDisease = Select(driver.find_element_by_id('diseaseReporting'))
            selectDisease.select_by_value('false')

            codesSubmit = driver.find_element_by_xpath('//*[@id="nextPageButton"]')
            codesSubmit.click()

            # Enter cost breakdown
            routineCostBox = driver.find_element_by_xpath('//*[@id="ucItems0.charges"]')
            refractionCostBox = driver.find_element_by_xpath('//*[@id="ucItems1.charges"]')

            routineCostBox.clear()
            routineCostBox.send_keys('145.00')
            refractionCostBox.clear()
            refractionCostBox.send_keys('45.00')

            costSubmit = driver.find_element_by_xpath('//*[@id="nextPageButton"]')
            costSubmit.click()
        elif fitYes and not examYes and benefitsArray[4] == True:
            print('fitonly')
            checkbox = driver.find_element_by_id('selectedEligibilityServiceType5')
            checkbox.click()

            submit_ben_selected_button = driver.find_element_by_xpath(
                '//*[@id="bottomSubmit"]/tbody/tr/th/span[1]/input')
            submit_ben_selected_button.click()

            selectCLFit = Select(driver.find_element_by_id('selectedFfEvaluationCode'))
            selectCLFit.select_by_value(exams[0])

            diagnosisFieldCLF = driver.find_element_by_xpath('//*[@id="otherFfDiagnosisCodes"]')
            diagnosticsString = ''
            for diagnostic in diagnosis[1:]:
                diagnosticsString = diagnosticsString + diagnostic + ','

            newdiagnosticsString = diagnosticsString.rstrip(',')
            diagnosisFieldCLF.send_keys(newdiagnosticsString)

            codesSubmit = driver.find_element_by_xpath('//*[@id="nextPageButton"]')
            codesSubmit.click()

            codesSubmit = driver.find_element_by_xpath('//*[@id="nextPageButton"]')
            codesSubmit.click()

            # Enter cost breakdown
            clfitCostBox = driver.find_element_by_xpath('//*[@id="ucItems0.charges"]')

            if exams.__contains__('9231025'):
                fitCost = '99.00'
            else:
                fitCost = '79.00'
            clfitCostBox.clear()
            clfitCostBox.send_keys(fitCost)

            costSubmit = driver.find_element_by_xpath('//*[@id="nextPageButton"]')
            costSubmit.click()
        else:
            self.statusBar.config(text='Benefits for that item are not available!', fg='red')



# MAIN OBJECT AND ROOT WINDOW
root = Tk()
root.title('Eyemedtron')
style = ttk.Style(root)
style.theme_use('alt')
print(style.theme_names())

myObject = EyemedInterface(root)
root.mainloop()




