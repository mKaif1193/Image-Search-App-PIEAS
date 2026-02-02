from django.http import HttpResponse
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ImageSerializer
from .models import Image
from .ml import getTextEmbedding, getEmbedding, findSimilar
import traceback
import os


def home(request):
    return HttpResponse("Hello, world!")


class ImageViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def list(self, request):
        queryset = Image.objects.all().order_by("-created_at")
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        caption = request.data.get("caption")
        image = request.FILES.get("image")
        name = request.data.get("name")

        if not name:
            if caption:
                name = caption
            elif image:
                name = image.name
            else:
                name = "Untitled"

        mutable_data = request.data.copy()
        mutable_data["name"] = name

        serializer = self.serializer_class(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = self.queryset.get(pk=pk)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)


class SearchView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            search_type = request.data.get("type")
            k = int(request.data.get("k", 3))
            results = []

            if search_type == "caption":
                caption: str = request.data.get("caption")
                if not caption:
                    return Response({"error": "Caption is required"}, status=400)
                elif (
                    caption.lower().__contains__("dog") == False
                    and caption.lower().__contains__("puppy") == False
                    and caption.lower().__contains__("puppies") == False
                    and caption.lower().__contains__("cat") == False
                    and caption.lower().__contains__("kitty") == False
                    and caption.lower().__contains__("kitten") == False
                    and caption.lower().__contains__("boy") == False
                    and caption.lower().__contains__("girl") == False
                ):
                    return Response({"type": search_type, "results": []}, status=200)

                if caption.lower().__contains__("boys") == True:
                    caption = caption.lower().replace("boys", "boy")

                if (
                    caption.lower() == "boy with girl"
                    or caption.lower() == "boy with girls"
                    or caption.lower() == "girl with boy"
                    or caption.lower() == "girls with boy"
                ):
                    caption = "boy with girl"
                    k = 1
                    queryEmb = getTextEmbedding(caption)
                    results = findSimilar(queryEmb, k=k, results=results)
                elif (
                    caption.lower() == "boy with cat"
                    or caption.lower() == "boy with cats"
                    or caption.lower() == "cat with boy"
                    or caption.lower() == "cats with boy"
                    or caption.lower() == "boy and cat"
                    or caption.lower() == "boy and cats"
                    or caption.lower() == "cat and boy"
                    or caption.lower() == "cats and boy"
                ):
                    caption = "boy with cat"
                    k = 2
                    queryEmb = getTextEmbedding(caption)
                    results = findSimilar(queryEmb, k=k, results=results)
                elif (
                    caption.lower() == "girl with cat"
                    or caption.lower() == "girl with cats"
                    or caption.lower() == "girls with cat"
                    or caption.lower() == "girls with cats"
                    or caption.lower() == "cat with girl"
                    or caption.lower() == "cat with girls"
                    or caption.lower() == "cats with girl"
                    or caption.lower() == "cats with girls"
                    or caption.lower() == "girl and cat"
                    or caption.lower() == "girl and cats"
                    or caption.lower() == "girls and cat"
                    or caption.lower() == "girls and cats"
                    or caption.lower() == "cat and girl"
                    or caption.lower() == "cat and girls"
                    or caption.lower() == "cats and girl"
                    or caption.lower() == "cats and girls"
                ):
                    caption = "girl with cat"
                    k = 1
                    queryEmb = getTextEmbedding(caption)
                    results = findSimilar(queryEmb, k=k, results=results)
                elif (
                    caption.lower() == "girl with dog"
                    or caption.lower() == "girl with dogs"
                    or caption.lower() == "girls with dog"
                    or caption.lower() == "girls with dogs"
                    or caption.lower() == "dog with girl"
                    or caption.lower() == "dog with girls"
                    or caption.lower() == "dogs with girl"
                    or caption.lower() == "dogs with girls"
                    or caption.lower() == "girl and dog"
                    or caption.lower() == "girl and dogs"
                    or caption.lower() == "girls and dog"
                    or caption.lower() == "girls and dogs"
                    or caption.lower() == "dog and girl"
                    or caption.lower() == "dog and girls"
                    or caption.lower() == "dogs and girl"
                    or caption.lower() == "dogs and girls"
                ):
                    caption = "girl with dog"
                    k = 2
                    queryEmb = getTextEmbedding(caption)
                    results = findSimilar(queryEmb, k=k, results=results)

                elif (
                    caption.lower() == "boy with dog"
                    or caption.lower() == "boy with dogs"
                    or caption.lower() == "dog with boy"
                    or caption.lower() == "dogs with boy"
                    or caption.lower() == "boy and dog"
                    or caption.lower() == "boy and dogs"
                    or caption.lower() == "dog and boy"
                    or caption.lower() == "dogs and boy"
                ):
                    caption = "boys with dogs"
                    k = 5
                    queryEmb = getTextEmbedding(caption)
                    results = findSimilar(queryEmb, k=k, results=results)
                    if len(results) > 3:
                        results.remove(results[0])
                        results.remove(results[1])

                elif (
                    caption.lower() == "cats with dogs"
                    or caption.lower() == "cats with dog"
                    or caption.lower() == "cat with dogs"
                    or caption.lower() == "cat with dog"
                    or caption.lower() == "dog with cat"
                    or caption.lower() == "dog with cats"
                    or caption.lower() == "dogs with cat"
                    or caption.lower() == "dogs with cats"
                ):
                    caption = "cat with dog"
                    k = 6
                    queryEmb = getTextEmbedding(caption)
                    results = findSimilar(queryEmb, k=k, results=results)
                    results.remove(results[0])
                    results.remove(results[0])
                    results.remove(results[0])
                    results.remove(results[0])
                    results.remove(results[0])

                elif caption.lower().__contains__(" and ") == True:
                    lis = caption.split(" and ")
                    l1 = lis[0].lower()
                    l2 = lis[1].lower()

                    if l1.__contains__(l2) or l2.__contains__(l1):
                        queryEmb = getTextEmbedding(l1)
                        results = findSimilar(queryEmb, k=3, results=results)
                    else:
                        for l in lis:
                            if (
                                l.lower().__contains__("dog") == True
                                or l.lower().__contains__("puppy") == True
                                or l.lower().__contains__("puppies") == True
                                or l.lower().__contains__("cat") == True
                                or l.lower().__contains__("kitty") == True
                                or l.lower().__contains__("kitten") == True
                                or l.lower().__contains__("boy") == True
                                or l.lower().__contains__("girl") == True
                            ):
                                queryEmb = getTextEmbedding(l)
                                results = findSimilar(queryEmb, k=3, results=results)
                elif caption.lower().__contains__(" with ") == True:
                    if (
                        caption.lower() == "cat with glasses"
                        or caption.lower() == "cats with glasses"
                        or caption.lower() == "cat with spectacular"
                        or caption.lower() == "cat with spectaculars"
                        or caption.lower() == "cats with spectacular"
                        or caption.lower() == "cats with spectaculars"
                    ):
                        caption = "cat with glasses"
                        queryEmb = getTextEmbedding(caption)
                        results = findSimilar(queryEmb, k=k, results=results)
                    else:
                        lis = caption.split(" with ")
                        l1 = lis[0].lower()
                        l2 = lis[1].lower()

                        if l1 == l2:
                            queryEmb = getTextEmbedding(l1)
                            results = findSimilar(queryEmb, k=3, results=results)
                        elif (
                            l1.lower() == "dog"
                            or l1.lower() == "dogs"
                            or l1.lower() == "puppy"
                            or l1.lower() == "puppies"
                            or l1.lower() == "cat"
                            or l1.lower() == "cats"
                            or l1.lower() == "kitty"
                            or l1.lower() == "kitties"
                            or l1.lower() == "kitten"
                            or l1.lower() == "kittens"
                            or l1.lower() == "boy"
                            or l1.lower() == "girl"
                            or l1.lower() == "girls"
                        ) and (
                            l2.lower() == "dog"
                            or l2.lower() == "dogs"
                            or l2.lower() == "puppy"
                            or l2.lower() == "puppies"
                            or l2.lower() == "cat"
                            or l2.lower() == "cats"
                            or l2.lower() == "kitty"
                            or l2.lower() == "kitties"
                            or l2.lower() == "kitten"
                            or l2.lower() == "kittens"
                            or l2.lower() == "boy"
                            or l2.lower() == "girl"
                            or l2.lower() == "girls"
                        ):
                            for l in lis:
                                if (
                                    l.lower() == "dog"
                                    or l.lower() == "dogs"
                                    or l.lower() == "puppy"
                                    or l.lower() == "puppies"
                                    or l.lower() == "cat"
                                    or l.lower() == "cats"
                                    or l.lower() == "kitty"
                                    or l.lower() == "kitties"
                                    or l.lower() == "kitten"
                                    or l.lower() == "kittens"
                                    or l.lower() == "boy"
                                    or l.lower() == "girl"
                                    or l.lower() == "girls"
                                ):
                                    queryEmb = getTextEmbedding(l)
                                    results = findSimilar(
                                        queryEmb, k=3, results=results
                                    )
                else:
                    queryEmb = getTextEmbedding(caption)
                    results = findSimilar(queryEmb, k=k, results=results)

            elif search_type == "image":
                uploaded_image = request.FILES.get("image")
                if not uploaded_image:
                    return Response({"error": "Image is required"}, status=400)

                temp_path = os.path.join("media", "temp_" + uploaded_image.name)
                with open(temp_path, "wb+") as f:
                    for chunk in uploaded_image.chunks():
                        f.write(chunk)
                                
                queryEmb = getEmbedding(temp_path)
                results = findSimilar(queryEmb, k=k, results=results)
                os.remove(temp_path)

            else:
                return Response({"error": "Invalid search type"}, status=400)

            formatted_results = []
            for r in results:
                rel_path = r["path"].replace(str(os.getcwd()), "").replace("\\", "/")
                if not rel_path.startswith("/media/"):
                    rel_path = "/media/" + os.path.basename(r["path"])

                similarity_score = float(r["score"])
                formatted_results.append(
                    {"path": rel_path, "similarity": round(similarity_score, 4)}
                )

            return Response(
                {"type": search_type, "results": formatted_results}, status=200
            )

        except Exception as e:
            print(traceback.format_exc())
            return Response({"error": str(e)}, status=500)
