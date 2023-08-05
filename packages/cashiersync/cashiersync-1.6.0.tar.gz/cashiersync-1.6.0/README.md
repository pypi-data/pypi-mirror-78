# cashier-sync

Cashier Sync is a server-side component that allows syncing Cashier to a local instance of ledger.

It is written in Python and is available for installation via pip (PyPi).

## Use

Run `cashiersync` from the folder which is setup for use with ledger. Having a configured .ledgerrc is useful, to point to the ledger files (book, prices, etc.) you want to use.
Ledger-cli must be in the path as it will be run to retrieve the data.

Optional: set up a tunnel to your machine so that it is available over the internet.
`ssh -R 80:localhost:5000 serveo.net`
or 
`ssh -R cashier:80:localhost:5000 serveo.net`

However, since Python runs in Termux, it might be more convenient to run the server component locally (cashier-sync and ledger).

## Run

### Production

The `cashiersync` executable console script is registered by the setup. This will run the web app.
This may require the wheel package.

The configuration file can be created if the default options are to be modified.

### Misc

In some cases, when the app was run through `cashiersync` entry point, the CORS was not initialized, but when run with `flask run`, it was. In that case, run:

```
export FLASK_APP=cashiersync.app
flask run
```

The code above could be placed into a `cashiersync` executable script in .local/bin folder, for example.

### Running on Mobile Devices

The server can also run on Android in Termux. All that is needed in such case is to get the ledger book onto the device, possibly using git. 

## Development

`flask run` from cashiersync folder. Or configure VS Code to run as a Flask application.

### Deployment

See distribute.sh script for the steps.
