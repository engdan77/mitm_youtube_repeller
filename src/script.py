from mitmproxy import http
from loguru import logger
import re
import time
from collections import UserList


def now():
    """
    Get the current time as an integer timestamp.

    :return: The current time as an integer timestamp.
    """
    return int(time.time())


class QueueList(UserList):
    """
    A class that represents a queue implemented as a list.

    Attributes:
        max_size (int): The maximum size of the queue. Default is 100.

    Methods:
        append(item, id_=None):
            Adds an item to the queue. If the item is already at the end of the queue, it is not added again.
            If the queue is already at its maximum size, the oldest item is removed before adding the new item.
            Args:
                item: The item to be added to the queue.
                id_ (optional): The unique identifier for the item. Default is None.

        last(id_=None):
            Returns the most recent item that matches the given id_.
            Args:
                id_ (optional): The unique identifier to match. Default is None.

        count_items_in_last_seconds(id_=None, seconds=30) -> int:
            Returns the count of items that match the given id_ in the last specified seconds.
            Args:
                id_ (optional): The unique identifier to match. Default is None.
                seconds (int): The number of seconds to consider. Default is 30.

            Returns:
                int: The count of items that match the given id_ in the last specified seconds.
    """
    max_size = 100

    def append(self, item, id_=None):
        if item == self.last(id_=id_):
            return
        if len(self.data) >= self.max_size:
            self.data.pop(0)
        self.data.append((now(), item, id_))

    def last(self, id_=None):
        for ts, item, id__ in reversed(self.data):
            if id__ == id_:
                return item

    def count_items_in_last_seconds(self, id_=None, seconds=30) -> int:
        count = 0
        for ts, item, id__ in reversed(self.data):
            if id__ == id_ and ts >= now() - seconds:
                count += 1
            else:
                break
        return count


q = QueueList()
client_last_blocked = {}
MAX_VIEWS = 10
WITHIN_SECONDS = 120
PENALTY_SECONDS = 300


def block_flow(flow: http.HTTPFlow):
    """
    :param flow: The flow object representing the HTTP flow
    :return: None

    This method blocks the flow by setting the response content to an empty byte string, setting the response status code to 503 (Service Unavailable), and then killing the flow.
    """
    flow.response.content = b''
    flow.response.status_code = 503
    flow.kill()


def youtube_repeller(flow: http.HTTPFlow):
    """
    :param flow: The HTTP flow object representing the request and response between the client and server.
    :return: None

    The `youtube_repeller` method is responsible for repelling unwanted traffic to YouTube. It checks the IP address of the client,
    the response content, and the request URL to determine if the traffic should be blocked or allowed.

    The method takes in a `flow` parameter of type `http.HTTPFlow`, which represents the HTTP flow containing the client request and server response.
    """
    from_ip = flow.client_conn.peername[0]
    content = flow.response.content
    headers = flow.response.headers
    url = flow.request.pretty_url
    content_type = headers.get('Content-Type', '')
    logger.info(f'content: {content_type} size: {len(content)}')

    global q
    counts_last_minutes = q.count_items_in_last_seconds(id_=from_ip, seconds=WITHIN_SECONDS)
    expire_ts = client_last_blocked.get(from_ip, False) and client_last_blocked.get(from_ip) + PENALTY_SECONDS
    logger.info(f'{from_ip} expire_ts: {expire_ts} counts_request_last_minutes: {counts_last_minutes} now: {now()}')
    if expire_ts and expire_ts >= now():
        logger.info(f'{from_ip} within penalty time, remaining seconds {expire_ts - now()} and blocking!!')
        block_flow(flow)
        return
    elif counts_last_minutes >= MAX_VIEWS:
        logger.info(f'Killed and start penalty timer for {from_ip}!!')
        client_last_blocked[from_ip] = now()
        block_flow(flow)
        return

    if 'application/vnd.yt-ump' in content_type and len(content) >= 50_000:
        google_video_id = re.findall(r'https://.+?.googlevideo.com.*?&ei=(.+?)&.*', url)
        if not google_video_id:
            return
        logger.info(f'{from_ip} allowed to access youtube {google_video_id}')
        q.append(google_video_id, id_=from_ip)


def request(flow: http.HTTPFlow):
    host = flow.request.host
    path = flow.request.path


def response(flow: http.HTTPFlow):
    youtube_repeller(flow)

