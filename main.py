from app import parser
from app import excel


def main() -> None:
    excel.new_excel()
    data = parser.run()
    for company in data:
        for founder in company.founders:
            linkedin = None
            for social in founder.socials:
                if social.name == "linkedin":
                    linkedin = social.link
            excel.add_excel(
                row=(founder.full_name, linkedin, company.link),
                title=("Полное имя", "Ссылка на LinkedIn", "Ссылка на компанию")
            )


if __name__ == "__main__":
    main()
