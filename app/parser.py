from .models import Founder, Company, Social
from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser, Node

BASE_URL = "https://www.ycombinator.com"


def get_attribute(block: Node, selector: str, attribute: str) -> str | None:
    try:
        if selector:
            return block.css_first(selector).attributes[attribute]
        else:
            return block.attributes[attribute]
    except AttributeError:
        return None


def get_text(block: Node, selector: str) -> str | None:
    try:
        return block.css_first(selector).text(strip=True)
    except AttributeError:
        return None


def parse_pages(html_page: str) -> set[str | None]:
    html = HTMLParser(html_page)
    data = html.css("a.WxyYeI15LZ5U_DOM0z8F.no-hovercard")
    founders_links = set([item.attributes['href'] for item in data])
    return founders_links


def parse_company(html_page: str) -> Company:
    html = HTMLParser(html_page)
    company_block = html.css_first(".flex.flex-col.gap-8")
    company_name = get_text(company_block, "h1")
    company_link = get_attribute(company_block, "a.whitespace-nowrap", "href")
    company_socials_blocks = company_block.css(".space-x-2 a")
    company_socials = parse_socials(company_socials_blocks)
    company_founders_block = html.css(".leading-snug")
    company_founders = parse_founders(company_founders_block)
    return Company(
        company_name,
        company_link,
        company_socials,
        company_founders
    )


def parse_socials(socials_blocks: list[Node]) -> tuple[Social]:
    socials = []
    for social_block in socials_blocks:
        social_name = get_attribute(social_block, "", "class")\
            .split()[-1].replace("bg-image-", "")
        social_link = get_attribute(social_block, "", "href")
        if social_name is not None:
            socials.append(Social(social_name, social_link))
    return tuple(socials)


def parse_founders(founder_blocks: list[Node]) -> tuple[Founder]:
    founders = []
    for founder_block in founder_blocks:
        founder_name = get_text(founder_block, ".font-bold")
        founder_socials_block = founder_block.css(".space-x-2 a")
        founder_socials = parse_socials(founder_socials_block)
        founders.append(Founder(
            founder_name,
            founder_socials
        ))
    return tuple(founders)


def run() -> list[Company]:
    data = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(BASE_URL + "/companies/founders?batches=S22&batches=W23&batches=W22",
                  wait_until="networkidle")
        work = True
        while work:
            next_page = page.get_by_text("Loading more...")
            count_text = page.get_by_text("Showing").text_content().split()
            if not next_page:
                break
            try:
                next_page.click(timeout=1000)
            except:
                work = False
            # print(
            #   f"Собрано ссылок на основателей {count_text[1]} из {count_text[3]}")
        links = parse_pages(page.content())
        print(f"Получилось {len(links)} ссылок на компании.")
        for index, link in enumerate(links, start=1):
            page.goto(f"{BASE_URL}{link}")
            data.append(parse_company(page.content()))
            # print(f"Собрано компаний {index} из {len(links)}")
    return data


if __name__ == "__main__":
    run()
