from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Module, ProfileDocument, CompetencePassport, Order, License

# ------------------------
# 1️⃣ Автоматическое удаление файлов при удалении объекта
# ------------------------

@receiver(post_delete, sender=Module)
def delete_module_files(sender, instance, **kwargs):
    for field_name in ['annotation', 'syllabus', 'assesment_fund']:
        file = getattr(instance, field_name)
        if file:
            file.delete(save=False)

@receiver(post_delete, sender=ProfileDocument)
def delete_profile_document(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(save=False)

@receiver(post_delete, sender=CompetencePassport)
def delete_competence_passport(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(save=False)

@receiver(post_delete, sender=Order)
def delete_order_file(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(save=False)

@receiver(post_delete, sender=License)
def delete_license_img(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(save=False)


# ------------------------
# 2️⃣ Автоматическое удаление старого файла при обновлении
# ------------------------

@receiver(pre_save, sender=Module)
def delete_old_module_files(sender, instance, **kwargs):
    if not instance.pk:
        return  # новый объект, нечего удалять

    old_instance = Module.objects.get(pk=instance.pk)
    for field_name in ['annotation', 'syllabus', 'assesment_fund']:
        old_file = getattr(old_instance, field_name)
        new_file = getattr(instance, field_name)
        if old_file and old_file != new_file:
            old_file.delete(save=False)

@receiver(pre_save, sender=ProfileDocument)
def delete_old_profile_document(sender, instance, **kwargs):
    if not instance.pk:
        return
    old_instance = ProfileDocument.objects.get(pk=instance.pk)
    if old_instance.file and old_instance.file != instance.file:
        old_instance.file.delete(save=False)

@receiver(pre_save, sender=CompetencePassport)
def delete_old_competence_passport(sender, instance, **kwargs):
    if not instance.pk:
        return
    old_instance = CompetencePassport.objects.get(pk=instance.pk)
    if old_instance.file and old_instance.file != instance.file:
        old_instance.file.delete(save=False)

@receiver(pre_save, sender=Order)
def delete_old_order_file(sender, instance, **kwargs):
    if not instance.pk:
        return
    old_instance = Order.objects.get(pk=instance.pk)
    if old_instance.file and old_instance.file != instance.file:
        old_instance.file.delete(save=False)

@receiver(pre_save, sender=License)
def delete_old_license_img(sender, instance, **kwargs):
    if not instance.pk:
        return
    old_instance = License.objects.get(pk=instance.pk)
    if old_instance.file and old_instance.file != instance.file:
        old_instance.file.delete(save=False)
