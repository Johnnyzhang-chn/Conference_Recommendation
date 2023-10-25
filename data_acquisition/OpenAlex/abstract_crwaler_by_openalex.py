from pyalex import Works, Sources

# result1 = Works().filter(publication_year=2021, locations={"source": {"id": "https://openalex.org/S4363607734"}}).select(["id", "doi"]).count()
# result2 = Sources().filter(default={"search": "cvpr"}).get()
# source_id = result2[0].get("id")
publication_year = 2022
# works = Works().filter(publication_year=publication_year,
#                        primary_location = {"source": {
#     "display_name": "Proceedings of the National Academy of Sciences of the United States of America",
#     "type": "conference"}
#                        }
#                        ).select(["id", "doi"]).count()

works = Works().filter(doi= "https://doi.org/10.1109/ICRA46639.2022").get()
works_test = Works().filter(doi= "https://doi.org/10.1109/GLOBECOM48099.2022").get()

print(works_test)