#Use with PYTHON3!

import oci
from ocimodules.functions import *
from ocimodules.EdgeServices import *
from ocimodules.ObjectStorage import *
from ocimodules.Instances import *
from ocimodules.Database import *
from ocimodules.IAM import *
from ocimodules.VCN import *
from ocimodules.BlockStorage import *
from ocimodules.ResourceManager import *
from ocimodules.FileStorage import *
from ocimodules.Monitoring import *
from ocimodules.Notifications import *
from ocimodules.Autoscaling import *
from ocimodules.FunctionsService import *

########## Configuration ####################
# Specify your config file
configfile = "~/.oci/config"

# Specify the compartment OCID that you want to delete
DeleteCompartmentOCID = "ocid1.compartment.oc1..aaaaaaaa456vlgfybg2obpz7hrwjrqcyzme5mtgtqcetgt4tl2bs3kubmmea"

# Search for resources in regions:
regions = ["eu-frankfurt-1", "uk-london-1"]

# Specify your home region
homeregion = "eu-frankfurt-1"
#############################################

config = oci.config.from_file(configfile)

print ("\n--[ Login check and getting all compartments from starting compartment ]--")
compartments = Login(config, DeleteCompartmentOCID)
processCompartments=[]

clear()

print ("\n--[ Compartments to process ]--")

# Add all active compartments, but exclude the ManagementCompartmentForPaas (as this is locked compartment)
for compartment in compartments:
    if compartment.lifecycle_state== "ACTIVE" and compartment.name != "ManagedCompartmentForPaaS":
        processCompartments.append(compartment)
        print (compartment.name)


confirm = input ("\ntype yes to delete all contents from these compartments: ")

if confirm == "yes":

    for region in regions:

        print ("============[ Deleting resources in {} ]================".format(region))
        config["region"] = region

        print ("\n--[ Deleting Edge Services ]--")
        DeleteWAFs(config,processCompartments)
        DeleteHTTPHealthchecks(config, processCompartments)
        DeletePINGHealthchecks(config, processCompartments)
        DeleteTrafficSteerings(config, processCompartments)
        DeleteZones(config, processCompartments)

        print ("\n--[ Deleting Object Storage ]--")
        DeleteBuckets(config, processCompartments)

        print ("\n--[ Deleting Auto Scaling Configurations ]--")
        DeleteAutoScalingConfigurations(config, processCompartments)

        print ("\n--[ Deleting Compute Instances ]--")
        DeleteInstancePools(config,processCompartments)
        DeleteInstanceConfigs(config, processCompartments)
        DeleteInstances(config,processCompartments)
        DeleteImages(config, processCompartments)
        DeleteBootVolumes(config, processCompartments)
        DeleteDedicatedVMHosts(config, processCompartments)

        print("\n--[ Deleting Application Functions ]--")
        DeleteApplications(config, processCompartments)

        print ("\n--[ Deleting Database Instances ]--")
        DeleteDBCS(config,processCompartments)
        DeleteAutonomousDB(config,processCompartments)
        DeleteDBBackups(config, processCompartments)

        print ("\n--[ Deleting Resource Manager Stacks ]--")
        DeleteStacks(config, processCompartments)

        print ("\n--[ Deleting Block Volumes ]--")
        DeleteVolumes(config, processCompartments)
        DeleteBlockVolumesBackups(config, processCompartments)

        print ("\n--[ Deleting FileSystem and Mount Targets ]--")
        DeleteMountTargets(config, processCompartments)
        DeleteFileStorage(config, processCompartments)

        print ("\n--[ Deleting VCNs ]--")
        DeleteVCN(config, processCompartments)

        print ("\n--[ Deleting Alarms ]--")
        DeleteAlarms(config, processCompartments)

        print ("\n--[ Deleting Notifications ]--")
        DeleteNotifications(config, processCompartments)

    print ("\n--[ Hopefully deleting compartments, if empty ]--")
    config["region"] = homeregion
    DeleteCompartments(config,processCompartments, DeleteCompartmentOCID)



