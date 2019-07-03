def humanise_passage(book: str, start_chapter: str, start_verse: str, end_chapter: str, end_verse: str) -> str:
    if len(start_chapter) == 0:  # e.g. James
        return book
    if len(start_verse) == 0 and len(end_chapter) == 0 and len(end_verse) == 0:  # e.g. Genesis 1
        return f"{book} chapter {start_chapter}"
    if len(start_verse) == 0 and len(end_verse) == 0:  # e.g. Genesis 1 - 2
        return f"{book} chapters {start_chapter} to {end_chapter}"
    if len(start_verse) == 0:  # e.g. Genesis 1 - 2:3
        return f"{book} chapter {start_chapter} to chapter {end_chapter} verse {end_verse}"
    if len(end_chapter) == 0 and len(end_verse) == 0:  # e.g. Genesis 1:2
        return f"{book} chapter {start_chapter} verse {start_verse}"
    if len(end_chapter) == 0:  # e.g. Genesis 1:2-3
        return f"{book} chapter {start_chapter} verses {start_verse} to {end_verse}"
    # e.g. Genesis 1:2 - 2:3
    return f"{book} chapter {start_chapter} verse {start_verse}- to chapter {end_chapter} verse {end_verse}"
