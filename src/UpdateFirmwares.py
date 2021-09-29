import meraki
import os
import json
import pprint
import pandas as pd

key = os.environ.get('API_KEY')
dashboard = meraki.DashboardAPI(key)

orgs = dashboard.organizations.getOrganizations()

# Get firmware for network with all devices (GBW Abbots Passage)

net_id = 'L_699183842149272497'

# Print out firmwares obtained from special network

firmwares = dashboard.networks.getNetworkFirmwareUpgrades(
     net_id
)

pprint.pprint(firmwares['products'])

MX_upgrade = int(input('Please enter desired MX upgrade ID, enter 0 otherwise : '))
MR_upgrade = int(input('Please enter desired MR upgrade ID, enter 0 otherwise : '))
MS_upgrade = int(input('Please enter desired MS upgrade ID, enter 0 otherwise : '))
MV_upgrade = int(input('Please enter desired MV upgrade ID, enter 0 otherwise : '))
MG_upgrade = int(input('Please enter desired MG upgrade ID, enter 0 otherwise : '))

# Get all getOrganizations

err = 0

for i in range(len(orgs)):

    # Check license state
    try:

        license = dashboard.organizations.getOrganizationLicensesOverview(orgs[i]['id'])

    # Get all networks

        networks = dashboard.organizations.getOrganizationNetworks(orgs[i]['id'])


    # Cycle through every network

        for j in range(len(networks)):

            try:
                network_id = networks[j]['id']

                #Get devices for this network

                devices = dashboard.networks.getNetworkDevices(
                    network_id
                )
                #Reset deviceModels variable from last iteration

                deviceModels = []

                for i in range(len(devices)):

                    # Define which deviceModels are present
                    deviceModels.append(devices[i]['model'])


                dashboard.networks.updateNetworkFirmwareUpgrades(
                    network_id,
                    upgradeWindow = {'hourOfDay': '2:00', 'dayOfWeek': 'Tue'}
                )

                current = dashboard.networks.getNetworkFirmwareUpgrades(
                    network_id
                )

                if any("MS" in s for s in deviceModels) and MS_upgrade > 0 and current['products']['switch']['currentVersion']['id'] != MS_upgrade:
                    dashboard.networks.updateNetworkFirmwareUpgrades(
                        network_id,
                        products={'switch': {'nextUpgrade': {'toVersion': {'id': MS_upgrade}}}}
                    )

                if any("MX" in s for s in deviceModels) and MX_upgrade > 0 and current['products']['appliance']['currentVersion']['id'] != MX_upgrade:
                    dashboard.networks.updateNetworkFirmwareUpgrades(
                        network_id,
                        products={'appliance': {'nextUpgrade': {'toVersion': {'id': MX_upgrade}}}}
                    )

                if any("MR" in s for s in deviceModels) and MR_upgrade > 0 and current['products']['wireless']['currentVersion']['id'] != MR_upgrade:
                    dashboard.networks.updateNetworkFirmwareUpgrades(
                        network_id,
                        products={'wireless': {'nextUpgrade': {'toVersion': {'id': MR_upgrade}}}}
                    )

                if any("MG" in s for s in deviceModels) and MG_upgrade > 0 and current['products']['cellularGateway']['currentVersion']['id'] != MG_upgrade:
                    dashboard.networks.updateNetworkFirmwareUpgrades(
                        network_id,
                        products={'cellularGateway': {'nextUpgrade': {'toVersion': {'id': MG_upgrade}}}}
                    )

                if any("MV" in s for s in deviceModels) and MV_upgrade > 0 and current['products']['camera']['currentVersion']['id'] != MV_upgrade:
                    dashboard.networks.updateNetworkFirmwareUpgrades(
                        network_id,
                        products={'camera': {'nextUpgrade': {'toVersion': {'id': MV_upgrade}}}}
                    )


            except meraki.APIError as e:


                if "firmware" in str(e):
                            print("Error! You have entered an incorrect firmware ID")
                            err = 1

                if "bound" in str(e):
                            print("Attempted to make change on bound network")

                if "403" in str(e):
                            print("You have tried to write to an org/network without access")

                if "404" in str(e):
                            print("Org license information unavailable")

    except meraki.APIError as a:

        if "404" in str(a):
                    print("Org license information unavailable")

if err == 0:
    print("Script finished successfully")
