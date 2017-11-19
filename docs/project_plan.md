Stage 0. Core
-------------

Adding following entities: 

- `account` which is supported following operations:
	- `create(name, description = none)` - creates new account with passed name and description.
	- `get_balance(datetime)` - returns account balance on passed date 
	- `confirm_balance(datetime)` - avoids simple transactions (without parallel correction) before confirmation.
	- `add_transaction(amount, description, datetime = now, other_account = none)`  - 
	adds transaction between this account and `other_account`. Sign of amount determines direction of transaction.
- `transaction`
	- `create(from, to, amount, description, datetime = now)` - creates new transaction between two accounts: `from` and `to`
	- `delete(transaction)`
	

All operations with transactions must check date of last balance confirmation for both passed accounts.
If new transaction has date less than the date of last balance confirmation of one of account, additional correction transaction must be created to save the resulting balance unchanged (and this correction transaction must contain reference to source transaction). 



Stage 1. Core improving
-----------------------

- multi currency support for accounts
	- currency exchanges
- support tags (like a "food", "household", "leisure" etc.) for purchases/orders



Stage 2. Importing
------------------

Importing:

- from budget app (in own format)
- from FNS electronic cheque (in json format)



Stage 3. Telegram bot
---------------------

Telegram bot as interface



Stage 4. Payment details
------------------------

Adding entities:

- `commodity` - reference book of services and goods	- `add(type, name, description)` - adds new good or service (specified by `type` argument)
- `invoice` - payment document with info about few purchases 
	- create(amount, date, vendor, customer)
	- pay(payer_account,payee_account, date, description = none)
	- connect_to_transaction(transaction)
	- add_item(commodity, price, quantity, discount = none)



Stage 5. Debts
--------------

- participants
- amount
- interest rate
- time-limit
- partially refunds
- kind:
	- borrowing
	- loaning
	- common bills 
	


Stage 4. Planning
-----------------

- planned outlays
- auto payments (full auto and as reminder after payment time)
	- accounting in budget planning (free money)
- reasons: gift, food, traveling. To see unnecessary outlays. May be it can be solved by tags



Stage N. None
-------------

- export aggregated data to supported external formats (budget) to decrease data size (by combining some data)
- add prices info without adding orders
- auto fill price in order details (based on ordering history for this supplier)
- support hierarchical suppliers networks (to get statistics about favourites)
- alert for extra outlays
- alert for expiration dates
- accounting money saving by discounts 
- barcode scanner support
- order details from check photo
- get info from banks API


