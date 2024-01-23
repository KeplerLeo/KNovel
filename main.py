import requests
from bs4 import BeautifulSoup
from typing import List

BASE_URL = "https://animecenterbr.com/light-novels-2/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/58.0.3029.110 Safari/537.3"
    )
}
NOVEL_CONTAINER_CLASS = "container-general"
CHAPTER_CONTAINER_CLASS = "post-text-content my-3"


def get_soup(url: str) -> BeautifulSoup:
    """Fetches the webpage and returns a BeautifulSoup object."""
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return BeautifulSoup(response.content, "html.parser")


def find_links(soup: BeautifulSoup, container_class: str) -> List[str]:
    """Finds all links within a specific container class."""
    return soup.find("div", class_=container_class).find_all("a")


def print_all_novels(soup: BeautifulSoup) -> None:
    """Prints all novel names."""
    novel_link_elements = find_links(soup, NOVEL_CONTAINER_CLASS)
    for novel in novel_link_elements:
        print(novel.text)


def get_novel_link(soup: BeautifulSoup, novel_name: str) -> str:
    """Returns the link of the specified novel."""
    novel_link_elements = find_links(soup, NOVEL_CONTAINER_CLASS)
    for novel in novel_link_elements:
        if novel.text == novel_name:
            return novel["href"]
    raise ValueError(f"No novel found with the name {novel_name}")


def print_all_chapters(soup: BeautifulSoup) -> None:
    """Prints all chapter names."""
    chapter_link_elements = find_links(soup, CHAPTER_CONTAINER_CLASS)
    chapter_link_elements = filter(
        lambda x: "Capítulo" in x.text, chapter_link_elements
    )
    for chapter in chapter_link_elements:
        print(chapter.text)


def get_chapter_link(soup: BeautifulSoup, chapter_number: str) -> str:
    """Returns the link of the specified chapter."""
    chapter_link_elements = find_links(soup, CHAPTER_CONTAINER_CLASS)
    for chapter in chapter_link_elements:
        if chapter_number in chapter.text:
            return chapter["href"]
    raise ValueError(f"No chapter found with the number {chapter_number}")


def write_chapter_to_file(
        soup: BeautifulSoup, novel_name: str, file_name: str
        ) -> None:
    """Writes the chapter content to a file."""
    chapter_number_and_title = soup.find_all("h3")
    chapter_content = soup.find("div", class_="post-text-content").find_all(
        "p"
        )
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(chapter_number_and_title[0].text + "\n\n")
        for paragraph in chapter_content:
            file.write(paragraph.text + "\n\n")


def main() -> None:
    """Main function to orchestrate the novel and chapter fetching process."""
    soup = get_soup(BASE_URL)
    print_all_novels(soup)
    novel_name = input("Enter the novel name: ")
    novel_link = get_novel_link(soup, novel_name)
    novel_soup = get_soup(novel_link)
    print_all_chapters(novel_soup)
    chapter_number = input("Enter the chapter number: ")
    chapter_link = get_chapter_link(novel_soup, chapter_number)
    chapter_soup = get_soup(chapter_link)
    file_name = f"{novel_name} - {chapter_number}.txt"
    write_chapter_to_file(chapter_soup, novel_name, file_name)


if __name__ == "__main__":
    main()
