#!/usr/bin/env python
#
# Copyright (C) 2020 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
FastAPI app
"""

import asyncio

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from gns3server.controller import Controller
from gns3server.compute import MODULES
from gns3server.compute.port_manager import PortManager
from gns3server.controller.controller_error import (
    ControllerError,
    ControllerNotFoundError,
    ControllerTimeoutError,
    ControllerForbiddenError,
    ControllerUnauthorizedError
)

from gns3server.endpoints import controller
from gns3server.endpoints import index
from gns3server.endpoints.compute import compute_api

import logging
log = logging.getLogger(__name__)

app = FastAPI(title="GNS3 controller API",
              description="This page describes the public controller API for GNS3",
              version="v2")

origins = [
    "http://127.0.0.1",
    "http://localhost",
    "http://127.0.0.1:8080",
    "http://localhost:8080",
    "http://127.0.0.1:3080",
    "http://localhost:3080",
    "http://gns3.github.io",
    "https://gns3.github.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(index.router, tags=["controller"])
app.include_router(controller.router, prefix="/v2")
app.mount("/v2/compute", compute_api)


@app.exception_handler(ControllerError)
async def controller_error_handler(request: Request, exc: ControllerError):
    return JSONResponse(
        status_code=409,
        content={"message": str(exc)},
    )


@app.exception_handler(ControllerTimeoutError)
async def controller_timeout_error_handler(request: Request, exc: ControllerTimeoutError):
    return JSONResponse(
        status_code=408,
        content={"message": str(exc)},
    )


@app.exception_handler(ControllerUnauthorizedError)
async def controller_unauthorized_error_handler(request: Request, exc: ControllerUnauthorizedError):
    return JSONResponse(
        status_code=401,
        content={"message": str(exc)},
    )


@app.exception_handler(ControllerForbiddenError)
async def controller_forbidden_error_handler(request: Request, exc: ControllerForbiddenError):
    return JSONResponse(
        status_code=403,
        content={"message": str(exc)},
    )


@app.exception_handler(ControllerNotFoundError)
async def controller_not_found_error_handler(request: Request, exc: ControllerNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"message": str(exc)},
    )


@app.on_event("startup")
async def startup_event():

    await Controller.instance().start()
    # Because with a large image collection
    # without md5sum already computed we start the
    # computing with server start

    from gns3server.compute.qemu import Qemu
    asyncio.ensure_future(Qemu.instance().list_images())

    for module in MODULES:
        log.debug("Loading module {}".format(module.__name__))
        m = module.instance()
        m.port_manager = PortManager.instance()


@app.on_event("shutdown")
async def shutdown_event():

    await Controller.instance().stop()

    for module in MODULES:
        log.debug("Unloading module {}".format(module.__name__))
        m = module.instance()
        await m.unload()

    if PortManager.instance().tcp_ports:
        log.warning("TCP ports are still used {}".format(PortManager.instance().tcp_ports))

    if PortManager.instance().udp_ports:
        log.warning("UDP ports are still used {}".format(PortManager.instance().udp_ports))
