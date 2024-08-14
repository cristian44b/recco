from diagrams import Diagram, Cluster, Edge
from diagrams.generic.network import Router
from diagrams.onprem.client import Users
from diagrams.onprem.compute import Server
from diagrams.onprem.database import Mssql
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.network import Internet
# from diagrams.onprem.identity import Okta
# from diagrams.saas.collaboration import Confluence
from diagrams.saas.chat import Slack
# from diagrams.saas.analytics import Datadog
from diagrams.custom import Custom

with Diagram("Architecture To-Be", show=True):
    users = Users("Users")

    with Cluster("Kong Konnect"):
        api_gateway = Router("API Gateway")

    with Cluster("DXP"):
        dxp = Server("DXP")
        user_profile = Server("User Profile")
        rec_ui = Server("REC UI")

    jira_atl = Server("JIRA (ATL)")
    jira_kanban = Server("JIRA Kanban Ticketing")
    jira_sm = Server("JIRA REC SM")
    jira_change = Server("JIRA REC Change")

    digital_rec = Server("Digital REC")
    service_desk = Server("Service Desk (ITSM)")

    appflow = Custom("AppFlow", "archi_app_component.png")
    confluence = Custom("Confluence")
    slack = Slack("Chatbot?")
    datadog = Datadog("Gas Engi Sensors")
    event_cmt = Server("Event CMT")

    data_store = Mssql("DataStore")
    dtm_extracts = Server("DTN Extracts")
    power_bi = Server("Power BI")
    analytics = Server("Deloitte Analysis")

    # Connections
    users >> Edge(label="Cloudflare Wrapper") >> dxp
    api_gateway >> dxp
    dxp >> Edge(label="Drupal") >> user_profile
    user_profile >> rec_ui
    rec_ui >> jira_change
    rec_ui >> jira_sm
    jira_sm >> jira_kanban
    jira_change >> jira_kanban
    jira_kanban >> service_desk
    service_desk >> Edge(label="JIRA") >> slack
    service_desk >> Edge(label="Email") >> jira_change

    jira_sm >> Edge(label="Email") >> rec_ui
    jira_kanban >> event_cmt
    event_cmt >> power_bi
    data_store >> Edge(label="SOD") >> power_bi
    power_bi >> analytics
    analytics << dtm_extracts

    confluence >> jira_change
    confluence >> Edge(label="Connects Capabilities") >> jira_sm
    api_gateway >> Edge(label="Contracts") >> rec_ui

    # Additional components
    internal_storage = Server("Internal Storage")
    internal_storage >> Edge(label="Confidential") >> confluence
    jira_change >> Edge(label="SQL DB & Data Spec") >> data_store
    meters_data = Server("Meters Prod Data")
    meters_data >> dtm_extracts
    gas_engi = Server("Gas Engi Sensors (4ES)")
    elect_engi = Server("Elect Engi Sensors (BLC)")

