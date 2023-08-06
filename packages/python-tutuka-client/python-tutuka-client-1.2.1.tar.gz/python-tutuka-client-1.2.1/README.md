[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
    
python-tutuka-client
===========

A library for accessing the Tutuka Local API XML-RPC API for python.

[Tutuka Local API Reference](https://developer.tutuka.com/companion-api/api-reference/local-api/)

## Installation
Use the package manager [pipenv](https://pypi.org/project/pipenv/2020.6.2/) to install.

    pipenv install python-tutuka-client

## Usage
Use your own Tutuka credentials.
* **terminal_id** - Tutuka issued terminal ID of the terminal requesting the transaction
* **password** - Tutuka issued terminal password
* **host** - Tutuka Host
* **path** - Tutuka Local API path

```python
from tutuka_client import LocalApiClient

client = LocalApiClient(
    terminal_id='terminal_id',
    password='password',
    host='https://companion.uat.tutuka.cloud',
    path='/v2_0/XmlRpc.cfm',    
)
```
## Class Methods

- [CreateLinkedCard](/docs/create_linked_card.md)
- [LinkCard](/docs/link_card.md)
- [OrderCard](/docs/order_card.md)
- [OrderCardWithPinBlock](/docs/order_card_with_pin_block.md)
- [ActivateCard](/docs/activate_card.md)
- [GetActiveLinkedCards](/docs/get_active_linked_cards.md)
- [ChangePin](/docs/change_pin.md)
- [ResetPin](/docs/reset_pin.md)
- [UpdateBearer](/docs/update_bearer.md)
- [TransferLink](/docs/transfer_link.md)
- [StopCard](/docs/stop_card.md)
- [UnstopCard](/docs/unstop_card.md)
- [Status](/docs/status.md)
- [Set3dSecureCode](/docs/set3d_secure_code.md)
- [UpdateCVV](/docs/update_cvv.md)
- [RetireCard](/docs/retire_card.md)


## Test
Tested with [mamba](https://mamba-framework.readthedocs.io/en/latest/), install pipenv dev packages and then run tests.

    pipenv install --dev
    pipenv run make test

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)