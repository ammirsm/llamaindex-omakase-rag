# TODO 4: make an APIViewset for Retrival of RAG
# 1. it will get the actual query from the user and the folder that they want to search on
# 2. It will check if the user have the permission with FolderPermission model (make django permission class)
# 3. it will convert it to embedding (this is exactly what we have in the document chunker post save)
# 4. it will search the database for similar embeddings
# https://github.com/pgvector/pgvector-python?tab=readme-ov-file#django
# from pgvector.django import L2Distance
# Item.objects.order_by(L2Distance('embedding', THE DOCUMENT WHICH WE GOT EMBEDDING from ))[:5]
# 5. it will return the results to the user in a paginated way with the most similar results first
# 6. it will also log the request and the response in the database
