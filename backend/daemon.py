from sqlite3.dbapi2 import Cursor, connect
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from pythonosc.udp_client import SimpleUDPClient
import asyncio
import sqlite3
from socket import gaierror
from logging import getLogger

logger = getLogger(__name__)

DATABASE = "/tmp/matrix.sql"
ip = "djpult.lan"
listen_ip = "0.0.0.0"
port_rx = 8001
port_tx = 8000


con = None
def get_connection():
    global con
    if con is None:
        create_database()
    return con


def create_database():
    logger.info("Creating database")
    global con
    try:
        con = sqlite3.connect(DATABASE)
    except sqlite3.OperationalError as err:
        create_database()
        con = sqlite3.connect(DATABASE)
    cursor = con.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS matrix (id INTEGER PRIMARY KEY, mode INT, brightness INT, speed INT)''')
    cursor.close()
    con.commit()


def status_handler(address, *args):
    logger.debug(f"New status {address}: {args}")
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("insert into matrix (mode,brightness,speed) values (?,?,?);", args)
        cursor.execute("select count(*) from matrix;")
        num = cursor.fetchone()[0]
        if (num > 1):
            cursor.execute(f"DELETE FROM matrix WHERE id in (SELECT id FROM matrix ORDER BY id ASC LIMIT {num-1});")
        connection.commit()
        cursor.close()


dispatcher = Dispatcher()
dispatcher.map("/djpult/status", status_handler)


async def loop():
    while True:
        try:
            client = SimpleUDPClient(ip, port_tx)
            client.send_message('/djpult/status', port_rx)
        except gaierror:
            logger.debug("Guess DJ pult is offline, skipping.")
        await asyncio.sleep(60)


async def init_main():
    server = AsyncIOOSCUDPServer((listen_ip, port_rx), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()
    
    create_database()
    
    await loop()  # Enter main loop of program

    transport.close()  # Clean up serve endpoint


if __name__ == "__main__":
    asyncio.run(init_main())