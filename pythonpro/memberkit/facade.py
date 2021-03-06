from typing import List

from django.utils import timezone

from pythonpro.memberkit import api
from pythonpro.memberkit.models import SubscriptionType, Subscription


def synchronize_subscription_types() -> List[SubscriptionType]:
    return [
        SubscriptionType.objects.update_or_create(
            id=dct['id'],
            defaults={'name': dct['name']}
        )[0]
        for dct in api.list_membership_levels()
    ]


def create_new_subscription(payment, observation: str = '') -> Subscription:
    subscription_types = [item.subscription_type_relation.subscription_type for item in payment.items.all()]
    if len(subscription_types) == 0:
        raise ValueError(f"Payment {payment} doesn't have subscription types")

    subscription = Subscription.objects.create(
        status=Subscription.Status.INACTIVE,
        payment=payment,
        subscriber=payment.user,
        observation=observation
    )
    subscription.subscription_types.set(subscription_types)
    return subscription


def activate(subscription, responsible=None, observation=''):
    user = subscription.subscriber
    for subscription_type in subscription.subscription_types.all():
        response_json = api.activate_user(
            user.get_full_name(), user.email, subscription_type.id
        )
    subscription.memberkit_user_id = response_json['id']
    subscription.status = Subscription.Status.ACTIVE
    if subscription.observation:
        subscription.observation += f'\n\n {observation}'
    else:
        subscription.observation = observation
    subscription.activated_at = timezone.now()
    if responsible:
        subscription.responsible = responsible
    subscription.save()
    return subscription
