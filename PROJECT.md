# Trip Generator - Part 2

### Objective:
To familiarize yourself with basic web development in Python using Flask and Jinja2 templating.

# Project Description

### Introduction
For Project 2 you will be building on the work you did for project1. To be specific, you will be creating a backend website to manage your trips.

The website should have the following 2 primary functionalities (in 2 simple webpages)

+ On the home page of your app, you should be able to see a list of trips as a table that you currently have. Note we are not using databases here, so your trips will be reset once you close down the server. To help you get started, I have provided a sample list of trips as a variable you can load in from a file using pickle and just work on this list. The table should have links to view/edit a trip and a link to delete the trip from the list. This is very similar to the student app I demoed in class. In addition to the table view, the user should be able to create a new trip and add it to their list of trips. To do this you will need a form, with a simple String field and a Submit button. The user will type in a list of places and upon hitting submit, a new Trip object should be created with the trip details. Note the logic of creating a trip by making the necessary API calls is already done (in Project 1), We just need to initialize a new trip object with the parameters in the text field and add it to the current list of trips.
+ The second webpage will have a dynamic route and should show the details of a trip when the user clicks on the view/edit link. This should show the summary of the trip, very similar to the summary() method you designed in Project1. Instead of printing to the console, this will now be displayed on a webpage. The information printed will be in the following format.
    + Some labels showing the overall trip details(like total distance, time, weather etc.)
    + A table view of the stops being made on the trip. 
    + An image description of the weather at the final destination. The url of the image is found in the weather Stacks response when querying the weather for a location, which I have already parse and include in the trip.details attribute.
    + A form to allow the user to add another stop on their trip.
    
    Like the previous page, the form will have a String field and a button to add locations to the above trip. This can be done by calling the overloaded '+' operator that you did for Project1. Again note that the logic is already there. You just need to make the appropriate method call to add a location to your trip object when the submit button is clicked. Also note that since your trip object is just a reference to the item in your list of trips, making changes to the object's properties, will also update the list as well. Finally this page should have link to go back to the home page somewhere on top of the page.

### Template Code
1. I have also uploaded a project skeleton, which also contains the solution to Project1 that will help you get started. You can either use this or use your own solution for Project 1 as a starting point. To run my code do the following
2. Unzip into a folder.
3. Open folder in VSCode (or your favorite IDE)
4. Create a virtual env (py -m venv env)
5. Activate it (./env/Scripts/Activate)
6. Install required packages (pip install -r requirements.txt)
7. Modify the contstants.py file and add in your API keys
8. Run app.py

Note you will only have to modify app.py , index.html and trip.html to complete the requirements. Also for any trip you can check trip.details, which will give you a dictionary of the information you need to display in these webpages.

Here is a walkthrough of what the website will look like and the basic functionality expected. 

#### Link to Template Code  

Download from your SVSU canvas

#### Video Walkthrough 

https://youtu.be/MW7o3ZiVN_Q

## To submit
+ Submit a .zip of everything in your project folder except the /env folder and the constants.py file

## Extra Credit (10%)
Any group submitting a stylized version of their app will receive an additional 10%. Your styling and layout should look something similar to the website shown in the demo video above. Please only attempt this if you have enough time. This requires a working knowledge of Bootstrap, which I don't expect everyone one to know, so this is mainly aimed towards those who are comfortable working with HTML and CSS.