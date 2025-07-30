from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import AlimentSerializer
from api.adapters.h2_aliment_repository import H2AlimentRepository
import logging

logger = logging.getLogger(__name__)
repo = H2AlimentRepository()

class ListCreateAlimentView(APIView):
    '''
    Class that handles creating and listing of aliments
    '''

    def get(self, request):
        '''
        Controller that retrieve the list of aliments registered.
        '''
        logger.debug('Getting all aliments')
        aliments = repo.get_all()
        serializer = AlimentSerializer(aliments, many=True)
        return Response(serializer.data)

    def put(self, request):
        '''
        Controller that register a new aliment.
        '''
        logger.debug(f'Creating new aliment {request.data}')
        serializer = AlimentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        aliment = serializer.save()
        aliment.id = repo.insert(aliment)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RetrieveUpdateDeleteAlimentView(APIView):
    '''
    Class that handles reading (detail), updating and deleting of aliments.
    '''

    def get(self, request, id: int):
        '''
        Controller that retrieve the detail of an aliment.
        '''
        logging.debug(f'Getting aliment {id}')
        aliment = repo.get_by_id(id)
        if not aliment:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AlimentSerializer(aliment)
        return Response(serializer.data)

    def put(self, request, id: int):
        '''
        Controller that update an previous registered aliment.
        '''
        logger.debug(f'Updateing aliment {id}')
        serializer = AlimentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if not repo.exists(id):
            return Response(status=status.HTTP_404_NOT_FOUND)
        aliment = serializer.save()
        aliment.id = id
        repo.update(aliment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id: int):
        '''
        Controller that deletes an previous registered aliment.
        '''
        logger.debug(f'Deleting aliment {id}')
        if not repo.exists(id):
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            repo.delete(id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)