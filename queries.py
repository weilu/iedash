from sqlalchemy import MetaData, Table, select
from db import corp_engine
import pandas as pd


def get_projects():
    metadata = MetaData()
    projects = Table("project", metadata, autoload_with=corp_engine)

    stmt = select(
        projects.c.Project_Id,
        projects.c.Project_Display_Name,
        projects.c.Lead_Global_Practice_Code,
        projects.c.Project_Status_Name
    )

    with corp_engine.connect() as connection:
        return pd.read_sql(stmt, con=connection)
