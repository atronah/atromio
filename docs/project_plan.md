## Stage 0. Core


Entities:

- `account`
- `transfer` - money transaction (word "transaction" is reserved in most dbms) between two accounts (one of them can be none/unknown).
- `account_balance` - account balance fixations


Supported API:

- `create_account(name, description = None)` returns `Account` instance
- `get_accounts()` returns list of `Account` instances
- `add_transfer(from_account_id, to_account_id, amount, description, committed_at=None)` returns `Transfer`
- `get_transfers(account_id, from_datetime=None, to_datetime=None)` returns list of `Transfer` instances
- `add_purchase(account_id, amount, description, purchased_at=None)` returns `Transfer`
- `get_purchases(account_id)` returns list of `Transfer` instances
- `add_income(account_id, amount, description, received_at=None)` returns `Transfer`
- `get_incomes(account_id)` - returns list of `Transfer` instances
- `fix_balance(account_id, amount, fixed_at=None)` returns `Account_Balance`
- `get_balance(account_id, at_datetime)` - returns account balance at passed date and time.


All operations with transfers must check date of last balance confirmation for both passed accounts.
If new transaction has date less than the date of last balance confirmation of one of account, additional correction transaction must be created to save the resulting balance unchanged (and this correction transaction must contain reference to source transaction). 



## Stage 1. Core improving


- multi currency support for accounts
	- currency exchanges
- support tags (like a "food", "household", "leisure" etc.) for purchases/orders



## Stage 2. Importing

Importing:

- from budget app (in own format)
- from FNS electronic cheque (in json format)



## Stage 3. Telegram bot

Telegram bot as interface



## Stage 4. Payment details


Adding entities:

- `commodity` - reference book of services and goods	- `add(type, name, description)` - adds new good or service (specified by `type` argument)
- `invoice` - payment document with info about few purchases 
	- create(amount, date, vendor, customer)
	- pay(payer_account,payee_account, date, description = none)
	- connect_to_transaction(transaction)
	- add_item(commodity, price, quantity, discount = none)



## Stage 5. Debts

- participants
- amount
- interest rate
- time-limit
- partially refunds
- kind:
	- borrowing
	- loaning
	- common bills 
	


## Stage 6. Planning


- planned outlays
- auto payments (full auto and as reminder after payment time)
	- accounting in budget planning (free money)
- reasons: gift, food, traveling. To see unnecessary outlays. May be it can be solved by tags



## Stage N. None

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


