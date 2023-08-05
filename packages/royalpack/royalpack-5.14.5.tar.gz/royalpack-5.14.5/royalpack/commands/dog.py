from typing import *
import royalnet.commands as rc
import aiohttp
import io


class DogCommand(rc.Command):
    name: str = "dog"

    description: str = "Invia un cane della razza specificata in chat."

    syntax: str = "[razza|list]"

    _breeds = [
        "affenpinscher",
        "african",
        "airedale",
        "akita",
        "appenzeller",
        "australian/shepherd",
        "basenji",
        "beagle",
        "bluetick",
        "borzoi",
        "bouvier",
        "boxer",
        "brabancon",
        "briard",
        "buhund/norwegian",
        "bulldog/boston",
        "bulldog/english",
        "bulldog/french",
        "bullterrier/staffordshire",
        "cairn",
        "cattledog/australian",
        "chihuahua",
        "chow",
        "clumber",
        "cockapoo",
        "collie/border",
        "coonhound",
        "corgi/cardigan",
        "cotondetulear",
        "dachshund",
        "dalmatian",
        "dane/great",
        "deerhound/scottish",
        "dhole",
        "dingo",
        "doberman",
        "elkhound/norwegian",
        "entlebucher",
        "eskimo",
        "finnish/lapphund",
        "frise/bichon",
        "germanshepherd",
        "greyhound/italian",
        "groenendael",
        "havanese",
        "hound/afghan",
        "hound/basset",
        "hound/blood",
        "hound/english",
        "hound/ibizan",
        "hound/plott",
        "hound/walker",
        "husky",
        "keeshond",
        "kelpie",
        "komondor",
        "kuvasz",
        "labrador",
        "leonberg",
        "lhasa",
        "malamute",
        "malinois",
        "maltese",
        "mastiff/bull",
        "mastiff/english",
        "mastiff/tibetan",
        "mexicanhairless",
        "mix",
        "mountain/bernese",
        "mountain/swiss",
        "newfoundland",
        "otterhound",
        "ovcharka/caucasian",
        "papillon",
        "pekinese",
        "pembroke",
        "pinscher/miniature",
        "pitbull",
        "pointer/german",
        "pointer/germanlonghair",
        "pomeranian",
        "poodle/miniature",
        "poodle/standard",
        "poodle/toy",
        "pug",
        "puggle",
        "pyrenees",
        "redbone",
        "retriever/chesapeake",
        "retriever/curly",
        "retriever/flatcoated",
        "retriever/golden",
        "ridgeback/rhodesian",
        "rottweiler",
        "saluki",
        "samoyed",
        "schipperke",
        "schnauzer/giant",
        "schnauzer/miniature",
        "setter/english",
        "setter/gordon",
        "setter/irish",
        "sheepdog/english",
        "sheepdog/shetland",
        "shiba",
        "shihtzu",
        "spaniel/blenheim",
        "spaniel/brittany",
        "spaniel/cocker",
        "spaniel/irish",
        "spaniel/japanese",
        "spaniel/sussex",
        "spaniel/welsh",
        "springer/english",
        "stbernard",
        "terrier/american",
        "terrier/australian",
        "terrier/bedlington",
        "terrier/border",
        "terrier/dandie",
        "terrier/fox",
        "terrier/irish",
        "terrier/kerryblue",
        "terrier/lakeland",
        "terrier/norfolk",
        "terrier/norwich",
        "terrier/patterdale",
        "terrier/russell",
        "terrier/scottish",
        "terrier/sealyham",
        "terrier/silky",
        "terrier/tibetan",
        "terrier/toy",
        "terrier/westhighland",
        "terrier/wheaten",
        "terrier/yorkshire",
        "vizsla",
        "waterdog/spanish",
        "weimaraner",
        "whippet",
        "wolfhound/irish",
    ]

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        breed = args.joined()
        if breed:
            if breed == "list":
                await data.reply("\n".join(["ℹ️ Razze disponibili:", *[f"[c]{breed}[/c]" for breed in self._breeds]]))
            if breed in self._breeds:
                url = f"https://dog.ceo/api/breed/{breed}/images/random"
            else:
                raise rc.InvalidInputError("Questa razza non è disponibile.\n")
        else:
            url = f"https://dog.ceo/api/breeds/image/random"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status >= 400:
                    raise rc.ExternalError(f"Request returned {response.status}")
                result = await response.json()
                assert "status" in result
                assert result["status"] == "success"
                assert "message" in result
                url = result["message"]
            async with session.get(url) as response:
                img = await response.content.read()
                await data.reply_image(image=io.BytesIO(img))
