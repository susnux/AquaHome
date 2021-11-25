from sqlite3.dbapi2 import Cursor, connect
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from pythonosc.udp_client import SimpleUDPClient
import asyncio
import sqlite3
from socket import gaierror
from logging import getLogger
import argparse

logger = getLogger(__name__)

database = "/tmp/matrix.sql"
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
        con = sqlite3.connect(database)
    except sqlite3.OperationalError as err:
        create_database()
        con = sqlite3.connect(database)
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
    parser = argparse.ArgumentParser()
    parser.add_argument('--remote', type=str, default="djpult.lan", help='IP of the remote device (Matrix)')
    parser.add_argument('--listen', type=str, default="127.0.0.1", help='IP to listen to')
    parser.add_argument('--database', type=str, default="matrix.sql", help='Database file')
    parser.add_argument('--tx', type=int, default=8000, help='TX port of remote device')
    parser.add_argument('--rx', type=int, default=8001, help='RX port of remote device')

    args = parser.parse_args()
    if args.remote:
        ip = args.remote
    if args.listen:
        listen_ip = args.listen
    if args.database:
        database = args.database
    if args.rx:
        port_rx = args.rx
    if args.tx:
        port_tx = args.tx
    asyncio.run(init_main())