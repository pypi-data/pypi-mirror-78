import csv
import aiohttp
import asyncio
import hashlib
import requests
import time
from tqdm import tqdm
from whisper_evaluate.utils import logging


class WhisperQuery(object):

    def __init__(self, url: str, source_file: str, target_file: str, semaphore: int = 500):
        """Initial configuration
        url: serving url to request
        source_file: the file of query
        target_file: the file of results
        semaphore: maximum concurrency
        """
        self.url = url
        self.source_file = source_file
        self.target_file = target_file
        self.semaphore = asyncio.Semaphore(semaphore)
        self.results = []

    def query_rows(self):
        with open(self.source_file, 'r', encoding='utf-8') as f:
            f_csv = csv.reader(f)
            next(f_csv)
            for row in f_csv:
                yield row

    def run(self):
        start_time = time.time()
        logging.info("Whisper text detection query start.")
        tasks = [asyncio.ensure_future(self.__post(row=row)) for row in self.query_rows()]
        with tqdm(total=len(tasks)) as pbar:
            for task in tasks:
                task.add_done_callback(lambda _: pbar.update(1))
            loop = asyncio.get_event_loop()
            self.results = loop.run_until_complete(asyncio.gather(*tasks))
            loop.close()
        logging.info("Complete stand test query, cost {} seconds.".format(int(time.time() - start_time)))
        logging.info("Start to write target file..")
        self._save()

    def _save(self):
        with open(self.target_file, 'w', encoding='utf-8') as f:
            w_csv = csv.writer(f)
            if len(self.results[0]) == 4:
                w_csv.writerow(["example", "label", "type", "result_json"])
            elif len(self.results[0]) == 3:
                w_csv.writerow(["example", "placeholder", "result_json"])
            elif len(self.results[0]) == 2:
                w_csv.writerow(["example", "result_json"])
            w_csv.writerows(self.results)

    async def __post(self, row: list) -> list:
        async with self.semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.url, json={"inputs": [row[0]]}) as response:
                    return row + [await response.json()]


class NeteaseQuery(WhisperQuery):

    def __init__(self, source_file: str, target_file: str, semaphore: int = 4):
        """Initial configuration
        url: serving url to request
        source_file: the file of query
        target_file: the file of results
        semaphore: maximum concurrency
        """
        self.url = "http://172.26.230.4:1163/check"
        self.source_file = source_file
        self.target_file = target_file
        self.semaphore = asyncio.Semaphore(semaphore)
        self.results = []

    async def __post(self, row: list) -> list:
        async with self.semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.url, json={"dataId": self.get_md5(row[0]), "content": row[0]}) as response:
                    return row + [await response.json()]

    def get_md5(self, s):
        md = hashlib.md5()
        md.update(s.encode('utf-8'))
        return md.hexdigest()

    def run(self):
        start_time = time.time()
        logging.info("NetEase text detection query start.")
        tasks = [asyncio.ensure_future(self.__post(row=row)) for row in self.query_rows()]
        with tqdm(total=len(tasks)) as pbar:
            for task in tasks:
                task.add_done_callback(lambda _: pbar.update(1))
            loop = asyncio.get_event_loop()
            self.results = loop.run_until_complete(asyncio.gather(*tasks))
            loop.close()
        logging.info("Complete stand test query, cost {} seconds.".format(int(time.time() - start_time)))
        logging.info("Start to write target file..")
        self._save()

    def fix_failed(self, file: str):
        rows = []
        with open(file, 'r', encoding='utf-8') as f:
            f_csv = csv.reader(f)
            rows.append(next(f_csv))
            for row in f_csv:
                if row[1] == "{'msg': '调用API接口失败'}":
                    res = requests.post(self.url, json={"dataId": self.get_md5(row[0]), "content": row[0]})
                    row[1] = res.json()
                rows.append(row)

        with open(file, 'w', encoding='utf-8') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(rows)
