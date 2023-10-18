from pyalex import Works

results = Works().filter(publication_year=2021, locations={"source": {"id": "https://openalex.org/S4363607734"}}).select(["id", "doi"]).count()

print(results)