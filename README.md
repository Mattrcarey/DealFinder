# DealFinder

## Setup : 

1. Run the command: python3 src/DealFinder.py -s

Command       | Function
------------- | -------------
a             | Adds a product
l             | Lists products
r             | Removes a product
c             | Clears products
h             | Help
i             | Initialize
s             | Exit

2. Use i and a to Initialize and add products respectively

3. If you want the script to send you an email navigate into DealFinder.py and update 
   the values for EMAIL and EMAIL_PASSWORD. This is for the email account that will send 
   emails. It needs to be a gmail account, you can make a new email for this. 
   
   You will also have to go to the settings and allow access to less secure apps for this 
   gmail account.
   
   Once you created the account you can do that at this link : 
   https://www.google.com/settings/security/lesssecureapps 
   
4. If you want to receive an email with goods under your willingness to pay run the script
   using the command: src/DealFinder.py -e
   
   If you don't want to receive an email and just want to see the results printed to the 
   console use the command: src/DealFinder.py
