def humanise_passage(book: str, start_chapter: str, start_verse: str, end_chapter: str, end_verse: str) -> str:
    same_chapter: bool = start_chapter == end_chapter
    same_verse: bool = start_verse == end_verse
    rest: str = (f"verse {start_verse}"
                 if same_chapter and same_verse
                 else (f"verses {start_verse} to {end_verse}"
                       if same_chapter
                       else f"verse {start_verse} to chapter {end_chapter} verse {end_verse}"))

    return f"{book} chapter {start_chapter} {rest}"
