import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from services.models import Service, ServiceTierPrice

def run():
    ids = [11, 14, 19]
    tier_data = [
        (25, 2000),
        (50, 1750),
        (100, 1500),
        (999999, 1250)
    ]
    
    count = 0
    for sid in ids:
        service = Service.objects.filter(id=sid).first()
        if not service:
            print(f"Service with ID {sid} not found.")
            continue
            
        print(f"Updating tiers for: {service.name} (ID: {sid})")
        service.tiers.all().delete()
        
        for max_area, price in tier_data:
            ServiceTierPrice.objects.create(
                service=service,
                max_area=max_area,
                price=price
            )
        count += 1
        
    print(f"Successfully populated {count} services with tiers.")

if __name__ == "__main__":
    run()
