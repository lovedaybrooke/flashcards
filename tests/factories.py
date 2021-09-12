import datetime

import factory

from app import models


class VerbStemFactory(factory.Factory):
    class Meta:
        model = models.VerbStem


class VerbPrefixFactory(factory.Factory):
    class Meta:
        model = models.VerbPrefix


class VerbMeaningFactory(factory.Factory):
    class Meta:
        model = models.VerbMeaning


class CombinationFactory(factory.Factory):
    class Meta:
        model = models.Combination


class LearnerFactory(factory.Factory):
    class Meta:
        model = models.Learner


def create_objects_for_testing(db):
    data = [
        LearnerFactory(name="Nigel")
        ]
    for item in data:
        db.session.add(item)
    db.session.commit()