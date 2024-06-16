import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings()


def parse(url: str = "https://www.infokea.narod.ru/podstr_5.htm") -> list:
    """
    Парсит сайт infokea.narod.ru и возвращает список с информацией о задачах
    """
    res_template = [
        {"school_class": "5", "tasks": []},
        {"school_class": "7", "tasks": []},
        {"school_class": "8", "tasks": []},
        {"school_class": "9", "tasks": []},
        {"school_class": "10", "tasks": []},
        {"school_class": "11", "tasks": []},
    ]
    t = -1
    soup = BeautifulSoup(requests.get(url, verify=False).text, "lxml")
    for c in soup.find_all("table", {"bordercolor": "#F7CE9C"}):
        for a in c.find_all("tr"):
            for i in a.find_all("td", {"valign": "top"}):
                t += 1
                for j in i.find_all("ul"):
                    for k in j.find_all("li"):
                        for l in k.find_all("p"):
                            for m in l.find_all("font"):
                                for n in m.find_all("a"):
                                    task_name = (
                                        n.text.replace("\t", "")
                                        .replace("\n", "")
                                        .replace("\r", "")
                                    )
                                    task_url = n.get("href")
                                    if not task_url.startswith("http"):
                                        task_url = (
                                            f"https://www.infokea.narod.ru/{task_url}"
                                        )
                                    res_template[t]["tasks"].append(
                                        {"name": task_name, "url": task_url}
                                    )
    return res_template


def format_parse(parsed_data: dict) -> None:
    """
    Форматирует вывод парсера
    """
    for i in parsed_data:
        print(f"{i['school_class']} класс")
        for j in i["tasks"]:
            print(f"\t{j['name']} - {j['url']}")


if __name__ == "__main__":
    format_parse(parse())
