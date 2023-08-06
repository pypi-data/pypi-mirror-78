import asyncio
from logging import getLogger
from time import time
from typing import Optional, List
from uuid import uuid4

import aiohttp
from aiohttp import ClientSession, ClientConnectorError, ClientPayloadError

from .request_data import RequestData
from .requests_result import RequestsResult
from .response_data import ResponseData

logger = getLogger()
ASYNCIO_SEMAPHORE = 1024


async def async_make_requests(*requests_data) -> RequestsResult:
    call_id = str(uuid4()).replace('-', '')

    requests_data: List[RequestData] = [RequestData.make(req) for req in requests_data]
    semaphore = asyncio.Semaphore(ASYNCIO_SEMAPHORE)
    results = list()
    tasks = list()
    start_at = time()

    requests_data_expanded: List[RequestData] = list()

    for req in requests_data:
        for i in range(req.count):
            requests_data_expanded.append(req)

    requests_count = len(requests_data_expanded)
    requests_id_len = len(str(requests_count))

    async with ClientSession() as session:
        for i in range(requests_count):
            request_data = requests_data_expanded[i]
            request_id = f'{call_id} | {i + 1:0>{requests_id_len}}'
            task = asyncio.create_task(_request_fetch(session=session,
                                                      semaphore=semaphore,
                                                      request_data=request_data,
                                                      request_id=request_id))
            # bodies_size += getsizeof(dumps(req.json)) if req.json is not None else 0
            tasks.append(task)
        await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
        # await asyncio.gather(*tasks)
        results = [task.result() for task in tasks]

    result = RequestsResult(responses=results,
                            elapsed=time() - start_at)
    logger.info(f'[ {call_id} ] ASYNC REQUESTS RESULT:\n'
                f'  Requests count: {len(result.responses)}\n'
                f'  Elapsed time:   {result.elapsed} seconds\n'
                f'  Average time:   {result.average} seconds\n'
                f'  Statuses:       {result.status_codes}\n'
                f'  Failed:         {result.failed}')

    return result


async def _request_fetch(session: ClientSession,
                         semaphore: asyncio.Semaphore,
                         request_data: RequestData,
                         timeout=None,
                         request_id: Optional[str] = None) -> Optional[ResponseData]:
    async with semaphore:
        started_at = time()
        logger.info(f'[ {request_id} ] -> start task with {request_data.method} request to {request_data.url}')
        # headers = {'Content-Type': 'application/json'}  if json else None

        try:
            async with session.request(
                    method=request_data.method,
                    url=request_data.url,
                    json=request_data.json,
                    headers=request_data.headers,
                    ssl=False,
                    timeout=timeout,
            ) as response:
                await response.read()
        except (asyncio.TimeoutError, ClientConnectorError, ClientPayloadError, Exception) as err:
            logger.warning(f'[ {request_id} ] {err.__class__.__name__} {request_data.url}')
            return ResponseData(service_name=request_data.service_name, exception=err, url=request_data.url,
                                started_at=started_at)

    finished_at = time()
    logger.info(f'[ {request_id} ] <- receive response from {request_data.url} ({finished_at - started_at:.3f} sec.)')

    response_data = ResponseData(service_name=request_data.service_name,
                                 response=response,
                                 url=request_data.url,
                                 started_at=started_at,
                                 finished_at=finished_at)
    response_data.text = await response.text()
    response_data.json = None

    try:
        response_data.json = await response.json()
    except aiohttp.ContentTypeError:
        logger.warning(f'[ {request_id} ] is not JSON response ({response.status} {response.reason})')

    return response_data
