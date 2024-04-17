from celery import shared_task
from django.contrib.auth import get_user_model
from .tezos_func import Create

User = get_user_model()

@shared_task
def create_blockchain_contract(user_id):
    user = User.objects.get(id=user_id)
    contract_id = Create()  # Call the function to create the blockchain contract
    user.blockchain_contract_id = contract_id
    user.save()
