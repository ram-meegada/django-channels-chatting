# your_app_name/cron.py

# from django_cron import CronJobBase, Schedule
# from .models import StateRealEstate
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from abstractbaseuser_project import settings
from time import sleep
from .models import *
from datetime import datetime
import pandas as pd
from django.db import transaction

def my_cron_job(commercial_real_estate_data, borrower_data, state_data, mortgage_lender_data, collateral_data):
    try:
        with transaction.atomic():
            state_time = datetime.now()
            existing_borrowers = set(Borrowers.objects.values_list('borrower', flat=True))
            result_records = []
            for i in borrower_data:
                if i not in result_records:
                    result_records.append(i)
            new_borrower_instances = [Borrowers(borrower=data['borrower_id']) for data in result_records if data['borrower_id'] not in existing_borrowers]
            borrower_instances = Borrowers.objects.bulk_create(new_borrower_instances, 1000)

            existing_states = set(StateRealEstate.objects.values_list('state', flat=True))
            state_result_records = []
            for i in state_data:
                if i not in state_result_records:
                    state_result_records.append(i)
            new_state_instances = [StateRealEstate(state=data['state_id']) for data in state_result_records if data['state_id'] not in existing_states]
            state_instances = StateRealEstate.objects.bulk_create(new_state_instances, 1000)
            
            existing_lenders = set(MortgageLender.objects.values_list('lender', flat=True))
            lender_result_records = []
            for i in mortgage_lender_data:
                if i not in lender_result_records:
                    lender_result_records.append(i)
            new_lender_instances = [MortgageLender(lender=data['lender_id']) for data in lender_result_records if data['lender_id'] not in existing_lenders]
            mortgage_lender_instances = MortgageLender.objects.bulk_create(new_lender_instances, 1000)
            
            existing_collaterals = set(CollateralModel.objects.values_list('collateral_type', flat=True))
            collateral_result_records = []
            for i in collateral_data:
                if i not in collateral_result_records:
                    collateral_result_records.append(i)
            new_collateral_instances = [CollateralModel(collateral_type=data['collateral_type_id']) for data in collateral_result_records if data['collateral_type_id'] not in existing_collaterals]
            collateral_instances = CollateralModel.objects.bulk_create(new_collateral_instances, 1000)

            print(datetime.now()-state_time, '------------time taken----------------')
        
        with transaction.atomic():
            starting_time = datetime.now()
            for data in commercial_real_estate_data:
                try:
                    data['borrower_id'] = Borrowers.objects.get(borrower=data['borrower_id']).id
                except:
                    obj = Borrowers.objects.create(borrower=data['borrower_id'])
                    data['borrower_id'] = obj.id
                try:
                    data['lender_id'] = MortgageLender.objects.get(lender=data['lender_id']).id
                except:
                    obj = MortgageLender.objects.create(lender=data['lender_id'])    
                    data['lender_id'] = obj.id
                state_instance = StateRealEstate.objects.filter(state=data['state_id']).first()

                if state_instance:
                    data['state_id'] = state_instance.id
                else:
                    data['state_id'] = StateRealEstate.objects.create(state=data['state_id']).id
                try:    
                    data['collateral_type_id'] = CollateralModel.objects.get(collateral_type=data['collateral_type_id']).id
                except:
                    data['collateral_type_id'] = CollateralModel.objects.create(collateral_type=data['collateral_type_id']).id 
            final_data = []        
            for i in commercial_real_estate_data:
                try:
                    get_obj = CommercialRealEstate.objects.get(loan_amount = i["loan_amount"], borrower_id = i["borrower_id"],
                                                               lender_id = i["lender_id"], collateral_type_id = i["collateral_type_id"], street_address = i["street_address"], city = i["city"], state_id = i["state_id"])
                except:
                    final_data.append(i)                                               
            CommercialRealEstate.objects.bulk_create([CommercialRealEstate(**data) for data in final_data], 1000)
        context = {"message": "Your csv file is successfully uploaded"}
        temp = render_to_string('key.html', context)
        msg = EmailMultiAlternatives(f"Csv file Update", temp, settings.DEFAULT_FROM_EMAIL, ["ram9014@yopmail.com"])
        msg.content_subtype = 'html'
        msg.send()    
        return "done email sent to mail"

    except ValueError as ve:
        print(f"ValueError: {ve}")
        result = {"data": None, "message": str(ve)}
        return result

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        result = {"data": str(e), "message": "Internal Server Error"}
        return result
