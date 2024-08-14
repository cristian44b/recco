from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.analytics import PowerBI
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.client import Users
from diagrams.onprem.compute import Server
from diagrams.onprem.database import Mssql
from diagrams.onprem.network import Internet
from diagrams.azure.identity import ActiveDirectory

with Diagram("Architecture As-Is", show=True):

    users = Users("Users")

    with Cluster("REC Portal"):
        rec_portal = Server("REC Portal")
        powerbi = PowerBI("PowerBI Dashboard")
        rec_portal >> powerbi

    dynamics = Mssql("Dynamics")
    sod_data = Mssql("SOD Data")

    deloitte = Server("Deloitte Analysis")
    dtm_extracts = Server("DTM Extracts")

    dn = Server("DN")
    ibm_jazz = Server("IBM Jazz")

    dynamics >> users
    sod_data >> users
    rec_portal >> users
    rec_portal >> dn
    rec_portal >> deloitte
    dn >> ibm_jazz
    deloitte << dtm_extracts

    dynamics >> Edge(label="User lists & service desk")
    sod_data >> Edge(label="SOD Data")
    ibm_jazz >> Edge(label="SQL Data Spec")

    teams = Server("Teams (shared)")
    access_do = ActiveDirectory("Access DO??")

    market_messaging = Internet("Market Messaging")
    data = Mssql("Data")

    market_messaging >> data
    access_do >> dynamics
    teams >> dynamics
