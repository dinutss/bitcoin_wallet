# Setup:
1) Git and python3 have to be preinstalled on your desktop
2) Open terminal and run   ```git clone git@github.com:dinutss/bitcoin_wallet.git```
3) Navigate to ```bitcoin_wallet``` folder in the terminal and run the following commands:
    - ```pip3 install virtualenv```
    - ```virtualenv venv```
    - ```source venv/bin/activate```
    - ```pip3 install -r requirements.txt```
    - ```python3 api.py```
4) Open ```main.html``` file in your browser    
 
# Test instructions
1) Add several new bitcoin addresses with the help of input field and button ```Add```
2) Click ```Synchronize data``` button (it can take a few seconds).
   After that data about all wallets will be loaded to the local db, also balance of each wallet will be updated
   #### Important: each time you want the data to be updated, press button ```Synchronize data```
3) Examine wallets transactions by clicking on its identifiers
4) Use ```Detect transfers``` button detect the likely transfers amongst added wallets

# Example of addresses
1BUNd2E5czA5hpZQZNWpbLEWATPvrLWJLS

3E8ociqZa9mZUSwGdSmAEMAoAxBK3FNDcd

bc1qr6lq3yvk6t4v2g2lhneehwntjzqpzmu6g2tptd

37XuVSEpWW4trkfmvWzegTHQt7BdktSKUs