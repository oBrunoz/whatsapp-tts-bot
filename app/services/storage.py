from app.core.config import Settings
from google.cloud import storage
from google.api_core import retry
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class StorageService():
    def __init__(self):
        self.settings = Settings()
        self.client = storage.Client()
        self.bucket_name = self.settings.STORAGE_BUCKET_NAME
        self.bucket = self.client.bucket(self.bucket_name)
    
    @retry.AsyncRetry()
    async def upload_cs_file(
        self, 
        source_file_path:str, 
        destination_blob_name:str, 
        content_type:str = None, 
        public:bool = False
        ) -> Optional[str]:
        """
            Função de upload de arquivo para Google Cloud.
        """
        blob = self.bucket.blob(destination_blob_name)

        if content_type:
            blob.content_type = content_type

        blob.upload_from_filename(source_file_path)

        if public:
            blob.make_public()
            return blob.public_url
        
        return blob.generate_signed_url(
            version="v4",
            expiration=self.settings.SIGNED_URL_EXPIRATION,
            method="GET"
        )

    async def download_cs_file(
            self,
            blob_name:str,
            destination_file_name:str
    ) -> bool:
        """
            Função de download de arquivo do Cloud Storage.
        """
        try:
            blob = self.bucket.blob(blob_name)
            blob.download_to_filename(destination_file_name)
            return True
        except Exception as e:
            print(f"Erro ao realizar download do arquivo {blob_name}: {str(e)}")
            return False
        
    async def delete_cs_file(self, blob_name:str) -> bool:
        """
            Função para deletar arquivos do Cloud Storage
        """
        try:
            blob = self.bucket.blob(blob_name)
            blob.delete()
            return True
        except Exception as e:
            print(f"Erro ao deletar arquivo {blob_name}: {str(e)}")
            return False
    
    async def list_cs_files(self, prefix:str = None) -> list:
        """
            Função para listar arquivos do bucket.
        """
        try:
            file_list = self.bucket.list_blobs(prefix=prefix)
            return [blob.name for blob in file_list]
        except Exception as e:
            print(f'Erro ao listar arquivos com prefixo "{prefix}": {str(e)}')
            return []