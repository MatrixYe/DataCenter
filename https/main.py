# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
from fastapi import FastAPI

from . import block, event, tool, fuck


def create_app() -> FastAPI:
    _app = FastAPI(title="数据中心", description="通用化链上数据同步方案", version="2.1.0", docs_url=None)
    # _app.include_router(admin.router, prefix="/admin")
    _app.include_router(block.router, prefix="/block")
    _app.include_router(event.router, prefix="/event")
    _app.include_router(fuck.router, prefix='/fuck')
    _app.include_router(fuck.router, prefix='/fuck')
    _app.include_router(tool.router, prefix='/tool')
    return _app


app = create_app()
